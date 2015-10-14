import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress


def SPMain():
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://streampleasure.com/page/1/?s=',213,'','')
    SPList('http://streampleasure.com/newest-videos/page/1/?orderby=date',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def SPList(url, page, onelist=None):
    if onelist:
        url = url.replace('/page/1/','/page/'+str(page)+'/')
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div id="main">(.*?)#content', re.DOTALL | re.IGNORECASE).findall(listhtml)
    match1 = re.compile('thumb">.*?href="([^"]+)">.*?<img.*?src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match[0])
    for videopage, img, name in match1:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 212, img, '')
    if not onelist:
        if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1        
            url = url.replace('/page/'+str(page)+'/','/page/'+str(npage)+'/')
            utils.addDir('Next Page ('+str(npage)+')', url, 211, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)

    
def SPSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    SPList(searchUrl,1)


def SPPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
