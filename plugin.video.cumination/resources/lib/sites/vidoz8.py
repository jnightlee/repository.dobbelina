'''
    Cumination
    Copyright (C) 2018 holisticdioxide
    Copyright (C) 2020 Team Cumination

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

import re
from resources.lib import utils
from resources.lib.adultsite import AdultSite

site = AdultSite('vidz7', '[COLOR hotpink]Vidoz8[/COLOR]', 'http://vidoz8.com/', 'vidoz8.png', 'vidoz8')

addon = utils.addon


@site.register(default_mode=True)
def v7_main():
    site.add_dir('[COLOR hotpink]Studios[/COLOR]', site.url + 'channels/?sort=name', 'v7_cat', '', '')
    site.add_dir('[COLOR hotpink]Tags[/COLOR]', site.url + 'tags/', 'v7_tag', '', '')
    site.add_dir('[COLOR hotpink]Search[/COLOR]', site.url + '?s=', 'v7_search', site.img_search)
    v7_list(site.url + '?orderby=date')


@site.register()
def v7_list(url):
    listhtml = utils.getHtml(url)
    match = re.compile(r'''cell\s*video-listing.+?url\("([^"]+).+?ico-p'>([^<]+).+?ico-t'>([^<]+).+?href='([^']+)'\s*>([^<]+)''', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, hd, duration, videopage, name in match:
        hd = 'HD' if 'HD' in hd else ''
        name = utils.cleantext(name)
        site.add_download_link(name, videopage, 'v7_play', img, name, duration=duration, quality=hd)

    np = re.compile(r'class="next"\s*href\s*="([^"]+)', re.DOTALL | re.IGNORECASE).search(listhtml)
    if np:
        site.add_dir('Next Page... ({0})'.format(np.group(1).split('/')[-2]), np.group(1), 'v7_list', site.img_next)
    utils.eod()


@site.register()
def v7_cat(url):
    nextpg = True
    while nextpg:
        cathtml = utils.getHtml(url, site.url)
        match = re.compile('class="channel-site.+?src="([^"]+).+?href="([^"]+)">([^<]+).+?videos <span>([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
        for img, catpage, name, nr in match:
            nr = int(nr.replace(' ', '').replace(',', ''))
            if nr > 0:
                name = '{0} [COLOR orange]{1} Videos[/COLOR]'.format(utils.cleantext(name), nr)
                site.add_dir(name, catpage + '?orderby=date', 'v7_list', img)
        np = re.compile(r'class="next"\s*href\s*="([^"]+)', re.DOTALL | re.IGNORECASE).search(cathtml)
        if np:
            url = np.group(1)
        else:
            nextpg = False

    utils.eod()


@site.register()
def v7_tag(url):
    taghtml = utils.getHtml(url, site.url)
    match = re.compile(r'<li\s*class="\s*(?:popclick)?"><a\s*href="([^"]+)">([^<]+)</a><span\s*class="count">\(([^)]+)').findall(taghtml)
    for tagpage, name, nr in match:
        nr = int(nr.replace(' ', ''))
        if nr > 0:
            name = '{0} [COLOR orange]{1} Videos[/COLOR]'.format(utils.cleantext(name), nr)
            site.add_dir(name, tagpage + '?orderby=date', 'v7_list', '')

    utils.eod()


@site.register()
def v7_search(url, keyword=None):
    if not keyword:
        site.search_dir(url, 'v7_search')
    else:
        url += keyword.replace(' ', '+') + '&orderby=date'
        v7_list(url)


@site.register()
def v7_play(url, name, download=None):
    vp = utils.VideoPlayer(name, download=download, regex=r'''<iframe.+?src\s*=\s*["']([^'"]+)''')
    vp.play_from_site_link(url)
