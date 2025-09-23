from robodk.robolink import *
from robodk.robomath import *

# Robot setup
RDK = Robolink()
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Init_target = RDK.Item('Init')
App_shake_target = RDK.Item('App_shake')
Shake_target = RDK.Item('Shake')
App_give5_target = RDK.Item('App_give5')
Give5_target = RDK.Item('Give5')

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

def Init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")

def Hand_shake():
    print("Hand Shake")
    robot.MoveL(App_shake_target, True)
    robot.MoveL(Shake_target, True)
    robot.MoveL(App_shake_target, True)
    print("Hand Shake FINISHED")

def Give_me_5():
    print("Give me 5!")
    robot.MoveL(App_give5_target, True)
    robot.MoveL(Give5_target, True)
    robot.MoveL(App_give5_target, True)
    print("Give me 5! FINISHED")

# Main function
def main():
    Init()
    Hand_shake()
    Give_me_5()
    Init()
     
if __name__ == "__main__":
    main()
    
    