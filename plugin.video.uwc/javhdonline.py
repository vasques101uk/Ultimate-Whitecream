import urllib, re
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def Main():
    utils.addDir('[COLOR yellow]Gravure Idol[/COLOR]','http://javhdonline.com/watch/category/gravure-idol/', 181, '', '')
    utils.addDir('[COLOR yellow]Uncensored[/COLOR]','http://javhdonline.com/watch/category/jav-uncensored/', 181, '', '')
    utils.addDir('[COLOR yellow]Censored[/COLOR]','http://javhdonline.com/watch/category/jav-censored/', 181, '', '')
    utils.addDir('[COLOR yellow]Hentai Anime[/COLOR]','http://javhdonline.com/watch/category/hentai-anime/', 181, '', '')
    utils.addDir('[COLOR yellow]Tags[/COLOR]','http://javhdonline.com/', 183, '', '')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://javhdonline.com/?s=', 184, '', '')
    List('http://javhdonline.com/watch/category/jav-uncensored/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div id="post-.*?<div class="thumb">.*?href="([^"]+)".*?src="([^"]+)".*?alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 182, img, '')
    try:
        nextp=re.compile('<a class="nextpostslink" rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 181,'')
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


def Tags(url):
    html = utils.getHtml(url, '')
    match = re.compile('<div class="tagcloud">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(html)
    match1 = re.compile("href='([^']+)[^>]+>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 181, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
