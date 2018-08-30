Jenkins-Automation
==================

This repository has some applications to help automate HPCC builds on Jenkins


Requirements
------------

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
 


