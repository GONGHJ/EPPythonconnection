from shutil import copyfile
import os
from threading import *
import numpy as np


total_house_number = 1

EPtime_step = 1
sim_days = 8 #8

MAXSTEPS = int(sim_days*24*(60/EPtime_step)) + 1
jobs=[]
num_signal_to_house = 5
num_EPoutputs = 14
EP_work_direc = os.path.join(os.getcwd(), 'Houses', 'EPWorkDirec')

# initialize global variables
global barrier, signal_to_house, EP_outputs, BES_capacity_joule, EV_capacity_joule, EVsoc, EVsignal, EV_arrive_SOC, \
    DRsignals, EVschedule, EWHonoffDailyCount, EWHONOFFSignal
BES_capacity_joule = 3.6e7
EV_capacity_joule = 2.16e+8
EVsoc = np.zeros(MAXSTEPS+1)
EVsignal = np.zeros(MAXSTEPS+1)
DRsignals = np.empty(MAXSTEPS)
DRsignals[:] = float('Nan')
EVscheduleHour=[7, 18]
EVschedule = [EVscheduleHour[0], EVscheduleHour[1]]
EVsoc[0] = 0.6
EV_arrive_SOC = 0.3 * np.random.random([sim_days, 1]) + 0.6    # [0.3, 0.9]
# EV_arrive_SOC = [0.5]     # demo case
EWHonoffDailyCount=np.zeros(sim_days)
EWHONOFFSignal=np.zeros(MAXSTEPS)

barrier = Barrier(total_house_number + 1, timeout=600)
signal_to_house = np.zeros((MAXSTEPS+1, num_signal_to_house, total_house_number))
EP_outputs = np.zeros((MAXSTEPS, num_EPoutputs, total_house_number))
# create directory for each house and copy .idf to the new folders
idf_file_path = os.path.join(os.getcwd(), 'Houses', 'IDFfiles')
for i in range(1, total_house_number + 1):
    folder_name = 'house' + str(i).rjust(2, '0')
    newpath =  os.path.join(EP_work_direc, folder_name)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    copyfile(os.path.join(idf_file_path, 'variables.cfg'), os.path.join(newpath, 'variables.cfg'))
    copyfile(os.path.join(idf_file_path, '1_sched.csv'), os.path.join(newpath, '1_sched.csv'))
    copyfile(os.path.join(idf_file_path, 'DHW_4bed_unit0_1min.csv'), os.path.join(newpath, 'DHW_4bed_unit0_1min.csv'))
    for file in os.listdir(idf_file_path):
        if file.endswith(str(i).rjust(2, '0') + '.idf'):
            idf = file
            copyfile(os.path.join(idf_file_path, idf), os.path.join(newpath, idf))
            break
print("Working directory generated. idf files moved.\n")

# put weather data to the right directory in C:\EnergyPlus
weather_file_name = 'USA_CA_Los.Angeles.Intl.AP.722950_TMY3'
if weather_file_name.endswith('.epw'):
    pass
else:
    weather_file_name = weather_file_name + ".epw"
if os.path.exists(r"C:/EnergyPlusV8-8-0/WeatherData/simulated_weather_data.epw"):
    os.remove(r'C:/EnergyPlusV8-8-0/WeatherData/simulated_weather_data.epw')
    copyfile('./Houses/weatherdata/' + weather_file_name,
             r'C:/EnergyPlusV8-8-0/WeatherData/simulated_weather_data.epw')
else:
    copyfile('./Houses/weatherdata/' + weather_file_name,
             r'C:/EnergyPlusV8-8-0/WeatherData/simulated_weather_data.epw')
# remove the previous .mat file
if os.path.exists(os.path.join(os.getcwd(), 'cosimresults.mat')):
    os.remove(os.path.join(os.getcwd(), 'cosimresults.mat'))




