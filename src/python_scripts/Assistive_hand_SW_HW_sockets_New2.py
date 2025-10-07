import time
from math import radians, degrees, pi
import numpy as np
import socket
#from spatialmath.base import * 
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
#Punts que hem definit nosaltres (nous)
inici_target = RDK.Item('inici')
ventilar_target = RDK.Item('ventilar')
abaix_target = RDK.Item('abaix')
ventilar2_target = RDK.Item('ventilar2')
abaix2_target = RDK.Item('abaix2')

# Set robot parameters
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

# Robot Constants setup
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002 # Default port for UR robots
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6# seconds to finish movej
timel = 4# seconds to finish movel

# Define robot movement commands as URScript strings

# X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(Target.Pose())
# movel_Target = f"movel(p[{X/1000}, {Y/1000}, {Z/1000}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel}, r={blend_r})"


# set_tcp="set_tcp(p[{0.000000}, {0.050000}, {0.000000}, {0.000000}, {0.000000])"
#movej_init = f"movej(p[{-1.009423/1000}, {-1.141297/1000}, -1.870417, 3.011723, -1.009423, 0.000000],1.20000,0.75000,{timel},0.0000)"
#movel_app_shake = f"movel([-2.268404, -1.482966, -2.153143, -2.647089, -2.268404, 0.000000],{accel_mss},{speed_ms},{timel},0.000)"
#movel_shake = f"movel([-2.268404, -1.663850, -2.294637, -2.324691, -2.268404, 0.000000],{accel_mss},{speed_ms},{timel/2},0.000)"
# movel_app_give5 = f"movel([-2.280779, -1.556743, -2.129529, 5.257071, -1.570796, 2.280779],{accel_mss},{speed_ms},{timel},0.000)"
# movel_give5 = f"movel([-2.195869, -1.642206, -2.040971, 5.253965, -1.570796, 2.195869],{accel_mss},{speed_ms},{timel/2},0.000)"
#new robor movement commands

set_tcp="set_tcp(p[{0.000000}, {0.050000}, {0.000000}, {0.000000}, {0.000000}, {0.000000}])"

# --- Movimiento inicial (Init) ---
X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(inici_target.Pose())
movel_inici = f"movej(p[{X/1000}, {Y/1000}, {Z/1000}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel}, r={blend_r})"

# --- Aproximación apretón de manos (App_shake) ---
X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(ventilar_target.Pose())
movel_ventilar = f"movel(p[{X/1000}, {Y/1000}, {Z/1000}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel}, r={blend_r})"

# --- Apretón de manos (Shake) ---
X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(abaix_target.Pose())
movel_abaix = f"movel(p[{X/1000}, {Y/1000}, {Z/1000}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel/2}, r={blend_r})"


X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(ventilar2_target.Pose())
movel_ventilar2 = f"movel(p[{X/1000}, {Y/1000}, {Z/1000}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel}, r={blend_r})"


X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(abaix2_target.Pose())
movel_abaix2 = f"movel(p[{X/1000}, {Y/1000}, {Z/1000}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel/2}, r={blend_r})"



#movel_inici = f"movel([-0.000000, -500.000000, 300.000000, 90.000000, -0.000000, -0.000000],{accel_mss},{speed_ms},{timel},0.000)"
#movel_ventilar = f"movel([-380.862000, -238.620000, 533.816000, 0.000000, -0.000000, -160.000000],{accel_mss},{speed_ms},{timel},0.000)"
#movel_abaix = f"movel([-380.862000, -238.620000, 533.816000, -45.000000, 0.000000, -160.000000],{accel_mss},{speed_ms},{timel},0.000)"
#movel_ventilar2 = f"([380.862000, -238.620000, 533.816000, -0.000000, 0.000000, -40.000000],{accel_mss},{speed_ms},{timel},0.000)"
#movel_abaix2 = f"([380.862000, -238.620000, 533.816000, -0.000000, -45.000000, -40.000000],{accel_mss},{speed_ms},{timel},0.000)"



# Initialize UR5e socket communication
def check_robot_port(ROBOT_IP, ROBOT_PORT):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)  # Tiempo de espera de 1 segundo
        robot_socket.connect((ROBOT_IP, ROBOT_PORT)) 
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
# Send commands to the UR5e robot using socket communication
def send_ur_script(command):
    robot_socket.send(("{}\n".format(command)).encode())
def receive_response(t):
    try:
        print("Waiting time: " + str(t))
        time.sleep(t)       
    except socket.error as e:
        print(f"Error receiving data from the robot: {e}")
        exit(1) #Non-zero exit status code to indicate the error

def nova_funcio():
    print("Quina calor!")
    robot.MoveL(inici_target, True)
    robot.MoveL(ventilar_target, True)
    robot.MoveL(abaix_target, True)
    robot.MoveL(ventilar_target, True)
    robot.MoveL(abaix_target, True)
    robot.MoveL(ventilar_target, True)
    robot.MoveL(abaix_target, True)
    robot.MoveL(ventilar_target, True)
    robot.MoveL(ventilar2_target, True)
    robot.MoveL(abaix2_target, True)
    robot.MoveL(ventilar2_target, True)
    robot.MoveL(abaix2_target, True)
    robot.MoveL(ventilar2_target, True)
    robot.MoveL(abaix2_target, True)
    robot.MoveL(ventilar2_target, True)
    print("nova_funcio FINISHED")

    if robot_is_connected:
        print("Ventilar REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_inici)
        receive_response(timel)
        send_ur_script(movel_ventilar)
        receive_response(timel)
        send_ur_script(movel_abaix)
        receive_response(timel)
        send_ur_script(movel_ventilar)
        receive_response(timel)
        send_ur_script(movel_abaix)
        receive_response(timel)
        send_ur_script(movel_ventilar)
        receive_response(timel)
        send_ur_script(movel_abaix)
        receive_response(timel)
        send_ur_script(movel_ventilar)
        receive_response(timel)   
        send_ur_script(movel_ventilar2)
        receive_response(timel)
        send_ur_script(movel_abaix2)
        receive_response(timel)
        send_ur_script(movel_ventilar2)
        receive_response(timel)
        send_ur_script(movel_abaix2)
        receive_response(timel)
        send_ur_script(movel_ventilar2)
        receive_response(timel)
        send_ur_script(movel_abaix2)
        receive_response(timel)
        send_ur_script(movel_ventilar2)
        receive_response(timel)
    else:
        print("UR5e is not connected. Only simulation will take place")


#Main function
def main():
    global robot_is_connected
    robot_is_connected=check_robot_port(ROBOT_IP, ROBOT_PORT)
    nova_funcio()
    if robot_is_connected:
        robot_socket.close()   
if __name__ == "__main__":
    main()
    