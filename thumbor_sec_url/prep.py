import falcon,json,hmac,hashlib,base64,re,urllib.parse
from falcon_prometheus import PrometheusMiddleware

class ObjReqClass:
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_405
        output = {
            'msg' : 'This method is not allowed'
        }
        resp.body = json.dumps(output)

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        url_p = req.get_param('url')
        if url_p != "":
            url_r = re.compile(r"https?://(www\.)?")
            url2 = url_r.sub('', url_p).strip().strip('/')
            url = url2.replace(" ", "%20")
            b_key = bytes('s2d4t5$02!16#96','UTF-8')
            b_url = bytes(url,'UTF-8')
            digester = hmac.new(b_key, b_url, hashlib.sha1)
            signature = digester.digest()
            safe_url_sign = base64.urlsafe_b64encode(signature)
            safe_url = str(safe_url_sign, "utf-8")
            img_url = 'https://img.xxxx.com/%s/%s' % (safe_url,url)
            output = {'status': 1, 'img': img_url}
        else:
            output = {'status': 0,'stat_desc': 'no param'}

        resp.body = json.dumps(output)

prometheus = PrometheusMiddleware()
app = falcon.API(middleware=prometheus)
app.add_route('/', ObjReqClass())
app.add_route('/metrics', prometheus)
