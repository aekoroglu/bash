import requests, json

def get_systems(url):
    req = requests.get(url,timeout=20)
    server = req.json()
    srv_list = ''
    count = 0
    for x in server:
        count += 1
        host = x[0]
        status = x[1]
        if (count == len(server)):
            tmp_list = "* %s %s" % (host,status)
        else:
            tmp_list = "* %s %s\n" % (host,status)
        srv_list += tmp_list
   
    return srv_list
