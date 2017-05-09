#-*- coding: utf-8 -*-
from resources.lib import utils
from resources.lib import globalvar
#import ptvsd
import re

title       = ['LCP']
img         = ['lcp']
readyForUse = True

url_catalog = 'http://www.lcp.fr/'

def list_shows(channel,folder):
    shows    = []
    if folder=='none' :
        shows.append([channel,'emissions', 'Emissions','','folder'])
        shows.append([channel,'documentaires',globalvar.LANGUAGE(33010),'','folder'])
    elif folder == 'documentaires':
        filePath = utils.downloadCatalog(url_catalog + folder, '%s.xml'%(channel), False, {})
        fileCat  = open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n','')

        filePath2 = utils.downloadCatalog(url_catalog + folder + '?page=1' , '%s2.xml'%(channel), False, {})
        fileCat = fileCat + open(filePath2).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n','')

        match = re.compile(r'<a href=\"/(emissions/[^ ]*?)\"><img class=\"img-responsive\" typeof=\"(.*?)\" src=\"(.*?)\"(.*?)content=\"(.*?)\"',re.DOTALL).findall(fileCat)

        for url, empty1, img, empty2, title in match:
            infoLabels={ "Title": title.replace('&#039;', '\'').lower().capitalize()}
            shows.append([channel,url,title.replace('&#039;', '\'').lower().capitalize(),img,'shows'])
    elif folder.lower() == "emissions" :
        filePath = utils.downloadCatalog(url_catalog + folder,'%s.xml'%(channel + folder),False,{})
        fileCat  = open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n','')
        cat      = re.compile(r'<a href=\"/emissions/(.*?)\" title=\"(.*?)\"><div><img (.*?) src=\"(.*?)\" alt',re.DOTALL).findall(fileCat)

        for url, title, empty, img in cat :
            infoLabels={ "Title": title.replace('&#039;', '\'').lower().capitalize()}
            shows.append([channel, 'emissions/' + url,title.replace('&#039;', '\'').lower().capitalize(),img,'folder'])
    else :
        filePath = utils.downloadCatalog(url_catalog + folder, '%s.xml'%(channel + folder), False, {})
        fileCat  = open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n','')
        cat      = re.compile(r'<span class=\"date\">(.*?)</span>.*?<a href=\"(.*?)\"',re.DOTALL).findall(fileCat)

        for title, url in cat:
            infoLabels={ "Title": title.replace('&#039;', '\'').lower().capitalize()}
            shows.append([channel,url,title.replace('&#039;', '\'').lower().capitalize(),'','shows'])

    return shows
            
def list_videos(channel,params):
    videos     = []

    #maintenant il faut chercher la vrai url de la video
    videoFilePath = utils.downloadCatalog(url_catalog + params, '%s.xml'%(channel + params), False, {})
    videoFileCat  = open(videoFilePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n','')

    titleMatch = re.compile(r'<h2 class=\"title-light-cap tv-episode-infos-title\">(.*?)</h2>',re.DOTALL).findall(videoFileCat)
    urlMatch = re.compile(r'http://play.lcp.fr/embed/(\d*)',re.DOTALL).findall(videoFileCat)
    dateDiffusionMatch = re.compile(r'<span class=\"text-muted\">Diffusée le (.*?)</span>',re.DOTALL).findall(videoFileCat)
    plotMatch = re.compile(r'<p><p>(.*?)<div',re.DOTALL).findall(videoFileCat)

    if len(titleMatch) > 0:
        title = titleMatch[0].replace('&#039;', '\'').lower().capitalize()
        video_url = 'http://httpod.scdn.arkena.com/11970/' + urlMatch[0] + '_4.mp4'
        img = 'http://httpod.scdn.arkena.com/11970/' + urlMatch[0] + '_4.jpg'
        dateDiffusion = dateDiffusionMatch[0]
        plot = plotMatch[0].replace('&#039;', '\'').replace('<p>', '').replace('</p>', '')

        infoLabels={ "Title": title.replace('&#039;', '\'').lower().capitalize(), "Plot": plot, "Duration": '', "Aired": dateDiffusion}
        videos.append([channel,video_url,title,img,infoLabels,'play'])
    

    return videos
    
def getVideoURL(channel,url_video):
    return url_video
