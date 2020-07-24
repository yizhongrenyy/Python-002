import requests
import lxml.etree
import pandas as pd


# 电影详细页面
url = 'https://maoyan.com/films?showType=3'

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
cookie = '__mta=55530900.1595498244881.1595498716397.1595499735520.5; uuid_n_v=v1; uuid=E87A9830CCCA11EABF2811F0086C462E97F42615A0D646198CE511D359158F0A; _csrf=d2e2e8539904705cff1d576dffa39ccb370e3b66b82266d7951a059eb02e1a84; mojo-uuid=0f1c6e86365e634f56d43d091689d2f2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595498245; _lxsdk_cuid=1737b1b2adec8-07f24758072927-31627402-384000-1737b1b2adec8; _lxsdk=E87A9830CCCA11EABF2811F0086C462E97F42615A0D646198CE511D359158F0A; mojo-session-id={"id":"eed67e805d452bc7b7018f2cd1274600","time":1595592699591}; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595592902; __mta=55530900.1595498244881.1595499735520.1595592902317.6; _lxsdk_s=17380bc6ee9-696-422-59f%7C%7C3'

# 声明为字典使用字典的语法赋值
header = {'user-agent':user_agent, 'Cookie': cookie}

response = requests.get(url, headers=header)

# xml化处理
selector = lxml.etree.HTML(response.text.replace("<dd>","</dd><dd>"))

mylist = []
for i in range(1, 11):
    movie_name = selector.xpath(f'//*[@id="app"]/div/div[2]/div[2]/dl/dd[{i}]/div[1]/div[2]/a/div/div[1]/span[1]/text()')[0]
    movie_type = selector.xpath(f'//*[@id="app"]/div/div[2]/div[2]/dl/dd[{i}]/div[1]/div[2]/a/div/div[2]/text()')[1].strip()
    release_date = selector.xpath(f'//*[@id="app"]/div/div[2]/div[2]/dl/dd[{i}]/div[1]/div[2]/a/div/div[4]/text()')[1].strip()

    mylist.append([movie_name, movie_type, release_date])


movie = pd.DataFrame(data = mylist)

movie.to_csv('./movie_xpath.csv', encoding='utf8', index=False, header=False)

