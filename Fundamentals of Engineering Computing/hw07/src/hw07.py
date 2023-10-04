#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
from scipy import integrate as inte
import matplotlib.pyplot as plt
import json
import os

def main():
	#create/initialize needed variables
	cal = sys.argv[1]
	imu = sys.argv[2]
	out = sys.argv[3]

	imuData = pd.read_csv(imu)
	d = open(cal)
	calData = json.load(d)
	d.close()
	time = imuData['time']

	vx = np.zeros([len(time)])
	vy = np.zeros([len(time)])
	vz = np.zeros([len(time)])
	x = np.zeros([len(time)])
	y = np.zeros([len(time)])
	z = np.zeros([len(time)])
	aRoll = np.zeros([len(time)])
	aPitch = np.zeros([len(time)])
	aYaw = np.zeros([len(time)])
	roll = np.zeros([len(time)])
	pitch = np.zeros([len(time)])
	yaw = np.zeros([len(time)])

	#calculate position, velocity and accelaration
	ax = imuData['a_x']*calData['a_x_scale']
	ay = imuData['a_y']*calData['a_y_scale']
	az = imuData['a_z']*calData['a_z_scale']
	vx[1:] = inte.cumtrapz(ax,x=time)
	vy[1:]= inte.cumtrapz(ay,x=time)
	vz[1:]= inte.cumtrapz(az,x=time)
	x[1:]= inte.cumtrapz(vx,x=time)
	y[1:] = inte.cumtrapz(vy,x=time)
	z[1:] = inte.cumtrapz(vz,x=time)

	vRoll = imuData['v_roll']*calData['v_roll_scale']
	vPitch = imuData['v_pitch']*calData['v_pitch_scale']
	vYaw = imuData['v_yaw']*calData['v_yaw_scale']
	aRoll[1:] = np.diff(vRoll)/np.diff(time)
	aPitch[1:] = np.diff(vPitch)/np.diff(time)
	aYaw[1:] = np.diff(vYaw)/np.diff(time)
	roll[1:] = inte.cumtrapz(vRoll,x=time)
	pitch[1:] = inte.cumtrapz(vPitch,x=time)
	yaw[1:] = inte.cumtrapz(vYaw, x=time)

	#Save data to output csv in the src directory
	pd.DataFrame({"timestamp":time,"x":x,"y":y,"z":z,"roll":roll,
						"pitch":pitch,"yaw":yaw,"v_x":vx,"v_y":vy,"v_z":vz,
						"v_roll":vRoll,"v_pitch":vPitch,"v_yaw":vYaw,
						"a_x":ax,"a_y":ay,"a_z":az,"a_roll":aRoll,
						"a_pitch":aPitch,"a_yaw":aYaw}).to_csv(
						out,float_format='%.6e')

	#plot data and save to .png
	fig, (ax0,ax1,ax2) = plt.subplots(3)
	fig.set_size_inches(8,8)
	fig.suptitle("Linear")

	ax0.plot(time,x,label='x')
	ax0.plot(time,y,label='y')
	ax0.plot(time,z,label='z')
	ax0.set_ylabel("Position [m]")
	ax0.legend(loc = "upper left")

	ax1.plot(time,vx,label='v_x')
	ax1.plot(time,vy,label='v_y')
	ax1.plot(time,vz,label='v_z')
	ax1.set_ylabel("Velocity [m/s]")
	ax1.legend(loc = "upper left")
	
	ax2.plot(time,ax,label='a_x')
	ax2.plot(time,ay,label='a_y')
	ax2.plot(time,az,label='a_z')
	ax2.set_ylabel("Accel [m/s^2]")
	ax2.set_xlabel("Time [s]")
	ax2.legend(loc = "upper right")
	
	plt.savefig("{:s}_linear.png".format(os.path.basename(imu)).replace(".csv",""))
	plt.show()

	fig, (ax0,ax1,ax2) = plt.subplots(3)
	fig.set_size_inches(8,8)
	fig.suptitle("Angular")

	ax0.plot(time,roll,label='roll')
	ax0.plot(time,pitch,label='pitch')
	ax0.plot(time,yaw,label='yaw')
	ax0.set_ylabel("Position [rad]")
	ax0.legend(loc = "upper left")
	
	ax1.plot(time,vRoll,label='v_roll')
	ax1.plot(time,vPitch,label='v_pitch')
	ax1.plot(time,vYaw,label='v_yaw')
	ax1.set_ylabel("Velocity [rad/s]")
	ax1.legend(loc = "upper right")
	
	ax2.plot(time,aRoll,label='a_roll')
	ax2.plot(time,aPitch,label='a_pitch')
	ax2.plot(time,aYaw,label='a_yaw')
	ax2.set_ylabel("Accel [rad/s^2]")
	ax2.set_xlabel("Time [s]")
	ax2.legend(loc = "upper right")

	plt.savefig("{:s}_angular.png".format(os.path.basename(imu)).replace(".csv",""))
	plt.show()
	
if __name__ == "__main__":
	main()
