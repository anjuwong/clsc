#!/usr/bin/python
import MySQLdb
import urllib
from bs4 import BeautifulSoup

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#<select> lstTermDisp = ctl00_BodyContentPlaceHolder_SOCmain_lstTermDisp -> termVal
#<select> lstSubjectArea = ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea -> subjVal
#<submit> btnGetClasses = ctl00_BodyContentPlaceHolder_SOCmain_btnGetClasses -> getBtn
# for timestamps, only remember the most recent one if no change
def main():
    quarter = "15S"
    f = open("/var/.mysqlinfo")
    usrnm = f.readline()[:-1]  
    psswd = f.readline()[:-1]
    con = MySQLdb.connect("localhost",usrnm,psswd,"registrar")
    cur = con.cursor()
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

    courseId = 0
    lectId = 0
    # class coursehead
    # class fachead
    # class dgdClassDataTimeStart
    # class dgdClassDataTimeEnd
    # class dgdClassDataEnrollTotal
    # class dgdClassDataEnrollCap
    # TODO: Ensure that the lectId and courseId are unique and constant
    for term in termVals:
        for subj in subjVals:
            if not term == quarter:
                continue
            if term == '141':
                continue
            #if not subj == "COM SCI":
            #    continue
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
                try:
                    crsRes = urllib.urlopen(classUrl+"?"+params[i])
                    crsSoup = BeautifulSoup(str(crsRes.read()))
                except:
                    continue
                # Remove 3 characters from the prof name for &nlbs
                profs = [str(fac.string[3:]) for fac in crsSoup.find_all('span','fachead')]
                
                # all_ are lists of all the _ tags, not necessarily the first ones
                # The first rows (class info, not disc info) are distinctly bolded
                allTimes = [t for t in crsSoup.find_all('td','dgdClassDataTimeStart') if t.find("span","bold")]
                allDays = [d for d in crsSoup.find_all('td','dgdClassDataDays') if d.find("span","bold")]
                allEnroll = [e for e in crsSoup.find_all('td','dgdClassDataEnrollTotal') if e.find("span","bold")]
                allCap = [c for c in crsSoup.find_all('td','dgdClassDataEnrollCap') if c.find("span","bold")]
                print term+" "+subj+" "+courses[i]
                try:
                    cur.execute("INSERT INTO Course VALUES ("+str(courseId)+",'"+term+"','"+subj+"','"+courses[i]+"')")
                    con.commit()
                    print "COMMITED COURSE TO DB @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                except:
                    print "Course already in table"
                for j in range(len(profs)):
                    # Ignore discussions (no bolded areas)
                    try:
                        print profs[j]
                        print allTimes[j].find("span","bold").string+" "+\
                            allDays[j].find("span","bold").string+" "+\
                            allEnroll[j].find("span","bold").string+"/"+\
                            allCap[j].find("span","bold").string
                    except:
                        continue

                    # Check if the most recent entry into Enroll has the same
                    # enrollcount; if there is none, there is a new enrollcount
                    enr = allEnroll[j].find("span","bold").string
                    try:
                        cur.execute("SELECT COUNT(*) FROM Enroll WHERE lectid ="+str(lectId)+" AND enrollcount ="+enr+" AND timestamp = (SELECT MAX(timestamp) FROM Enroll E WHERE E.lectid = "+str(lectId)+")")
                        ret = cur.fetchone()
                    except:
                        ret = ""
                    # Add the new enrollcount, otherwise, do nothing
                    if str(ret) == "(0L,)":
                        print "Inserting new enrollcount"
                        try:
                            cur.execute("INSERT INTO Enroll VALUES ("+str(lectId)+",'"+\
                        allEnroll[j].find("span","bold").string+\
                        "',CURDATE())")
                            con.commit()
                            print "COMMITED ENROLLCOUNT TO DB @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                        except:
                            print "Could not put enrollment into table"
                    
                    # Add the lecture time to Lect and increment lectId
                    try:
                        cur.execute("INSERT INTO Lect VALUES ("+str(courseId)+","+str(lectId)+",'"+profs[j]+"','"+\
                            allTimes[j].find("span","bold").string+" "+\
                            allDays[j].find("span","bold").string+"','"+\
                            allCap[j].find("span","bold").string+"')")
                        con.commit()
                        print "COMMITED LECTURE TO DB @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                        lectId += 1
                    except:
                        print "Lecture time already in table"
                        lectId += 1
                        continue
                courseId += 1
if __name__ == "__main__":
    main()
