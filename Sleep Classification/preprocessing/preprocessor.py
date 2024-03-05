import os
import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import StandardScaler

class Features:
    def __init__(self):
        self.motion_data_path = '/Users/rishabhmallela/Documents/Sleep Classification/data/counts'
        self.hr_data_path = '/Users/rishabhmallela/Documents/Sleep Classification/data/heart_rate' 
        self.labels_data_path = '/Users/rishabhmallela/Documents/Sleep Classification/data/labels'
        self.features_path = '/Users/rishabhmallela/Documents/Sleep Classification/features'

        self.master_hr_data = self.readData(self.hr_data_path, False)
        self.master_motion_data = self.readData(self.motion_data_path, False)
        self.master_labels_data = self.readData(self.labels_data_path, True)

        self.master_hr_features = []
        self.master_motion_features = []
        self.master_time_features = []
        self.master_labels_features = []
        self.index = -1
        self.groups = []
        self.group_num = 1
        self.motion_scaling_constant = 1500
        
    def makeFeatures(self):
        files = []
        for file in os.walk(self.features_path):
            files.append(file)

        feature_files = sorted(files[0][2], key=str.lower)
        del feature_files[0]

        for file in feature_files:
            if "time" in file: #time features
                # if "1360686" in file: #data is messed up, handle separately, index skipped is 1
                #     self.master_hr_features.append([])
                #     self.master_motion_features.append([])
                #     self.master_time_features.append([])
                #     self.master_labels_features.append([])
                #     self.index += 1
                #     continue
                if '1360686' in file: continue
                self.master_labels_features.append([])
                self.index += 1
                file_path = f'{self.features_path}/{file}'
                f = open(file_path, 'r')

                #get last time and initialize time features
                last_line = float(f.readlines()[-1][:-1])
                last_time = int(last_line*3600)
                arr = []
                for i in range(30, last_time+1, 30):
                    arr.append(float(i/3600))
                arr = np.array(arr)
                self.master_time_features.append(arr)

                #initialize psg label features
                i = 1
                while self.master_labels_data[self.index][i][0] <= last_time:
                    if self.master_labels_data[self.index][i][1] == -1 or self.master_labels_data[self.index][i][1] == 0:
                        self.master_labels_features[self.index].append(0)
                    elif self.master_labels_data[self.index][i][1] == 4:
                        self.master_labels_features[self.index].append(3)
                    else:
                        self.master_labels_features[self.index].append(self.master_labels_data[self.index][i][1])
                    i += 1

                #initialize heart rate and motion features
                self.init_HR_Features(self.index, last_time)
                self.init_Motion_Features(self.index, last_time)

                self.master_hr_features[self.index] = np.array(self.master_hr_features[self.index])
                self.master_motion_features[self.index] = np.array(self.master_motion_features[self.index])
            
        self.feat_1360686()

                
    def getFeatures(self):
        return self.master_hr_features, self.master_motion_features, self.master_time_features, self.master_labels_features

    def readData(self, path, delim):
        files = []
        for file in os.walk(path):
            files.append(file)
        files = sorted(files[0][2], key=str.lower)

        master_data = []
        for file in files:
            if '1360686' in file: continue
            file_path = f'{path}/{file}'
            if delim: 
                data = pd.read_csv(file_path, delim_whitespace=True, header=None)
            else:
                data = pd.read_csv(file_path, delimiter=',', header=0)            
            arr = data.values
            master_data.append(arr)

        return master_data
    
    def init_HR_Features(self, index, end_time):
        subject = self.master_hr_data[index]
        # self.master_hr_features.append([])
        row = 0
        hr = []
        for epoch_end_time in range(30, end_time+1, 30):
            avg_hr = 0.0
            num_hr = 0
            while row < len(subject) and subject[row][0] < epoch_end_time:
                avg_hr += subject[row][1]
                num_hr += 1
                row += 1
            if num_hr == 0: 
                hr.append(hr[-1])
                # self.master_hr_features[index].append(self.master_hr_features[index][-1]) #if there is no hr data for that epoch, copy the data from the last one
                continue
            avg_hr /= num_hr
            # self.master_hr_features[index].append(avg_hr)
            hr.append(avg_hr)


        
        #for interpolating hr values
        # time_index = pd.date_range(start='2023-05-01', periods=len(hr), freq='5S')
        # new_time_index = pd.date_range(start=time_index[0], end=time_index[-1], freq='1S')

        # # Create a Series with the original time index and heart rate data
        # heart_rate_series = pd.Series(hr, index=time_index)

        # # Interpolate the data to have a reading for every second
        # interpolated_data = heart_rate_series.reindex(new_time_index).interpolate()

        # hr = interpolated_data.values

        ema_values = []
        ema = hr[0]
        ema_values.append(ema)
        alpha = 0.95

        for i in range(1, len(hr)):
            ema = (1 - alpha) * hr[i] + alpha * ema
            ema_values.append(ema)
            
                
        
        
        ema_values = np.array(ema_values)

        new_vals = []
        for i in range(len(ema_values)):
            if i < 14:
                # new_vals.append(ema_values[i])
                new_vals.append(float(ema_values[i])/1000)
            else:
                # new_vals.append((ema_values[i]-ema_values[i-8])**3)
                new_vals.append(float(((ema_values[i]-ema_values[i-8])**3)/1000))

            

        self.master_hr_features.append(new_vals)

