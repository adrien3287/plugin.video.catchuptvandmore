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
if KodiV >= 19:
    __cwd__ = xbmcvfs.translatePath( __addon__.getAddonInfo('path') )
    kanali = xbmcvfs.translatePath( os.path.join( __cwd__, 'resources', 'kanali.jpg' ) )
    predavaniq = xbmcvfs.translatePath( os.path.join( __cwd__, 'resources', 'predavaniq.jpg' ) )
    bnt1 = xbmcvfs.translatePath( os.path.join( __cwd__, 'resources', 'bnt1.png' ) )
    bnt2 = xbmcvfs.translatePath( os.path.join( __cwd__, 'resources', 'bnt2.png' ) )
    bnt3 = xbmcvfs.translatePath( os.path.join( __cwd__, 'resources', 'bnt3.png' ) )
    bnt4 = xbmcvfs.translatePath( os.path.join( __cwd__, 'resources', 'bnt4.png' ) )
    bnt1subs = xbmcvfs.translatePath( os.path.join( __cwd__, 'resources', 'bnt1subs.png' ) )
else:
    __cwd__ = xbmc.translatePath( __addon__.getAddonInfo('path') ).decode('utf-8')
    kanali = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'kanali.jpg' ) ).decode('utf-8')
    predavaniq = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'predavaniq.jpg' ) ).decode('utf-8')
    bnt1 = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'bnt1.png' ) ).decode('utf-8')
    bnt2 = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'bnt2.png' ) ).decode('utf-8')
    bnt3 = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'bnt3.png' ) ).decode('utf-8')
    bnt4 = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'bnt4.png' ) ).decode('utf-8')
    bnt1subs = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'bnt1subs.png' ) ).decode('utf-8')

bntchannels = ['','bnt2','bnt3','bnt4','bnt1subs']
bntchlogo = [bnt1,bnt2,bnt3,bnt4,bnt1subs]

s = requests.Session()

def takeThurd(elem):
    return elem[2]

def takeSecond(elem):
    return elem[1]

def CATEGORIES():
    addDir('КАНАЛИ','http://tv.bnt.bg/',4,kanali,'','')
    addDir('ПРЕДАВАНИЯ','https://bnt1.bnt.bg/bg/shows/type/bnt2',4,predavaniq,'','')
    

def SUBCATEGORIES(name,url,mode):
    if name=='ПРЕДАВАНИЯ':
        addDir('БНТ 1','https://bnt.bg/bnt1/shows',3,bnt1,'','')
        addDir('БНТ 2','https://bnt.bg/bnt2/shows',3,bnt2,'','')
        addDir('БНТ 3','https://bnt.bg/bnt3/shows',3,bnt3,'','')
        addDir('БНТ 4','https://bnt.bg/bnt4/shows',3,bnt4,'','')
        
    if name=='КАНАЛИ':
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
                cdn_url = match_cdn.group(1)
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
                addLink(title,urlPlay,2,thumb)
            response.close()


def SUBSUBCATEGORIES(name,url,mode):
    response = requests.get(url)  
    r = response.content
    if KodiV >= 19:
        r = r.decode('utf-8').replace('\n','')
    else:
        r = r.replace('\n','')
    match=re.compile('<div class="news-img-hld">.+?<a href="(.+?)" title="(.+?)" class="hov-img".+?img src="(.+?)" alt').findall(r)
    #match.sort(key=takeThurd)
    for link, title, thumb in match:
        url = link
        thumbnail = thumb
        addDir(title,url,1,thumbnail,'','1')
    response.close()
    
          
