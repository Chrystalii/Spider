#coding=utf-8
import requests
import urllib
import urllib.request
# import urllib.request
from bs4 import BeautifulSoup
import random
import time
import traceback
import json
import insertinto_db
import insertinto_db_2
import re

import insertinto_db_2_1
import insertinto_db_2_2
import insertinto_db_3


def get_firstpage_content(url, data=None):
    header={
        'Accept': 'text/css,*/*;q=0.1',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            req = urllib.request.Request(url, data, header)
            response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            response.close()
            break
        except urllib.request.HTTPError as e:
                print( 'except 1:', e)
                time.sleep(random.choice(range(5, 10)))
        except urllib.request.URLError as e:
            print( 'except 2:', e)
            time.sleep(random.choice(range(5, 10)))
        except:
            print('except 0')
    return rep.text

def get_firstpage_url(html):
    # final = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body  # 获取body部分
    # print(type(body))
    # print(body)
    data = body.find_all('div', {'class': 'category-info'})  # 找到id为7d的div
    # print(type(data))
    # print(data)
    urls_list=[]
    links_list=[]
    for a in data:
        ul = a.find('h5')
        url=ul.find('a')
        urls_list.append(url)
    return urls_list
 # find_all出来的结果是列表形式，不能再进行后续查找了！用for可解决

def get_firstpage_tagid(firstpage_urls):
    links_list=[]
    # print(firstpage_urls)
    for i in firstpage_urls:
        firstpage_title= i.get_text()
        links = i.get('href')
        links_list.append(links)
        # for a in links_list:
        #     firstpage_url = a
        # print(links)
        # print(firstpage_title)
        # ******插入表数据1 id=1—11  insertinto_db.insert(firstpage_title,links)
    # print(links_list)
    # 切片问题 如果不把href提取出来无法使用tagid=b[1:5]，这时候再用一次列表遍历
    tagid_list=[]
    for b in links_list:
        tagid=b[46:51]
        tagid_list.append(tagid)
    del tagid_list[0]
    # print(tagid_list)
    return tagid_list #检测出返回值最好跟你要输出的内容保持一直，出错率比较低

def get_secondpage_url(url, tagId, page):
     headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
        }
     data = {
            "limit": "24",
            "timeout": 3000,
            "filterTags": [],
            "tagId": tagId,
            "fromLemma": False,
            "contentLength": 40,
            "page": page
        }
     time.sleep(5)
     try:
            url3_to_url3_dict = {}
            content = requests.post(url, data=data, headers=headers).content  # 就是这里
            response = content.decode('unicode-escape').replace("\/", "/")
            # response = content.decode('utf-8').replace("\/", "/")
            js = json.loads(response)
            for i in range(len(js['lemmaList'])):#这边要写总结报告的 就是关于json解析的问题（函数类型不一致，我前面output的是字典类型，字典类型查找内容方法）
                mytitle=(js['lemmaList'][i]['lemmaTitle'])
            # for j in range(len(js['lemmaList'])):
                myurl=(js['lemmaList'][i]['lemmaUrl'])
                mycontent=(js['lemmaList'][i]['lemmaDesc'])
                url3_to_url3_dict[mytitle] = myurl
                # print(mytitle)
                # print(myurl)
                # print(mycontent)
                # print(time)
                # insert_db.insert(time,myurl, mytitle, mycontent)
            # print(url3_to_url3_dict)
     except:
            print(traceback.format_exc())
     global url3_to_url3_dict    ###global这个用法，记下
     return url3_to_url3_dict

def get_thirdpage_content(url2, data=None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'


    }
    timeout = random.choice(range(80, 180))
    # while True:
    time.sleep(5)

    try:
          rep2 = requests.get(url2, headers=header, timeout=timeout)
          rep2.encoding = 'utf-8'
          req2 = urllib.request.Request(url2, data, header)
          response = urllib.request.urlopen(req2, timeout=timeout)
          response.close()


    except urllib.request.HTTPError as e:
            print('except 1:', e.code)
            # time.sleep(random.choice(range(5, 10)))
    except urllib.request.URLError as e:
            print('except 2:', e.reason)
            # time.sleep(random.choice(range(5, 10)))
    except:
            print('except 0')
        # except :
        #     return 0
    global rep2
    return rep2.text

