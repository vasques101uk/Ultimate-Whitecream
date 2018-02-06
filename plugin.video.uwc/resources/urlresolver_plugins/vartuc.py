'''
    vartuc resolver for URLResolver
    Copyright (C) 2018 holisticdioxide

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import re
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError

class VartucResolver(UrlResolver):
    name = "vartuc"
    domains = ['vartuc.com', "azblowjobtube.com"]
    pattern = '(?://|\.)(vartuc\.com|azblowjobtube\.com)/embed/([^"]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        self.headers = {'User-Agent': common.RAND_UA,
                        'Referer': web_url}
        html = self.net.http_GET(web_url, headers=self.headers).content
        js_link = re.compile("src='(/kt_player/.*?)'", re.DOTALL | re.IGNORECASE).search(html).group(1)
        js_path = 'https://' + self.domains[0] + js_link + '&ver=x'
        js = self.net.http_GET(js_path, headers=self.headers).content
        js = js.split(";")
        js = [line for line in js if (line.startswith("gh") and '=' in line) or line.startswith("irue842")]
        js = "\n".join(js)
        exec js
        try:
            vid = re.compile('src="([^"]+)"', re.DOTALL | re.IGNORECASE).search(irue842).group(1)
            return vid
        except (AttributeError, NameError):
            raise ResolverError('Video not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://www.vartuc.com/embed/{media_id}')

    @classmethod
    def _is_enabled(cls):
        return True
