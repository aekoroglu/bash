import json, falcon, time
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

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_405
        output = {
            'msg' : 'This method is not allowed'
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
                    driver.set_page_load_timeout(15)
                    try:
                        driver.get(site_url)
                        element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
                        WebDriverWait(driver, 6).until(element_present)
                        site_source = driver.page_source
                        if 'BEGIN CERTIFICATE' in site_source:
                            ssl_err = True
                    except TimeoutException:
                        site_timeout = True
                    finally:
                        rdr_url =  driver.current_url
                        sfy = driver.execute_script("return window._SgmntfY_ != undefined")
                        if sfy == True:
                            js_rsp='Success'
                        elif site_timeout == True:
                            js_rsp='Failed, %s has timed out' % site_url
                            rdr_url = ''
                        elif ssl_err == True:
                            js_rsp='Failed, %s has SSL problems' % driver.current_url
                        else:
                            js_rsp='Failed'
                
                        output = {
                            'account_id' : account_id,
                            'apiKey': apiKey,
                            'url' : site_url,
                            'rdr_url' : rdr_url,
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
