import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

# 80 BGMain
# 81 BGList
# 82 BGPlayvid
# 83 BGCat
# 84 BGSearch

def BGMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.beeg.com',83,'','')
    utils.addDir('[COLOR yellow]Long videos[/COLOR]','http://beeg.com/tag/long+videos/',81,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://beeg.com/search?q=',84,'','')
    BGList('http://beeg.com/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def BGList(url):
    listhtml = utils.getHtml(url, '')
    Ids = re.compile(r"tumb_id  =\[(.*?)\]", re.DOTALL | re.IGNORECASE).findall(listhtml)
    Names = re.compile(r"tumb_alt =\[(.*?)\]", re.DOTALL | re.IGNORECASE).findall(listhtml)
    
    SplitIds = re.split('\,+', Ids[0])
    Names[0] = Names[0].lstrip('\'')
    Names[0] = Names[0].rstrip('\'')
    SplitNames = re.split('\'\,\'+', Names[0])
    
    for id, name in zip(SplitIds, SplitNames):
        name = utils.cleantext(name)
        name = name.replace('\\\'','\'')
        videopage = 'http://www.beeg.com/' + id
        img = 'http://img.beeg.com/236x177/' + id + '.jpg'
        utils.addDownLink(name, videopage, 82, img, '')
    
    try:
        nextp=re.compile('<a href="([^"]+)" target="_self" id="paging_next"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        nextp = 'http://www.beeg.com' + nextp[0]
        utils.addDir('Next Page', nextp,81,'')
    except: pass
    
    xbmcplugin.endOfDirectory(utils.addon_handle)


def BGPlayvid(url, name):
    videopage = utils.getHtml(url, '')
    match = re.compile("file': '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = match[0]
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
    xbmc.Player().play(videourl, listitem)


def BGCat(url):
    caturl = utils.getHtml(url, '')
    match = re.compile(r'<li><a target="_self" href="([^"]+)"\s+title="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(caturl)
    for videolist, name in match:
        videolist = "http://www.beeg.com" + videolist
        utils.addDir(name, videolist, 81, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def BGSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    BGList(searchUrl)
