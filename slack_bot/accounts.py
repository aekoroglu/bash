import requests, json

def get_acc(acc_id):
    with open('data/list.json') as json_file:
        data = json.load(json_file)
        for i in data:
            if i['accountId'] == acc_id:
                if i['features'].get("push") == "ACTIVE":
                    return i['apiKey'],i['domain'],i['type'],i['features'].get("trendify"),i['features'].get("bannerify"),i['features'].get("recommendation"),i['features'].get("email"),i['features'].get("search"),i['features'].get("push"),i['dataCenter'],i['pushConfiguration']['webConfiguration'].get('serviceWorkerPath')
                else:
                    return i['apiKey'],i['domain'],i['type'],i['features'].get("trendify"),i['features'].get("bannerify"),i['features'].get("recommendation"),i['features'].get("email"),i['features'].get("search"),i['features']. get("push"),i['dataCenter']

def test_acc(acc_id):
    data = {'account_id': acc_id,'notification': 'no'}
    r = requests.post(url='http://10.156.0.0:8000/account', json=data,headers={'Content-type':'application/json','Accept':'application/json'},timeout=30)
    res = r.json()
    return res
