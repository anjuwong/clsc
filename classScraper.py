#!/usr/bin/python
import urllib
from HTMLParser import HTMLParser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#<select> lstTermDisp = ctl00_BodyContentPlaceHolder_SOCmain_lstTermDisp -> termVal
#<select> lstSubjectArea = ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea -> subjVal
#<submit> btnGetClasses = ctl00_BodyContentPlaceHolder_SOCmain_btnGetClasses -> getBtn

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
    driver = webdriver.Firefox()
    driver.get(homeUrl)
    terms = driver.find_element_by_id(lstTermDisp) # gives the options
    termVals = [opt.get_attribute("value").encode("ascii") for opt in terms.find_elements_by_tag_name("option")]
    subjs = driver.find_element_by_id(lstSubjectArea) # gives the options
    subjVals = [opt.get_attribute("value").encode("ascii") for opt in subjs.find_elements_by_tag_name("option")]
    # print termVals
    # print subjVals

    

    for term in termVals:
        for subj in subjVals:
            if term == '141' or term == '15S':
                continue
            params = urllib.urlencode({'termsel':term,'subareasel':subj})
            driver.get(deptUrl+"?"+params) 
            #courses = driver.find_element_by_id(sess) for sess in lstSession
            try:
                courses = driver.find_element_by_id(lstSession)
            except:
                continue
            courseVals = [opt.get_attribute("value").encode("ascii") for opt in courses.find_elements_by_tag_name("option")]
            print term+" "+subj+" ======================="
            print courseVals

if __name__ == "__main__":
    main()
