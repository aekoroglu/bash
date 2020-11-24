import falcon, json, requests, tldextract, datetime, sys, os
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
from requests.exceptions import SSLError
import os.path as path
from slack import send_slack_msg

sfy_user = os.environ["SFY_USER"]
sfy_pass = os.environ["SFY_PASS"]

class ObjReqClass:
    __json_content = {}

    def __validate_json_input(self, req):
        try:
            self.__json_content = json.loads(req.stream.read())
            return True

        except ValueError:
            self.__json_content = {}
            return False

    def __get_list(self,version):
        data = {'username': sfy_user,'password': sfy_pass}

        if version == 'v1':
            token_url = 'https://y1.xxxx.com/getToken'
            acc_list = 'https://y1.xxxx.com/admin/v1/get/account/list.json'
            json_file = 'data/list1.json'
        else:
            token_url = 'https://y.xxxx.com/getToken'
            acc_list = 'https://y.xxxx.com/admin/v1/get/account/list.json'
            json_file = 'data/list3.json'

        try:
            f = open(json_file)
            tnow = datetime.datetime.now().timestamp()
            last_mod = path.getmtime(json_file)
            if tnow - last_mod > 7200:
                r = requests.post(url=token_url, json=data, headers = {'Content-type':'application/json', 'Accept':'application/json'})
                res = r.json()
                panel_token = res["token"]
                r = requests.get(acc_list, headers={'Authorization': panel_token})
                with open(json_file, 'wb') as f:
                    f.write(r.content)
        except Exception:
            r = requests.post(url=token_url, json=data, headers = {'Content-type':'application/json', 'Accept':'application/json'})
            res = r.json()
            panel_token = res["token"]
            r = requests.get(acc_list, headers={'Authorization': panel_token})
            with open(json_file, 'wb') as f:
                f.write(r.content)
        finally:
            f.close()

    def __v1_acc(self,account_id):
        self.__get_list('v1')
        with open('data/list1.json') as json_file:
            data = json.load(json_file)
            dc = 'pk'
            for i in data:
                if i['accountId'] == account_id:
                    return i['apiKey'],i['domain'],i['type'],i['features'].get("push"),dc

    def __v3_acc(self,account_id):
        self.__get_list('v3')
        with open('data/list3.json') as json_file:
            data = json.load(json_file)
            for i in data:
                if i['accountId'] == account_id:
                    if i['features'].get("push") == "ACTIVE":
                        return i['apiKey'],i['domain'],i['type'],i['features'].get("push"),i['dataCenter'],i['pushConfiguration']['webConfiguration'].get('serviceWorkerPath')
                    else:
                        return i['apiKey'],i['domain'],i['type'],i['features'].get("push"),i['dataCenter']

    def __selenium(self,account_id,apikey,url,dc):
        try:
            if dc == 'tr':
                selen = "http://192.168.0.0:8000/selenium"
            elif dc == 'eu':
                selen = "http://10.154.0.0:8000/selenium"
            else:
                selen = "http://10.156.0.0:8000/selenium"
            data = {'account_id': account_id,'apikey': apikey, 'url': url}
            r = requests.post(url=selen, json=data, headers={'Content-type':'application/json', 'Accept':'application/json'})
            selen_res = r.json()
            return selen_res
        except HTTPError as http_err:
            return 'An error occured : ' + str(http_err)
        except Exception as err:
            return 'An error occurred : ' + str(err)

    def __swjs_check(self,apikey,sw_url,dc):
        try:
            if dc == 'pk':
                selen_sw = "http://192.168.0.0:8000/selenium/sw"
            elif dc == 'gc':
                selen_sw = "http://10.154.0.0:8000/selenium/sw"
            else:
                selen_sw = "http://10.156.0.0:8000/selenium/sw"
            data = {'apikey': apikey, 'sw_url': sw_url}
            r = requests.post(url=selen_sw, json=data, headers={'Content-type':'application/json', 'Accept':'application/json'})
            selen_sw_res = r.json()
            return selen_sw_res
        except HTTPError as http_err:
            return 'An error occured : ' + str(http_err)
        except Exception as err:
            return 'An error occurred : ' + str(err)

    def on_get(self,req,resp):
        resp.status = falcon.HTTP_405
        output = {
            'msg' : 'This method is not allowed'
        }
        resp.body = json.dumps(output)

    def on_post(self,req,resp):
        resp.status = falcon.HTTP_200
        validated = self.__validate_json_input(req)
            
        if(validated == True):
            if 'account_id' in self.__json_content:
                try:
                    account_id = str(self.__json_content['account_id'])
                    qacc = self.__v3_acc(account_id)
                    if qacc is None:
                        qacc = self.__v1_acc(account_id)
                    
                    if qacc is None:
                        output = {
                            'status' : 'Failed',
                            'msg': '%s does not exists' % account_id
                        }
                    else:
                        purl = tldextract.extract(qacc[1])
                        if purl[0] == '':
                            url = 'https://www.%s.%s' % (purl[1],purl[2])
                        else:
                            url = 'https://%s.%s.%s' % (purl[0],purl[1],purl[2])

                        tries = 2
                        for i in range(tries):
                            try:
                                r = requests.get(url,timeout=5)
                                status = r.status_code
                            except Timeout as err:
                                if i < tries - 1:
                                    continue
                                else:
                                    print('Request timed out')
                            except SSLError as err:
                                if i < tries - 1:
                                    continue
                                else:
                                    print('SSL error')
                            except HTTPError as err:
                                if i < tries - 1:
                                    continue
                                else:
                                    print('HTTP error')
                            except Exception as err:
                                if i < tries - 1:
                                    continue
                                else:
                                    print(err)
                            break

                        selen_test = self.__selenium(account_id,qacc[0],url,qacc[4])

                        if 'An error occurred' in selen_test:
                            output = {
                                'status' : 'Failed',
                                'msg' : selen_test
                            }
                        else:
                            if qacc[3] == "ACTIVE":
                                sw_url = qacc[5]
                                swjs_resp = self.__swjs_check(qacc[0],sw_url,qacc[4])
                                swjs = swjs_resp['status']
                            else:
                                swjs = 'none'
                                sw_url = 'none'

                            if 'notification' in self.__json_content:
                                try:
                                    msg_noti = str(self.__json_content['notification'])
                                except ValueError:
                                    print('psstt..')
                            else:
                                msg_noti = 'none'
 
                            if msg_noti == 'none':
                                if 'Failed' in selen_test['js'] or 'Failed' in swjs:
                                    send_slack_msg(account_id,qacc[0],selen_test['url'],qacc[2],selen_test['js'],swjs)

                        output = {'account_id':account_id,'apikey':qacc[0],'url':selen_test['url'],'type':qacc[2],'js':selen_test['js'],'sw':swjs,'sw_url':sw_url,'date':selen_test['date']}
                except ValueError:
                    output = {
                        'status' : 'Failed',
                        'msg' : 'Authentication was not successful'
                    }
                    pass
            else:
                output = {
                    'status' : 'Failed',
                    'msg' : 'Input is not valid'
                }
        else:
            output = {
                'status' : 'Failed',
                'msg' : 'JSON is not valid'
            }
        resp.body = json.dumps(output)

app = falcon.API()
app.add_route('/account', ObjReqClass())
