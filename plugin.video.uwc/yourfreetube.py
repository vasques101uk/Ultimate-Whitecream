import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def YFTMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.yourfreetube.net/index.html',193,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://www.yourfreetube.net/search.php?keywords=',194,'','')
    YFTList('http://www.yourfreetube.net/newvideos.html')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def YFTList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a href="([^"]+)"[^<]+<[^<]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        utils.addDownLink(name, videopage, 192, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)">&raquo;', re.DOTALL | re.IGNORECASE).findall(listhtml)
        nextp = "http://www.yourfreetube.net/" + nextp[0]
        utils.addDir('Next Page', nextp, 191,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def YFTSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    YFTList(searchUrl)


def YFTCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<ul class="pm-browse-ul-subcats">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('<a href="([^"]+)" class="">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 191, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def YFTPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)

