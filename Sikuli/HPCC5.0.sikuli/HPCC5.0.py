build_sequence = "rc2"
version = "5.0.6"

##############################################
#                                            #
# Create Workflow projects                   #
#                                            #
##############################################


type("Create Jenkins Projects")
myApp = App.open("C:\Program Files (x86)\Google\Chrome\Application\chrome")
wait(5)
type("http://10.176.32.6/view/HPCC-5.x/\n")
wait(5)

click("1424379630194.png")

wait(2)
click("1424364405084.png")
wait(2)
click("1424379685177.png")
wait(2)
type(Key.DOWN)
wait(1)
click("1424379744941.png")
wait(1)
click("1424371251191.png")
type("WF-HPCC-" + version + "-" + build_sequence)
wait(1)

# Defined jobs
project_prefix_list = [
        'CE-Candidate-',
        'CE-Candidate-clienttools-',
        'CE-Candidate-clienttools-win-32bit-',
        'CE-Candidate-docs-',
        'CE-Candidate-ECLIDE-Win-32bit-',
        'CE-Candidate-gangliamonitoring-',
        'CE-Candidate-graphcontrol-',
        'CE-Candidate-graphcontrol-osx-',
        'CE-Candidate-nagiosmonitoring-',
        'CE-Candidate-vm-32bit-',
        'CE-Candidate-vm-64bit-',
        'CE-Candidate-withplugins-',
        'CE-graphcontrol-Win-32bit-',
        'CE-graphcontrol-Win-64bit-',
        'EE-Candidate-',
        'EE-Candidate-withplugins-',
        'LN-Candidate-',
        'LN-Candidate-Clienttools-',
        'LN-Candidate-withplugins-'
        ]

for project_prefix in project_prefix_list:
    type(Key.TAB)
    type(project_prefix + version + "-" + build_sequence)
    wait(1)
    


#Workflow Parameters
for i in range(11):
    type(Key.TAB)
    if (i == 4):
        type(version)
    else:
        type(version + "-" + build_sequence)
    wait(1)

wait(2)
loc = SCREEN.getCenter()
wheel(loc, WHEEL_DOWN, 5)
wait(3)

click("1424376486681.png")
wait(1)

##############################################
#                                            #
# Add Clienttools and Graphcontrol to        #
# ECLIDE Project                             #
#                                            #
##############################################
click("1424381363527.png")
wait(3)
click("1424380583579.png")
wait(2)
click("1424380615452.png")
wait(1)
for i in range(60):
   type(Key.DOWN)
click("1424380709407.png")
wait(1)
type("CE-graphcontrol-Win-32bit-" + version + "-" + build_sequence)
wait(1)
for i in range(10):
    type(Key.TAB)
    
wait(1)
click("1424380709407.png")
wait(1)
type("CE-Candidate-clienttools-win-32bit-" + version + "-" + build_sequence)
wait(1)
click("1424380968663.png")
wait(2)
##############################################
#                                            #
# Create List View                           #
#                                            #
##############################################
click("1424381175353.png")
wait(2)

click("1424376618419.png")
wait(1)
click("1424376664710.png")
wait(1)
type("HPCC-" + version + "-" + build_sequence)
click("1424376812717.png")
wait(1)
click("1424376840150.png")
wait(2)

for i in range(5):
   type(Key.DOWN)


wait(2)
click("1424376906302.png")
click("1424376926049.png")
type(".*" + version + "-" + build_sequence)
click("1424377002994.png")
wait(2)

#myApp.close()