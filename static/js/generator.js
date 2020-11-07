const QUERY_BOX = document.getElementById('query');
const ACTION = document.getElementById('action');
const MSG_BOX = document.getElementsByClassName('msg')[0];
const CONTENTS = document.getElementsByClassName('contents')[0];
const DEL = document.getElementById('delete');
const BASE = '../'

let query, id;

fetch(BASE + 'get_id').then(
    res => res.json()
).then(data => {
    let results = JSON.parse(data);
    id = results['id'];
})

ACTION.addEventListener('click', e => {
    query = QUERY_BOX.value;
    MSG_BOX.innerHTML = "ただいまクエリを登録しています。";
    fetch(BASE + 'update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'id': id, 'query': query,}),
    }).then(
        res => res.json()
    ).then(data => {
        let results = JSON.parse(data);
        MSG_BOX.innerHTML = results.msg;
    })
})


DEL.addEventListener('click', e => {
    fetch(BASE + 'delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'id': id})
    }).then(
        res => res.json()
    ).then(data => {
        let results = JSON.parse(data);
        MSG_BOX.innerHTML = results.msg;
    })
})