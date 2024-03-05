import os
import pandas as pd
import numpy as np

path_in = '/Users/rishabhmallela/Documents/Sleep Classification/data/motion'
path_out = '/Users/rishabhmallela/Documents/Sleep Classification/data/cleaned_motion'

# files = files = os.listdir(path_in)
# files.remove('5383425_acceleration.txt')
# files.remove('8258170_acceleration.txt')

# files = ['5383425_acceleration.txt', '8258170_acceleration.txt']

files = ['1360686_acceleration.txt']

frequency = 50 #frequency with which motion data was collected

for file in files:
    file_path_in = f'{path_in}/{file}'
    data = pd.read_csv(file_path_in, delim_whitespace=True, header=0)
    data = data.sort_values('time')
    arr = data.values
    
    file_path_out = f'{path_out}/cleaned_{file}'
    f = open(file_path_out, 'w')
    f.write('time x y z\n')
    print("mokam")
    line = 0
    last_line = ''
    for target in range(1255, int(arr[-1][0])):
        counter = 0
        while int(arr[line][0]) == target and counter < frequency:
            str = f'{arr[line][0]} {arr[line][1]*10} {arr[line][2]*10} {arr[line][3]*10}\n'
            last_line = f'{arr[line][1]} {arr[line][2]} {arr[line][3]}\n'
            f.write(str)
            if frequency == 10:
                f.write(str) #for interpolation to get to 30Hz only for the two 10Hz files
                f.write(str)

            counter += 1
            line += 1

        while int(arr[line][0]) == target: line += 1 #disregard readings that happen after the first 50 per second

        for i in range(frequency - counter): #interpolation
            f.write(f'{target} {last_line}')
            if frequency == 10:
                f.write(f'{target} {last_line}') #for interpolation to get to 30Hz only for the two 10Hz files
                f.write(f'{target} {last_line}')

    f.close()


