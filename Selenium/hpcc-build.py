#!/usr/bin/python
#############################################
#    HPCC SYSTEMS software Copyright (C) 2012 HPCC Systems®.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License along with All rights reserved.
#    This program is free software: you can redistribute program.  
#    If not, see <http://www.gnu.org/licenses/>.
#############################################

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from optparse import OptionParser
import re, sys, os


# search an item
def search(driver, searchElem):
    sleep(1)
    # find the search box element by id
    searchBox = driver.find_element_by_id("search-box")

    # type in the search box
    searchBox.send_keys(searchElem)

    # submit the form
    searchBox.submit()

# create a workflow if none exists
def isWorkflow(driver, which_jenkins, build_version):
    try:
        # find element by text
        textElem = driver.find_element_by_link_text("Create Workflow")
        textElem.click()
    except Exception as e:
        print('New Workflow needed', format(e))
        
        #navigate to HPCC-7.x
        templateElem = driver.find_element_by_xpath("//ul[@id='breadcrumbs']/li[3]/a")
        templateElem.click()

        #create new item
        createItem = driver.find_element_by_xpath("(//a[contains(@href, '/view/HPCC-7.x/newJob')])[2]")
        createItem.click()
        workflowName = driver.find_element_by_id("name")
        workflowName.send_keys("HPCC-" + build_version)
        if (which_jenkins == "cloud_jenkins"):
            itemType = driver.find_element_by_xpath("//div[@id='j-add-item-type-uncategorized']/ul/li[2]/label")
        elif (which_jenkins == "old_jenkins"):
            itemType = driver.find_element_by_xpath("//div[@id='j-add-item-type-uncategorized']/ul/li[1]/label")
        itemType.click()
        createItem = driver.find_element_by_xpath("//button[@id='ok-button']")
        createItem.click()

# setup all builds except ECLIDE
def setupBuilds(driver, build_version, full_version, build_series, search,
                prev_platform_rc, prev_eclide_rc, prev_platform_gold, prev_eclide_gold, build_seq):
    #search 
    search(driver, "HPCC-" + build_version)

    #create build
    textElem = driver.find_element_by_link_text("Create Workflow")
    textElem.click()

    # important!
    # wait for elements to be loaded
    sleep(1)

    # select a workflow template
    template = Select(driver.find_element_by_id("template.templateName"))

    if (re.search("^\d*", build_series).group() == "7"):
        if (build_series == "7.0.x"):
            template.select_by_value("HPCC-Template-All-7.0.x")
        elif (build_series == "7.2.x"):
            template.select_by_value("HPCC-Template-All-7.2.x")
        else:
            template.select_by_value("HPCC-Template-All-7.x")
    elif (re.search("^\d*", build_series).group() == "6"):
        if (build_series == "6.4.x"):
            template.select_by_value("HPCC-Template-All-6.x")
    else:
        print("No template found for " + full_version)


    # important!
    # wait for elements to be loaded
    """wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.NAME, 'template.templateInstanceName')))"""
    sleep(1)

    # select a workflow name
    workflowName = driver.find_element_by_name("template.templateInstanceName")
    workflowName.send_keys("WF-HPCC-" + full_version)

    # get job names
    workflowJob_list = driver.find_elements_by_xpath("//div[@id='msg']/table/tbody/tr/td/input")

    for workflowJob in workflowJob_list:
        jobName = workflowJob.get_attribute("name")

        try:
            job_prefix = re.match("(.*)\.(.*)\-.", jobName).group(2)
        except Exception as e:
            job_prefix = re.match("(.*)\.(.*)", jobName).group(2)

        if (job_prefix == 'EE_PLATFORM_VER_SEQ'):
            workflowJob.send_keys(full_version)
        elif(job_prefix == 'CE_PLATFORM_SEQ'):
            workflowJob.send_keys(build_seq)
        elif(job_prefix == 'PREV_CE_PLATFORM_RC'):
            workflowJob.send_keys(prev_platform_rc)
        elif(job_prefix == 'PREV_ECLIDE_RC'):
            workflowJob.send_keys(prev_eclide_rc)
        elif(job_prefix == 'PREV_CE_PLATFORM_GOLD'):
            workflowJob.send_keys(prev_platform_gold)
        elif(job_prefix == 'PREV_ECLIDE_GOLD'):
            workflowJob.send_keys(prev_eclide_gold)
        elif (job_prefix == 'GANGLIA_MONITORING_VER_SEQ'):
            workflowJob.send_keys(full_version)
        elif (job_prefix == 'CE_PLATFORM_VER_SEQ'):
            workflowJob.send_keys(full_version)
        elif (job_prefix == 'NAGIOS_MONITORING_VER_SEQ'):
            workflowJob.send_keys(full_version)
        elif (job_prefix == 'GRAPH_CONTROL_VER_SEQ'):
            workflowJob.send_keys(full_version)
        elif (job_prefix == 'WSSQL_VER_SEQ'):
            workflowJob.send_keys(full_version)
        elif (job_prefix == 'VERSION'):
            workflowJob.send_keys(build_version)
        elif (job_prefix == 'SERIES'):
            workflowJob.send_keys(build_series)
        else:
            workflowJob.send_keys(job_prefix + "-" + full_version)

    #click to create build
    buttonElem = driver.find_element_by_xpath("//input[@value='Create']")
    buttonElem.click()

