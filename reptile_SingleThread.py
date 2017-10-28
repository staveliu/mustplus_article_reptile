import requests
from lxml import etree
import pymysql.cursors
i="1"
title=[]
url=[]
connection = pymysql.connect(host='',
                             port=3306,
                             user='',
                             password='',
                             db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
while True:
    try:
        response = requests.get("https://must.plus/article/?paged="+i,timeout=5)
        html = etree.HTML(response.text)
        title_new = html.xpath('//article/header/h1/a/text()')
        url_new = html.xpath('//article/header/h1/a/@href')
        title = title+title_new
        url = url+url_new
        print(i)
        print(title_new)
        print(url_new)
        if "早期文章" in response.text:
            i = str((int(i)+1))
        else:
            break
    except:
        print("Timed Out, Retry")
print("ok")
i=0
url_content=[]
for url_current in url:
    while True:
        try:
            response = requests.get(url_current,timeout=5)
            break
        except:
            print("Timed Out, Retry")
    html = etree.HTML(response.text)
    url_content = html.xpath("//article/div/p/a/@href")
    article_time = html.xpath("//article/header/div/a/time/@datetime")
    content_new = ""
    for url_content_current in url_content:
        content_new = content_new+url_content_current.replace("./","https://must.plus/article/")+";"
    if content_new=="":
        content_new = "null"
    content_time=article_time[0].replace("T"," ")
    print(content_new)
    print(content_time)
    try:
        with connection.cursor() as cursor:
            verify=cursor.execute("SELECT * FROM cxh WHERE content='"+content_new+"'")
            if verify==0:
                sql="INSERT INTO cxh (title,content,article_time) VALUES (%s,%s,%s)"
                cursor.execute(sql,(title[i],content_new,content_time))
            else:
                print("Exist. Jump over")
        connection.commit()
    except:
        print("Sql Run Error")
    i=i+1
