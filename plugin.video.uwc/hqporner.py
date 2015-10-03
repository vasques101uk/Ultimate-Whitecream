import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils


def HQMAIN():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://hqporner.com/porn-categories.php',153,'','')
    utils.addDir('[COLOR yellow]Studios[/COLOR]','http://hqporner.com/porn-studios.php',155,'','')
    utils.addDir('[COLOR yellow]Girls[/COLOR]','http://hqporner.com/porn-actress.php',156,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://hqporner.com/?s=',154,'','')
    HQLIST('http://hqporner.com/hdporn/1')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def HQLIST(url):
    link = utils.getHtml(url, '')
    match = re.compile('<a href="([^"]+)"[^<]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for url, img, name in match:
        name = utils.cleantext(name)    
        videourl = "http://www.hqporner.com" + url
        utils.addDownLink(name, videourl, 152, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)"[^>]+>Next', re.DOTALL | re.IGNORECASE).findall(link)
        nextp = "http://www.hqporner.com" + nextp[0]
        utils.addDir('Next Page', nextp,151,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def HQCAT(url):
    link = utils.getHtml(url, '')
    tags = re.compile('<a href="([^"]+)"[^<]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for caturl, catimg, catname in tags:
        caturl = "http://www.hqporner.com" + caturl
        catimg = "http://www.hqporner.com" + catimg        
        utils.addDir(catname,caturl,151,catimg)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def HQSTUDIOS(url):
    link = utils.getHtml(url, '')
    tags = re.compile('<a href="([^"]+)"[^<]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for caturl, catimg, catname in tags:
        caturl = "http://www.hqporner.com" + caturl
        catimg = "http://www.hqporner.com" + catimg        
        utils.addDir(catname,caturl,151,catimg)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def HQGIRLS(url):
    link = utils.getHtml(url, '')
    tags = re.compile('<a href="([^"]+)"[^<]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for caturl, catimg, catname in tags:
        caturl = "http://www.hqporner.com" + caturl
        catimg = "http://www.hqporner.com" + catimg
        utils.addDir(catname,caturl,151,catimg)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def HQSEARCH(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    HQLIST(searchUrl) 


def HQPLAY(url, name, download=None):

    def playvid():
        if download == 1:
            utils.downloadVideo(videourl, name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
            xbmc.Player().play(videourl, listitem) 
            
    videopage = utils.getHtml(url, '')
    iframeurl = re.compile(r'<iframe\swidth="\d+"\sheight="\d+"\ssrc="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    #if re.search('hqporner', iframeurl[0], re.DOTALL | re.IGNORECASE):
    #    videourl = getHQ(iframeurl[0])
    #    playvid()
    if re.search('bemywife', iframeurl[0], re.DOTALL | re.IGNORECASE):
        videourl = getBMW(iframeurl[0])
        playvid()
    elif re.search('5\.79', iframeurl[0], re.DOTALL | re.IGNORECASE):
        videourl = getIP(iframeurl[0])
        playvid()
    else:
        utils.dialog.ok('Oh oh','Couldn\'t find a supported videohost')


def getBMW(url):
    videopage = utils.getHtml(url, '')
    videos = re.compile('file: "([^"]+mp4)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = "http://bemywife.cc" + videos[-1]
    return videourl

def getIP(url):
    videopage = utils.getHtml(url, '')
    videos = re.compile('file": "([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videos[-1]
    return videourl
