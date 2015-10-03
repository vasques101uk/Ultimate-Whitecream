import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

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


def PAQList(url, page, onelist=None):
    if onelist:
        url = url.replace('page/1/','page/'+str(page)+'/')    
    listhtml = utils.getHtml(url, '')
    match = re.compile('src="([^"]+)" class="attachment-primary-post-thumbnail wp-post-image".*?<a title="([^"]+)" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, name, videopage in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 62, img, '')
    if not onelist:
        if re.search("<span class='current'>\d+?</span><span>", listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1        
            url = url.replace('page/'+str(page)+'/','page/'+str(npage)+'/')
            utils.addDir('Next Page ('+str(npage)+')', url, 61, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)


def GetAlternative(url, alternative):
    progress.update( 70, "", "Loading alternative page", "" )
    if alternative == 1:
        nalternative = 2
        url = url + str(nalternative)
    else:
        nalternative = int(alternative) + 1
        url.replace('/'+str(alternative),'/'+str(nalternative))
    return url, nalternative


def PPlayvid(url, name, alternative=1, download=None):

    def playvid():
        progress.close()
        if download == 1:
            utils.downloadVideo(videourl, name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
            xbmc.Player().play(videourl, listitem)    
    
    progress.create('Play video', 'Searching videofile.')
    progress.update( 25, "", "Loading video page", "" )
    
    videopage = utils.getHtml(url, '')
    if re.search('server/\?t=', videopage, re.DOTALL | re.IGNORECASE):
        match = re.compile(r'/server/\?t=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videopage)
        match = "http://www.porn00.org/server/?t=" + match[0]
        progress.update( 50, "", "Opening porn00 video page", "" )
        iframepage = utils.getHtml(match, url)
        video720 = re.compile(r'file: "([^"]+)",\s+label: "7', re.DOTALL | re.IGNORECASE).findall(iframepage)
        if not video720:
            if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                alturl, nalternative = GetAlternative(url, alternative)
                PPlayvid(alturl, name, nalternative, download)
            else:
                progress.close()
                utils.dialog.ok('Oh oh','Couldn\'t find a supported videohost')
        else:
            videourl = video720[0]
            playvid()
    elif re.search('video_ext.php\?', videopage, re.DOTALL | re.IGNORECASE):
        match = re.compile('<iframe.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
        progress.update( 30, "", "Opening VK video page", "" )
        vkpage = utils.getHtml(match[0], url)
        
        link = re.search('script.setAttribute\(\'src\',\s\'(.*?access_token=)(.*?)&callback', vkpage)
        
        if link:
            token = link.group(2).decode('string-escape')
            link = link.group(1) + token + '&callback=callbackFunc'
        i = 30
        while 1:
            if i < 98:
                i += 1
            progress.update( i, "", "Trying to load video from VK", "" )
            vkpage2 = utils.getHtml(link, '')
            if not 'Too many requests per second' in vkpage2:
                break
        videolink = re.findall(r'mp4_\d+":"([^"]+)"', vkpage2)
        if videolink:
            videolink = videolink[-1].replace('\/','/')
        if not videolink:
            if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                alturl, nalternative = GetAlternative(url, alternative)
                PPlayvid(alturl, name, nalternative, download)
            else:
                progress.close()
                utils.dialog.ok('Oh oh','Couldn\'t find a supported videohost')
        else:
            videourl = videolink
            playvid()              
    elif re.search('/\?V=', videopage, re.DOTALL | re.IGNORECASE):
        try:
            match = re.compile('-->\s+<iframe.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
            progress.update( 50, "", "Opening porn00/pornAQ video page", "" )
            iframepage = utils.getHtml(match[0], url)
            video720 = re.compile(r'file: "([^"]+)",\s+label: "7', re.DOTALL | re.IGNORECASE).findall(iframepage)
            if not video720:
                if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                    alturl, nalternative = GetAlternative(url, alternative)
                    PPlayvid(alturl, name, nalternative, download)
                else:
                    progress.close()
                    utils.dialog.ok('Oh oh','Couldn\'t find a supported videohost')
            else:
                videourl = video720[0]
                playvid()
        except:
            if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                alturl, nalternative = GetAlternative(url, alternative)
                PPlayvid(alturl, name, nalternative, download)
            else:
                progress.close()
                utils.dialog.ok('Oh oh','Couldn\'t find a supported videohost')        
    elif re.search('google.com/file', videopage, re.DOTALL | re.IGNORECASE):
        match = re.compile('file/d/([^/]+)/', re.DOTALL | re.IGNORECASE).findall(videopage)
        googleurl = "https://docs.google.com/uc?id="+match[0]+"&export=download"
        progress.update( 50, "", "Opening Google docs video page", "" )
        googlepage = utils.getHtml(googleurl, '')
        video720 = re.compile('"downloadUrl":"([^?]+)', re.DOTALL | re.IGNORECASE).findall(googlepage)
        if not video720:
            if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                alturl, nalternative = GetAlternative(url, alternative)
                PPlayvid(alturl, name, nalternative, download)
            else:
                progress.close()
                utils.dialog.ok('Oh oh','Couldn\'t find a supported videohost')
        else:
            videourl = video720[0]
            playvid()
    elif re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
        alturl, nalternative = GetAlternative(url, alternative)
        PPlayvid(alturl, name, nalternative, download)
    else:
        progress.close()
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
            utils.addDir(name, videolist, 61, '', 1)            
    xbmcplugin.endOfDirectory(utils.addon_handle)


def PSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    PAQList(searchUrl, 1)
