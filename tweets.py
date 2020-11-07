import requests
from requests_oauthlib import OAuth1Session

def parser(text: str):
    comb = text.split('&')
    parameters = dict()

    for param in comb:
        param_list = param.split('=')
        parameters[param_list[0]] = param_list[1]

    return parameters
