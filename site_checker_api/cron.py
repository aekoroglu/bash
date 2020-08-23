import json, requests, os, sys, datetime
import os.path as path

acc_list = []
acc_test = []
acc_result = []

def get_list():
    tnow = datetime.datetime.now().timestamp()
    l1_lastmod = path.getmtime('data/list1.json')
    l3_lastmod = path.getmtime('data/list3.json')
    if tnow - l1_lastmod > 5400 or tnow - l3_lastmod > 5400:
        token1 = 'https://xxx.xxx.com/getToken'
        token3 = 'https://xxx.xxx.com/getToken'
        list_v1 = 'https://xxx.xxx.com/admin/v1/get/account/list.json'
        list_v3 = 'https://xxx.xxx.com/admin/v1/get/account/list.json'
        data = {'username': 'xxxx','password': 'xxxx'}
        req1 = requests.post(url=token1, json=data, headers={'Content-type':'application/json', 'Accept':'application/json'})
        res1 = req1.json()
        token_v1 = res1["token"]
        r = requests.get(list_v1, headers={'Authorization': token_v1})
        with open('data/list1.json', 'wb') as f:
            f.write(r.content)
        req3 = requests.post(url=token3, json=data, headers={'Content-type':'application/json', 'Accept':'application/json'})
        res3 = req3.json()
        token_v3 = res3["token"]
        r = requests.get(list_v3, headers={'Authorization': token_v3})
        with open('data/list3.json', 'wb') as f:
            f.write(r.content)

def send_req(data):
    try:
        local = 'http://localhost:8000/account'
        req = requests.post(url=local, json=data, headers={'Content-type':'application/json', 'Accept':'application/json'})
        r2 = req.json()
        return r2
    except requests.exceptions.RequestException as e:
        return "An error occurred : " + str(e)

def slack(acc_type,slack_json,title):
    data = acc_result
    f = open(slack_json, "w")
    f.write('{"blocks":[{"type":"section","text":{"type":"mrkdwn","text":"*%s*"}},{"type":"divider"},' % (title))
    for i in data:
        if i['js'] == 'Failed' or 'Failed' in i['sw']:
            f.write('{"type":"section","text":{"type":"mrkdwn","text":"*%s* - %s - Js: %s - Sw: %s"}},' % (i['account_id'],i['url'],i['js'],i['sw']))
    f.write('{"type":"divider"}]}')
    f.close()

    webhook_url = 'https://hooks.slack.com/services/xxxxx'
    with open(slack_json, 'rt') as sdata:
        data = json.load(sdata)

    response = requests.post(webhook_url,data=json.dumps(data),headers={'Content-type':'application/json', 'Accept':'application/json'})

def main():
    get_list()
    os.system("jq -s '[.[][]]' data/*.json > data/list.json")
    acc_type = sys.argv[1]

    with open('data/list.json') as json_file:
        data = json.load(json_file)
        for i in data:
            if i['type'] == acc_type:
                acc_list.append(i['accountId'])
                slack_json = 'tmp/%s.json' % acc_type
                msg_title = 'Test Results for %s Accounts' % acc_type

        for i in acc_list:
            data = {'account_id': i,'notification': 'no'}
            res = send_req(data)
            acc_test.append(res)

        for i in acc_test:
            if 'An error occurred' in i:
                print(i)
                sys.exit(2)
            else:
                if 'Failed' in i['js'] or 'Failed' in i['sw']:
                    acc_result.append(i)

        slack(acc_type,slack_json,msg_title)

if __name__ == "__main__":
    main()
