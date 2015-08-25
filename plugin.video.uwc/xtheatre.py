import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

addon = utils.addon

sortlistxt = [addon.getLocalizedString(30022), addon.getLocalizedString(30023), addon.getLocalizedString(30024),
            addon.getLocalizedString(30025)]   


def XTMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://xtheatre.net/categories/',22,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://xtheatre.net/page/1/?s=',24,'','')
    Sort = '[COLOR yellow]Current sort:[/COLOR] ' + sortlistxt[int(addon.getSetting("sortxt"))]
    utils.addDir(Sort, '', 25, '', '')    
    XTList('http://xtheatre.net/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def XTCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('src="([^"]+)"[^<]+</noscript>.*?<a href="([^"]+)"[^<]+<span>([^<]+)</s.*?">([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for img, catpage, name, videos in match:
        catpage = catpage + 'page/1/'
        name = name + ' [COLOR blue]' + videos + '[/COLOR]'
        utils.addDir(name, catpage, 21, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
    
def XTSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    XTList(searchUrl, 1)     


def XTList(url, page):
    sort = getXTSortMethod()
    if re.search('\?', url, re.DOTALL | re.IGNORECASE):
        url = url + '&filtre=' + sort
    else:
        url = url + '?filtre=' + sort
    print url
    listhtml = utils.getHtml(url, '')
    match = re.compile('src="([^"]+?)" class="attachment.*?<a href="([^"]+)" title="([^"]+)".*?<div class="right">.<p>([^<]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, videopage, name, desc in match:
        name = utils.cleantext(name)
        desc = utils.cleantext(desc)
        utils.addDownLink(name, videopage, 23, img, desc)
    if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('/page/'+str(page)+'/','/page/'+str(npage)+'/')
        utils.addDir('Next Page ('+str(npage)+')', url, 21, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)

def XTVideo(url, name, download):
    utils.PLAYVIDEO(url, name, download)
    
def getXTSortMethod():
    sortoptions = {0: 'date',
                   1: 'title',
                   2: 'views',
                   3: 'likes'}
    sortvalue = addon.getSetting("sortxt")
    return sortoptions[int(sortvalue)]    
