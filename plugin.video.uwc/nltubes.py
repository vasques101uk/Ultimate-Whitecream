import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

# 100 NLTUBES
# 101 NLVIDEOLIST
# 102 NLPLAYVID
# 103 NLCAT
# 104 NLSEARCH


sitelist = ['http://www.poldertube.nl', 'http://www.milf.nl', 'http://www.sextube.nl']



def NLTUBES(url, site):
    siteurl = sitelist[site]
    utils.addDir('Categories', siteurl + '/categorieen',103,'', site)
    if site == 0:
        utils.addDir('Search', siteurl + '/pornofilms/zoeken/',104,'', site)
    else:
        utils.addDir('Search', siteurl + '/videos/zoeken/',104,'', site)
    NLVIDEOLIST(url, site)


def NLVIDEOLIST(url, site):
    siteurl = sitelist[site]
    link = utils.getHtml(url, '')
    match = re.compile(r'<article([^>]*)>.*?href="([^"]+)".*?src="([^"]+)".*?<h3>([^<]+)<.*?duration">[^\d]+([^\s<]+)(?:\s|<)', re.DOTALL | re.IGNORECASE).findall(link)
    for hd, url, img, name, duration in match:
        if len(hd) > 2:
            hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "    
        videourl = siteurl + url
        duration2 = "[COLOR blue]" +  duration + "[/COLOR]"
        utils.addDownLink(name + hd + duration2, videourl, 102, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)" title="volg', re.DOTALL | re.IGNORECASE).findall(link)
        nextp = siteurl + nextp[0]
        utils.addDir('Next Page', nextp,101,'',site)
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def NLPLAYVID(url,name, download=None):
    videopage = utils.getHtml(url, '')
    videourl = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videourl[0]
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:    
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


def NLSEARCH(url, site):
    searchUrl = url
    vq = utils._get_keyboard(heading="Enter the query")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','%20')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    NLVIDEOLIST(searchUrl, site)


def NLCAT(url, site):
    siteurl = sitelist[site]
    link = utils.getHtml(url, '')
    tags = re.compile('<div class="category".*?href="([^"]+)".*?<h2>([^<]+)<.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for caturl, catname, catimg in tags:
        catimg = siteurl + catimg
        utils.addDir(catname,caturl,101,catimg,site)
