build_sequence = "rc1"
version = "7.0.20"


##############################################
#                                            #
# Create Workflow projects                   #
#                                            #
##############################################

type("Create Jenkins Projects")
myApp = App.open("C:\Program Files (x86)\Google\Chrome\Application\chrome http://10.240.32.243/view/HPCC-7.x/\n")
wait(5)
click("1483460695919.png")
wait(2)
type("HPCC-" + version + "\n")
wait(2)

click("1426786909458.png")
wait(2)
click("1550595716202.png")
wait(2)
type(Key.DOWN)
type(Key.DOWN)
type(Key.DOWN)
type(Key.DOWN)
wait(1)
click("1550672383385.png")
wait(1)
click("1550595850387.png")
type("WF-HPCC-" + version + "-" + build_sequence)
wait(1)

# Defined jobs
project_prefix_list = [
        'CE-Candidate-',
        'CE-Candidate-clienttools-',
        'CE-Candidate-clienttools-osx-',
        'CE-Candidate-docs-',
        'CE-Candidate-ECLIDE-Win-32bit-',
        'CE-Candidate-gangliamonitoring-',
        'CE-Candidate-nagiosmonitoring-',
        'CE-Candidate-Plugins-',
        'CE-Candidate-Plugins-Spark-',
        'CE-Candidate-vm-32bit-',
        'CE-Candidate-vm-64bit-',
        'CTW32-',
        'CTW64-',
        'EE-Candidate-',
        'LN-Candidate-Clienttools-',
        'LN-Candidate-with-Plugins-',
        'LN-Candidate-with-Plugins-Spark-',
        'LNCTW32-',
        'LNCTW64-',
        ]

for project_prefix in project_prefix_list:
    type(Key.TAB)
    type(project_prefix + version + "-" + build_sequence)
    wait(1)
    


#Workflow Parameters
for i in range(4):
    type(Key.TAB)
    if (i == 3):
        type(version)
    else:
        type(version + "-" + build_sequence)
    wait(1)

wait(2)
loc = SCREEN.getCenter()
wheel(loc, WHEEL_DOWN, 5)
wait(2)
click("1550596201286.png")
wait(3)
##############################################
#                                            #
# Add Clienttools Docs, and Graphcontrol to  #
# ECLIDE Project                             #
#                                            #
##############################################
click("1550596226110.png")
wait(4)
type("CE-Candidate-ECLIDE-Win-32bit-" + version + "-" + build_sequence + "\n")
wait(4)
click("1550594958264.png")
wait(2)
for i in range(64):
   type(Key.DOWN)
wait(1)   
for i in range(37):
   type(Key.DOWN)
   if exists("1550595089946.png"):
       break

wait(3)
type(Key.DOWN)
wait(2)
click("1550595089946.png")
wait(2)
type("CE-Candidate-docs-" + version + "-" + build_sequence)
wait(5)
for i in range(10):
    type(Key.TAB)
    wait(1)

wait(3)
click("1550595089946.png")
wait(1)
type("CTW32-" + version + "-" + build_sequence)
wait(2)
click("1550595282986.png")
wait(2)
##############################################
#                                            #
# Create List View                           #
#                                            #
##############################################
click("1550595307101.png")

wait(3)
click("1550595342635.png")
wheel(loc, WHEEL_UP, 5)
wait(2)
click("1550595372337.png")
wait(1)
type("HPCC-" + version + "-" + build_sequence)
click("1550595405004.png")
wait(1)
click("1550595432510.png")
wait(2)

for i in range(50):
   type(Key.DOWN)
   if exists("1550595501899.png"):
       break

for i in range(3):
   type(Key.DOWN)

wait(1)
click("1550595501899.png")
click("1550595574973.png")
type(".*" + version + "-" + build_sequence)
click("1550595591784.png")
wait(2)

#myApp.close()