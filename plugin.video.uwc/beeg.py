'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import json

import utils

# from youtube-dl
from compat import (
    compat_chr,
    compat_ord,
    compat_urllib_parse_unquote,
)

dialog = utils.dialog

# 80 BGMain
# 81 BGList
# 82 BGPlayvid
# 83 BGCat
# 84 BGSearch

def BGMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://api2.beeg.com/api/v6/1739/index/main/0/pc',83,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://api2.beeg.com/api/v6/1739/index/main/0/pc?query=',84,'','')
    BGList('http://api2.beeg.com/api/v6/1739/index/main/0/pc')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def BGList(url):
    listjson = utils.getHtml(url,'')
    jsondata = json.loads(listjson)

    for videos in jsondata["videos"]:
        img = "http://img.beeg.com/236x177/" + videos["id"] +  ".jpg"
        videopage = "https://api.beeg.com/api/v6/1738/video/" + videos["id"]
        name = videos["title"].encode("utf8")
        utils.addDownLink(name, videopage, 82, img, '')
    try:
        page=re.compile('http://api2.beeg.com/api/v6/1739/index/[^/]+/([0-9]+)/pc', re.DOTALL | re.IGNORECASE).findall(url)[0]
        page = int(page)
        npage = page + 1
        if jsondata["pages"] > page:
            nextp = url.replace("/"+str(page)+"/", "/"+str(npage)+"/")
            utils.addDir('Next Page ('+str(npage)+')', nextp,81,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

# from youtube-dl   
def split(o, e):
    def cut(s, x):
        n.append(s[:x])
        return s[x:]
    n = []
    r = len(o) % e
    if r > 0:
        o = cut(o, r)
    while len(o) > e:
        o = cut(o, e)
    n.append(o)
    return n

def decrypt_key(key):
    # Reverse engineered from http://static.beeg.com/cpl/1738.js
    a = 'GUuyodcfS8FW8gQp4OKLMsZBcX0T7B'
    e = compat_urllib_parse_unquote(key)
    o = ''.join([
        compat_chr(compat_ord(e[n]) - compat_ord(a[n % len(a)]) % 21)
        for n in range(len(e))])
    return ''.join(split(o, 3)[::-1])   
##

def BGPlayvid(url, name, download=None):
    videopage = utils.getHtml(url,'http://beeg.com')
    videopage = json.loads(videopage)
    
   
    if not videopage["240p"] == None:
        url = videopage["240p"].encode("utf8")
    if not videopage["480p"] == None:
        url = videopage["480p"].encode("utf8")
    if not videopage["720p"] == None:
        url = videopage["720p"].encode("utf8")


    url = url.replace("{DATA_MARKERS}","data=pc_XX")
    if not url.startswith("http:"): url = "https:" + url
    
    key = re.compile("/key=(.*?)%2Cend", re.DOTALL | re.IGNORECASE).findall(url)[0]
    decryptedkey = decrypt_key(key)
    
    videourl = url.replace(key, decryptedkey)

    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        listitem.setProperty("IsPlayable","true")
        if int(sys.argv[1]) == -1:
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            pl.clear()
            pl.add(videourl, listitem)
            xbmc.Player().play(pl)
        else:
            listitem.setPath(str(videourl))
            xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)


def BGCat(url):
    caturl = utils.getHtml2(url)
    catjson = json.loads(caturl)
    
    for tag in catjson["tags"]["popular"]:
        videolist = "http://api2.beeg.com/api/v6/1739/index/tag/0/mobile?tag=" + tag.encode("utf8")
        name = tag.encode("utf8")
        name = name[:1].upper() + name[1:]
        utils.addDir(name, videolist, 81, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def BGSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 84)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        BGList(searchUrl)
