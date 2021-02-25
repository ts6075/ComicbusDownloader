# coding=utf8
# #################
# 作者: ts6075
# 開始日期: 20190511
# 程式目的: 爬取並下載漫畫圖片
# 版本記錄
# v1.0 - 20190511 - 初版
# 備註: 撰寫完畢已可正常執行,尚可優化及提供動態設定、自動偵測新集數等功能
# #################
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os

# #################
# # 基礎設定       #
# #################
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.comicbus.com/online/comic-7340.html?ch=' # 漫畫內頁url
chapter = '117'                                             # 第幾集
page = '1'                                                  # 第幾頁
getUrl = url + chapter + '-' + page                         # 漫畫內頁完整url
imgUrls = []                                                # 記錄所有漫畫圖片url
folderPath = './Comic/'                                     # 存放圖片的資料夾

driver = webdriver.Chrome('./chromedriver')                 # 啟動Chrome

# #################
# # 取得最大頁數   #
# #################
driver.get(getUrl)                                          # 載入頁面
soup = BeautifulSoup(driver.page_source, 'lxml')            # 取得網頁資訊
maxPage = soup.select('select[id=pageindex] option')[-1]    # 取得頁數下拉單最後一筆
maxPage = int(maxPage.get('value'))                         # 取得最大頁數

# #################
# # 取得所有漫畫圖片url #
# #################
for i in range(1, maxPage + 1):
    page = str(i)
    getUrl = url + chapter + '-' + page

    driver.get(getUrl)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    imgUrl = soup.select_one('img[id=TheImg]').get('src')   # 取得漫畫圖片url

    if (imgUrl is None):                                    # 預防error
        print('未找到圖片url' + imgUrl)
    else:
        imgUrls.append(imgUrl)
driver.close()                                              # 關閉Chrome
print(imgUrls)

# #################
# # 建立存放圖片資料夾 #
# #################
if (os.path.exists(folderPath) is False):    # 判斷資料夾是否存在
    os.makedirs(folderPath)                  # Create folder

# #################
# # 批次下載圖片   #
# #################
ses = requests.Session()                     # 建立Session
for i, src in enumerate(imgUrls):
    if (src):
        srcUrl = 'http:' + src               # src已經有//,故不再加上
        res = ses.get(srcUrl, headers=headers)

        imgName = folderPath + chapter + '-' + str(i + 1) + '.jpg'
        with open(imgName, 'wb') as file:    # 以byte的形式將圖片數據寫入
            file.write(res.content)
            file.flush()
        file.close()                         # close file
        print('第 %d 張' % (i + 1))
print('Done')
