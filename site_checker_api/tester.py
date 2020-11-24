import json, falcon, requests, time
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
from requests.exceptions import SSLError
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class ObjReqClass:
    __json_content = {}

    def __validate_json_input(self, req):
        try:
            self.__json_content = json.loads(req.stream.read())
            return True

        except ValueError:
            self.__json_content = {}
            return False

    def __swjs_check(self,apiKey,sw_url):
        try:
            api_url = 'https://yyyy.xxxx.com/%s/sw.js' % apiKey
            session = requests.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.3'})
            resp = session.get(sw_url,timeout=5, verify=False)
            sw_js = resp.text

            if resp.status_code == 200:
                if api_url in sw_js:
                    return ('Success');
                elif 'https://yyyy.xxxx.com/v3/push/sw.js' in sw_js:
                    return ('Success')
                elif 'yyyy.xxxx.com' in sw_js:
                    return('Failed, apikey does not match with account id')
                else:
                    return ('Failed, sw does not pointing to yyyy.xxxx.com')
            else:
                return ('Failed, sw.js does not exists')
        except HTTPError as http_err:
            return 'Failed ,' + str(http_err)
        except Timeout as err:
            return 'Failed , %s has timed out' % sw_url
        except Exception as err:
            return 'Failed ,' + str(err)

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_405
        output = {
            'msg' : 'This method is not allowed'
        }
        resp.body = json.dumps(output)

    def on_post_sw(self, req, resp):
        resp.status = falcon.HTTP_200
        validated = self.__validate_json_input(req)

        if(validated == True):
            if 'apikey' and 'sw_url' in self.__json_content:
                try:
                    apikey = str(self.__json_content['apikey'])
                    sw_url = str(self.__json_content['sw_url'])
                    swjs_check = self.__swjs_check(apikey,sw_url)
                    output = {
                        'status' : swjs_check,
                        'date' : int(time.time())
                    }

                except ValueError:
                    output = {
                        'status' : 'Failed',
                        'msg' : 'Input parameter is not valid'
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

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        validated = self.__validate_json_input(req)

        if(validated == True):
            if 'account_id' and 'apikey' and 'url' in self.__json_content:
                try:
                    account_id = str(self.__json_content['account_id'])
                    apiKey = str(self.__json_content['apikey'])
                    site_url = str(self.__json_content['url'])
                    site_timeout = []
                    ssl_err = []
                    options = webdriver.ChromeOptions()
                    options.add_argument("--headless")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--disable-dev-shm-usage")
                    driver = webdriver.Chrome(options=options)
                    driver.set_page_load_timeout(20)
                    try:
                        driver.get(site_url)
                        time.sleep(10)
                        site_source = driver.page_source
                        if 'BEGIN CERTIFICATE' in site_source:
                            ssl_err = True
                    except TimeoutException:
                        site_timeout = True
                    finally:
                        sfy = driver.execute_script("return window._xxxx_ != undefined")
                        if sfy == True:
                            js_rsp='Success'
                        elif site_timeout == True:
                            js_rsp='Failed, %s has timed out' % site_url
                        elif ssl_err == True:
                            js_rsp='Failed, %s has SSL problems' % driver.current_url
                        else:
                            js_rsp='Failed, xxx.js not loaded'
                
                        output = {
                            'account_id' : account_id,
                            'apiKey': apiKey,
                            'url' : site_url,
                            'js' : js_rsp,
                            'date' : int(time.time())
                        }

                        driver.quit()
                except ValueError:
                    output = {
                        'status' : 'Failed',
                        'msg' : 'Input parameter is not valid'
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
app.add_route('/selenium', ObjReqClass())
app.add_route('/selenium/sw', ObjReqClass(), suffix='sw')
