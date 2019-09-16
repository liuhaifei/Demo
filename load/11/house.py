import requests
import re
import os
from bs4 import BeautifulSoup
from util.msyql_DButils import mysql

#写数据库
def write_db(param):
    try:
        sql = "insert into house (url,housing_estate,position,square_metre,unit_price,total_price,follow,take_look,pub_date) "
        sql = sql + "VALUES(%(url)s,%(housing_estate)s, %(position)s,%(square_metre)s,"
        sql = sql + "%(unit_price)s,%(total_price)s,%(follow)s,%(take_look)s,%(pub_date)s)"
        mysql.insert(sql, param)
    except Exception as e:
        print(e)
def main():
    # 给请求指定一个请求头来模拟chrome浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    page_max = 100
    # 爬图地址
    for i in range(1,int(page_max)+1):
        print("第几页:"+str(i))
        if i==1:
            house='https://cq.lianjia.com/ershoufang/jiangbei/'
        else:
            house = 'https://cq.lianjia.com/ershoufang/jiangbei/pg' + str(i)
        res=requests.get(house,headers=headers)
        soup=BeautifulSoup(res.text,'html.parser')
        li_max=soup.find('ul',class_='sellListContent').find_all('li')
        for li in li_max:
            try:
                house_param={}
                #格式
                """紫薇新村|三室两厅|85平米|南北|毛坯|无电梯"""
                content=li.find('div',class_='houseInfo').text
                content=content.split("|")
                house_param['housing_estate']=content[0]
                house_param['square_metre']=re.findall(r'-?\d+\.?\d*e?-?\d*?',content[2])[0]
                #-------------------------------------------#
                #位置
                position = li.find('div', class_='positionInfo').find('a').text
                house_param['position'] = position
                # --------------------------------------------------------#
                totalprice = li.find('div', class_='totalPrice').text
                house_param['total_price'] = re.sub("\D", "", totalprice)
                unitprice = li.find('div', class_='unitPrice').text
                house_param['unit_price'] = re.sub("\D", "", unitprice)
                # --------------------------------------------------------#
                # 57人关注 / 共13次带看 / 6个月以前发布
                follow = li.find('div', class_='followInfo').text
                follow = follow.split("/")
                house_param['follow'] = re.sub("\D", "", follow[0])
                house_param['take_look'] = re.sub("\D", "", follow[1])
                # --------------------------------------------------------#
                # 二手房地址
                title_src = li.find('div', class_='title').find('a').attrs['href']
                house_param['url'] = re.sub("\D", "", title_src)
                res = requests.get(title_src, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                # --------------------------------------------------------#
                # 挂牌时间(重要数据)
                pub_date = soup.find('div', class_='transaction').find_all('li')[0].find_all('span')[1].text
                house_param['pub_date'] = pub_date
                write_db(house_param)
                mysql.commit()
            except Exception as e:
                print(e)
    mysql.dispose()


if __name__ == '__main__':
    main()