#!/usr/bin/python3
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

from multiprocessing.connection import wait
import os
import sys
import re
import time
import xml.etree.ElementTree as ET
from wsgiref.headers import Headers
import requests
from urllib import request
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from beautifultable import BeautifulTable
from optparse import OptionParser
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chromeOptions = Options()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--disable-gpu')
chromeOptions.add_argument('--remote-debugging-port=9222')
# from webdriver_manager.chrome import ChromeDriverManager


# search an item
def search(driver, dashboard, searchElem):
    sleep(1)
    print("Searching: " + searchElem)
    # clear search box
    dashboard(driver)
    # find the search box element by id
    searchBox = driver.find_element(By.ID, "search-box")

    # type in the search box
    searchBox.send_keys(searchElem)

    # submit the form
    searchBox.submit()

# navigate to dashboard


def dashboard(driver):
    d = driver.find_element(By.ID, "jenkins-name-icon")
    d.click()
    print("Return to dashboard")

# create a workflow if none exists


def isWorkflow(driver, build_version, version_series, search, dashboard):
    search(driver, dashboard, "HPCC-" + build_version)
    try:
        # find element by text
        textElem = driver.find_element(By.LINK_TEXT, "Create Workflow")
        textElem.click()
        print("New item and workflow needed: No")
    except Exception as e:
        print('New item and workflow needed: Yes', format(e))

        search(driver, dashboard, "HPCC-" + version_series)

        # create new item
        print("Creating a new item.")
        createItem = driver.find_element(
            # By.XPATH, "//div[@id='tasks']/div/span/a/span[2]"
            By.LINK_TEXT, "New Item")
        createItem.click()

        sleep(5)

        # workflowName = driver.find_element(By.ID, "name")
        workflowName = driver.find_element(By.XPATH, "//input[@id='name']")
        workflowName.send_keys("HPCC-" + build_version)

        sleep(2)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(1)
        itemType = driver.find_element(
            By.XPATH, "//div[@id='j-add-item-type-uncategorized']/ul/li[2]/label"
        )
        itemType.click()
        print("Selected: Template Workflow Job")

        sleep(2)

        createItem = driver.find_element(By.XPATH, "//button[@id='ok-button']")
        createItem.click()
        print("New workflow created: HPCC-" + build_version)

# setup all builds except ECLIDE


def setupBuilds(driver, build_version, full_version, template_series, version_series, search,
                prev_platform_rc, prev_platform_gold, build_seq, release_type):
    # search
    search(driver, dashboard, "HPCC-" + build_version)

    print("Setting up jobs for: HPCC-" + full_version)

    # get the major.minor.
    major_minor = re.search("(\d*\.\d*\.*)", build_version).group()

    # create build
    textElem = driver.find_element(By.LINK_TEXT, "Create Workflow")
    textElem.click()

    # important!
    # wait for elements to be loaded
    sleep(3)

    # select a workflow template
    template = Select(driver.find_element(By.ID, "template.templateName"))

    if (version_series != "6.x"):
        print(full_version + " template found: Template-" + template_series)
        if (release_type == "rc"):
            template.select_by_value("HPCC-Template-All-RC-" + template_series)
        else:
            template.select_by_value(
                "HPCC-Template-All-Gold-" + template_series)
    elif (version_series == "6.x"):
        if (template_series == "6.4.x"):
            template.select_by_value("HPCC-Template-All-6.x")
    else:
        print(full_version + " template found: None ")

    # important!
    # wait for elements to be loaded
    # WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    #     (By.NAME, 'template.templateInstanceName')))
    sleep(5)

    # select a workflow name
    workflowName = driver.find_element(
        By.NAME, "template.templateInstanceName")
    workflowName.send_keys("WF-HPCC-" + full_version)

    # get job names
    workflowJob_list = driver.find_elements(
        By.XPATH, "//div[@id='msg']/table/tbody/tr/td/input")

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
            job_id_2 = job_prefix + '-' + major_minor + 'validation'

            try:
                validateElem = driver.find_element(By.ID, job_id)
            except Exception as e:
                validateElem = driver.find_element(By.ID, job_id_2)
            if (validateElem.text == 'valid name'):
                print("Valid name: Yes")
            elif (validateElem.text == 'invalid name'):
                print("Valid name: No")
            else:
                print("Valid name: Unknown")

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    a = 0
    while a < 10:
        try:
            buttonElem = driver.find_element(
                By.XPATH, "//input[@value='Create']")
            # allowExistName = driver.find_element(By.ID, "allow_exist_name")
            # allowExistName.click()
            buttonElem.click()
            # buttonElem.assertFalse(element.is_displayed())
            print("a=" + a)
        except Exception as e:
            try:
                driver.find_element(By.XPATH, "//input[@value='Create']")
            except Exception as e:
                break
            print("Build name validation failed.")
            print("Build names will be validated again in 5 seconds.")
            sleep(5)
            a += 1

    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    #     (By.XPATH, '//*[@id="side-panel"]/div[2]/div[2]/table/tbody/tr/td[2]/input')))
    sleep(5)
    print("Build list set: Yes")

