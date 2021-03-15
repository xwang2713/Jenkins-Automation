#!/usr/bin/python
# -*- coding: utf-8 -*-

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
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--disable-gpu')
chromeOptions.add_argument('--remote-debugging-port=9222')
#from webdriver_manager.chrome import ChromeDriverManager
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
def search(driver, dashboard, searchElem):
    sleep(1)
    print("Search: " + searchElem)
    # clear search box 
    dashboard(driver)
    # find the search box element by id
    searchBox = driver.find_element_by_id("search-box")

    # type in the search box
    searchBox.send_keys(searchElem)

    # submit the form
    searchBox.submit()

# navigate to dashboard 
def dashboard(driver):
    d=driver.find_element_by_id("jenkins-name-icon")
    d.click()
    print("Return to dashboard")

# create a workflow if none exists
def isWorkflow(driver, which_jenkins, build_version, version_series, search, dashboard):
    search(driver, dashboard, "HPCC-" + build_version)
    try:
        # find element by text
        textElem = driver.find_element_by_link_text("Create Workflow")
        textElem.click()
        print("New item and workflow needed: No")
    except Exception as e:
        print('New item and workflow needed: Yes', format(e))

        search(driver, dashboard, "HPCC-" + version_series)

        #create new item
        createItem = driver.find_element_by_xpath("//div[@id='tasks']/div/span/a/span[2]")
        createItem.click()
        sleep(5)
        #workflowName = driver.find_element_by_id("name")
        workflowName = driver.find_element_by_xpath("//input[@id='name']")
        workflowName.send_keys("HPCC-" + build_version)
        if (which_jenkins == "new"):
            itemType = driver.find_element_by_xpath("//div[@id='j-add-item-type-uncategorized']/ul/li[2]/label")
        elif (which_jenkins == "old"):
            itemType = driver.find_element_by_xpath("//div[@id='j-add-item-type-uncategorized']/ul/li[1]/label")
        itemType.click()
        createItem = driver.find_element_by_xpath("//button[@id='ok-button']")
        createItem.click()
        print("New workflow created: HPCC-" + build_version)

