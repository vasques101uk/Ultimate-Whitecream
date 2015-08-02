import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils


def NFMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.nudeflix.com/browse',44,'','')
    NFList('http://www.nudeflix.com/browse?order=released&page=1',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def NFCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<select name="category[^>]+>(.*?)</select>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('<option value="([^"]+)">([^<]+)</', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        catpage = catpage.replace(' ','%20')
        catpage = 'http://www.nudeflix.com/browse/category/' + catpage + '?order=released&page=1'
        utils.addDir(name, catpage, 41, '', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def NFList(url,page):
    listhtml = utils.getHtml(url, '')
    match = re.compile('href="([^"]+)" class="link">[^"]+?"([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        videopage = 'http://www.nudeflix.com' + videopage
        utils.addDir(name, videopage, 42, img, '')
    if re.search("<strong>next &raquo;</strong>", listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('page='+str(page),'page='+str(npage))
        utils.addDir('Next Page ('+str(npage)+')', url, 41, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def NFScenes(url):
    scenehtml = utils.getHtml(url, '')
    match = re.compile(r'class="scene">.*?href="([^"]+)"[^(]+?\(([^)]+)\).*?<div class="description">[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(scenehtml)
    scenecount = 1
    for sceneurl, img, desc in match:
        name = 'Scene ' + str(scenecount)
        scenecount = scenecount + 1
        sceneurl = 'http://www.nudeflix.com' + sceneurl
        utils.addDownLink(name, sceneurl, 43, img, desc)        
    xbmcplugin.endOfDirectory(utils.addon_handle)


def NFPlayvid(url, name):
    videopage = utils.getHtml(url, '')
    match = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = match[0]
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
    xbmc.Player().play(videourl, listitem)
