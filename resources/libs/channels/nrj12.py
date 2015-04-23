#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
common = CommonFunctions

title=['NRJ12']
img=['nrj12']
readyForUse=True

def list_shows(channel,folder):
    shows=[]
    
    req = urllib2.Request('http://www.nrj12.fr/replay-4203/collectionvideo/')
    req.add_header('User-agent', 'Mozilla 5.10')
    html=urllib2.urlopen(req).read().replace('\xe9', 'e').replace('\xe0', 'a')

    if folder=='none':      
        match = re.compile(r'<a href="#" rel="nofollow" class="nocursor">(.*?)</a>',re.DOTALL).findall(html)
            
        if match:
            for title in match:
                shows.append( [channel,title, title , '','folder'] )
    else:
        line_replay_s = common.parseDOM(html,"div",attrs={"class":"line replay"})
        for line_replay in line_replay_s :
            Categorie = common.parseDOM(line_replay,"a",attrs={"class":"nocursor"}) [0]
            if Categorie.encode("utf-8") == folder:
                li_s = common.parseDOM(line_replay,"li",attrs={"id":u"*"})
                for li in li_s :
                    replay_hover_s = common.parseDOM(li,"div",attrs={"class":u"replay_hover"})
                    if replay_hover_s :
                        image_div = common.parseDOM(li,"div",attrs={"class":"image"}) [0]
                        image_a_u = common.parseDOM(image_div,"a") [0]
                        image_url = re.findall(""".*src="(.*)">""",image_a_u) [0]
                        titre_p   = common.parseDOM(li,"p",attrs={"class":"titre"}) [0]
                        titre_u   = common.parseDOM(titre_p,"a") [0]
                        titre     = titre_u.encode("utf-8")
                        shows.append( [channel,titre, titre , image_url, 'shows'] )                            
                     
    return shows


def getVideoURL(channel,mediaId):
    return 'http://videos.enrj.net/web/' + mediaId + '_h264_12.mp4'

def list_videos(channel,show):
    
    videos=[] 
    req = urllib2.Request('http://www.nrj12.fr/replay-4203/collectionvideo/')
    req.add_header('User-agent', 'Mozilla 5.10')
    html=urllib2.urlopen(req).read().replace('\xe9', 'e').replace('\xe0', 'a')
        
    line_replay_s = common.parseDOM(html,"div",attrs={"class":"line replay"})
    for line_replay in line_replay_s :
        li_s = common.parseDOM(line_replay,"li",attrs={"id":u"*"})
        for li in li_s :
            replay_hover_s = common.parseDOM(li,"div",attrs={"class":u"replay_hover"})
            if replay_hover_s :
                titre_p   = common.parseDOM(li,"p",attrs={"class":"titre"}) [0]
                titre_u   = common.parseDOM(titre_p,"a") [0]
                titre     = titre_u.encode("utf-8")
                if titre==show:
                    print show
                    replay_hover = replay_hover_s[0]
                    content_ul   = common.parseDOM(replay_hover,"ul",attrs={"class":"content"}) [0]
                    li_s         = common.parseDOM(content_ul,"li")
                    for li in li_s :
                        image_div   = common.parseDOM(li,"div",attrs={"class":"image"}) [0]
                        image_a_u   = common.parseDOM(image_div,"a") [0]
                        image_url   = re.findall(""".*src="(.*)".*>""",image_a_u) [0]
                        titre_p     = common.parseDOM(li,"p",attrs={"class":"titre"}) [0]
                        titre_u     = common.parseDOM(titre_p,"a") [0]
                        titre       = show+" : "+titre_u.encode("utf-8")
                        date=common.parseDOM(li,"p",attrs={"class":"date"}) [0]   
                        pos=image_url.rfind('/')+1                    
                        media_id=image_url[pos:pos+8]

                        infoLabels={ "Title": titre,"Aired":date, "Year":date[:4]}
                        videos.append( [channel, media_id, titre, image_url,infoLabels,'play'] )
             
    return videos