import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

addon = utils.addon

sortlistwxf = [addon.getLocalizedString(30012), addon.getLocalizedString(30013), addon.getLocalizedString(30014)]


def WXFMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.watchxxxfree.com/categories/',12,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://www.watchxxxfree.com/page/1/?s=',14,'','')
    utils.addDir('[COLOR yellow]Top Pornstars[/COLOR]','http://www.watchxxxfree.com/top-pornstars/',15,'','')
    Sort = '[COLOR yellow]Current sort:[/COLOR] ' + sortlistwxf[int(addon.getSetting("sortwxf"))]
    utils.addDir(Sort, '', 16, '', '')
    WXFList('http://www.watchxxxfree.com/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def WXFCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('src="([^"]+)"[^<]+</noscript>.*?<a href="([^"]+)"[^<]+<span>([^<]+)</s.*?">([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for img, catpage, name, videos in match:
        catpage = catpage + 'page/1/'
        name = name + ' [COLOR blue]' + videos + '[/COLOR]'
        utils.addDir(name, catpage, 11, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
def WXFTPS(url):
    tpshtml = utils.getHtml(url, '')
    match = re.compile("<li><a href='([^']+)[^>]+>([^<]+)", re.DOTALL | re.IGNORECASE).findall(tpshtml)
    for tpsurl, name in match:
        tpsurl = tpsurl + 'page/1/'
        utils.addDir(name, tpsurl, 11, '', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)    
    
    
def WXFSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    WXFList(searchUrl, 1)    


def WXFList(url, page):
    sort = getWXFSortMethod()
    if re.search('\?', url, re.DOTALL | re.IGNORECASE):
        url = url + '&filtre=' + sort + '&display=extract'
    else:
        url = url + '?filtre=' + sort + '&display=extract'
    print url
    listhtml = utils.getHtml(url, '')
    match = re.compile('src="([^"]+)"[^<]+</noscript>.*?<a href="([^"]+)" title="([^"]+)".*?<p>([^<]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, videopage, name, desc in match:
        name = utils.cleantext(name)
        desc = utils.cleantext(desc)
        utils.addDownLink(name, videopage, 13, img, desc)
    if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('/page/'+str(page)+'/','/page/'+str(npage)+'/')
        utils.addDir('Next Page ('+str(npage)+')', url, 11, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def WXFVideo(url, name, download):
    utils.PLAYVIDEO(url, name, download)


def getWXFSortMethod():
    sortoptions = {0: 'date',
                   1: 'rate',
                   2: 'views'}
    sortvalue = addon.getSetting("sortwxf")
    return sortoptions[int(sortvalue)]    