def parsethirdpage_main_content(content):
    global thirdpage_id
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.body  # 获取body部分
    contenttitles = body.find_all('h1')
    # print(contenttitles)
    ###[<h1>xxxxxx</h1> +content形式 要入库要把这里改了
    for a in contenttitles:
         contenttitle=a.get_text()
         # print(contenttitle)
    data = body.find_all('div', {'class': 'para', 'label-module':"para"})  # 找到id为7d的div
    # print(data)
    # for i in data:
    #     thirdpage_content=i.get_text()
    #     print(i.get_text())
    linksa_list = []

    for j in data:
        linksa=j.find_all('a', {'target': '_blank'})
        # print(linksa)
        for a in linksa:
            linksa_list.append(a)
            # print(linksa_list)
    for everylink in linksa_list:
                fourthpage_url = everylink.get('href')
                # print(fourthpage_url)
                pattern = re.compile(r'/pic')
                match = pattern.match(fourthpage_url)
                if match:
                    return 0
                else:
                    global thirdpage_id
                    thirdpage_id = thirdpage_id + 1
                    print('this is thirdpage_id of    ' + str(thirdpage_id))
                    fourthpage_title = everylink.get_text()
                    print(fourthpage_title)    #·1
                    fourthpage_urloutput="http://baike.baidu.com"+fourthpage_url  #2
                    print(fourthpage_urloutput)##这边要总结一下 就是返回值为None如何清除 用if is None return 0 else print（）
                        #下载第四级页面url的html
                    header = {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip,deflate,sdch',
                            'Accept-Language': 'zh-CN,zh;q=0.8',
                            'Connection': 'keep-alive',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'

                        }
                    timeout = random.choice(range(80, 180))
                    # while True:
                    # time.sleep(5)
                    try:
                        response3 = urllib.request.urlopen(fourthpage_urloutput)
                        raw_data = response3.read().decode('utf-8')
                    except urllib.request.HTTPError as e:
                         print('except 1:', e.code)
                            # time.sleep(random.choice(range(5, 10)))
                    except urllib.request.URLError as e:
                        print('except 2:', e.reason)
                            # time.sleep(random.choice(range(5, 10)))
                    except:
                         print('except 0')
                            # except :
                            #     return 0
                        # print(raw_data)
                        #解析之
                    global raw_data
                    soup3 = BeautifulSoup(raw_data, 'html.parser')
                        # body3 = soup3.body  # 获取body部分
                        # print(body3)  #2、no attribute to.....这个错误 解决方法
                    data3 = soup3.find_all('meta', {'name': 'keywords'})  # 找到id为7d的div
                        # print(data3)
                    for i in data3:
                            fourthpage_content=i.get('content')
                            # print(fourthpage_title)
                            # print(fourthpage_urloutput)
                            # print(fourthpage_content)   #`3
                            insertinto_db_2_1.insert(thirdpage_id, fourthpage_title, fourthpage_urloutput,
                                                     fourthpage_content)
                            insertinto_db_2_2.insert(thirdpage_url_id, thirdpage_id)

                    soup_findattribute= BeautifulSoup(raw_data, 'html.parser')
                    data_findattribute = soup_findattribute.find_all('div', {'class': 'basic-info cmn-clearfix'})
                    # print(data_findattribute)
                    data_findattribute_dict={}
                    for attributes in data_findattribute:
                        attribute_names=attributes.find_all('dt', {'class': 'basicInfo-item name'})
                        names_list=[]
                        for a in attribute_names:
                            attribute_name=a.get_text()
                            names_list.append(attribute_name)
                            # print(attribute_name)
                        attribute_values =attributes.find_all('dd', {'class': 'basicInfo-item value'})
                        values_list=[]
                        for b in attribute_values:
                            attributes_value = b.get_text()
                            values_list.append(attributes_value)
                        nvs = zip(names_list, values_list)
                        nvDict = dict((str(names_list), str(values_list)) for names_list, values_list in nvs)
                        for names_lists, values_lists in nvDict.items():
                            # print(fourthpage_title)
                            names_lists_insert=names_lists
                            value_lists_insert =values_lists
                            # print(names_lists,values_lists)
                            # print('0000000')
                            insertinto_db_3.insert(fourthpage_title, names_lists_insert, value_lists_insert,thirdpage_id)
                        # print(nvDict)
                        # print(type(nvDict))
                # return fourthpage_url
    return

if __name__ == '__main__':
    firstpage_html= get_firstpage_content("https://baike.baidu.com/science")
    firstpage_urls=get_firstpage_url(firstpage_html)
    tagids=get_firstpage_tagid(firstpage_urls)
    thistime = 0
    thirdpage_id = 64480 #227 #15730巴西红耳龟 17199自切
    thirdpage_url_id = 64264 #11
    global thirdpage_url_id
    pageid = 21
    for i in range(0,len(firstpage_urls)-1):
        # pageid=pageid+1
        global thirdpage_id
        global thirdpage_url_id
        # print(type(tagids[i]))
        whichtime = thistime + 1

        url = firstpage_urls[i]
        id = tagids[i]
        url='https://baike.baidu.com/wikitag/api/getlemmas'
        pageid=pageid+1
        thirdpage_url = get_secondpage_url(url, id, pageid)
        # title3_to_url3_dict = get_third_webpage_title_and_url(root_url, tag_id, page)
        print(whichtime)
        # secondpage_id=0
        # global thirdpage_id
        global thirdpage_url_id
        for title3, url3 in thirdpage_url.items():
            thirdpage_url_id = thirdpage_url_id+1
            print(thirdpage_url)
            print('this is thirdpage_url_id of  '+str(thirdpage_url_id)+title3)
            global thirdpage_id

            # thistime_secondpage_id = secondpage_id+1
            # print('ralation'+str(thistime_secondpage_id))
            content3 = get_thirdpage_content(url3)
            # thirdpage_id =thirdpage_id+1
            # print(thirdpage_id)
            # print(content3)

            thirdpage_content=parsethirdpage_main_content(content3)
            #
            # print(title3)
            # print(url3)
            # print(thirdpage_content)
            insertinto_db.insert(thirdpage_url_id,title3, url3, thirdpage_content)#第二次插入24*9个二级url的title url、content-277纪录



        # myurl=
    # thirdpage_content=get_thirdpage_content(myurl)
    # print(thirdpage_content)

