# -*- coding: utf-8 -*-
import re
import sys
import requests
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import urllib
try:
  import urllib.request
except:
  import urllib2
import base64
import os
import codecs
import xbmcvfs

KodiV = xbmc.getInfoLabel('System.BuildVersion')
KodiV = int(KodiV[:2])

__addon__ = xbmcaddon.Addon()

        countch = 0
        countlogo = 0
        for link in bntchannels:
            thumb = bntchlogo[countlogo]
            countlogo = countlogo + 1
            countch = countch + 1
            url1 = url+link  
            response = requests.get(url1)  
            r = response.content
            
            if KodiV >= 19:
                match_cdn = re.search('src="(.+?)".+?frameborder="0"',r.decode('utf-8'))
            else:
                match_cdn = re.search('src="(.+?)".+?frameborder="0"',r)
            if match_cdn:
                cdn_url = "http://tv.bnt.bg/bnt2"
                checkhttp = re.search('http', cdn_url)
                if checkhttp:
                    pass
                else:
                    cdn_url = 'http:' + cdn_url
                headers = {
                              'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                              'Referer': url1
                          }
                r_play = s.post(cdn_url, headers=headers)
                match_play = re.search("sdata.src = '(.+?)';",r_play.text)
                if match_play:
                    pass
                else:
                    match_play = re.search('source src="(.+?)"',r_play.text)
                certpass = '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36&Referer=http://i.cdn.bg/'
                urlPlay = match_play.group(1)
                urlhttp = re.search('http', urlPlay)
                if urlhttp:
                    pass
                else:
                    urlPlay = 'http:' + urlPlay
                urlPlay = urlPlay + certpass
                if link == 'bnt1subs':
                    title = 'БНТ Субтитри'
                else:
                    title = 'БНТ '+str(countch)
                PLAY(urlPlay)
		

def PLAY(url):
        
        link = url
        if KodiV >= 19:
            li = xbmcgui.ListItem(path=link)
        else:       
            li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=link)
        li.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        li.setInfo('video', { 'title': name })
        try:
          xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
        except:
          xbmc.executebuiltin("Notification('Error','Missing video!')")          
		
