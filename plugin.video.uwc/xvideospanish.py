import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def Main():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.xvideospanish.com/categorias/',133,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://www.xvideospanish.com/?s=',134,'','')
    List('http://www.xvideospanish.com/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<section class="pst-cn.*?<figure><a href="([^"]+)".*?data-original="([^"]+)".*?alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name[7:])
        utils.addDownLink(name, videopage, 132, img, '')
    try:
        nextp=re.compile('<a class="nextpostslink" rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 131,'')
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
    match = re.compile('<figure class="ctg-img.*?<a href="([^"]+)".*?alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 131, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