# set up ECLIDE build
def setupECLIDE(driver, full_version, search):
    search(driver, "CE-Candidate-ECLIDE-Win32-" + full_version)

    textElem = driver.find_element_by_link_text("Configure")

    try:
        textElem.click()
    except Exception as e:
        sleep(1)
        textElem.click()

    # important!
    sleep(1)

    # xpaths of artifacts' name input box
    artifacts = driver.find_elements_by_xpath("//input[@name='_.filter']")

    for artifact in artifacts:
        if(artifact.get_attribute("value") == "**/build-docs/docs/EN_US/HTMLHelp/html_help*.zip"):
            elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[3]")
            elem.send_keys("CE-Candidate-Docs-" + full_version)
        elif(artifact.get_attribute("value") == "**/build/GraphControl/bin/HPCCSystemsGraphViewControl/RelWithDebInfo/npHPCCSystemsGraphViewControl.*"):
            elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[4]")
            elem.send_keys("CE-Candidate-Graphcontrol-" + full_version)
        elif(artifact.get_attribute("value") == "**/build/hpccsystems-clienttools*.exe"):
            try:
                elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[5]")
                elem.send_keys("CTW32-" + full_version)
            except Exception as e:
                elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[4]")
                elem.send_keys("CTW32-" + full_version)
        else:
            print("Warning: Unrecognized artifact found. Please add artifact in line 145 of the source code.")

    saveConfig = driver.find_element_by_xpath("//button[contains(.,'Save')]")
    saveConfig.click()

# create new view
def createView(driver, which_jenkins, full_version):
    allViewElem = driver.find_element_by_id("jenkins-name-icon")
    allViewElem.click()

    newViewElem = driver.find_element_by_xpath("//a[contains(text(),'+')]")
    newViewElem.click()

    newViewName = driver.find_element_by_id("name")
    newViewName.send_keys("HPCC-" + full_version)

    # scroll to the location of the radio button to click it
    driver.execute_script("window.scrollTo(23, 3325)")
    if (which_jenkins == "cloud_jenkins"):
        listViewElem = driver.find_element_by_xpath("(//input[@name='mode'])[1]")
    elif (which_jenkins == "old_jenkins"):
        listViewElem = driver.find_element_by_xpath("(//input[@name='mode'])[2]")
    sleep(1)
    listViewElem.click()

    okButtonElem = driver.find_element_by_id("ok-button")
    okButtonElem.click()

    # execute a click event using JavaScript
    driver.execute_script("document.getElementById('cb2').click();")
    """wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.NAME, 'includeRegex')))"""
    sleep(1)

    regxElem = driver.find_element_by_name("includeRegex")
    sleep(1)
    regxElem.send_keys(".*" + full_version)

    okButtonElem = driver.find_element_by_xpath("//button[contains(.,'OK')]")

    try:
        okButtonElem.click()
    except Exception as e:
        sleep(1)
        okButtonElem.click()