# setup all builds except ECLIDE
def setupBuilds(driver, build_version, full_version, template_series, version_series, search,
                prev_platform_rc, prev_platform_gold, build_seq, release_type):
    #search 
    search(driver, dashboard, "HPCC-" + build_version)

    print("Setting up: HPCC-" + full_version + " jobs")

    #get the major.minor.
    major_minor = re.search("(\d*\.\d*\.*)", build_version).group()

    #create build
    textElem = driver.find_element_by_link_text("Create Workflow")
    textElem.click()

    # important!
    # wait for elements to be loaded
    sleep(1)

    # select a workflow template
    template = Select(driver.find_element_by_id("template.templateName"))

    if (version_series == "7.x"):
        if (template_series == "7.0.x"):
            print(full_version + " template found: Template-7.0.x ")
            template.select_by_value("HPCC-Template-All-7.0.x")
        elif (template_series == "7.2.x"):
            print(full_version + " template found: Template-7.2.x ")
            template.select_by_value("HPCC-Template-All-7.2.x")
        elif (template_series == "7.4.x"):
            print(full_version + " template found: Template-7.4.x ")
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-7.4.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-7.4.x")
        elif (template_series == "7.6.x"):
            print(full_version + " template found: Template-7.6.x ")
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-7.6.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-7.6.x")
        elif (template_series == "7.8.x"):
            print(full_version + " template found: Template-7.8.x ")
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-7.8.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-7.8.x")
        elif (template_series == "7.10.x"):
            print(full_version + " template found: Template-7.10.x ")
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-7.10.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-7.10.x")
        elif (template_series == "7.12.x"):
            print(full_version + " template found: Template-7.12.x ")
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-7.12.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-7.12.x")
        else:
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-7.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-7.x")
    elif (version_series == "8.x"):
        if (template_series == "8.0.x"):
            print(full_version + " template found: Template-8.0.x ")
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-8.0.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-8.0.x")
        else:
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-7.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-7.x")
    elif (version_series == "20.x"):
        if (template_series == "20.0.x"):
            print(full_version + " template found: Template-20.0.x ")
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-20.0.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-20.0.x")
        else:
            if (release_type == "rc"):
                template.select_by_value("HPCC-Template-All-RC-7.x")
            else:
                template.select_by_value("HPCC-Template-All-Gold-7.x")
    elif (version_series == "6.x"):
        if (template_series == "6.4.x"):
            template.select_by_value("HPCC-Template-All-6.x")
    else:
        print(full_version + " template found: None ")


    # important!
    # wait for elements to be loaded
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.NAME, 'template.templateInstanceName')))
    sleep(3)

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
            print("EE_PLATFORM_VER_SEQ: " + full_version)
        elif(job_prefix == 'CE_PLATFORM_SEQ'):
            workflowJob.send_keys(build_seq)
            print("CE_PLATFORM_SEQ: " + build_seq)
        elif(job_prefix == 'PREV_CE_PLATFORM_RC'):
            workflowJob.send_keys(prev_platform_rc)
            print("PREV_CE_PLATFORM_RC: " + prev_platform_rc)
        elif(job_prefix == 'PREV_ECLIDE_RC'):
            workflowJob.send_keys(prev_platform_rc)
            print("PREV_ECLIDE_RC: " + prev_platform_rc)
        elif(job_prefix == 'PREV_CE_PLATFORM_GOLD'):
            workflowJob.send_keys(prev_platform_gold)
            print("PREV_CE_PLATFORM_GOLD: " + prev_platform_gold)
        elif(job_prefix == 'PREV_ECLIDE_GOLD'):
            workflowJob.send_keys(prev_platform_gold)
            print("PREV_ECLIDE_GOLD: " + prev_platform_gold)
        elif (job_prefix == 'GANGLIA_MONITORING_VER_SEQ'):
            workflowJob.send_keys(full_version)
        elif (job_prefix == 'CE_PLATFORM_VER_SEQ'):
            workflowJob.send_keys(full_version)
            print("CE_PLATFORM_VER_SEQ: " + full_version)
        elif (job_prefix == 'NAGIOS_MONITORING_VER_SEQ'):
            workflowJob.send_keys(full_version)
            print("NAGIOS_MONITORING_VER_SEQ: " + full_version)
        elif (job_prefix == 'GRAPH_CONTROL_VER_SEQ'):
            workflowJob.send_keys(full_version)
            print("GRAPH_CONTROL_VER_SEQ: " + full_version)
        elif (job_prefix == 'WSSQL_VER_SEQ'):
            workflowJob.send_keys(full_version)
            print("WSSQL_VER_SEQ: " + full_version)
        elif (job_prefix == 'VERSION'):
            workflowJob.send_keys(build_version)
            print("VERSION: " + build_version)
        elif (job_prefix == 'SERIES'):
            workflowJob.send_keys(template_series)
            print("SERIES: " + template_series)
        else:
            job = job_prefix + "-" + full_version
            workflowJob.send_keys(job)
            print("Build name: " + job)
            
            jobName = workflowJob.get_attribute("name")

            try:
                job_prefix = re.match("(.*)\.(.*)\-.", jobName).group(2)
            except Exception as e:
                job_prefix = re.match("(.*)\.(.*)", jobName).group(2)

            job_id = job_prefix + '-' + major_minor + '.validation'
            
            validateElem = driver.find_element_by_id(job_id)
            if (validateElem.text == 'valid name'):
                print("Valid name: Yes")
            elif (validateElem.text == 'invalid name'):
                print("Valid name: No")
            else:
                print("Valid name: Unknown")
            


    
    for i in range(4):
        try:
            buttonElem = driver.find_element_by_xpath("//input[@value='Create']")
            # allowExistName = driver.find_element_by_id("allow_exist_name")
            # allowExistName.click()
            buttonElem.click()
            # buttonElem.assertFalse(element.is_displayed())
            print("ok button clicked for setting up builds" + i + "time(s)")
            sleep(3)
            print("slept for 3 seconds to catch potential exceptions")
            break
        except Exception as e:
            sleep(3)
            print("Build name validation failed.")
            print("Build names will be validated again in 5 seconds.")
            sleep(5)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tasks']/div[3]/span/a/span[2]")))
    print("Build list set: Yes")

