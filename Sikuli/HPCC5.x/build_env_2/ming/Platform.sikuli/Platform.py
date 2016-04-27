build_sequence = "rc3"
version = "5.6.4"
##############################################
#                                            #
# Create Workflow projects                   #
#                                            #
##############################################

type("Create Jenkins Projects")
myApp = App.open("C:\Program Files (x86)\Google\Chrome\Application\chrome http://10.240.32.243/view/HPCC-5.x/\n")
wait(10)
#type("http://10.240.32.243/view/HPCC-6.x/\n")
#wait(2)

click("1461687452292.png")      
wait(2)
type("HPCC-" + version + "\n")
wait(2)

click("1461687598941.png")  
wait(2)
click("1461688483089.png")
wait(2)
type(Key.DOWN)
wait(1)
click("1461777512748.png")

wait(1)
click("1461769224117.png")

type("WF-HPCC-" + version + "-" + build_sequence)
wait(1)

# Defined jobs
project_prefix_list = [
        'CE-Candidate-',
        'CE-Candidate-Clienttools-',
        'CE-Candidate-Clienttools-Win32-',
        'CE-Candidate-withplugins-',
        'EE-Candidate-',
        'EE-Candidate-withplugins-',
        'LN-Candidate-',
        'LN-Candidate-withplugins-',
        ]

for project_prefix in project_prefix_list:
    type(Key.TAB)
    type(project_prefix + version + "-" + build_sequence)
    wait(1)
    
#Workflow Parameters
for i in range(4):
    type(Key.TAB)
    if (i == 2):
        type(version)
    else:
        type(version + "-" + build_sequence)
    wait(1)

wait(2)
loc = SCREEN.getCenter()
wheel(loc, WHEEL_DOWN, 5)
wait(2)
click("1461691112277.png")
wait(3)

##############################################
#                                            #
# Create List View                           #
#                                            #
##############################################
click("1461691662352.png")
wait(10)
click("1461691704595.png")
wheel(loc, WHEEL_UP, 5)
wait(14)
click("1461691763944.png")

wait(1)
type("HPCC-" + version + "-" + build_sequence)
click("1461691838578.png")

wait(1)
click("1461691871921.png")

wait(2)

for i in range(15):
   type(Key.DOWN)
   if exists("1461691945348.png"):
       break


click("1461769801543.png")


for i in range(3):
   type(Key.DOWN)

wait(1)
click("1461692044885.png")


type(".*" + version + "-" + build_sequence)
click("1461692084650.png")

wait(2)

#myApp.close()