# ECLIDE build setup


def setupECLIDE(driver, full_version, search):
    print("Build name: CE-Candidate-ECLIDE-" + full_version)
    search(driver, dashboard, "ECLIDE-W32-" + full_version)

    textElem = driver.find_element(By.LINK_TEXT, "Configure")

    try:
        textElem.click()
    except Exception as e:
        sleep(1)
        textElem.click()

    # important!
    sleep(1)

    # xpaths of artifacts' name input box
    artifacts = driver.find_elements(By.XPATH, "//input[@name='_.filter']")

    for artifact in artifacts:
        if(artifact.get_attribute("value") == "**/build-docs/docs/EN_US/HTMLHelp/html_help*.zip,**/build-docs/docs/PT_BR/HTMLHelp/html_help*.zip"):  # English and Portuguese docs
            elem = driver.find_element(
                By.XPATH, "(//input[@name='_.projectName'])[1]")
            elem.send_keys("CE-Candidate-Docs-" + full_version)
        elif(artifact.get_attribute("value") == "**/build/hpccsystems-clienttools*.exe"):
            elem = driver.find_element(
                By.XPATH, "(//input[@name='_.projectName'])[2]")
            elem.send_keys("CTW32-" + full_version)
        else:
            print(
                "Warning: Unrecognized artifact found. Please add artifact in line 145 of the source code.")

    saveConfig = driver.find_element(By.XPATH, "//button[contains(.,'Save')]")
    saveConfig.click()
    print("Configured: Yes")

# CE-Candidate-Plugins-Spark setup


def sparkPlugin(driver, full_version, search):
    print("Build name: CE-Candidate-Plugins-Spark-" + full_version)
    search(driver, dashboard, "CE-Candidate-Plugins-Spark-" + full_version)

    textElem = driver.find_element(By.LINK_TEXT, "Configure")
    sleep(1)
    textElem.click()
    sleep(1)

    driver.execute_script("window.scrollTo(72,document.body.scrollHeight)")

    # xpaths of artifacts' name input box
    artifacts = driver.find_elements(By.XPATH, "//input[@name='_.filter']")

    for artifact in artifacts:
        if(artifact.get_attribute("value") == "**/*.jar"):
            elem = driver.find_element(
                By.XPATH, "(//input[@name='_.projectName'])[1]")
            elem.send_keys("Java-Projects-" + full_version)
        else:
            print(
                "Warning: Unrecognized artifact found. Please add artifact in the source code.")

    saveConfig = driver.find_element(By.XPATH, "//button[contains(.,'Save')]")
    saveConfig.click()
    print("Configured: Yes")

# LN-Candidate-with-Plugins-Spark setup


def lnWithPluginSpark(driver, full_version, search):
    print("Build name: LN-Candidate-with-Plugins-Spark-" + full_version)
    search(driver, dashboard, "LN-Candidate-with-Plugins-Spark-" + full_version)

    textElem = driver.find_element(By.LINK_TEXT, "Configure")
    sleep(1)
    textElem.click()
    sleep(1)

    driver.execute_script("window.scrollTo(72,document.body.scrollHeight)")

    # xpaths of artifacts' name input box
    artifacts = driver.find_elements(By.XPATH, "//input[@name='_.filter']")

    for artifact in artifacts:
        if(artifact.get_attribute("value") == "**/*.jar"):
            elem = driver.find_element(
                By.XPATH, "(//input[@name='_.projectName'])[1]")
            elem.send_keys("Java-Projects-" + full_version)
        else:
            print(
                "Warning: Unrecognized artifact found. Please add artifact in line 248 of the source code.")

    saveConfig = driver.find_element(By.XPATH, "//button[contains(.,'Save')]")
    saveConfig.click()
    print("Configured: Yes")

# create new view