# ECLIDE build setup
def setupECLIDE(driver, full_version, search):
    print("Build name: CE-Candidate-ECLIDE-" + full_version)
    search(driver, dashboard, "ECLIDE-W32-" + full_version)

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
        if(artifact.get_attribute("value") == "**/build-docs/docs/EN_US/HTMLHelp/html_help*.zip"): # English docs
            try:
                elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[3]")
            except Exception as e:
                elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[4]")
            elem.send_keys("CE-Candidate-Docs-" + full_version)
        elif(artifact.get_attribute("value") == "**/build-docs/docs/EN_US/HTMLHelp/html_help*.zip,**/build-docs/docs/PT_BR/HTMLHelp/html_help*.zip"): # English and Portuguese docs
            try:
                elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[3]")
            except Exception as e:
                elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[4]")
            elem.send_keys("CE-Candidate-Docs-" + full_version)
        elif(artifact.get_attribute("value") == "**/build/GraphControl/bin/HPCCSystemsGraphViewControl/RelWithDebInfo/npHPCCSystemsGraphViewControl.*"):
            elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[5]")
            elem.send_keys("CE-Candidate-Graphcontrol-" + full_version)
        elif(artifact.get_attribute("value") == "**/build/hpccsystems-clienttools*.exe"):
            try:
                elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[4]")
            except Exception as e:
                try:
                    elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[5]")
                except Exception as e:
                    elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[6]")
            elem.send_keys("CTW32-" + full_version)
        else:
            print("Warning: Unrecognized artifact found. Please add artifact in line 145 of the source code.")

    saveConfig = driver.find_element_by_xpath("//button[contains(.,'Save')]")
    saveConfig.click()
    print("Configured: Yes")

# CE-Candidate-Plugins-Spark setup
def sparkPlugins(driver, full_version, search):
    print("Build name: CE-Candidate-Plugins-Spark-" + full_version)
    search(driver, dashboard, "CE-Candidate-Plugins-Spark-" + full_version)

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
        if(artifact.get_attribute("value") == "**/*.jar"):
            elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[3]")
            elem.send_keys("Java-Projects-" + full_version)
        else:
            print("Warning: Unrecognized artifact found. Please add artifact in line 220 of the source code.")

    saveConfig = driver.find_element_by_xpath("//button[contains(.,'Save')]")
    saveConfig.click()
    print("Configured: Yes")

# LN-Candidate-with-Plugins-Spark setup
def lnWithPluginSpark(driver, full_version, search):
    print("Build name: LN-Candidate-with-Plugins-Spark-" + full_version)
    search(driver, dashboard, "LN-Candidate-with-Plugins-Spark-" + full_version)

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
        if(artifact.get_attribute("value") == "**/*.jar"):
            elem = driver.find_element_by_xpath("(//input[@name='_.projectName'])[3]")
            elem.send_keys("Java-Projects-" + full_version)
        else:
            print("Warning: Unrecognized artifact found. Please add artifact in line 248 of the source code.")

    saveConfig = driver.find_element_by_xpath("//button[contains(.,'Save')]")
    saveConfig.click()
    print("Configured: Yes")

# create new view
def createView(driver, which_jenkins, full_version):
    print("Creating view: HPCC-" + full_version)
    allViewElem = driver.find_element_by_id("jenkins-name-icon")
    allViewElem.click()

    newViewElem = driver.find_element_by_xpath("(//a[contains(@href, '/newView')])[2]")
    newViewElem.click()

    newViewName = driver.find_element_by_id("name")
    newViewName.send_keys("HPCC-" + full_version)

    # scroll to the location of the radio button to click it
    # driver.execute_script("window.scrollTo(23, 3425)")
    if (which_jenkins == "new"):
        listViewElem = driver.find_element_by_xpath("//div[@id='main-panel']/form/table/tbody/tr[3]/td/input")
    elif (which_jenkins == "old"):
        listViewElem = driver.find_element_by_xpath("(//input[@name='mode'])[2]")
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main-panel']/form/table/tbody/tr[3]/td/input")))
    listViewElem.click()

    okButtonElem = driver.find_element_by_id("ok-button")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "ok-button")))

    try:
        okButtonElem.click()
    except Exception as e:
        print("A view with the name HPCC-" + full_version + " " + "might already exist.")
         

    # execute a click event using JavaScript
    driver.execute_script("document.getElementById('cb2').click();")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME, 'includeRegex')))

    regxElem = driver.find_element_by_name("includeRegex")
    regxElem.send_keys(".*" + full_version)

    okButtonElem = driver.find_element_by_xpath("//button[contains(.,'OK')]")

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'OK')]")))
    okButtonElem.click()
    print("View created: Yes")

