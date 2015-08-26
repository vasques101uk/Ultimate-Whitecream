import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils


def PAQMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.pornaq.com',63,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://www.pornaq.com/page/1/?s=',68,'','')
    PAQList('http://www.pornaq.com/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def P00Main():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.porn00.org',63,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://www.porn00.org/page/1/?s=',68,'','')
    PAQList('http://www.porn00.org/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)    


def PAQList(url, page):
    listhtml = utils.getHtml(url, '')
    match = re.compile('src="([^"]+)" class="attachment-primary-post-thumbnail wp-post-image".*?<a title="([^"]+)" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, name, videopage in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 62, img, '')
    if re.search("<span class='current'>\d+?</span><span>", listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('page/'+str(page)+'/','page/'+str(npage)+'/')
        utils.addDir('Next Page ('+str(npage)+')', url, 61, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def P00List(url, page):
    listhtml = utils.getHtml(url, '')
    match = re.compile('src="([^"]+)" class="attachment-primary-post-thumbnail wp-post-image".*?<a title="([^"]+)" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, name, videopage in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 62, img, '')
    if re.search("<span class='current'>\d+?</span><span>", listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('page/'+str(page)+'/','page/'+str(npage)+'/')
        utils.addDir('Next Page ('+str(npage)+')', url, 65, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def PPlayvid(url, name, alternative=1, download=None):
    print url
    videopage = utils.getHtml(url, '')
    if re.search('player/\?V', videopage, re.DOTALL | re.IGNORECASE):
        match = re.compile('<iframe.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
        iframepage = utils.getHtml(match[0], url)
        video720 = re.compile("_720 = '([^']+)'", re.DOTALL | re.IGNORECASE).findall(iframepage)
        videourl = video720[0]
        if download == 1:
            utils.downloadVideo(videourl, name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
            xbmc.Player().play(videourl, listitem)
    elif re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
        if alternative == 1:
            alternative = 2
            url = url + str(alternative)
            PPlayvid(url, name, alternative, download)
        else:
            nalternative = alternative + 1
            url.replace('/'+str(alternative),'/'+str(nalternative))
            PPlayvid(url, name, nalternative, download)
    else:
        utils.dialog.ok('Oh oh','Couldn\'t find a supported videohost')


def PCat(url):
    caturl = utils.getHtml(url, '')
    cathtml = re.compile('<ul id="categorias">(.*?)</html>', re.DOTALL | re.IGNORECASE).findall(caturl)
    if 'pornaq' in url:
        match = re.compile("""<li.*?href=(?:'|")(/[^'"]+)(?:'|").*?>([^<]+)""", re.DOTALL | re.IGNORECASE).findall(cathtml[0])
    elif 'porn00' in url:
        match = re.compile("""<li.*?href=(?:'|")([^'"]+)(?:'|").*?>([^<]+)""", re.DOTALL | re.IGNORECASE).findall(cathtml[0])
    for videolist, name in match:
        if 'pornaq' in url:
            videolist = "http://www.pornaq.com" + videolist + "page/1/"
            utils.addDir(name, videolist, 61, '', 1)
        elif 'porn00' in url:
            videolist = videolist + "page/1/"
            utils.addDir(name, videolist, 65, '', 1)            
    xbmcplugin.endOfDirectory(utils.addon_handle)


def PSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    if url.find('porn00'):
        P00List(searchUrl, 1)
    elif url.find('pornaq'):
        PAQList(searchUrl, 1)
