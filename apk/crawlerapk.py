from bs4 import BeautifulSoup
from termcolor import colored
import urllib
import urllib2
import threading,time
import collections
import traceback
import sys
import logging
#filepath = /home/peterhsiao/
#filename =pge_name+'.apk'
source = "http://www.androidapksfree.com/applications/apps"
soup = BeautifulSoup(urllib.urlopen(source))

logging.basicConfig(format='%(asctime)s %(message)s',
                    dtefmt='%Y-%m-%d %I:%M:%S',
                    level=logging.ERROR)



def Retry_session(link,max_retry = 10):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

    while max_retry > 0:
        try:
            request = urllib2.Request(link,headers=headers)
            session = urllib2.urlopen(request,timeout = 150)
            return session
        except:
            time.sleep(3)
            logging.info('Reconnect %s %d',link,(10 - max_retry))
            max_retry = max_retry - 1
    return False


def _download_apk(dlink,apkname):
    #dlink = "https://sirius.androidapks.com/rdata/e84da00b1ab12f4a0e4ecf9f52f57b9d/io.friendly_v1.9.84-321_Android-4.4.apk"
    hdr = {'User-Agent':'Mozilla/5.0 (Linux x86_64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    # use header to change crawler to browser for crawling
    request = urllib2.Request(dlink,headers=hdr)
    try:
        page = urllib2.urlopen(request)
        apk_content = page.read()
        filepath='/home/peterhsiao/Desktop/apk/'
        filename = filepath+apkname+'.apk'
        with open(filename,"wb") as f:
            f.write(apk_content)
            f.close()
    except urllib2.HTTPError, e:
        traceback.print_exc()

    #targetapk = "https://sirius.androidapks.com/rdata/e84da00b1ab12f4a0e4ecf9f52f57b9d/io.friendly_v1.9.84-321_Android-4.4.apk"

def _get_d_link(fakeURL):
    d_link = fakeURL + '/download'
    src_exist_page = BeautifulSoup(urllib.urlopen(str(d_link)))
    #print "src page : ",src_exist_page
    #print "dlink : ",d_link
    for url in src_exist_page.findAll('iframe',{'class':'hidden-frame'}):
        d_link = url.get('src')
    #print "src_exist_page : ",src_exist_page
    return d_link

def _get_pkg_name(fakeURL):
    pkg_exist_page = BeautifulSoup(urllib.urlopen(fakeURL))
    pkg_name = pkg_exist_page.find("div",{"class":"apk_file_div"}).dd.string
    #print "pkgName : ",pkg_name
    return pkg_name

class download_thread(threading.Thread):
    print "download_thread function!"
    def __init__(self,rawContent,data):
        super(download_thread,self).__init__()
        #threading.Thread.__init__(self)
        self.rawContent = rawContent
        #self.category = category
        self.data = data

def run(rawContent,data):
    #data = self.rawContent.findAll("div",{"class": "image-style-for-related-posts"})# 84 items
    fakeURL_list = []
    pkg_name_list = []
    dlink_list = []
    for content in xrange(0,len(data)):
        for url in data[content].findAll("a"):
            try:
                fakeURL = url.get('href')
                fakeURL_list.append(fakeURL)
                apk_name=url.get('href')[36:][:-1]
                #time.sleep(0.1)
                print fakeURL
                print colored("downloading",'red'),apk_name,"..."
                pkg_name = _get_pkg_name(fakeURL)
                pkg_name_list.append(pkg_name)
                #print pkg_name

                dlink = _get_d_link(fakeURL)
                dlink_list.append(dlink)
                #print "dlink : ",dlink
                #print "apk_name : ",apk_name
                #_download_apk(dlink,apk_name)
            except Exception,e:
                traceback.print_exc()
    print "Size of fakeURL_list",len(fakeURL_list)
    print "Size of pkg_name_list",len(pkg_name_list)
    print "Size of dlink_list",len(dlink_list)
def main():
    category_list = []
    category_subpage=[]
    for content in range(0,1):
        rawContent = soup.findAll("div",{"class": "col-8 main-content"})[content] #main content
        herf = rawContent.findAll("a",{"class": "taxonomy_button limit-line"}) # size of herf is 14
        for rawCategory in herf:
            try:
                category_list.append(rawCategory.get('href')[44:][:-1]) # grep category string
                category_subpage.append(rawCategory.get('href'))
                #print category
                #DownloadThread=download_thread(rawContent,category).run()
                #test(rawContent,category)
            except Exception,e:
                traceback.print_exc()
                print "download error"
    data = rawContent.findAll("div",{"class": "image-style-for-related-posts"})# 84 items

    #download_thread(rawContent,data).run()
    run(rawContent,data)

if __name__=='__main__':
    main()
