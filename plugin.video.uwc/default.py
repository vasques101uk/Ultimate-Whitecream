import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils, hdporn, porntrex, nudeflix, hentaicraving, watchxxxfree, xtheatre, pornhive, beeg

socket.setdefaulttimeout(60)

xbmcplugin.setContent(utils.addon_handle, 'movies')
addon = xbmcaddon.Addon(id=utils.__scriptid__)

progress = utils.progress
dialog = utils.dialog

imgDir = utils.imgDir


def INDEX():
    utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Scenes[/COLOR]','',2,'','')
    utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Movies[/COLOR]','',3,'','')
    utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Hentai[/COLOR]','http://www.hentaicraving.com/?genre=Uncensored',30,os.path.join(imgDir, 'hc.jpg'),'')
    download_path = addon.getSetting('download_path')
    if download_path != '' and os.path.exists(download_path):
        utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Download Folder[/COLOR]',download_path,4,'','')
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
def INDEXS():
    utils.addDir('[COLOR yellow]WatchXXXFree[/COLOR]','http://www.watchxxxfree.com/page/1/',10,os.path.join(imgDir, 'wxf.png'),'')
    utils.addDir('[COLOR yellow]PornTrex[/COLOR]','http://www.porntrex.com/videos?o=mr&page=1',50,os.path.join(imgDir, 'pt.png'),'')
    utils.addDir('[COLOR yellow]PornAQ[/COLOR]','http://www.pornaq.com/page/1/',60,os.path.join(imgDir, 'paq.png'),'')
    utils.addDir('[COLOR yellow]Porn00[/COLOR]','http://www.porn00.com/page/1/',64,os.path.join(imgDir, 'p00.png'),'')
    utils.addDir('[COLOR yellow]Beeg[/COLOR]','http://beeg.com/page-1',80,os.path.join(imgDir, 'bg.png'),'')

def INDEXM():    
    utils.addDir('[COLOR yellow]Xtheatre[/COLOR]','http://xtheatre.net/page/1/',20,os.path.join(imgDir, 'xt.png'),'')
    utils.addDir('[COLOR yellow]Nudeflix[/COLOR]','http://www.nudeflix.com/browse?order=released&page=1',40,os.path.join(imgDir, 'nf.png'),'')
    utils.addDir('[COLOR yellow]PornHive[/COLOR]','http://www.pornhive.tv/en/movies/all',70,os.path.join(imgDir, 'ph.png'),'')


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

   
params = getParams()
url = None
name = None
mode = None
img = None
page = 1
download = None

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
try:
    download = int(params["download"])
except:
    pass    

if mode is None:
    INDEX()
    
elif mode == 2:
    INDEXS()
elif mode == 3:
    INDEXM()
elif mode == 4:
    print url
    xbmc.executebuiltin('ActivateWindow(Videos, '+url+')')
    
elif mode == 10:
    watchxxxfree.WXFMain()
elif mode == 11:
    watchxxxfree.WXFList(url, page)
elif mode == 12:
    watchxxxfree.WXFCat(url)
elif mode == 13:
    watchxxxfree.WXFVideo(url, name, download)
elif mode == 14:
    watchxxxfree.WXFSearch(url) 
elif mode == 15:
    watchxxxfree.WXFTPS(url)  
elif mode == 16:
    addon.openSettings()
    watchxxxfree.WXFMain()    
    
elif mode == 20:
    xtheatre.XTMain()
elif mode == 21:
    xtheatre.XTList(url, page)
elif mode == 22:
    xtheatre.XTCat(url)
elif mode == 23:
    xtheatre.XTVideo(url, name, download)
elif mode == 24:
    xtheatre.XTSearch(url)  
elif mode == 25:
    addon.openSettings()
    xtheatre.XTMain()    

elif mode == 30:
    hentaicraving.HCList(url)
elif mode == 31:
    hentaicraving.HCEpisodes(url, name, img)
elif mode == 32:
    hentaicraving.HCPlayvid(url, name, download)
elif mode == 33:
    hentaicraving.HCA2Z(url) 

elif mode == 40:
    nudeflix.NFMain()
elif mode == 41:
    nudeflix.NFList(url, page)
elif mode == 42:
    nudeflix.NFScenes(url)
elif mode == 43:
    nudeflix.NFPlayvid(url, name, download)
elif mode == 44:
    nudeflix.NFCat(url)

elif mode == 50:
    porntrex.PTMain()
elif mode == 51:
    porntrex.PTList(url, page)
elif mode == 52:
    porntrex.PTPlayvid(url, name, download)
elif mode == 53:
    porntrex.PTCat(url)
elif mode == 54:
    porntrex.PTSearch(url)

elif mode == 60:
    hdporn.PAQMain()
elif mode == 61:
    hdporn.PAQList(url, page)
elif mode == 62:
    hdporn.PPlayvid(url, name, download)
elif mode == 63:
    hdporn.PCat(url)
elif mode == 64:
    hdporn.P00Main()
elif mode == 65:
    hdporn.P00List(url, page)
elif mode == 68:
    hdporn.PSearch(url)
    
elif mode == 70:
    pornhive.PHMain()
elif mode == 71:
    pornhive.PHList(url)
elif mode == 72:
    pornhive.PHVideo(url, name, download)
elif mode == 73:
    pornhive.PHCat(url)
elif mode == 74:
    pornhive.PHSearch(url)

elif mode == 80:
    beeg.BGMain()
elif mode == 81:
    beeg.BGList(url)
elif mode == 82:
    beeg.BGPlayvid(url, name, download)
elif mode == 83:
    beeg.BGCat(url)
elif mode == 84:
    beeg.BGSearch(url)       


xbmcplugin.endOfDirectory(utils.addon_handle)