def createView(driver, full_version, server, username, password):
    build_name = "HPCC-" + full_version
    url = "http://" + server + "/newView"

    # tree = ET.parse('config/view.xml')
    # root = tree.getroot()
    # root.find('name').text = str(build_name)
    # new_file_name = 'last-rendered-view.xml'
    # tree.write(new_file_name)
    # f = open(new_file_name, 'r')
    # new_file = f.read()
    # try:
    #     view = requests.post(
    #         url, data={'file': new_file}, headers={'Content-Type': 'application/xml'}, auth=(username, password))
    #     print(view.text)
    # allViewElem = driver.find_element(By.ID, "jenkins-name-icon")
    # allViewElem.click()
    # print('Home button clicked')
    # newViewElem = driver.find_element(
    #     By.XPATH, "(//a[contains(@href, '/newView')])")
    # newViewElem.click()

    driver.get(url)
    print(f'Creating a new view for {build_name}')
    newViewName = driver.find_element(By.ID, "name")
    newViewName.send_keys(build_name)
    listViewElem = driver.find_element(
        By.XPATH, "//label[contains(.,'List View')]")
    try:
        listViewElem.click()
    except Exception as e:
        listViewElem.click()

    okButtonElem = driver.find_element(By.NAME, "Submit")
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.NAME, "Submit")))

    try:
        okButtonElem.click()
        print("A new view has been created for " + build_name)
    except Exception as e:
        try:
            okButtonElem.click()
            print("A new view has been created for " + build_name)
        except Exception as e:
            print("A view with the name " + build_name + "might already exist.")

    print(f'Configuring {build_name} view')
    # execute a click event using JavaScript
    driver.execute_script("document.getElementById('cb2').click();")
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.NAME, 'includeRegex')))
    regxElem = driver.find_element(By.NAME, "includeRegex")
    regxElem.send_keys(".*" + full_version)

    okButtonElem = driver.find_element(By.XPATH, "//button[contains(.,'OK')]")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'OK')]")))
    driver.execute_script("arguments[0].click();", okButtonElem)
    print("View created: Yes")


def runBuilds(driver, server, search, full_version, build_version, username, password):

    # search
    search(driver, dashboard, "HPCC-" + build_version)

    sleep(5)
    wflow = driver.find_element(By.LINK_TEXT, "WF-HPCC-" + full_version)
    wflow.click()

    # get job names
    sleep(5)
    jobs = driver.find_elements(
        By.XPATH, "//div[@id='msg']/table/tbody/tr/td/a")
    builds = []

    for job in jobs:
        builds.append(job.text)

    search(driver, dashboard, 'HPCC-' + full_version)

    # Table vars
    h0 = ["Name"]
    h0.append("Type")
    h0.append("Status")
    r = ['a', 'b', 'c']
    table = BeautifulTable()
    table.columns.header = h0

    for build in builds:
        try:
            if (build != "CE-Candidate-HyperV-64bit-" + full_version and build != "CE-Candidate-Plugins-Spark-" + full_version
                and build != "ECLIDE-W32-" + full_version and build != "CE-Candidate-VM-64bit-" + full_version
                and build != "Java-Projects-Maven-Central-Release-" + full_version and build != "LN-Candidate-with-Plugins-Spark-" + full_version
                    and build != "Promote-LN-Docker-Image-" + full_version and build != "Regression-" + full_version):

                # url = "http://" + server + "/view/HPCC-" + full_version + \
                #     "/job/" + build + "/build?delay=0sec"
                url = "http://" + server + "/view/HPCC-" + full_version + \
                    "/job/" + build + "/build"
                print("Launching: " + url)
                trigger = requests.post(url, auth=(username, password))
                print(trigger.text)
                # driver.get(url)

                # p = driver.find_element(
                #     By.XPATH, "//*[@id='main-panel']/form/input")

                # p.click()

                r[0] = build
                r[1] = '-'
                r[2] = 'Running'
                table.rows.append(r)
            else:
                r[0] = build
                r[1] = 'Downstream'
                r[2] = 'Will be triggered by another build'
                table.rows.append(r)
        except Exception as e:
            print(("The run button for" + " " + build + " " + "couldn't be found."))
            print((build + " " + "might be disabled by default"))

    print(table)


