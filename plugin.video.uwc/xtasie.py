import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress


def XTCMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://xtasie.com/video-porn-categories/',203,'','')
    utils.addDir('[COLOR yellow]Top Rated[/COLOR]','http://xtasie.com/top-rated-porn-videos/page/1/',201,'','')
    utils.addDir('[COLOR yellow]Most Rated[/COLOR]','http://xtasie.com/most-viewed-porn-videos/page/1/',201,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://xtasie.com/?s=',204,'','')
    XTCList('http://xtasie.com/porn-video-list/page/1/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def XTCList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile(r'<div class="image-holder">\s+<a href="([^"]+)".*?><img.*?data-original="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 202, img, '')
    try:
        nextp=re.compile('<a class="next page-numbers" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = nextp[0]
        utils.addDir('Next Page', next, 201,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def XTCSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    XTCList(searchUrl)


def XTCCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<p><a href="([^"]+)".*?<img src="([^"]+)".*?<h2>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, img, name in match:
        utils.addDir(name, catpage, 201, img)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def XTCPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
