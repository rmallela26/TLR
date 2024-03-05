import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import coremltools as ct



import os

"""
Read all data
"""
features_path = '/Users/rishabhmallela/Documents/Sleep Classification/features'

master_train_data = []
master_train_labels = []

files = []
for file in os.walk(features_path):
    files.append(file)

feature_files = sorted(files[0][2], key=str.lower)
del feature_files[0]
counter = 1
epoch = 0
data = []
for file in feature_files:
    file_path = f'{features_path}/{file}'
    f = open(file_path, 'r')

    if "psg" in file: #labels
        labels = []
        for line in f:
            val = line[:-1]
            #CONSIDER DIFFERENTIATING REM, NREM, AND WAKE BECAUSE WAKE AND REM ARE SIMILAR AND IT MIGHT BE CAUSING
            #ACCURACY TO DECREASE BY CAUSING NOISE AND DECREASING PRECISION OF NREM
            if float(val) == 0 or float(val) == 1: #only differentiate wake, rem, non rem
                val = 1
            elif float(val) == 2:
                val = 2
            elif float(val) == 3:
                val = 3
            else:
                val = 5
            labels.append(val)
        master_train_labels.append(np.array(labels))
    else: #data
        if counter == 1:
            for line in f:
                row = []
                val = line[:-1]
                row.append(val)
                data.append(row)
        else:
            for line in f:
                val = line[:-1]
                data[epoch].append(val)
                epoch += 1
        if counter == 4:
            counter = 0
            master_train_data.append(np.array(data))
            data = []
            
        epoch = 0
        counter += 1

group_num = 1
groups = []
train_data = []
train_labels = []

for i in range(len(master_train_data)):
    if i == 13 or i == 19: #not included because neither had rem sleep
        continue
    for j in range(len(master_train_data[i])):
        groups.append(group_num)
        train_data.append(master_train_data[i][j])
        train_labels.append(master_train_labels[i][j])
    group_num += 1

model = GradientBoostingClassifier(n_estimators=100, max_depth=3)

model.fit(train_data, train_labels)

#Use to create coreml file: sudo pip install 'scikit-learn==0.19.2' 

coreml_model = ct.converters.sklearn.convert(model)

coreml_model.author = "Rishabh Mallela"
coreml_model.short_description = "Model does 2 stage sleep classification, between REM and nonREM"
coreml_model.input_description["input"] = "heart rate, motion, steps"
# coreml_model.output_description["prediction"] = "1 corresponding to REM sleep, 0 corresponding to nonREM sleep"

coreml_model.save('sleep_classification_gbc.mlmodel')