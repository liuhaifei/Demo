

import requests
from bs4 import BeautifulSoup
# 设置一个全局的请求头模拟chrome浏览

global headers
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
server='http://www.biquge.cm'
#设置小说地址
book='http://www.biquge.cm/2/2042'
#定义存储位置
global save_path
save_path='D:\Python\download'


#获取章节内容
def get_contents(chapter):
    req=requests.get(url=chapter)
    html=req.content
    html_doc=str(html,'gbk')
    bf=BeautifulSoup(html_doc,'html.parser')
    texts=bf.find_all('div',id='content')
    # 获取div标签id属性content的内容 \xa0 是不间断空白符 &nbsp;
    content = texts[0].text.replace('\xa0' * 4, '\n')
    return content

#写入文件
def write_txt(chapter,content,code):
    with open(chapter,'a',encoding=code) as f:
        f.write(content)


#主方法
def mian():
    res=requests.get(book,headers=headers)
    html=res.content
    html_doc=str(html,'gbk')
    #使用自带的html_parser解析
    soup=BeautifulSoup(html_doc,'html.parser')
    #获取所有章节
    a=soup.find('div',id='list').find_all('a')
    print('总章节数: %d ' % len(a))
    #循环所有章节
    for each in a:
        try:
            chapter=server+each.get('href')
            print('章节: %s' % chapter)
            content=get_contents(chapter)
            chapter=save_path+'\\'+each.string+'.txt'
            write_txt(chapter,content,'utf-8')
        except Exception as e:
            print('111')
            print(e)


if __name__=='__main__':
    mian()