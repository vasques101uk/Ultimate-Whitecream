import os.path
import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress


def LIBMain(url):
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://libogski.com/',123,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://libogski.com/?s=',124,'','')
    utils.addDir('[COLOR yellow]Movies[/COLOR]','http://libogski.com/category/movies/',125,'','')
    LIBList(url)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def LIBMainMovies(url):
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://libogski.com/',126,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://libogski.com/?s=',124,'','')
    utils.addDir('[COLOR yellow]Scenes[/COLOR]','http://libogski.com/category/videos/',120,'','')
    LIBList(url)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def LIBList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('class="peli">.*?<img src="([^"]+)" alt="([^"]+)".*?href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, name, videopage in match:
        name = name.replace("&#8211;", "-")
        utils.addDownLink(name, videopage, 122, img, '')
    try:
        nextp=re.compile("previouspostslink' href='([^']+)'>Next", re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = nextp[0]
        utils.addDir('Next Page', os.path.split(url)[0] + '/' + next, 121,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def LIBSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    LIBSearchList(searchUrl)


def LIBSearchList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('class="search_vid">.*?<a href="([^"]+)".*?src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = name.replace("&#8211;", "-")
        utils.addDownLink(name, videopage, 122, img, '')
    try:
        nextp=re.compile("previouspostslink' href='([^']+)'>Next", re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = nextp[0]
        utils.addDir('Next Page', next, 127,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def LIBCat(url, index):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div class="categorias">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[index])
    for catpage, name in match1:
        utils.addDir(name, catpage, 121, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def LIBPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
