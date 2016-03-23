build_sequence = "rc3"
version = "5.6.0"
##############################################
#                                            #
# Create Workflow projects                   #
#                                            #
##############################################

type("Create Jenkins Projects")
myApp = App.open("C:\Program Files (x86)\Google\Chrome\Application\chrome http://10.176.32.6/view/HPCC-5.x/\n")
wait(10)
#type("http://10.176.32.6/view/HPCC-5.x/\n")
#wait(2)

click("1426087140656.png")
wait(2)
type("HPCC-" + version + "\n")
wait(2)

click("1426786909458.png")
wait(2)
click("1426190248434.png")
wait(2)
type(Key.DOWN)
wait(1)
click("1436448912506.png")
wait(1)
click("1426786924923.png")
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
        'CE-Platform-Libraries-Win32-',
        'CE-Platform-Libraries-Win64-',
        'EE-Candidate-',
        'EE-Candidate-withplugins-',
        'LN-Candidate-',
        'LN-Candidate-Clienttools-',
        'LN-Candidate-withplugins-',
        'LN-Clienttools-win-32bit-',
        'Post-Build-Community-'
        ]

for project_prefix in project_prefix_list:
    type(Key.TAB)
    type(project_prefix + version + "-" + build_sequence)
    wait(1)
    


#Workflow Parameters
for i in range(12):
    type(Key.TAB)
    if (i == 5):
        type(version)
    else:
        type(version + "-" + build_sequence)
    wait(1)

wait(2)
loc = SCREEN.getCenter()
wheel(loc, WHEEL_DOWN, 5)
wait(3)

click("1426786938291.png")
wait(3)
##############################################
#                                            #
# Add Clienttools and Graphcontrol to        #
# ECLIDE Project                             #
#                                            #
##############################################
click("1426087140656.png")
wait(4)
type("CE-Candidate-ECLIDE-Win-32bit-" + version + "-" + build_sequence + "\n")
wait(4)
click("1426787070856.png")
wait(1)
for i in range(50):
   type(Key.DOWN)
wait(1)   
for i in range(30):
   type(Key.DOWN)
   if exists("1426787123802.png"):
       break

wait(3)
type(Key.DOWN)
type(Key.DOWN)
type(Key.DOWN)
type(Key.DOWN)
wait(2)
click("1426787137084.png")
wait(2)
type("CE-graphcontrol-Win-32bit-" + version + "-" + build_sequence)
wait(5)

for i in range(10):
    type(Key.TAB)
    wait(1)
wait(3)
click("1426787152300.png")
wait(1)
type("CE-Candidate-clienttools-win-32bit-" + version + "-" + build_sequence)
wait(2)
click("1426787164469.png")
wait(2)
##############################################
#                                            #
# Create List View                           #
#                                            #
##############################################
click("1426787234809.png")

wait(10)
click("1426787245264.png")
wait(14)
click("1426787256257.png")
wait(1)
type("HPCC-" + version + "-" + build_sequence)
click("1426787286042.png")
wait(1)
click("1426787305331.png")
wait(2)

for i in range(50):
   type(Key.DOWN)
   if exists("1426787345581.png"):
       break

for i in range(3):
   type(Key.DOWN)

wait(1)
click("1426787336853.png")
click("1426787359557.png")
type(".*" + version + "-" + build_sequence)
click("1426787383622.png")
wait(2)

#myApp.close()