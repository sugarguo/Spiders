#coding=utf-8
'''
Created on 2015年9月15日

@Site:  http://www.sugarguo.com/

@author: 'Sugarguo'
'''


from bs4 import BeautifulSoup
import requests
import re
import xlwt
import time
import os
import threading

ListName = []
ListId = []
ListAct = []
ListState = []
ListTime = []
ListSize = []
dataList = []

wb = xlwt.Workbook()
style0 = xlwt.easyxf('font: name Arial, color-index green, bold on')
style1 = xlwt.easyxf('font: name Arial, color-index red, bold on')
style2 = xlwt.easyxf('font: name Arial, color-index blue, bold on')

ws = wb.add_sheet(u'All-By-Sugarguo',cell_overwrite_ok=True)

startUrl = 'http://www.freexs.cn/top/allvisit_'
endUrl = '.htm'
UrlList = []

def GetUrlList(StartNum,EndNum):
    while(1):
        if StartNum > EndNum:
            break
        else:
            Url = startUrl + str(StartNum) + endUrl
            UrlList.append(Url)
            StartNum = StartNum + 1
    return UrlList

def InstertList(Url):
    r = requests.get(Url)
    html_doc = r.text
    html_doc = html_doc.encode('latin1').decode('gbk').encode('utf-8')
    
    soup = BeautifulSoup(html_doc)
    i = 0
    tdlist = soup.find_all(re.compile('^td'))
    for index,item in enumerate(tdlist):
        if index == i :
            Name = BeautifulSoup(str(item)).a.string
            getid = BeautifulSoup(str(item)).a['href']
            Id = re.findall(r'(\w*[0-9]+)\w*',getid)[0]
            Act = BeautifulSoup(str(tdlist[i + 1])).td.string
            State = BeautifulSoup(str(tdlist[i + 2])).string
            Time = BeautifulSoup(str(tdlist[i + 3])).td.string
            Size = BeautifulSoup(str(tdlist[i + 4])).td.string
            data = [Name,Id,Act,State,Time,Size]
            dataList.append(data)
            ListName.append(Name)
            ListId.append(Id)
            ListAct.append(Act)
            ListState.append(State)
            ListTime.append(Time)
            ListSize.append(Size)
            #print Name,Id
            #print '\n======================================\n'
            i = i + 5
        else:
            continue

def WriteXLS(dataList):
    ws.write(0, 0 , 'Num', style0)
    ws.write(0, 1 , 'Name', style1)
    ws.write(0, 2 , 'ID', style2)
    ws.write(0, 3 , 'Act', style0)
    ws.write(0, 4 , 'State', style1)
    ws.write(0, 5 , 'Time', style2)
    ws.write(0, 6 , 'Size', style0) 
    for i in range(7):
        ws.col(i).width = 5000
    i = 1
    for item in dataList:
        #print dataList[item[0]]
        ws.write(i, 0, str(i), style0)
        ws.write(i, 1, item[0].strip(), style1)
        ws.write(i, 2, item[1].strip(), style2)
        ws.write(i, 3, item[2].strip(), style0)
        ws.write(i, 4, item[3].strip(), style1)
        ws.write(i, 5, item[4].strip(), style2)
        ws.write(i, 6, item[5].strip(), style0)
        i = i + 1 
    
    ws.write(len(dataList) + 3, 0 , '-By: Sugarguo', style0)
    ws.write(len(dataList) + 3, 2 , '-Url: http://www.sugarguo.com/', style0) 
    
    wb.save('GetID-All-By-Sugarguo.xls')
    print '\tSave OK!\n'
    print '\tYou can open GetID-All-By-Sugarguo.xls\n'
    print '\tSleep 3s Auto Open Directory'
    print '\n***************[ End ]***************\n'
    time.sleep( 3 )
    os.system("explorer.exe %s" % os.getcwd())
    
UrlList = GetUrlList(1,2)
for index,item in enumerate(UrlList):
    print str(index),item
    InstertList(item.strip())
    
print '\n***************[ Next]***************\n'
print '\tWrite XLS...\n'
WriteXLS(dataList)
