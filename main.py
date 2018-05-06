import requests, os, urllib.request, progressbar,sys, siteinterface, img2pdf, fitz
from bs4 import BeautifulSoup
from PIL import Image

currentPages = 1

def findLastPage(options):
    while True:
        cond = True
        s = options.pop().get_text()
        try:
            return int(s)
        except ValueError as verr:
            cond = False
        if cond == True:
            break

def createIfNotExists(name):
    if not os.path.exists(name):
        os.mkdir(name)
        print("Creating '" + name + "' folder...")


def download_image(url, file_name, images):
    if not os.path.exists(file_name):
        try:
            urllib.request.urlretrieve(url, file_name)
            basewidth = 600
            img = Image.open(file_name)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            img.save(file_name)
        except Exception as ex:
            workingdirectory = os.getcwd()
            os.chdir("..")
            os.chdir("..")
            img = Image.open("error.jpg")
            os.chdir(workingdirectory)
            img.save(file_name)
            print("there was an error with " + file_name)
            
    images.append(file_name)

def chapterCrawl(name, url, images, toc):
    print("Downloading '" + name + "'...")
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    last_page = findLastPage(soup.findAll("option"))
    global currentPages
    toc.append([1, name, currentPages+1])
    currentPages = currentPages + last_page
    bar = progressbar.ProgressBar(max_value=last_page, redirect_stdout=True)
    current_url = url
    while True:
        current_soup = BeautifulSoup(requests.get(current_url).text, "html.parser")
        try:
            current_page = int(current_soup.find("option", {"selected" : "selected"}).get_text())
		
            image_url = current_soup.find("img", {"id": "image"}).get("src")
            bar.update(current_page)
            download_image(image_url, name + str(current_page) + ".jpg", images)

            if not current_page < last_page:
                break
        except Exception as ex:
            print("error with currentPage")
        current_url = "https:" + current_soup.find("img", {"id" : "image"}).parent.get("href")

def download_manga(url, arg2):
    home = "mangahome" in url
    try:
        page = requests.get(url)
    except Exception as ex:
        print("Not a URL")
        return
		
    try:
        max_chapters = int(arg2)
    except ValueError as verr:
        print("no max chapter number provided, downloading all chapters...")
        max_chapters = 999999
   
    plain_text = page.text #siteinterface.getSavedPage(home)#
    soup = BeautifulSoup(plain_text,"html.parser")

    manga_title = siteinterface.getMangaTitle(soup, home)
    createIfNotExists(manga_title)
    os.chdir(manga_title)

    images = []
    toc = []
    cover_image_url = siteinterface.getCoverImageUrl(soup, home)
    download_image(cover_image_url, "cover.jpg", images)
    ul = siteinterface.findChapterUl(soup, home)
    counter = 1
    for li in reversed(ul.findAll("li")):
        chapter_link = "https:" + li.a.get("href")
        chapter_name = str(counter) + " - " + siteinterface.getChapterName(li, home)
        chapterCrawl(chapter_name, chapter_link, images, toc)

        if counter >= max_chapters:
            break
        else:
            counter += 1
    pdf_bytes = img2pdf.convert(images)
    for image_file in images:
        os.remove(image_file)
    file = open(manga_title + ".pdf","wb")
    file.write(pdf_bytes)
    
    doc = fitz.open(manga_title + ".pdf")
    doc.setToC(toc)
    doc.save(doc.name, incremental=True)
    print(doc.getToC())

os.chdir(os.path.dirname(os.path.abspath(__file__)))
createIfNotExists("mangas")
os.chdir("mangas")

if len(sys.argv) > 1:
    if len(sys.argv) > 2:
        download_manga(str(sys.argv[1]), sys.argv[2])
    else:
        download_manga(str(sys.argv[1]), "noNumber")    
else:
	print("Missing url")