'''
    Cumination
    Copyright (C) 2021 Team Cumination

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
import xbmc
import xbmcgui
from six.moves import urllib_parse
from resources.lib import utils
from resources.lib.adultsite import AdultSite

site = AdultSite('thepornfull', '[COLOR hotpink]Thepornfull[/COLOR]', 'https://thepornfull.com/', 'https://thepornfull.com/wp-content/uploads/2022/05/Logo-Thepornfull.png', 'thepornfull')


@site.register(default_mode=True)
def thepornfull_main():
    site.add_dir('[COLOR hotpink]Categories[/COLOR]', site.url + 'categorias/', 'Categories', site.img_cat)
    site.add_dir('[COLOR hotpink]Search[/COLOR]', site.url + '?s=', 'thepornfull_search', site.img_search)
    thepornfull_list(site.url + '?order=recent')


@site.register()
def thepornfull_list(url):
    listhtml = utils.getHtml(url, site.url)
    if 'No results</h2>' in listhtml:
        utils.notify(msg='Nothing found')
        utils.eod()
        return

    match = re.compile(r'class="video-thumb".*?href="([^"]+)"\s*title="([^"]+).*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for video, name, img in match:
        name = utils.cleantext(name)
        site.add_download_link(name, video, 'thepornfull_play', img, name)

    utils.next_page(site, 'thepornfull.thepornfull_list', listhtml, r'href="([^"]+)">Next<', r'page/(\d+)/[^>]*>Next<', re_lpnr=r'>(\d+)\D+class="next"', contextm='thepornfull.GotoPage')
    utils.eod()


@site.register()
def GotoPage(list_mode, url, np, lp):
    dialog = xbmcgui.Dialog()
    pg = dialog.numeric(0, 'Enter Page number')
    if pg:
        url = url.replace('/page/{}/'.format(np), '/page/{}/'.format(pg))
        if int(lp) > 0 and int(pg) > int(lp):
            utils.notify(msg='Out of range!')
            return
        contexturl = (utils.addon_sys + "?mode=" + str(list_mode) + "&url=" + urllib_parse.quote_plus(url))
        xbmc.executebuiltin('Container.Update(' + contexturl + ')')


@site.register()
def thepornfull_search(url, keyword=None):
    if not keyword:
        site.search_dir(url, 'thepornfull_search')
    else:
        title = keyword.replace(' ', '+')
        url += title
        thepornfull_list(url)


@site.register()
def Categories(url):
    cathtml = utils.getHtml(url, site.url)
    match = re.compile(r'class="titulo".+?href="([^"]+)".+?title="([^"]+)".+?src="([^"]+)"', re.DOTALL).findall(cathtml)
    for catpage, name, img in match:
        site.add_dir(name, catpage, 'thepornfull_list', img, '')
    if 'class="current">1<' in cathtml:
        Categories(url + 'page/2/')
    utils.eod()


@site.register()
def thepornfull_play(url, name, download=None):
    vp = utils.VideoPlayer(name, download=download)
    vp.progress.update(25, "[CR]Loading video page[CR]")
    videohtml = utils.getHtml(url, site.url)
    match = re.compile('iframe src="([^"]+)"', re.IGNORECASE | re.DOTALL).search(videohtml)
    if match:
        iframeurl = match.group(1)
        headers = {'referer': iframeurl}
        iframehtml = utils.getHtml(iframeurl, url)
        iframefile = re.compile('file: "([^"]+)', re.IGNORECASE | re.DOTALL).search(iframehtml)
        if iframefile:
            videourl = iframefile.group(1)
            videourl = "{0}|{1}".format(videourl, urllib_parse.urlencode(headers))
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            subject = xbmc.getInfoLabel("ListItem.Plot")
            listitem = xbmcgui.ListItem(name)
            listitem.setArt({'thumb': iconimage, 'icon': "DefaultVideo.png", 'poster': iconimage})
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn', 'plot': subject, 'plotoutline': subject})
            listitem.setMimeType('application/vnd.apple.mpegurl')
            listitem.setContentLookup(False)
            xbmc.Player().play(videourl, listitem)