def runBuilds(driver, search, full_version, build_version):
    #search 
    search(driver, dashboard, "HPCC-" + build_version)

    wflow = driver.find_element_by_link_text("WF-HPCC-" + full_version)
    wflow.click()

    # get job names
    sleep(5)
    jobs = driver.find_elements_by_xpath("//div[@id='msg']/table/tbody/tr/td/a")
    builds = []

    for job in jobs:
        builds.append (job.text)
    
    search(driver, dashboard, 'HPCC-' + full_version)
    
    for build in builds:
        try:
            x = driver.find_element_by_xpath("//img[@alt='Schedule a Build for" + " " + build + "']")
            if(build != "CE-Candidate-HyperV-64bit-" + full_version or build != "CE-Candidate-Plugins-Spark-" + full_version
            or build != "ECLIDE-W32-" + full_version or build != "CE-Candidate-VM-64-bit-" + full_version or build != "LN-Candidate-with-Plugins-Spark-" + full_version):
                x.click()
        except Exception as e:
            print(("The run button for" + " " + build + " " + "couldn't be found."))
            print((build + " " + "might be disabled by default"))


# Main 
def main():
    parser = OptionParser()
    parser.set_usage("Usage: hpcc-build.py -s <server ip> v <version> -r <prev_platform_rc_version> -g <prev_platform_gold_version> --run")
    parser.add_option("-v", "--version", type="string", dest="build_ver_seq",
                    help="Build versions are in the form of XX.XX.XX-X. Ex. 7.2.8-rc1")
    parser.add_option("-r", "--prev-platform-rc", type="string", dest="prev_platform_rc", 
                    help="Previous full platform rc version from current release. Ex. 7.2.8-rc1")
    parser.add_option("-g", "--prev-platform-gold", type="string", dest="prev_platform_gold", 
                    help="Previous full platform gold version from current release. Ex. 7.2.8-1")
    parser.add_option("--run", action="store_true", default=True, dest="run",
                    help="Run builds")
    options, args = parser.parse_args()

    server = ""
    full_version = options.build_ver_seq
    ver_seq = re.split("-",  full_version, 1)
    build_version = ver_seq[0]
    build_seq =  ver_seq[1]
    which_jenkins = ""

    prev_platform_rc = options.prev_platform_rc
    prev_platform_gold = options.prev_platform_gold
   

    try:
        template_series = re.search("(\d*\.\d*\.*)", build_version).group() + "x" #example: 8.0.x
        version_series = re.search("(\d*\.\.*\.*)", build_version).group() + "x" #example: 8.x
        print("Building from template series: " + "HPCC-" + template_series)
    except Exception as e:
        print(("Please enter a valid version or type " + os.path.basename(__file__) + " -h for help."))
        sys.exit()
    
    # install webdriver: pip install webdriver-manager
    # Create a new instance (object) of the Chrome driver
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chromeOptions)
    #driver = webdriver.Firefox(executable_path=r'C:/Users/fortgo01/geckodriver.exe')

    if (template_series == "7.2.x"):
        server = "10.240.32.243"
        which_jenkins = "old"
    else:
        server = "10.240.61.86"
        which_jenkins = "new"
        
    x = re.search("^rc[1-9]",build_seq)
    if (x):
        release_type = "rc"
    else:
        release_type = "gold"

    # go to the template for HPCC-7.x page
    url = "http://" + server + "/view/HPCC-7.x/"
    driver.get(url)
    
    print(("Setting up HPCC-" + full_version))

    print("----------------------------------")
    isWorkflow(driver, which_jenkins, build_version, version_series, search, dashboard)
    print("----------------------------------")
    setupBuilds(driver, build_version, full_version, template_series, version_series, search,
            prev_platform_rc, prev_platform_gold, build_seq, release_type)
    print("----------------------------------")
    setupECLIDE(driver, full_version, search)
    print("----------------------------------")
    sparkPlugins(driver, full_version, search)
    print("----------------------------------")
    lnWithPluginSpark(driver, full_version, search)
    print("----------------------------------")
    createView(driver, which_jenkins, full_version)
    print("----------------------------------")
    # runBuilds(driver, search, full_version, build_version)
    print("Configurations: Done")
if __name__=="__main__":
    main()