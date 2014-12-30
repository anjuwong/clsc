#!/usr/bin/python
import urllib
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#<select> lstTermDisp = ctl00_BodyContentPlaceHolder_SOCmain_lstTermDisp -> termVal
#<select> lstSubjectArea = ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea -> subjVal
#<submit> btnGetClasses = ctl00_BodyContentPlaceHolder_SOCmain_btnGetClasses -> getBtn
# for timestamps, only remember the most recent one if no change
def main():
    lstTermDisp = "ctl00_BodyContentPlaceHolder_SOCmain_lstTermDisp"
    lstSubjectArea = "ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea"
    btnGetClasses = "ctl00_BodyContentPlaceHolder_SOCmain_btnGetClasses"
    #lstSessions = ["ctl00_BodyContentPlaceHolder_crsredir1_lstCourseSessionA",\
    #                "ctl00_BodyContentPlaceHolder_crsredir1_lstCourseSessionC",\
    #                "ctl00_BodyContentPlaceHolder_crsredir1_lstCourseTentative",\
    lstSession=      "ctl00_BodyContentPlaceHolder_crsredir1_lstCourseNormal"                
        
    #url = "http://www.registrar.ucla.edu/schedule/crsredir.aspx?termsel=15W&subareasel=COM+SCI"
    #url = "http://www.registrar.ucla.edu/schedule/detmain.aspx?termsel=15W&subareasel=COM+SCI"
    homeUrl ="http://www.registrar.ucla.edu/schedule/schedulehome.aspx" 
    deptUrl = "http://www.registrar.ucla.edu/schedule/crsredir.aspx"
    classUrl = "http://www.registrar.ucla.edu/schedule/detselect.aspx"
    # params: termsel, subareasel, idxcrs
    # option value " " -> "+"
    termVal = '15W'
    subjVal = 'COM SCI'
    
    crsredirUrl = "http://www.registrar.ucla.edu/schedule/crsredir.aspx"
    crsredirParams = urllib.urlencode({'termsel':termVal, 'subareasel':subjVal})
    # res = urllib.urlopen(crsredirUrl+"?",crsredirParams)
    res = urllib.urlopen(homeUrl)
    soup = BeautifulSoup(str(res.read()))
    termSoup = BeautifulSoup(str(soup.find(id=lstTermDisp)))
    termVals = [opt['value'] for opt in termSoup.find_all('option')]
    print termVals
    
    subjSoup = BeautifulSoup(str(soup.find(id=lstSubjectArea)))
    subjVals = [opt['value'] for opt in subjSoup.find_all('option')]
    print subjVals

    termId = 0
    lectId = 0
    # class coursehead
    # class fachead
    # class dgdClassDataTimeStart
    # class dgdClassDataTimeEnd
    # class dgdClassDataEnrollTotal
    # class dgdClassDataEnrollCap
    # style border-width:0px;border-style:None;border-collapse:collapse;
    for term in termVals:
        for subj in subjVals:
            if term == '141' or term == '15S':
                continue
            if not subj == "COM SCI":
                continue
            params = urllib.urlencode({'termsel':term,'subareasel':subj})
            crsRes = urllib.urlopen(deptUrl+"?"+params)
            crsSoup = BeautifulSoup(str(crsRes.read()))
            try:
                courses = [opt['value'] for opt in \
                    BeautifulSoup(str(crsSoup.find(id=lstSession))).find_all('option')]
            except:
                continue
            print term+" "+subj+" ============"
            print courses
            # params is a list of URL tails for the given term
            params = [urllib.urlencode({'termsel':term,'subareasel':subj,'idxcrs':course})\
                 for course in courses]
            for i in range(len(params)):
                crsRes = urllib.urlopen(classUrl+"?"+params[i])
                crsSoup = BeautifulSoup(str(crsRes.read()))
                # Remove 3 characters from the prof name for &nlbs
                profs = [str(fac.string[3:]) for fac in crsSoup.find_all('span','fachead')]
                allTimes = [t for t in crsSoup.find_all('td','dgdClassDataTimeStart')]
                allDays = [d for d in crsSoup.find_all('td','dgdClassDataDays')]
                allEnroll = [e for e in crsSoup.find_all('td','dgdClassDataEnrollTotal')]
                allCap = [c for c in crsSoup.find_all('td','dgdClassDataEnrollCap')]
                print term+" "+subj+" "+courses[i]
                for j in range(len(profs)):
                    try:
                        print profs[j]
                        print allTimes[j].find("span","bold").string+" "+\
                            allDays[j].find("span","bold").string+" "+\
                            allEnroll[j].find("span","bold").string+"/"+\
                            allCap[j].find("span","bold").string
                            
                    except:
                        continue

if __name__ == "__main__":
    main()
