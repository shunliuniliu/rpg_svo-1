# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

# SeqNameList = ['MH_01_easy'];
# SeqNameList = ['V1_03_difficult', 'V2_02_medium', 'V2_03_difficult'];
SeqNameList = ['MH_01_easy', 'MH_02_easy', 'MH_03_medium', 'MH_04_difficult', 'MH_05_difficult', 'V1_01_easy', 'V1_02_medium', 'V1_03_difficult', 'V2_01_easy', 'V2_02_medium', 'V2_03_difficult'];
Number_GF_List = [400, 600, 800, 1000, 1500, 2000]; # [2000]; # 
Result_root = '/home/turtlebot/tmp/SVO2_Baseline/'
Num_Repeating = 10 # 20 #  5 # 
SleepTime = 5

#----------------------------------------------------------------------------------------------------------------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ALERT = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for ri, num_gf in enumerate(Number_GF_List):
    
    Experiment_prefix = 'ObsNumber_' + str(int(num_gf))

    for iteration in range(0, Num_Repeating):

        # Experiment_dir = Result_root + Experiment_prefix + '_Round' + str(iteration + 1)
        Experiment_dir = Result_root + Experiment_prefix + '_Round' + str(iteration + 1)
        cmd_mkdir = 'mkdir ' + Experiment_dir
        subprocess.call(cmd_mkdir, shell=True)

        for sn, sname in enumerate(SeqNameList):
            
            print bcolors.ALERT + "====================================================================" + bcolors.ENDC

            SeqName = SeqNameList[sn] #+ '_blur_9'
            print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName

            File_rosbag  = '/home/turtlebot/DATA/EuRoC_dataset/BagFiles/' + SeqName + '.bag'

            # rosrun ORB_SLAM2 Mono PATH_TO_VOCABULARY PATH_TO_SETTINGS_FILE
            cmd_slam   = str('LD_PRELOAD=~/svo_install_ws/install/lib/libgflags.so.2.2.0 roslaunch svo_ros ' + 'euroc_mono_lmk' + str(int(num_gf)) + '.launch')
            cmd_record = str('rosbag record -O ' + Experiment_dir + '/' + SeqName + '_tf /tf __name:=rec_bag')
            cmd_timelog = str('cp /home/turtlebot/svo_install_overlay_ws/tmpLog.txt ' + Experiment_dir + '/' + SeqName + '_Log.txt')
            cmd_rosbag = 'rosbag play ' + File_rosbag # + ' -u 30' # + ' -r 0.3'
            print bcolors.WARNING + "cmd_slam: \n"   + cmd_slam   + bcolors.ENDC
            print bcolors.WARNING + "cmd_record: \n" + cmd_record + bcolors.ENDC
            print bcolors.WARNING + "cmd_timelog: \n" + cmd_timelog + bcolors.ENDC
            print bcolors.WARNING + "cmd_rosbag: \n" + cmd_rosbag + bcolors.ENDC

            print bcolors.OKGREEN + "Launching SLAM" + bcolors.ENDC
            proc_slam = subprocess.Popen(cmd_slam, shell=True)
            # proc_slam = subprocess.Popen("exec " + cmd_slam, stdout=subprocess.PIPE, shell=True)

            print bcolors.OKGREEN + "Recording tf" + bcolors.ENDC
            proc_rec = subprocess.Popen(cmd_record, shell=True)
            # proc_rec = subprocess.Popen("exec " + cmd_record, stdout=subprocess.PIPE, shell=True)

            print bcolors.OKGREEN + "Sleeping for a few secs to wait for svo init" + bcolors.ENDC
            time.sleep(SleepTime)

            print bcolors.OKGREEN + "Launching rosbag" + bcolors.ENDC
            proc_bag = subprocess.call(cmd_rosbag, shell=True)

            print bcolors.OKGREEN + "Finished rosbag playback, kill the process" + bcolors.ENDC
            subprocess.call('rosnode kill /rec_bag', shell=True)
            subprocess.call('rosnode kill /svo', shell=True)
            # subprocess.call('pkill roslaunch', shell=True)
            # subprocess.call('pkill svo_node', shell=True)

            print bcolors.OKGREEN + "Sleeping for a few secs to wait for svo quit" + bcolors.ENDC
            time.sleep(SleepTime)
            print bcolors.OKGREEN + "Copy the time log to result folder" + bcolors.ENDC
            subprocess.call(cmd_timelog, shell=True)
            # proc_rec.terminate()
            # outs, errs = proc_rec.communicate()
            # proc_slam.kill()
