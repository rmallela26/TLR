#do all data processing here. import model from saved file

import pandas as pd
import numpy as np

import asyncio

import math

import pickle
from sklearn.ensemble import RandomForestClassifier
from numpy import loadtxt

from sklearn.metrics import accuracy_score, precision_score, recall_score

import time

import sys
# requestId = sys.argv[1]
requestId = '54480551-b173-4c01-801d-81fc4bf22f9d'

# myUpdates = open("updates.txt", "w")
# myUpdates.write("")
# myUpdates = open("updates.txt", "a")
 
#read in motion data, hr feature, time data
# motion_data = pd.read_csv(f"{requestId}_motion_data.txt", delimiter=',', header=None)
# motion_data = np.array(motion_data)

# other_data = pd.read_csv(f"{requestId}_other_data.txt", delimiter=',', header=None)
# other_data = np.array(other_data)

hr_feature = 0.73
time = float(2000)
time_feature = time/3600
# last_motion_ema = other_data[0][2]

#process motion data

#interpolation
# async def interpolate():

#     frequency = 50
#     line = 0
#     f = open(f'{requestId}_cleaned_motion_data.txt', 'w')
#     f.write('time x y z\n')

#     for target in range(0, int(motion_data[-1][0])):
#         counter = 0
#         while int(motion_data[line][0]) == target and counter < frequency:
#             str = f'{motion_data[line][0]} {motion_data[line][1]*10} {motion_data[line][2]*10} {motion_data[line][3]*10}\n'
#             last_line = f'{motion_data[line][1]} {motion_data[line][2]} {motion_data[line][3]}\n'
#             f.write(str)
#             if frequency == 10:
#                 f.write(str) #for interpolation to get to 30Hz only for the two 10Hz files
#                 f.write(str)

#             counter += 1
#             line += 1

#         while int(motion_data[line][0]) == target: line += 1 #disregard readings that happen after the first 50 per second

#         for i in range(frequency - counter): #interpolation
#             f.write(f'{target} {last_line}')
#             if frequency == 10:
#                 f.write(f'{target} {last_line}') #for interpolation to get to 30Hz only for the two 10Hz files
#                 f.write(f'{target} {last_line}')

# # asyncio.run(interpolate())
# # print("interpolation done")

# #convert to activity counts
# async def counts():
#     from activity_counts_converter import call_main
#     call_main(requestId)
# # asyncio.run(counts())
# # import activity_counts_converter
# # print("counts done")

# async def main():
#     await interpolate()
#     print("interpolation done")
#     myUpdates.write("interpolation done\n")
#     await counts()
#     print("counts done")
#     myUpdates.write("counts done\n")

# asyncio.run(main())

# # motion_feature = 0
# # motion_ema = 0
# #magnitudes and ema
# # async def get_motion_feature():
# counts = pd.read_csv(f'{requestId}_counts.txt', delimiter=',', header=0)
# counts = np.array(counts)

# i = len(counts) - 30
# tot_motion = 0

# while i < len(counts):
#     x = float(counts[i][0])
#     y = float(counts[i][1])
#     z = float(counts[i][2])
#     mag = math.sqrt(x*x + y*y + z*z)
#     tot_motion += mag
#     i += 1

# tot_motion = tot_motion**2
# alpha = 0.90
# if last_motion_ema == -1:
#     motion_ema = tot_motion
# else:
#     motion_ema = (1 - alpha) * tot_motion + alpha * last_motion_ema
# motion_feature = float(motion_ema/1e9)

# print("got motion feature")
# myUpdates.write("got motion feature\n")
# # return motion_feature, motion_ema

# # motion_feature, motion_ema = asyncio.run(get_motion_feature())

# #input features to model
# filename = 'random_forest.sav'
# model = pickle.load(open(filename, 'rb'))
# test_data = [[hr_feature, motion_feature, time_feature]]
# probabilities = model.predict_proba(test_data)

# print("got probabilities")
# myUpdates.write("got probabilities\n")
# print(probabilities)

probabilities = [[0.41, 0.22, 0.1, 0.27]]
motion_feature = 1.0

#post processing
pred = np.argmax(probabilities[0])
probs = np.sort(probabilities[0])
prediction = -1
if motion_feature > 1.16 and motion_feature < 2.24:
    prediction = 1
elif pred == 3:
    prediction = 1
elif pred == 1 and probs[3] <= 0.7 and ((probs[2] == probabilities[0][3] and probs[2] > 0.20) or (probs[2] == probabilities[0][0] and probs[1] == probabilities[0][3] and probs[1] > 0.24)):
    prediction = 1
elif pred == 0 and time_feature > 0.41: #guessing it is 0 in the middle of the night
    prediction = 1
else:
    prediction = 0

print("post processing done")
# myUpdates.write("post processing done\n")

# #write answer to file
# l = str(prediction)
# l1 = l+"\n"
# # l1 = f'{prediction}\n'
# l2 = str(motion_ema)
# f = open(f'{requestId}_answer.txt', "w")
# f.writelines([l1, l2])
# print("done writing to answer")
# f = open('answerID.txt', "a")
# f.write(requestId + "\n")
# myUpdates.write(f"{requestId} done writing to answer")
# # sys.stdout.flush()
