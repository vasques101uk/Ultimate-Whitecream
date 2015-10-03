import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def Main():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.pelisxporno.com/',143,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://www.pelisxporno.com/?s=',144,'','')
    List('http://www.pelisxporno.com/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div class="thumb">.*?href="([^"]+)".*?src="([^"]+)".*?alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 142, img, '')
    try:
        nextp=re.compile('<a class="nextpostslink" rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 141,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def Search(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    List(searchUrl)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<li id="categories-2"(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 141, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
