try:
    # Python2
    from urllib import urlretrieve
except ImportError:
    # Python3
    from urllib.request import urlretrieve
# find yourself a picture on an internet web page you like
# (right click on the picture, look under properties and copy the address)
#url = "http://www.google.com/intl/en/images/logo.gif"
url="https://sirius.androidapks.com/rdata/e84da00b1ab12f4a0e4ecf9f52f57b9d/io.friendly_v1.9.84-321_Android-4.4.apk"
filename = "logo.apk"
# retrieve the image from the url and save it to file
urlretrieve(url, filename)
