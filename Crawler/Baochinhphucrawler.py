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
link_temp =[]
content_temp =""
tenbao='Báo Chính Phủ'
topiclist = {
"Chính trị": "https://baochinhphu.vn/chinh-tri.htm",
"Kinh tế": "https://baochinhphu.vn/kinh-te.htm",
"Văn hoá": "https://baochinhphu.vn/van-hoa.htm",
"Xã hội": "https://baochinhphu.vn/xa-hoi.htm",
"Khoa giáo":"https://baochinhphu.vn/khoa-giao.htm",
"Quốc tế":"https://baochinhphu.vn/quoc-te.htm"
}
tablename="public.newtable"

def get_all_link(topiclist):
  for i in topiclist:
    print(topiclist[i])
    html = httpx.get(topiclist[i])
    soup = BeautifulSoup(html)
    for div in soup.find_all("div",class_="box-stream-item"):
      links.append("https://baochinhphu.vn" + f"{div.find('a').get('href')}")
      topic.append(i)

def parsing_link():
  for lk in links:
    html = httpx.get(lk,follow_redirects=True)
    soup = BeautifulSoup(html)
    try:
      a=(soup.find("h1",class_="detail-title").get_text())
      b=(soup.find("h2", class_="detail-sapo").get_text(strip=True))
      c=(soup.find(attrs={"data-role": "content"}).get_text(" ", strip=True))
      d=(soup.find("div", class_="detail-time").get_text(" ", strip=True))
    except:
      print(lk)
    else: 
      title.append(a)
      des.append(b)
      content.append(c)
      date.append(d)


def df_to_DB():
  get_all_link(topiclist)
  parsing_link()

  df=pd.DataFrame([])
  df_temp = pd.DataFrame({ 'Title':title, 'Link':links, 'Topic':topic, 'Mô tả':des, "Nội dung":content,"Tên báo":tenbao, "Ngày đăng":date}) #Tạo DF
  df = pd.concat([df, df_temp], axis = 0, ignore_index=True) #nối DF
  print(df)
  # for i in range(len(df)):
  #   temp = df.iloc[i-1:i]
  #   Connection.InsertData(temp,tablename)

def main():
  df_to_DB()

if __name__ == "__main__":
    main()
