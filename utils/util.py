import httplib2
from bs4 import BeautifulSoup
import time
import json

def update_wanIP():
    http = httplib2.Http()
    status, response = http.request('http://wanip.info/')

    soup = BeautifulSoup(response, 'html.parser')

    while 1:
        # print(soup.prettify())
        print("Updating")
        ip_info = soup.find_all(class_='ipinfo')
        spans = ip_info[0].find_all('span')
        span_texts = [span.text for span in spans]
        wan_ip = ".".join(span_texts)
        print(wan_ip)
        w_file = open("/home/pi/data/smart_house/src/backend/extra_files/wanIP.txt", "w", encoding="utf-8")
        w_file.write(wan_ip)
        w_file.close()
        time.sleep(3600)


def update_status_is_watching(status):
    f = open("/home/pi/data/smart_house/src/backend/extra_files/common_var_door_server.json")
    common_var = json.load(f)
    f.close()
    common_var["is_watching"] = status
    f = open("/home/pi/data/smart_house/src/backend/extra_files/common_var_door_server.json", "w")
    json.dump(common_var, f)
    f.close()