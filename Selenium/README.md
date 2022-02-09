# Jenkins Automation with Selenium for HPCC Systems Platform

## This project currently supports Selenium 4


| Dependencies                          | Installation Commands                                                                        |
| ------------------------------------- | -------------------------------------------------------------------------------------------- |
| Python >=3.8                          | `sudo apt-get update; sudo apt-get install python3.8 -y                  `                   |
| Selenium 4                            | `pip3 install --target='/home/ubuntu/.local/lib/python3.8/site-packages' selenium~=4.0.0.a7` |
| WebDriver Manager 'webdriver_manager' | `pip3 install --target='/home/ubuntu/.local/lib/python3.8/site-packages' webdriver_manager`  |
| BeautifulTable 'beautifultable'       | `pip3 install --target='/home/ubuntu/.local/lib/python3.8/site-packages' beautifultable`     |


```
Usage: hpcc-build.py -s <server ip> v <version> -r <prev_platform_rc_version> -g <prev_platform_gold_version> --run

Options:
  -h, --help            show this help message and exit
  -v BUILD_VER_SEQ, --version=BUILD_VER_SEQ
                        Build versions are in the form of XX.XX.XX-X. Ex.
                        7.2.8-rc1
  -r PREV_PLATFORM_RC, --prev-platform-rc=PREV_PLATFORM_RC
                        Previous full platform rc version from current
                        release. Ex. 7.2.8-rc1
  -g PREV_PLATFORM_GOLD, --prev-platform-gold=PREV_PLATFORM_GOLD
                        Previous full platform gold version from current
                        release. Ex. 7.2.8-1
  --set                 Create builds on Jenkins server
  --run                 Run builds
  --headless            Create projects without browser GUI
  ```