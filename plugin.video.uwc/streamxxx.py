import urllib, re
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def Main():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://streamxxx.tv/', 177, '', '')
    utils.addDir('[COLOR yellow]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR yellow]Search Overall[/COLOR]','http://streamxxx.tv/?s=', 174, '', '')
    utils.addDir('[COLOR yellow]Search Scenes[/COLOR]','http://streamxxx.tv/?cat=1981&s=', 174, '', '')
    utils.addDir('[COLOR yellow]Movies[/COLOR]','http://streamxxx.tv/category/movies/', 175, '', '')
    utils.addDir('[COLOR yellow]International Movies[/COLOR]','http://streamxxx.tv/category/movies/international-movies/', 176, '', '')
    List('http://streamxxx.tv/category/clips/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def MainMovies():
    utils.addDir('[COLOR yellow]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR yellow]Search Overall[/COLOR]','http://streamxxx.tv/&s=', 174, '', '')
    utils.addDir('[COLOR yellow]Search Movies[/COLOR]','http://streamxxx.tv/?cat=41&s=', 174, '', '')
    utils.addDir('[COLOR yellow]International Movies[/COLOR]','http://streamxxx.tv/category/movies/international-movies/', 176, '', '')
    utils.addDir('[COLOR yellow]Scenes[/COLOR]','http://streamxxx.tv/category/clips/', 170, '', '')
    List('http://streamxxx.tv/category/movies/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def MainInternationalMovies():
    utils.addDir('[COLOR yellow]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR yellow]Search Overall[/COLOR]','http://streamxxx.tv/&s=', 174, '', '')
    utils.addDir('[COLOR yellow]Search International Movies[/COLOR]','http://streamxxx.tv/?cat=9&s=', 174, '', '')
    utils.addDir('[COLOR yellow]Movies[/COLOR]','http://streamxxx.tv/category/movies/', 175, '', '')
    utils.addDir('[COLOR yellow]Scenes[/COLOR]','http://streamxxx.tv/category/clips/', 170, '', '')
    List('http://streamxxx.tv/category/movies/international-movies/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div id="post-.*?<div class="thumb">.*?href="([^"]+)".*?src="([^"]+)".*?alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 172, img, '')
    try:
        nextp=re.compile('<a class="nextpostslink" rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 171,'')
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
    match = re.compile('Clips</a>.+<ul class="sub-menu">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 161, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Tags(url):
    html = utils.getHtml(url, '')
    match = re.compile('<div class="tagcloud">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(html)
    match1 = re.compile("href='([^']+)[^>]+>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 171, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 25, "", "Loading video page", "" )
    html = utils.getHtml(url, '')
    videosource = re.compile('<div class="webwarez">(.*?)</iframe>', re.DOTALL | re.IGNORECASE).findall(html)
    utils.playvideo(videosource[0], name, download)
