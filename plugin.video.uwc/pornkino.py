'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael
    Copyright (C) 2015 Fr33m1nd

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

import urllib, re
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def MainMovies():
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://pornkino.to/?s=', 254, '', '')
    List('http://pornkino.to/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a href="(.+?)" title="(.+?)"><img class="cover" src="(.+?)" width').findall(listhtml)
    for videopage, name, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 252, img, '')
    try:
        nextp=re.compile('<li><a class="next page-numbers" href="(.+?)"><i class="icon-angle-right"></i></a></li>', re.DOTALL | re.IGNORECASE).findall(listhtml)
        nextp = nextp[0]
        utils.addDir('Next Page', nextp, 251,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def Search(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    List(searchUrl)


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
