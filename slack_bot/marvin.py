import os, random, json, requests, time
from weather import get_weather
from corona import get_corona_top10
from corona import get_corona_today
from corona import get_corona_yesterday
from systems import get_systems
from accounts import get_acc
from accounts import test_acc
from slack import RTMClient

def marv_help(tmp_user):
    user = tmp_user
    ans_text = f"Merhaba <@{user}>, ben marvin\nHer lafa karışmayayım diye büyük abiler sadece adımın geçtiği yerlerde konuşmamı istediler.!!\nBana adımı yazdıktan sonra aşağıdaki komutları yazarak soru sorabilirsiniz.\n\napps-tr/gc - Türkiye ve GoogleCloud'daki          uygulamalarımızın durumu\n acc_id acc_xxxxx - Hesap bilgileri\nhava durumu - Acıbadem için 5 günlük hava tahmini\ndöviz - Anlık döviz kuru\naltın - Anlık altın bilgileri\nborsa - Anlık borsa bilgileri"
    return ans_text

@RTMClient.run_on(event="message")
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    r = data['text']

    if ('marvin' in r.lower() or 'marv' in r.lower()):
        if ('yardım' in r.lower()) or ('help' in r.lower()):
            channel_id = data['channel']
            ans_text = marv_help(data['user'])

        if ('merhaba' in r.lower()) or ('selam' in r.lower()):
            channel_id = data['channel']
            user = data['user']
            texts = [f"Merhaba <@{user}>", f"Selam <@{user}>, ne var ne yok ?", f"Aloha <@{user}"]
            ans_text = random.choice(texts)

        if ('naber' in r.lower()) or ('nasılsın' in r.lower()):
            channel_id = data['channel']
            texts = [f"Nolsun be abi, bildiğin gibi..", f"İyilik, sende var ne yok ?", f"Klişe hayatlara devam"]
            ans_text = random.choice(texts)

        if ('hava durumu' in r.lower()) or ('havalar' in r.lower()):
            channel_id = data['channel']
            ans_text = f"%s" % get_weather()

        if ('eferim' in r.lower()) or ('aferin' in r.lower()):
            channel_id = data['channel']
            texts = [f"Teşekkürler, iyi çalışmalar", f"Eyvallah abi", f"Danke cicim"]
            ans_text = random.choice(texts)

        if ('hayat' in r.lower()) or ('life' in r.lower()):
            channel_id = data['channel']
            ans_text = f"Life. Don't talk to me about life.."

        if ('döviz' in r.lower()) or ('battık mı' in r.lower()):
            channel_id = data['channel']
            req = requests.get('https://kur.doviz.com/api/v5/converterItems',timeout=5)
            server = req.json()
            ans_text = f"Valla bilemedim ki..\n:dollar: %s   :euro: %s   :pound: %s" % (server[0]['1']['selling'],server[0]['2']['selling'],server[0]['3']['selling'])

        if 'altın' in r.lower():
            channel_id = data['channel']
            req = requests.get('https://kur.doviz.com/api/v5/converterItems',timeout=5)
            server = req.json()
            ans_text = f"Bize La Macchina dell'Oro lazım..  :gold::gold:\ngram: %s   çeyrek: %s   yarım: %s" % (round(server[1]['2']['selling'],3),round(server[1]['3']['selling'],3),round(server[1]['4']['selling'],3))

        if 'borsa' in r.lower():
            channel_id = data['channel']
            session = requests.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.3'})
            req = session.get('https://www.borsaistanbul.com/datfile/indexdata',timeout=5)
            server = req.json()
            bist = server['bist'][0]
            bist_value = bist['value']
            bist_cp = "{:.3f}".format(bist['changePerCent'])
            ans_text = f"BIST 100 Endeksi :chart:\nSon: %s   Değişim: %s" % (bist_value, bist_cp)

        if 'corona top10' in r:
            channel_id = data['channel']
            ans_text = f"%s" % get_corona_top10()

        if 'öldük mü' in r:
            channel_id = data['channel']
            ccode = "tr"
            cd = get_corona_today(ccode)
            if cd == "0":
                ans_text = f"Country code does not exists"
            else:
                ans_text = f"COVID-19 Details for %s\nNew infections : %s\nNew deaths : %s\nNew recovered : %s\nLast update : %s" % (cd[1],cd[3],cd[4],cd[5],cd[2])

        if 'corona today' in r:
            channel_id = data['channel']
            split_commands = r.strip().split(' ')
            ccode = split_commands[3]
            cd = get_corona_today(ccode)
            if cd == "0":
                ans_text = f"Country code does not exists"
            else:
                ans_text = f"COVID-19 Details for %s\nNew infections : %s\nNew deaths : %s\nNew recovered : %s\nLast update : %s" % (cd[1],cd[3],cd[4],cd[5],cd[2])

        if 'corona yesterday' in r:
            channel_id = data['channel']
            split_commands = r.strip().split(' ')
            ccode = split_commands[3]
            cd = get_corona_yesterday(ccode)
            if cd == "0":
                ans_text = f"Country code does not exists"
            else:
                ans_text = f"COVID-19 Details for %s\nNew infections : %s\nNew deaths : %s\nNew recovered : %s\nLast update : %s" % (cd[1],cd[3],cd[4],cd[5],cd[2])

        if 'apps-tr' in r:
            channel_id = data['channel']
            ans_text = f"%s" % get_systems('http://127.0.0.1:8000/services/apps?dc=tr')

        if 'apps-gc' in r:
            channel_id = data['channel']
            ans_text = f"%s" % get_systems('http://127.0.0.1:8000/services/apps?dc=gc')

        if 'ignite-tr' in r:
            channel_id = data['channel']
            ans_text = f"%s" % get_systems('http://127.0.0.1:8000/services/ignite?dc=tr')

        if 'ignite-gc' in r:
            channel_id = data['channel']
            ans_text = f"%s" % get_systems('http://127.0.0.1:8000/services/ignite?dc=gc')

        if ('acc_id' in r) or ('acc_ip' in r):
            channel_id = data['channel']
            split_commands = r.strip().split(' ')
            acc = get_acc(split_commands[2])
            if acc is None:
                ans_text = f"Account does not exists"
            else:
                if acc[8] == "ACTIVE":
                    ans_text = f"Type : %s\nDomain : %s\nApiKey : %s\nDC : %s\n>Bannerify : %s\n>Email : %s\n>Push : %s\n>Push sw_url : %s\n>Recommendation : %s\n>Search : %s\n>Trendify : %s\n" % (acc[2],acc[1],acc[0],acc[9],acc[4],acc[6],acc[8],acc[10],acc[5],acc[7],acc[3])
                else:
                    ans_text = f"Type : %s\nDomain : %s\nApiKey : %s\nDC : %s\nBannerify : %s\nEmail : %s\nPush : %s\nRecommendation : %s\nSearch : %s\nTrendify : %s" % (acc[2],acc[1],acc[0],acc[9],acc[4],acc[6],acc[8],acc[5],acc[7],acc[3])

        if 'test' in r:
            channel_id = data['channel']
            split_commands = r.strip().split(' ')
            acc = split_commands[2]
            selen = test_acc(acc)
            if selen['apikey'] is None:
                ans_text = f"Account does not exists"
            else:
                ans_text = f"Selenium test result for %s\nApikey : %s\nUrl : %s\nType : %s\nDc : %s\nJs : %s\nSw : %s\nSw_url : %s" % (acc,selen['apikey'],selen['url'],selen['type'],selen['dc'],selen['js'],selen['sw'],selen['sw_url'])

        web_client.chat_postMessage(channel=channel_id,text=ans_text)

slack_token = os.environ["SLACK_BOT_TOKEN"]
rtm_client = RTMClient(token=slack_token)
print("Bot is up and running!")
rtm_client.start()
