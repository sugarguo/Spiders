#coding=utf-8
'''
Created on 2015年9月17日

@Site:  http://www.sugarguo.com/

@author: 'Sugarguo'
'''

from bs4 import BeautifulSoup
import requests
import re
import time

ListNames = []
SearchWord = ' 搜  索 '
print '\n***************[Start]***************\n'

#定义一些文件头
headers = {'Host': 'www.freexs.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': 'jq_Obj=1; jieqiVisitId=article_articleviews%3D98052%7C105973%7C69789%7C105925; jieqiVisitTime=jieqiArticlesearchTime%3D1442408752',
            'Connection': 'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded'
            }


def getConfig():
    f = open('config.txt')
    for line in f.readlines():
        line = line.replace('\n','').strip()
        ListNames.append(line)
    f.close()
    print '\tGet Config is OK!\n'
    return ListNames

def GetHtml(TextBookName,GetUrl):
    try:     
        data = {'searchtype':'articlename',
                'searchkey': TextBookName.decode('utf-8').encode('GBK'),
                'action':'login',
                'submit': SearchWord.decode('utf-8').encode('GBK')}
        r = requests.post("http://www.freexs.cn/modules/article/search.php",headers=headers,data=data)
        r.encoding = 'GBK'
        GetUrl = str(r.url).strip()
        print 'Get Url : ',GetUrl
        
        if GetUrl == "http://www.freexs.cn/modules/article/search.php":
            f3 = file('No.txt','a+')
            if TextBookName in f3.read():
                f3.close()
            else:
                f3.write(TextBookName + '\n')
                f3.close()
        else:
            f = file('All.txt','a')
            f2 = file('All.html','a')
            Id = re.findall(r'(\w*[0-9]+)\w*',GetUrl)[0]
            print 'Name: ',TextBookName.decode('utf-8').strip(),'Id: ',Id
            print 'Url: ',GetUrl
            print '***************[ Next ]***************\n'
            f.write(TextBookName.strip() + '\t\t\t' + str(Id) +'\n')
            f.close()
            f2.write('\t<tr>\n\t\t<th>' + str(TextBookName).strip() + '</th>\n\t\t<th>' + str(Id).strip() + '</th>\n\t\t<th>' + GetUrl + '</th>\n\t\t<th><a href=' + GetUrl + '>点击浏览</a></th>\n\t<tr>')
            f2.close()
            time.sleep(2)                
    except Exception as e:
        print(e)
        f3 = file('No.txt','a+')
        f3.write(TextBookName + '\n')
        f3.close()
        
f2 = file('All.html','w')
f2.write('<html>\n<body>\n<head>\n<meta charset="utf-8" />\n</head><table border="1">\n')
f2.close()
ListNames = getConfig()
for item in ListNames:
    GetHtml(item.strip(),item.strip())
f2 = file('All.html','a')
f2.write('</table>\n</body>\n</html>')
f2.close()
print '\n***************[  OK! ]***************\n'