# Main
def main():
    py_version = sys.version_info
    parser = OptionParser()
    parser.set_usage(
        "Usage: hpcc-build.py -s <server ip> --username <Jenkins username> --password <Jenkins password, token, or API key> v <version> -r <prev_platform_rc_version> -g <prev_platform_gold_version> --create --run")
    parser.add_option("-v", "--version", type="string", dest="build_ver_seq",
                      help="Build versions are in the form of XX.XX.XX-X. Ex. 7.2.8-rc1")
    parser.add_option("-r", "--prev-platform-rc", type="string", dest="prev_platform_rc",
                      help="Previous full platform rc version from current release. Ex. 7.2.8-rc1")
    parser.add_option("-g", "--prev-platform-gold", type="string", dest="prev_platform_gold",
                      help="Previous full platform gold version from current release. Ex. 7.2.8-1")
    parser.add_option("--create", action="store_true", default=False, dest="create",
                      help="Create builds on Jenkins server")
    parser.add_option("--noide", action="store_true", default=False, dest="noide",
                      help="Do not create ECL IDE build")
    parser.add_option("-s", "--server", type="string", dest="server",
                      help="Jenkins server IP")
    parser.add_option("--run", action="store_true", default=False, dest="run",
                      help="Run builds")
    parser.add_option("-u", "--username", type="string", default="jenkins-auto", dest="username",
                      help="Jenkins username")
    parser.add_option("-p", "--password", type="string", dest="password",
                      help="Jenkins password")
    parser.add_option("--headless", action="store_true", default=False, dest="headless",
                      help="Create projects without browser GUI")
    options, args = parser.parse_args()

    server = options.server
    full_version = options.build_ver_seq
    ver_seq = re.split("-",  full_version, 1)
    build_version = ver_seq[0]
    build_seq = ver_seq[1]
    major = int(re.search("(^[0-9]*)", build_version).group())

    prev_platform_rc = options.prev_platform_rc
    prev_platform_gold = options.prev_platform_gold
    create_builds = options.create
    no_ide = options.noide
    trigger_builds = options.run
    headless = options.headless
    username = options.username
    password = options.password

    try:
        template_series = re.search(
            "(\d*\.\d*\.*)", build_version).group() + "x"  # example: 8.0.x
        version_series = re.search(
            "(\d*\.*\.*\.*)", build_version).group() + "x"  # example: 8.x
        print("Building from template series: " + "HPCC-" + template_series)
    except Exception as e:
        print(("Please enter a valid version or type " +
              os.path.basename(__file__) + " -h for help."))
        sys.exit()

    # install dependencies: pip3 install webdriver_manager beautifultable
    if (py_version >= (3, 8)):
        print("Running Selenium 4 with Python {}.{}.{}".format
              (py_version.major, py_version.minor, py_version.micro))
        service = Service('/usr/local/bin/chromedriver')
        # Create a new instance (object) of the Chrome driver
        if (headless == True):
            driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=chromeOptions)
        else:
            driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()))
    else:
        print("Running Selenium 3 with Python {}.{}.{}" .format
              (py_version.major, py_version.minor, py_version.micro))
        if (headless == True):
            driver = webdriver.Chrome(
                executable_path="/usr/local/bin/chromedriver", options=chromeOptions)
        else:
            driver = webdriver.Chrome('/usr/local/bin/chromedriver')
            # driver = webdriver.Firefox(executable_path=r'C:/Users/fortgo01/geckodriver.exe')

    x = re.search("^rc[1-9]", build_seq)
    if (x):
        release_type = "rc"
    else:
        release_type = "gold"

    # go to the template for HPCC-7.x page
    url = "http://" + server 
    print("Launching Jenkins server" + " " + url)
    driver.get(url)

    if create_builds:
        print(("Setting up HPCC-" + full_version))
        print("----------------------------------")
        isWorkflow(driver, build_version,
                   version_series, search, dashboard)
        print("----------------------------------")
        setupBuilds(driver, build_version, full_version, template_series, version_series, search,
                    prev_platform_rc, prev_platform_gold, build_seq, release_type)
        print("----------------------------------")
        if no_ide == False:
            setupECLIDE(driver, full_version, search)
            print("----------------------------------")
        if major < 9:
            sparkPlugin(driver, full_version, search)
            print("----------------------------------")
            lnWithPluginSpark(driver, full_version, search)
        try:
            print("----------------------------------")
            createView(driver, full_version, server, username, password)
        except Exception as e:
            print("Unable to create the view.")
            print("A view might have already been created.")
        print("----------------------------------")
        print("Configurations: Done")
    if trigger_builds:
        runBuilds(driver, server, search, full_version,
                  build_version, username, password)


if __name__ == "__main__":
    main()
