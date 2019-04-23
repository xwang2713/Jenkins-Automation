build_sequence = "rc1"
version = "6.4.42"

gm_version = "6.4.6-1"
nm_version = "6.4.6-1"
gc_version = version + "-" + build_sequence
wssql_version = "6.4.6-1"

##############################################
#                                            #
# Create Workflow projects                   #
#                                            #
##############################################

type("Create Jenkins Projects")
myApp = App.open("C:\Program Files (x86)\Google\Chrome\Application\chrome http://10.240.32.243/view/HPCC-6.x/\n")
wait(3)
click("1549990620242.png")
wait(2)
type("HPCC-" + version + "\n")
wait(2)

click("1550074647131.png")
wait(2)
click("1550856335559.png")
wait(2)
type(Key.DOWN)
type(Key.DOWN)
type(Key.DOWN)
type(Key.DOWN)
wait(1)
click("1550856888450.png")
wait(1)
click("1550856437810.png")
type("WF-HPCC-" + version + "-" + build_sequence)
wait(1)

# Defined jobs
project_prefix_list = [
        'CE-Candidate-',
        'CE-Candidate-Clienttools-',
        'CE-Candidate-Clienttools-OSX-',
        'CE-Candidate-Docs-',
        'CE-Candidate-ECLIDE-Win32-',
        'CE-Candidate-Gangliamonitoring-',
        'CE-Candidate-Graphcontrol-',
        'CE-Candidate-Nagiosmonitoring-',
        'CE-Candidate-Plugins-',
        'CE-Candidate-VM-32bit-',
        'CE-Candidate-vm-64bit-',
        'CECTW32-',
        'CECTW64-',
        'EE-Candidate-',
        'LN-Candidate-Clienttools-',
        'LN-Candidate-with-Plugins-',
        'LNCTW32-',
        'LNCTW64-',
        ]

for project_prefix in project_prefix_list:
    type(Key.TAB)
    type(project_prefix + version + "-" + build_sequence)
    wait(1)
    


#Workflow Parameters
for i in range(8):
    type(Key.TAB)
    if (i == 2):
        type(gm_version)
    elif (i == 4):
        type(version)
    elif (i == 5):
        type(nm_version)
    elif (i == 6):
        type(gc_version)
    elif (i == 7):
        type(wssql_version)
    else:
        type(version + "-" + build_sequence)
    wait(1)

wait(2)
loc = SCREEN.getCenter()
wheel(loc, WHEEL_DOWN, 5)
wait(2)
click("1550857372736.png")
wait(3)
##############################################
#                                            #
# Add Clienttools Docs, and Graphcontrol to  #
# ECLIDE Project                             #
#                                            #
##############################################
click("1550856481436.png")
wait(4)
type("CE-Candidate-ECLIDE-Win32-" + version + "-" + build_sequence + "\n")
wait(4)
click("1550857493102.png")
wait(2)   
for i in range(122):
   type(Key.DOWN)
   if exists("1550857573072.png"):
       break

wait(3)
type(Key.DOWN)
wait(2)
click("1550857616915.png")
wait(2)
type("CE-Candidate-Docs-" + version + "-" + build_sequence)
wait(5)
for i in range(10):
    type(Key.TAB)
    wait(1)

type(Key.DOWN)
wait(2)
click("1550857616915.png")
wait(2)
type("CE-GC-W32-" + version + "-" + build_sequence)
wait(5)

for i in range(10):
    type(Key.TAB)
    wait(1)
wait(3)
click("1550857616915.png")
wait(1)
type("CE-Candidate-Clienttools-" + version + "-" + build_sequence)
wait(2)
click("1550857710973.png")
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