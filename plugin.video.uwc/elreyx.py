import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def EXMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://elreyx.com/index1.html',113,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://elreyx.com/search-',114,'','')
    utils.addDir('[COLOR yellow]Pornstars[/COLOR]','http://elreyx.com/index1.html',115,'','')
    utils.addDir('[COLOR yellow]Movies[/COLOR]','http://elreyx.com/index1.html',116,'','')
    EXList('http://elreyx.com/index1.html')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def EXList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('notice_image">.*?<a title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for name, videopage, img in match:
        utils.addDownLink(name, videopage, 112, img, '')
    try:
        nextp=re.compile("<a href='([^']+)' title='([^']+)'>&raquo;</a>", re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = urllib.quote_plus(nextp[0][0])
        next = next.replace(' ','+')
        utils.addDir('Next Page', os.path.split(url)[0] + '/' + next, 111,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def EXSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title + ".html"
    print "Searching URL: " + searchUrl
    EXList(searchUrl)


def EXCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div id="categories">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 111, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def EXPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)


def EXPornstars(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div id="pornstars">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 111, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def EXMovies(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div id="movies">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 117, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def EXMoviesList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div class="container_news">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    match1 = re.compile('<td.*?<a title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match[0])
    for name, videopage, img in match1:
        utils.addDownLink(name, videopage, 112, img, '')
    try:
        nextp=re.compile("<a href='([^']+)' title='([^']+)'>&raquo;</a>", re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = urllib.quote_plus(nextp[0][0])
        next = next.replace(' ','+')
        utils.addDir('Next Page', os.path.split(url)[0] + '/' + next, 117,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)
