__scriptname__ = "Ultimate Whitecream"
__author__ = "mortael"
__scriptid__ = "plugin.video.uwc"
__credits__ = "mortael"
__version__ = "1.0.6"

import urllib
import urllib2
import re
import cookielib
import os.path
import sys
import socket
from jsbeautifier import beautify

socket.setdefaulttimeout(60)

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
addon = xbmcaddon.Addon(id=__scriptid__)
progress = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")
cookiePath = os.path.join(profileDir, 'cookies.lwp')

if not os.path.exists(profileDir):
    os.makedirs(profileDir)

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request

if cj != None:
    if os.path.isfile(xbmc.translatePath(cookiePath)):
        cj.load(xbmc.translatePath(cookiePath))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
else:
    opener = urllib2.build_opener()

urllib2.install_opener(opener)

sortlistwxf = [addon.getLocalizedString(30012), addon.getLocalizedString(30013), addon.getLocalizedString(30014)]
            
sortlistxt = [addon.getLocalizedString(30022), addon.getLocalizedString(30023), addon.getLocalizedString(30024),
            addon.getLocalizedString(30025)]            


def INDEX():
    addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Scenes[/COLOR]','http://www.watchxxxfree.com/page/1/',10,'','')
    addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Movies[/COLOR]','http://xtheatre.net/page/1/',20,'','')
    addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Hentai[/COLOR]','http://www.hentaicraving.com/?genre=Uncensored',30,'','')
    xbmcplugin.endOfDirectory(addon_handle)


def getHtml(url, referer):
    req = Request(url, '', headers)
    if len(referer) > 1:
        req.add_header('Referer', referer)
    response = urlopen(req, timeout=60)
    data = response.read()
    cj.save(cookiePath)
    response.close()
    return data
 
def getHtml2(url):
    req = Request(url)
    response = urlopen(req, timeout=60)
    data = response.read()
    response.close()
    return data 
 
def getVideoLink(url, referer):
    req2 = Request(url, '', headers)
    req2.add_header('Referer', referer)
    url2 = urlopen(req2).geturl()
    return url2

def cleantext(text):
    text = text.replace('&#8211;','-')
    text = text.replace('&#038;','&')
    text = text.replace('&#8217;','\'')
    text = text.replace('&#8230;','...')
    return text


