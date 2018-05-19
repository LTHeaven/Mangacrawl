from bs4 import BeautifulSoup

def getMangaTitle(soup, home):
    if home:
        return soup.find("div", {"class": "manga-detail"}).find("h1").get_text()
    else:
        return soup.find("h1", {"class" : "title"}).get_text()      
        
def findChapterUl(soup, home):
    if home:
        return soup.find("ul", {"class" : "detail-chlist"})
    else:
        return soup.find("div", {"class" : "detail_list"}).ul
        
def getChapterName(li, home):
    if home:
        return li.find("span", {"class" : "mobile-none"}).get_text()
    else:
        return li.find("a").get_text().replace("\n", "")
        
def getCoverImageUrl(soup, home):
    if home:
        return soup.find("img", {"class" : "detail-cover"}).get("src")    
    else:
        return soup.find("img", {"class" : "img"}).get("src")

def getNextUrl(soup, home):
    if home:
        return "https:" + soup.find("img", {"id" : "image"}).parent.get("href")
    else:
        return "https:" + soup.find("a", {"class" : "next_page"}).get("href")

        
      
        
        
        
        
        
        
        
#def getSavedPage(home):
 #   if home:
  #      with open('C:\Users\Med. Informatik\Documents\Mangacrawler/home.txt', 'r') as myfile:
   #         return myfile.read().replace('\n', '')
    #else:
     #   with open('C:\Users\Med. Informatik\Documents\Mangacrawler/here.txt', 'r') as myfile:
      #      return myfile.read().replace('\n', '')