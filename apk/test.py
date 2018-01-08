from bs4 import BeautifulSoup
from termcolor import colored
from pymongo import MongoClient, HASHED
from datetime import datetime
#from Mongo import DB

from core.db.Mongo import DB
import urllib
import urllib2
import threading,time
import collections
import traceback
import sys
import logging
import time
#filepath = /home/peterhsiao/
#filename =pge_name+'.apk'
source = "http://www.androidapksfree.com/applications/apps"
soup = BeautifulSoup(urllib.urlopen(source))

logging.basicConfig(format='%(asctime)s %(message)s',
                    dtefmt='%Y-%m-%d %I:%M:%S',
                    level=logging.ERROR)

timestamp = datetime.now().strftime('%y-%m-%d')

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
        filepath='/home/peterhsiao/Desktop/fullapk/'
        filename = filepath+apkname+'.apk'
        with open(filename,"wb") as f:
            f.write(apk_content)
            f.close()
            return apk_content
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
    if type(pkg_name) =='None':
         pkg_name = pkg_exist_page.findAll("div",{"class":"post-content description"}).p.text()[1]

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

def run(category_subpage):

    #data = self.rawContent.findAll("div",{"class": "image-style-for-related-posts"})# 84 items
    apk_info = {}
    apk_info['appCategory'] = []
    apk_info['source'] = source
    apk_info['packageName']=[]
    apk_info['apkName']=[]
    fakeURL_list = []
    pkg_name_list = []
    dlink_list = []

    result = {}
    result['vt_scan']=False
    result['url_scan']=False
    result['source']='androidapksfree.com/applications/apps'
    #result['title']=category_subpage

    for subpage_link in category_subpage:
        subpage = BeautifulSoup(urllib.urlopen('https://'+subpage_link))
        subpg = subpage.findAll("div",{"class": "image-style-for-related-posts"})
        for content in xrange(0,len(subpg)):
            for url in subpg[content].findAll("a"):
                try :
                    fakeURL = url.get('href')
                    fakeURL_list.append(fakeURL)
                    #print "fakeURL : ",fakeURL
                    apk_name=url.get('href')[36:][:-1]
                    print colored("downloading",'red'),apk_name,"..."
                    pkg_name = _get_pkg_name(fakeURL)
                    pkg_name_list.append(pkg_name)

                    dlink = _get_d_link(fakeURL)
                    dlink_list.append(dlink)
                    apk_category = subpage_link[42:][:-1]

                    apk_info['appCategory'].append(apk_category)
                    apk_info['packageName'].append(pkg_name)
                    apk_info['apkName'].append(apk_name)

                    result['title'] = apk_category
                    result['pkgName'] = pkg_name
                    file_name = result['pkgName']+'.apk'
                    result['name'] = file_name
                    result['timeStamp'] = timestamp
                    #print "apk_name : ",apk_name
                    #apkdata=_download_apk(dlink,apk_name)
                    #result['apkData'] = apkdata
                    DB().insert_apk(result)
                    DB().get_apk_info()
                except Exception,e:
                    traceback.print_exc()

    #print "Size of fakeURL_list",len(fakeURL_list)
    #print "Size of pkg_name_list",len(pkg_name_list)
    #print "Size of dlink_list",len(dlink_list)
def main():
    category_list = []
    category_subpage=[]
    for content in range(0,1):
        rawContent = soup.findAll("div",{"class": "col-8 main-content"})[content] #main content
        herf = rawContent.findAll("a",{"class": "taxonomy_button limit-line"}) # size of herf is 14
        for rawCategory in herf:
            try:
                category_list.append(rawCategory.get('href')[44:][:-1]) # grep category string
                category_subpage.append(rawCategory.get('href')[2:][:-1])
            except Exception,e:
                traceback.print_exc()
                print "download error"

    run(category_subpage)

if __name__=='__main__':
    main()