def PLAYVIDEO(url, name):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    hosts = []
    videosource = getHtml(url, url)
    if re.search('videomega', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('VideoMega')
    if re.search('openload', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('OpenLoad')
    if re.search('www.flashx.tv', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('FlashX')        
    if len(hosts) == 0:
        progress.close()
        dialog.ok('Oh oh','Couldn\'t find any video')
        return
    elif len(hosts) > 1:
        if addon.getSetting("dontask") == "true":
            vidhost = hosts[0]            
        else:
            vh = dialog.select('Videohost:', hosts)
            vidhost = hosts[vh]
    else:
        vidhost = hosts[0]
    
    if vidhost == 'VideoMega':
        progress.update( 40, "", "Loading videomegatv", "" )
        if re.search("videomega.tv/iframe.js", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile("""javascript["']>ref=['"]([^'"]+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/iframe.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r"iframe\.php\?ref=([^&]+)&", re.DOTALL | re.IGNORECASE).findall(videosource)
        else:
            hashkey = re.compile("""hashkey=([^"']+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
            hashpage = getHtml('http://videomega.tv/validatehash.php?hashkey='+hashkey[0], url)
            hashref = re.compile('ref="([^"]+)', re.DOTALL | re.IGNORECASE).findall(hashpage)
        progress.update( 80, "", "Getting video file", "" )
        videopage = getHtml('http://videomega.tv/view.php?ref='+hashref[0], url)
        videourl = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
        videourl = videourl[0]
    elif vidhost == 'OpenLoad':
        progress.update( 40, "", "Loading Openload", "" )
        openloadurl = re.compile('<iframe src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videosource)
        openloadsrc = getHtml(openloadurl[0], url)
        videourl = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(openloadsrc)
        progress.update( 80, "", "Getting video file", "" )
        openload302 = getVideoLink(videourl[0],openloadurl[0])
        realurl = openload302.replace('https://','http://')
        videourl = realurl + "|" + openloadurl[0]
    elif vidhost == 'FlashX':
        progress.update( 40, "", "Loading FlashX", "" )
        flashxurl = re.compile('<iframe src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videosource)
        flashxsrc = getHtml2(flashxurl[0])
        flashxjs = re.compile("<script type='text/javascript'>([^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(flashxsrc)
        progress.update( 80, "", "Getting video file", "" )
        flashxujs = beautify(flashxjs[0])
        videourl = re.compile(r',.*file: "([^"]+)".*\}\],', re.DOTALL | re.IGNORECASE).findall(flashxujs)
        videourl = videourl[0]
    progress.close()
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
    xbmc.Player().play(videourl, listitem)


def getParams():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def addDownLink(name, url, mode, iconimage, desc):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    if len(desc) < 1:
        liz.setInfo(type="Video", infoLabels={"Title": name})
    else:
        liz.setInfo(type="Video", infoLabels={"Title": name, "plot": desc, "plotoutline": desc})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=False)
    return ok
    

def addDir(name, url, mode, iconimage, page):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&page=" + str(page) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=True)
    return ok
    
def _get_keyboard(default="", heading="", hidden=False):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return unicode(keyboard.getText(), "utf-8")
    return default    

########### WatchXXXFree

def WXFMain():
    addDir('[COLOR yellow]Categories[/COLOR]','http://www.watchxxxfree.com/categories/',12,'','')
    addDir('[COLOR yellow]Search[/COLOR]','http://www.watchxxxfree.com/page/1/?s=',14,'','')
    addDir('[COLOR yellow]Top Pornstars[/COLOR]','http://www.watchxxxfree.com/top-pornstars/',15,'','')
    Sort = '[COLOR yellow]Current sort:[/COLOR] ' + sortlistwxf[int(addon.getSetting("sortwxf"))]
    addDir(Sort, '', 16, '', '')
    WXFList('http://www.watchxxxfree.com/page/1/',1)
    xbmcplugin.endOfDirectory(addon_handle)


def WXFCat(url):
    cathtml = getHtml(url, '')
    match = re.compile('src="([^"]+)"[^<]+</noscript>.*?<a href="([^"]+)"[^<]+<span>([^<]+)</s.*?">([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for img, catpage, name, videos in match:
        catpage = catpage + 'page/1/'
        name = name + ' [COLOR blue]' + videos + '[/COLOR]'
        addDir(name, catpage, 11, img, 1)
    xbmcplugin.endOfDirectory(addon_handle)
    
def WXFTPS(url):
    tpshtml = getHtml(url, '')
    match = re.compile("<li><a href='([^']+)[^>]+>([^<]+)", re.DOTALL | re.IGNORECASE).findall(tpshtml)
    for tpsurl, name in match:
        tpsurl = tpsurl + 'page/1/'
        addDir(name, tpsurl, 11, '', 1)
    xbmcplugin.endOfDirectory(addon_handle)    
    
    
def WXFSearch(url):
    searchUrl = url
    vq = _get_keyboard(heading="Searching for...")
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
    listhtml = getHtml(url, '')
    match = re.compile('src="([^"]+)"[^<]+</noscript>.*?<a href="([^"]+)" title="([^"]+)".*?<p>([^<]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, videopage, name, desc in match:
        name = cleantext(name)
        desc = cleantext(desc)
        addDownLink(name, videopage, 13, img, desc)
    if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('/page/'+str(page)+'/','/page/'+str(npage)+'/')
        addDir('Next Page ('+str(npage)+')', url, 11, '', npage)
    xbmcplugin.endOfDirectory(addon_handle)


def WXFVideo(url, name):
    PLAYVIDEO(url, name)


def getWXFSortMethod():
    sortoptions = {0: 'date',
                   1: 'rate',
                   2: 'views'}
    sortvalue = addon.getSetting("sortwxf")
    return sortoptions[int(sortvalue)]    

####################


########### WatchXXXFree

def XTMain():
    addDir('[COLOR yellow]Categories[/COLOR]','http://xtheatre.net/categories/',22,'','')
    addDir('[COLOR yellow]Search[/COLOR]','http://xtheatre.net/page/1/?s=',24,'','')
    Sort = '[COLOR yellow]Current sort:[/COLOR] ' + sortlistxt[int(addon.getSetting("sortxt"))]
    addDir(Sort, '', 25, '', '')    
    XTList('http://xtheatre.net/page/1/',1)
    xbmcplugin.endOfDirectory(addon_handle)


def XTCat(url):
    cathtml = getHtml(url, '')
    match = re.compile('<li class="cat[^<]+<a href="([^"]+)">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        catpage = catpage + 'page/1/'
        addDir(name, catpage, 21, '', 1)
    xbmcplugin.endOfDirectory(addon_handle)
    
    
def XTSearch(url):
    searchUrl = url
    vq = _get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    XTList(searchUrl, 1)     


def XTList(url, page):
    sort = getXTSortMethod()
    if re.search('\?', url, re.DOTALL | re.IGNORECASE):
        url = url + '&orderby=' + sort
    else:
        url = url + '?orderby=' + sort
    print url
    listhtml = getHtml(url, '')
    match = re.compile('src="([^"]+)" alt="([^"]+)"[^<]+<span class="vertical-align"></span>.*?<h2 class="entry-title"><a href="([^"]+)".*?summary">([^<]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, name, videopage, desc in match:
        name = cleantext(name)
        desc = cleantext(desc)
        addDownLink(name, videopage, 23, img, desc)
    if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('/page/'+str(page)+'/','/page/'+str(npage)+'/')
        addDir('Next Page ('+str(npage)+')', url, 21, '', npage)
    xbmcplugin.endOfDirectory(addon_handle)

def XTVideo(url, name):
    PLAYVIDEO(url, name)
    
def getXTSortMethod():
    sortoptions = {0: 'date',
                   1: 'title',
                   2: 'views',
                   3: 'likes'}
    sortvalue = addon.getSetting("sortxt")
    return sortoptions[int(sortvalue)]    

####################
    
    
########### HCraving
def getHC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    response = urllib2.urlopen(req, timeout=60)
    data = response.read()
    response.close()
    return data

def HCList(url):
    addDir('[COLOR white]A-Z List[/COLOR] [COLOR yellow]Censored & Uncensored[/COLOR]','http://www.hentaicraving.com/hentai-list/',33,'','')
    link = getHtml(url, '')
    match = re.compile("""<a href='([^']+)'><img.*?title="([^"]+)".*?src="([^"]+)".*?Description: </b> ([^<]+)<p>""", re.DOTALL | re.IGNORECASE).findall(link)
    for videourl, name, img, desc in match:
        addHCDir(name, videourl, 31, img, desc)
    xbmc.executebuiltin('Container.SetViewMode(503)')
    xbmcplugin.endOfDirectory(addon_handle)
    
def HCA2Z(url):
    link = getHtml(url, '')
    match = re.compile('hentai-series/([^/]+)/">([^<]+)', re.DOTALL | re.IGNORECASE).findall(link)
    for link, name in match:
        url = 'http://www.hentaicraving.com/hentai-series/' + link + '/'
        img = 'http://www.hentaicraving.com/images/' + link + '.jpg'
        addHCDir(name, url, 31, img, '')
    xbmcplugin.endOfDirectory(addon_handle)    
    
def HCEpisodes(url,name, img):
    link = getHtml(url, '')
    eps = re.compile('<li><a href="([^"]+)">([^<]+)</a> <', re.DOTALL | re.IGNORECASE).findall(link)
    for url, name in eps:
        addDownLink(name,url,32,img, '')
        
def HCPlayvid(url,name):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    link = getHtml(url,'')
    match = re.compile('<iframe.*? src="([^"]+)" FRAME', re.DOTALL | re.IGNORECASE).findall(link)
    if len(match) > 1:
        vh = dialog.select('Videohost:', match)
    else:
        vh = 0
    progress.update( 40, "", "Loading video host", "" )
    urldata2 = getHC(match[vh])
    if match[vh].find('hentaiupload') > 0:
        progress.update( 80, "", "Loading hentaiupload", "" )    
        try:
            match1 = re.compile('url: "([^"]+mp4)', re.DOTALL | re.IGNORECASE).findall(urldata2)
            url = match1[0]
        except: pass
        videourl = url + "|referer="+ match[vh]
    elif match[vh].find('hvidengine') > 0:
        progress.update( 80, "", "Loading hvidengine", "" )        
        try:
            match1 = re.compile('file: "([^"]+)', re.DOTALL | re.IGNORECASE).findall(urldata2)
            url = match1[0]
        except: pass
        videourl = url + "|referer="+ match[vh]
    else:
        progress.update( 80, "", "Loading video", "" )
        match2 = re.compile("<script type='text/javascript'>([^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(urldata2)
        res = beautify(match2[0])
        match3 = re.compile("file.*?(http.*?mp4)", re.DOTALL | re.IGNORECASE).findall(res)
        videourl = match3[0]
    progress.close()
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
    xbmc.Player().play(videourl, listitem)
    
def addHCDir(name,url,mode,iconimage,desc):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name) +
         "&img=" + urllib.quote_plus(iconimage))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "plot": desc, "plotoutline": desc })
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=True)
    return ok

#####################
    
    
params = getParams()
url = None
name = None
mode = None
img = None
page = 1

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    page = int(params["page"])
except:
    pass
try:
    img = urllib.unquote_plus(params["img"])
except:
    pass

if mode is None:
    INDEX()
    
elif mode == 10:
    WXFMain()
elif mode == 11:
    WXFList(url, page)
elif mode == 12:
    WXFCat(url)
elif mode == 13:
    WXFVideo(url, name)
elif mode == 14:
    WXFSearch(url) 
elif mode == 15:
    WXFTPS(url)  
elif mode == 16:
    addon.openSettings()
    WXFMain()    
    
elif mode == 20:
    XTMain()
elif mode == 21:
    XTList(url, page)
elif mode == 22:
    XTCat(url)
elif mode == 23:
    XTVideo(url, name)
elif mode == 24:
    XTSearch(url)  
elif mode == 25:
    addon.openSettings()
    XTMain()    

elif mode == 30:
    HCList(url)
elif mode == 31:
    HCEpisodes(url, name, img)
elif mode == 32:
    HCPlayvid(url, name)
elif mode == 33:
    HCA2Z(url)     

xbmcplugin.endOfDirectory(addon_handle)
