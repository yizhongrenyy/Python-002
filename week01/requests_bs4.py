# 使用BeautifulSoup解析网页
# bs4是第三方库需要使用pip命令安装

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
cookie = '__mta=55530900.1595498244881.1595498716397.1595499735520.5; uuid_n_v=v1; uuid=E87A9830CCCA11EABF2811F0086C462E97F42615A0D646198CE511D359158F0A; _csrf=d2e2e8539904705cff1d576dffa39ccb370e3b66b82266d7951a059eb02e1a84; mojo-uuid=0f1c6e86365e634f56d43d091689d2f2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595498245; _lxsdk_cuid=1737b1b2adec8-07f24758072927-31627402-384000-1737b1b2adec8; _lxsdk=E87A9830CCCA11EABF2811F0086C462E97F42615A0D646198CE511D359158F0A; mojo-session-id={"id":"eed67e805d452bc7b7018f2cd1274600","time":1595592699591}; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595592902; __mta=55530900.1595498244881.1595499735520.1595592902317.6; _lxsdk_s=17380bc6ee9-696-422-59f%7C%7C3'

header = {'user-agent':user_agent, 'Cookie': cookie}

myurl = 'https://maoyan.com/films?showType=3'

response = requests.get(myurl,headers=header)

bs_info = bs(response.text, 'html.parser')

movie_list = []
i = 0

for tags in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}):
    if i < 3:
        sub_tag = tags.find_all('div', attrs={'class': 'movie-hover-title'})
        movie_name = sub_tag[0].find('span', attrs={'class': 'name'}).text
        movie_type = sub_tag[1].text.replace("\n", "").split(":")[1].strip()
        movie_time = sub_tag[3].text.replace("\n", "").split(":")[1].strip()

        movie_list.append({
        "电影名称": movie_name,
        "电影类型": movie_type,
        "上映时间": movie_time,
        })

        i += 1
    else:
        break
    
            
movie = pd.DataFrame(data = movie_list)
movie.to_csv('./movie.csv', encoding='utf8', index=False, header=False)