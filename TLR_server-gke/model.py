#train model here and save the trained model in a file

from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd
import numpy as np
from numpy import loadtxt

model = RandomForestClassifier(max_depth=None, random_state=1, n_estimators=100, min_samples_leaf=48)
td_path = '/home/rishabh_mallela/helloworld-gke/train_data.csv'
tl_path = '/home/rishabh_mallela/helloworld-gke/train_labels.csv'
train_data = loadtxt(td_path, delimiter=',')
train_labels = loadtxt(tl_path, delimiter=',')

model.fit(train_data, train_labels)

filename = 'random_forest.sav'
pickle.dump(model, open(filename, 'wb'))