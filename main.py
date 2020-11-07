import requests
from requests_oauthlib import OAuth1Session
import json
import time
import re
import datetime
from datetime import datetime as dt
from typing import List, Dict
from collections import defaultdict

from database import fetch_all_users

CK = os.environ.get('CK')
CS = os.environ.get('CS')
GETID_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
POST_URL = 'https://api.twitter.com/1.1/statuses/update.json'

def create_session(CK: str, CS: str, AK: str, AS: str) -> OAuth1Session:
    session = OAuth1Session(CK, CS, AK, AS)
    return session


def search(session, query: str, lang: str='ja', result_type: str='recent', count: int=100, max_id=None) -> list:
    params = {
            'q': query,
            'lang': lang,
            'result_type': result_type,
            'count': count,
            'max_id': max_id,
        }
    res = session.get(SEARCH_URL, params=params)
    tweets = json.loads(res.text)['statuses']

    return tweets

def time_fomatter(time: str) -> None:
    time = re.sub('\+0000', '', time)
    time = dt.strptime(time, "%a %b %d %H:%M:%S %Y")
    return time

def count(datas: dict) -> dict:
    s_index = None
    e_index = None
    flag = True
    key = 0
    results = defaultdict(int)

    times = [
        time_fomatter(data['created_at']).minute // 10
            for data in datas
    ]
    start = times[0] - 1
    if start < 0:
        start == 5

    for i, time in enumerate(times):
        if s_index is None and time == start:
            s_index = i
            flag = False
        
        if not flag:
            if time > start:
                flag = True
        if flag == True and s_index is not None and time == start:
            e_index = i
            break
    
    times = times[s_index:e_index]

    tmp = times[0]
    for time in times:
        if tmp == time:
            results[str(key)] += 1
        else:
            tmp = time
            key += 1
            results[str(key)] += 1

    return results
        

def get_max_id(datas: List[Dict], index: int=-1) -> str:
    return datas[index]['id']

def post_tweet(session, text: str):
    params = {
        'status': text,
    }
    result = session.post(POST_URL, params)

    return result

def _get_top_tweet(datas: List[Dict]) -> dict:
    criteria = 0
    top_tweet = None
    for data in datas:
        this_criteria = data['favorite_count'] + data['retweet_count']
        if this_criteria > criteria:
            criteria = this_criteria
            top_tweet = data

    return top_tweet

def _fetch_tweet_link(data: dict) -> str:
    tweet_id = data['id_str']
    screen_name = data['user']['screen_name']

    link = 'https://twitter.com/{}/status/{}'.format(screen_name, tweet_id)

    return link

def fetch_top_link(datas: List[Dict]) -> str:
    top_tweet = _get_top_tweet(datas)
    link = _fetch_tweet_link(top_tweet)

    return link


if __name__ == "__main__":
    users = fetch_all_users()

    for user in users:
        id_, AK, AS, query = user
        session = create_session(CK, CS, AK, AS)
        tweets = []
        max_id = None
        for i in range(10):
            tweets += search(session, query, max_id=max_id)
            max_id = get_max_id(tweets)
            time.sleep(2)
            
        results = count(tweets)
        detector = list(results.values())[:6]
        recent = detector[0]
        avg = sum(detector[1:]) / len(detector) - 1
        if recent > 3 * avg:
            link = fetch_top_link(tweets[:recent])
            text = '「{}」の話題で盛り上がってみます。\n\nチェックしましょう!!\n\n👇現在のトップツイート👇{}'.format(query, link)
            tweeted = post_tweet(session=session, text=text)
            print(json.loads(tweeted.text))