#bett alpha = 0.95, power = 3



    def init_Motion_Features(self, index, end_time): #for each epoch, just add all the magnitudes of motion
        # subject = self.master_motion_data[index]
        # self.master_motion_features.append([])

        # tot_motion = 0
        # time = 30
        
        # while time <= end_time:
        #     for i in range(30):
        #         x = float(subject[time][0])
        #         y = float(subject[time][1])
        #         z = float(subject[time][2])
        #         mag = math.sqrt(x*x + y*y + z*z)
        #         tot_motion += mag
        #         time += 1
        #     self.master_motion_features[index].append(tot_motion**2)
        #     tot_motion = 0


        subject = self.master_motion_data[index]
        motion = []

        tot_motion = 0
        time = 30
        
        while time <= end_time:
            for i in range(30):
                x = float(subject[time][0])
                y = float(subject[time][1])
                z = float(subject[time][2])
                mag = math.sqrt(x*x + y*y + z*z)
                tot_motion += mag
                time += 1
            motion.append(tot_motion**2)
            tot_motion = 0

        ema_values = []
        ema = motion[0]
        ema_values.append(ema)
        alpha = 0.90

        for i in range(1, len(motion)):
            ema = (1 - alpha) * motion[i] + alpha * ema
            ema_values.append(ema)
        
        ema_values = np.array(ema_values)

        new_vals = []
        for i in range(len(ema_values)):
            # new_vals.append(ema_values[i])
            new_vals.append(float(ema_values[i]/1e9))
        self.master_motion_features.append(new_vals)

    def feat_1360686(self):
        label_path = '/Users/rishabhmallela/Documents/Sleep Classification/data/labels/1360686_labeled_sleep.txt'
        motion_path = '/Users/rishabhmallela/Documents/Sleep Classification/data/counts/cleaned_1360686_acceleration.txt'
        hr_path = '/Users/rishabhmallela/Documents/Sleep Classification/data/heart_rate/1360686_heartrate.txt'

        #get time features
        last_time = 28950
        times = []
        for i in range(1290, last_time+1, 30):
            times.append(float(i/3600))
        times = np.array(times)

        self.master_time_features.append(times)

        #get labels features
        data = pd.read_csv(label_path, delim_whitespace=True, header=None)
        arr = data.values
        labels = []
        for i in range(1, len(arr)-2):
            labels.append(arr[i][1])

        labels = np.array(labels)
        self.master_labels_features.append(labels)

        #get hr features
        data = pd.read_csv(hr_path, delimiter=',', header=None)
        arr = data.values
        hr = []
        row = 0
        for epoch_end_time in range(1290, last_time+1, 30):
            avg_hr = 0.0
            num_hr = 0
            while row < len(arr) and arr[row][0] < epoch_end_time:
                avg_hr += arr[row][1]
                num_hr += 1
                row += 1
            if num_hr == 0: 
                hr.append(hr[-1])
                # self.master_hr_features[index].append(self.master_hr_features[index][-1]) #if there is no hr data for that epoch, copy the data from the last one
                continue
            avg_hr /= num_hr
            # self.master_hr_features[index].append(avg_hr)
            hr.append(avg_hr)

        ema_values = []
        ema = hr[0]
        ema_values.append(ema)
        alpha = 0.95

        for i in range(1, len(hr)):
            ema = (1 - alpha) * hr[i] + alpha * ema
            ema_values.append(ema)
        
        ema_values = np.array(ema_values)

        new_vals = []
        for i in range(len(ema_values)):
            if i < 14:
                # new_vals.append(ema_values[i])
                new_vals.append(float(ema_values[i])/1000)
            else:
                # new_vals.append((ema_values[i]-ema_values[i-8])**3)
                new_vals.append(float(((ema_values[i]-ema_values[i-8])**3)/1000))
        new_vals = np.array(new_vals)
        self.master_hr_features.append(new_vals)


        #get motion values
        data = pd.read_csv(motion_path, delimiter=',', header=0)
        arr = data.values
        motion = []

        tot_motion = 0
        time = 0
        
        while time < len(arr)-939:
            for i in range(30):
                x = float(arr[time][0])
                y = float(arr[time][1])
                z = float(arr[time][2])
                mag = math.sqrt(x*x + y*y + z*z)
                tot_motion += mag
                time += 1
            motion.append(tot_motion**2)
            tot_motion = 0

        ema_values = []
        ema = motion[0]
        ema_values.append(ema)
        alpha = 0.90

        for i in range(1, len(motion)):
            ema = (1 - alpha) * motion[i] + alpha * ema
            ema_values.append(ema)
        
        ema_values = np.array(ema_values)

        new_vals = []
        for i in range(len(ema_values)):
            # new_vals.append(ema_values[i])
            new_vals.append(float(ema_values[i]/1e9))
        new_vals = np.array(new_vals)
        self.master_motion_features.append(new_vals)