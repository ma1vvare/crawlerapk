import urllib2
import collections
import traceback
import requests
import time
import logging
import socket

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename='logging.txt') #write all logs into logging.txt
def get_time():
    return time.strftime('%H:%M:%S')

def get_full_time():
    return time.strftime('%H:%M:%S, %A %b %Y')

socket.setdedaulttimeout(5)
dlink = "https://sirius.androidapks.com/rdata/e84da00b1ab12f4a0e4ecf9f52f57b9d/io.friendly_v1.9.84-321_Android-4.4.apk"
hdr = {'User-Agent':'Mozilla/5.0 (Linux x86_64)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
request = urllib2.Request(dlink,headers=hdr)
try:
    page = urllib2.urlopen(request)

except urllib2.HTTPError, e:
    traceback.print_exc()
logging.warning('this is warning')
logging.info('this is information')
apk_content = page.read()

filename ='/home/peterhsiao/Desktop/apk/test.apk'

with open(filename,"wb") as code:
    code.write(apk_content)
    code.close()
#urlretrieve(dlink, filename)