# Main 
def main():
    parser = OptionParser()
    parser.set_usage("Usage: hpcc-build.py -s <server ip> v <version> -p <prev_platform_rc_version> -q <prev_platform_gold_version> -i <prev_ide_rc_version> -j <prev_ide_gold_version>")
    parser.add_option("-s", "--server-ip", type="string", dest="jenkins_ip", help="Examples: 10.240.61.86, new, old")
    parser.add_option("-v", "--version", type="string", dest="build_ver_seq",
                    help="Build versions are in the form of XX.XX.XX-X. Ex. 7.2.8-rc1")
    parser.add_option("-p", "--prev-platform-rc", type="string", dest="prev_platform_rc", 
                    help="Previous full platform rc version from current release. Ex. 7.2.8-rc1")
    parser.add_option("-q", "--prev-platform-gold", type="string", dest="prev_platform_gold", 
                    help="Previous full platform gold version from current release. Ex. 7.2.8-1")
    parser.add_option("-i", "--prev-eclide-rc", type="string", dest="prev_eclide_rc", 
                    help="Previous full eclide rc version from current release. Ex. 7.2.8-rc1")
    parser.add_option("-j", "--prev-eclide-gold", type="string", dest="prev_eclide_gold", 
                    help="Previous full eclide gold version from current release. Ex. 7.2.8-rc1")
    options, args = parser.parse_args()

    server = options.jenkins_ip
    full_version = options.build_ver_seq
    ver_seq = re.split("-",  full_version, 1)
    build_version = ver_seq[0]
    build_seq =  ver_seq[1]
    prev_platform_rc = options.prev_platform_rc
    prev_platform_gold = options.prev_platform_gold
    prev_eclide_rc = options.prev_eclide_rc
    prev_eclide_gold = options.prev_eclide_gold
    which_jenkins = ""
    
    if len(args) != 1:
        try:
            build_series = re.search("(\d*\.\d*\.*)", build_version).group() + "x"
        except Exception as e:
            print ("Please enter a valid version or type " + os.path.basename(__file__) + " -h for help.")
            sys.exit()
        
        # install webdriver: pip install webdriver-manager
        # Create a new instance (object) of the Chrome driver
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        driver = webdriver.Chrome('C:/Users/fortgo01/chromedriver.exe')

        if (server == "10.240.61.86" or server == "new"):
            server = "10.240.61.86"
            which_jenkins = "cloud_jenkins"
        elif (server == "10.240.32.243" or server == "old"):
            server = "10.240.32.243"
            which_jenkins = "old_jenkins"
        else:
            print ("Unrecognized HPCC Jenkins Server: " + server)
            sys.exit()
            
        # go to the template for HPCC-7.x page
        driver.get("http://" + server + "/view/HPCC-7.x/")

        print ("Setting up HPCC-" + full_version)

        search(driver, "HPCC-" + build_version)
        isWorkflow(driver, which_jenkins, build_version)
        setupBuilds(driver, build_version, full_version, build_series, search,
                    prev_platform_rc, prev_eclide_rc, prev_platform_gold, prev_eclide_gold, build_seq)
        setupECLIDE(driver, full_version, search)
        createView(driver, which_jenkins, full_version)

        print("Successful!")
        print("Hello HPCC-" + full_version)
    else:
        parser.error("Missing required argument(s)")
if __name__=="__main__":
    main()
