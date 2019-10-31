Jenkins-Automation
==================

This repository has some applications to help automate HPCC builds on Jenkins

Selenium Requirements
---------------------

+ Windows OS
+ Linux OS
+ MacOS
+ Selenium Webdriver
+ Chromedriver
+ Google Chrome Browser
+ Python 3

Install Selenium and dependencies
---------------------------------

+ Download Selenium from https://www.seleniumhq.org/
+ Download Chromedriver from http://chromedriver.chromium.org/downloads
+ Download Chrome from https://www.google.com/chrome/b/
+ Download Python
    + Windows:
        + https://www.python.org/downloads/windows/
    + MacOS:
        + https://www.python.org/downloads/mac-osx/
    + Linux:
        + CentOS:
            ```
            sudo yum update -y
            sudo yum install python36u
            ```
        + Ubuntu
            ```
            sudo apt-get update
            sudo apt-get instal python3.6
            ```
 Usage
 -----

```
Usage: hpcc-build.py -v <version> -p <prev_platform_rc_version> -q <prev_platform_gold_version> -i <prev_ide_rc_version> -j <prev_ide_gold_version>

Options:
  -h, --help            show this help message and exit
  -v BUILD_VER_SEQ, --version=BUILD_VER_SEQ
                        Build versions are in the form of XX.XX.XX-X. Ex.
                        7.2.8-rc1
  -p PREV_PLATFORM_RC, --prev-platform-rc=PREV_PLATFORM_RC
                        Previous full platform rc version from current
                        release. Ex. 7.2.6-rc1
  -q PREV_PLATFORM_GOLD, --prev-platform-gold=PREV_PLATFORM_GOLD
                        Previous full platform gold version from current
                        release. Ex. 7.2.6-1
  -i PREV_ECLIDE_RC, --prev-eclide-rc=PREV_ECLIDE_RC
                        Previous full eclide rc version from current release.
                        Ex. 7.2.6-rc1
  -j PREV_ECLIDE_GOLD, --prev-eclide-gold=PREV_ECLIDE_GOLD
                        Previous full eclide gold version from current
                        release. Ex. 7.2.6-1
```


Note: All the arguments use full version
Full Version Example: 7.2.16-rc1, 7.2.16-1





Sikuli Requirements
-------------------

+ Windows
+ Linux (maybe need recapture the images)
+ Mac (maybe need recapture the images)
+ Sikuli
+ Java 6, 7 or 8
+ Chrome



Install and configure Sikuli
----------------------------
+ Download stable sikuli-setup.jar from http://www.sikuli.org/download.html
+ Place sikuli-setup.jar in desired location. For example c:/software/sikuli
+ Run:  java -jar sikuli-setup.jar
+ Select the first (IDE and Command-line) and the last (compatible cross OS) options
+ Follow the instruction to finish setup and configuration.


Usage
-----


Currently there are multiple sikuli applications. For instance, HPCC5.0.sikuli is for generating HPCC 5.0.x projects. 
HPCC5.2.sikuli is for generating HPCC 5.2.x projects.

+ It is better to close other Chrome or at lest move them to the top of the Windows
+ Start Sikuli IDE: runIDE.cmd
+ From "File" open the sikuli application. For example HPCC5.2.sikuli
+ Modify "build_tag" and "version"
+ Click "Run" which may prompt you save and run.