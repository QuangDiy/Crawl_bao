from bs4 import BeautifulSoup
import httpx
import pandas as pd
import Connection

topic =[]
title =[]
des =[]
content =[]
links=[]
tenbao=[]
date = []
news_type=[]
link_temp =[]
tenbao='Báo Thanh Niên'
topiclist = {
"Thời sự": "https://thanhnien.vn/thoi-su.htm",
"Thế giới": "https://thanhnien.vn/the-gioi.htm",
"Kinh tế":"https://thanhnien.vn/kinh-te.htm",
"Đời sống":"https://thanhnien.vn/doi-song.htm",
"Giải trí":"https://thanhnien.vn/giai-tri.htm",
"Thể thao":"https://thanhnien.vn/the-thao.htm",
"Giáo dục":"https://thanhnien.vn/giao-duc.htm",
"Sức khoẻ":"https://thanhnien.vn/suc-khoe.htm",
"Giới trẻ""":"https://thanhnien.vn/gioi-tre.htm",
"Du lịch":"https://thanhnien.vn/du-lich.htm",
"Văn hoá":"https://thanhnien.vn/van-hoa.htm",
"Công nghệ - Game":"https://thanhnien.vn/cong-nghe-game.htm",
"Xe":"https://thanhnien.vn/xe.htm",
"Tiêu dùng":"https://thanhnien.vn/tieu-dung-thong-minh.htm"
}

def news_classifier(link):
  html = httpx.get(link,follow_redirects=True)
  soup = BeautifulSoup(html)
  if ("video" in link):
    a = (soup.find("h1",class_="title").get_text())
    b = (soup.find("div",class_="lead_detail").get_text(" ",strip=True))
    c = None
    d = (soup.find("span", class_="time").get_text())
    e= "Video"
    return a,b,c,d,e
  else:
    a = soup.title.get_text()
    b = (soup.find(attrs={"name": "description"}).attrs)['content']
    content_temp =""
    for i in soup.find_all("p"):
      content_temp += i.get_text("" ,strip=True)
    c = content_temp 
    d = (soup.find(attrs={"itemprop": "dateModified"}).attrs)['content']
    e= "Megazine"
    return a,b,c,d,e

def get_all_link(topiclist):
  for i in topiclist:
    print(topiclist[i])
    html = httpx.get(topiclist[i])
    soup = BeautifulSoup(html)
    for div in soup.find_all("h3" , class_="box-title-text"):
      links.append("https://thanhnien.vn" + f"{div.find('a').get('href')}")
      topic.append(i)
  print(len(links))

def parsing_link():
  content_temp=""
  for lk in links:
    html = httpx.get(lk,follow_redirects=True)
    soup = BeautifulSoup(html)
    try:
      a=soup.title.get_text()
      b=(soup.find("h2", class_="detail-sapo").get_text())
      for i in soup.find_all("p"):
        content_temp = content_temp + i.get_text(" ",strip=True) 
      c = content_temp
      d=(soup.find(attrs={"data-role": "publishdate"}).get_text(" ", strip=True))
      e="Text"
    except:
      # a,b,c,d,e = news_classifier(lk)
      # title.append(a)
      # des.append(b)
      # content.append(c)
      # date.append(d)
      # news_type.append(e)
      print(lk)
    else: 
      title.append(a)
      des.append(b)
      content.append(c)
      date.append(d)
      news_type.append(e)


def df_to_DB():
  get_all_link(topiclist)
  parsing_link()
  df=pd.DataFrame([])
  df_temp = pd.DataFrame({ 'Title':title, 'Link':links, 'Topic':topic, 'Mô tả':des, "Nội dung":content,"Tên báo":tenbao, "Ngày đăng":date}) #Tạo DF
  df = pd.concat([df, df_temp], axis = 0, ignore_index=True) #nối DF
  df.to_csv("VNE.csv")




def main():
  df_to_DB()

if __name__ == "__main__":
    main()