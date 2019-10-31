build_sequence = "rc3"
version = "6.4.0"
##############################################
#                                            #
# Create Workflow projects                   #
#                                            #
##############################################

type("Create Jenkins Projects")
myApp = App.open("C:\Program Files (x86)\Google\Chrome\Application\chrome http://10.240.32.243/view/HPCC-6.x/\n")
wait(5)
#type("http://10.240.32.243/view/HPCC-6.x/\n")
#wait(2)

click("1483460695919.png")
wait(2)
type("HPCC-" + version + "\n")
wait(2)

click("1426786909458.png")
wait(2)
click("1486563544735.png")
wait(2)
type(Key.DOWN)
type(Key.DOWN)
type(Key.DOWN)
type(Key.DOWN)
wait(1)
click("1486563711315.png")
wait(1)
click("1486563119703.png")
type("WF-HPCC-" + version + "-" + build_sequence)
wait(1)

# Defined jobs
project_prefix_list = [
        'CE-Candidate-',
        'CE-Candidate-clienttools-',
        'CE-Candidate-clienttools-osx-',
        'CE-Candidate-clienttools-win-32bit-',
        'CE-Candidate-clienttools-win-64bit-',
        'CE-Candidate-docs-',
        'CE-Candidate-ECLIDE-Win-32bit-',
        'CE-Candidate-gangliamonitoring-',
        'CE-Candidate-graphcontrol-',
        'CE-Candidate-nagiosmonitoring-',
        'CE-Candidate-Plugins-',
        'CE-Candidate-vm-32bit-',
        'CE-Candidate-vm-64bit-',
        'CE-GC-W32-',
        'CE-GC-W64-',
        'EE-Candidate-',
        'LN-Candidate-',
        'LN-Candidate-Clienttools-',
        'LN-Clienttools-win-32bit-',
        'LN-Candidate-with-Plugins-',
        'WSSQL-Candidate-'
        ]

for project_prefix in project_prefix_list:
    type(Key.TAB)
    type(project_prefix + version + "-" + build_sequence)
    wait(1)
    


#Workflow Parameters
for i in range(8):
    type(Key.TAB)
    if (i == 4):
        type(version)
    else:
        type(version + "-" + build_sequence)
    wait(1)

wait(2)
loc = SCREEN.getCenter()
wheel(loc, WHEEL_DOWN, 5)
wait(2)
click("1486563135135.png")
wait(3)
##############################################
#                                            #
# Add Clienttools and Graphcontrol to        #
# ECLIDE Project                             #
#                                            #
##############################################
click("1486563149401.png")
wait(4)
type("CE-Candidate-ECLIDE-Win-32bit-" + version + "-" + build_sequence + "\n")
wait(4)
click("1486563170834.png")
wait(1)
for i in range(50):
   type(Key.DOWN)
wait(1)   
for i in range(30):
   type(Key.DOWN)
   if exists("1486563237152.png"):
       break

wait(3)
type(Key.DOWN)
wait(2)
click("1486563237152.png")
wait(2)
type("CE-GC-W32-" + version + "-" + build_sequence)
wait(5)

for i in range(10):
    type(Key.TAB)
    wait(1)
wait(3)
click("1486563237152.png")
wait(1)
type("CE-Candidate-clienttools-win-32bit-" + version + "-" + build_sequence)
wait(2)
click("1486563310807.png")
wait(2)
##############################################
#                                            #
# Create List View                           #
#                                            #
##############################################
click("1486563336911.png")

wait(3)
click("1486563343080.png")
wheel(loc, WHEEL_UP, 5)
wait(2)
click("1486563355570.png")
wait(1)
type("HPCC-" + version + "-" + build_sequence)
click("1486563380531.png")
wait(1)
click("1486563395035.png")
wait(2)

for i in range(50):
   type(Key.DOWN)
   if exists("1483461236486.png"):
       break

for i in range(3):
   type(Key.DOWN)

wait(1)
click("1483461236486.png")
click("1483461280975.png")
type(".*" + version + "-" + build_sequence)
click("1483461291104.png")
wait(2)

#myApp.close()