def INDEXPAGES(name,url,mode,count,groupID):
    response = requests.get(url)
    r = response.content
    if KodiV >= 19:
        r = r.decode('utf-8').replace('\n','')
    else:
        r = r.replace('\n','')

    match=re.compile('<div class="news-img-hld">.+?<a href="(.+?)" title="(.+?)" class="hov-img".+?img src="(.+?)" alt').findall(r)
    for link, title, thumb in match:
        url1 = link
        thumbnail = thumb
        title = title.replace('&ndash;','-')
        addDir(title,url1,5,thumbnail,'','')
        
    response.close()
    
    if groupID==1:
        nexturl = url+'?page='+str(groupID+1)
        addDir("Следваща страница",nexturl,1,'','',groupID+1)
    else:
        nexturl = url[:-1]+str(groupID+1)
        addDir("Следваща страница",nexturl,1,'','',groupID+1)

def SUBPAGES(name,url,mode,count,groupID):
    responseCh = requests.get(url)
    rCh = responseCh.content
    if KodiV >= 19:
        rCh = rCh.decode('utf-8').replace('\n','')
    else:
        rCh = rCh.replace('\n','')
    
    matchPlay = re.search('"type":.+?"src": "(.+?)".+?"poster":"(.+?)"', rCh)
    
    if matchPlay:
        urlPlay = matchPlay.group(1)
        titleCh = name
        thumbnail = matchPlay.group(2)
        addLink(titleCh,urlPlay,2,thumbnail)
    else:    
        matchCh=re.compile('<div class="scroll-item.+?data-original="(.+?)".+?<a href="(.+?)" class="item-url" ><span class="sr-only">(.+?)</span></a>').findall(rCh)
        for thumbCh, linkCh, titleCh in matchCh:
            urlCh = linkCh
            responsePlay = requests.get(urlCh)
            rPlay = responsePlay.content
            if KodiV >= 19:
                matchPlay = re.search('data-source="(.+?)"', rPlay.decode('utf-8'))
            else:
                matchPlay = re.search('data-source="(.+?)"', rPlay)
            if matchPlay:
                urlPlay = matchPlay.group(1)
                thumbnail = thumbCh
                addLink(titleCh,urlPlay,2,thumbnail)
    

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
		
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addDir(name,url,mode,iconimage,count,groupID):
        if KodiV >= 19:
            u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&count="+str(count)+"&groupID="+str(groupID)
            liz=xbmcgui.ListItem(name)
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&count="+str(count)+"&groupID="+str(groupID)
            liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        ok=True
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage):
        if KodiV >= 19:
            u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)
            liz=xbmcgui.ListItem(name)
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        ok=True
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok   

params=get_params()
url=None
name=None
iconimage=None
mode=None
count=None
groupID=None

if KodiV >= 19:
    try:
            url=urllib.parse.unquote_plus(params["url"])
    except:
            pass
    try:
            name=urllib.parse.unquote_plus(params["name"])
    except:
            pass
    try:
            name=urllib.parse.unquote_plus(params["iconimage"])
    except:
            pass
    try:
            mode=int(params["mode"])
    except:
            pass
    try:
            count=int(params["count"])
    except:
            pass
    try:
            groupID=int(params["groupID"])
    except:
            pass
else:
    try:
            url=urllib.unquote_plus(params["url"])
    except:
            pass
    try:
            name=urllib.unquote_plus(params["name"])
    except:
            pass
    try:
            name=urllib.unquote_plus(params["iconimage"])
    except:
            pass
    try:
            mode=int(params["mode"])
    except:
            pass
    try:
            count=int(params["count"])
    except:
            pass
    try:
            groupID=int(params["groupID"])
    except:
            pass

if mode==None or url==None or len(url)<1:
        print ("")
        CATEGORIES()

elif mode==4:
        print (""+url)
        SUBCATEGORIES(name,url,mode)
        
elif mode==3:
        print (""+url)
        SUBSUBCATEGORIES(name,url,mode)

elif mode==1:
        print (""+url)
        INDEXPAGES(name,url,mode,count,groupID)
        
elif mode==5:
        print (""+url)
        SUBPAGES(name,url,mode,count,groupID)

elif mode==2:
        print (""+url)
        PLAY(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
