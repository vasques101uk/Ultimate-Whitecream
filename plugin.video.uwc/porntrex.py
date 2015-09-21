import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils


def PTMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.porntrex.com/categories',53,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://www.porntrex.com/search?search_type=videos&page=1&search_query=',54,'','')
    PTList('http://www.porntrex.com/videos?o=mr&page=1',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)

def PTList(url, page, onelist=None):
    if onelist:
        url = url.replace('page=1','page='+str(page))
    listhtml = utils.getHtml(url, '')
    match = re.compile(r'data-original="([^"]+)" title="([^"]+)".*?rotate_([^_]+)_[^>]+>(.*?)duration">[^\d]+([^\t\n\r]+)', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, name, urlid, hd, duration in match:
        name = utils.cleantext(name)
        if hd.find('HD') > 0:
            hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "
        videopage = "http://www.porntrex.com/media/nuevo/config.php?key=" + urlid + "-1-1"
        name = name + hd + "[COLOR blue]" + duration + "[/COLOR]"
        utils.addDownLink(name, videopage, 52, img, '')
    if not onelist:
        if re.search('class="prevnext">&raquo;', listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1        
            url = url.replace('page='+str(page),'page='+str(npage))
            utils.addDir('Next Page ('+str(npage)+')', url, 51, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)

def PTPlayvid(url, name, download=None):
    videopage = utils.getHtml(url, '')
    match = re.compile("<filehd>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(videopage)
    match2 = re.compile("<file>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(videopage)
    try: videourl = match[0]
    except: videourl = match2[0]
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


def PTCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('c=([^"]+)".*?data-original="([^"]+)" title="([^"]+)".*?badge">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catid, img, name, videos in match:
        img = "http://www.porntrex.com/" + img
        catpage = "http://www.porntrex.com/videos?c="+ catid + "&o=mr&page=1"
        name = name + ' [COLOR blue]' + videos + '[/COLOR]'
        utils.addDir(name, catpage, 51, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def PTSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    PTList(searchUrl, 1) 
