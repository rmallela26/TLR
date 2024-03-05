import numpy as np
import sys
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.model_selection import GridSearchCV, LeaveOneGroupOut, cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

import matplotlib.pyplot as plt
from numpy import savetxt, loadtxt

np.set_printoptions(threshold=sys.maxsize)


#CONSIDER USING A RECURRENT NEURAL NETWORK RNN TO USE DATA UP TILL THE CURRENT MOMENT TO CREATE THE PREDCITION
#THIS MIGHT MAKE THE PREDICTION MORE ACCURATE BECAUSE PREVIOUS DATA MIGHT IMPLY SOMETHING ABOUT THE CURRENT DATA

# import yasa
# import matplotlib.pyplot as plt

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
print(feature_files[0])
print(feature_files[1])
print(feature_files[2])
print(feature_files[3])
print(feature_files[4])
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
            labels.append(float(val))
        master_train_labels.append(np.array(labels))
    else: #data
        if counter == 1:
            for line in f:
                row = []
                val = line[:-1]
                row.append(float(val))
                data.append(row)
        else:
            for line in f:
                val = line[:-1]
                data[epoch].append(float(val))
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

train_data = np.array(train_data)
train_data = np.delete(train_data, 0, 1) #remove the cosine feature, proven that it isn't needed
# train_data = np.delete(train_data, 0, 1) #remove activity count
# train_data = np.delete(train_data, 2, 1) #remove the time feature, decreases accuracy, not worth it
print(np.array(train_data).shape)
print()
print()
print()

print(len(train_data))

# savetxt('test_train.csv', train_data, delimiter=',')
# savetxt('test_labels.csv', train_labels, delimiter=',')
# savetxt('test_groups.csv', groups, delimiter=',')

#######################PROBLEM: IT IS ALSO TESTING ON BALANCED DATA, THE DATA IN IMPLEMENTATION WILL NOT BE BALANCED
#NEED TO RUN LOGO MANUALLY, CAN'T USE CROSS VAL PREDICT

#oversampling
#go through each subject and undersample the data, creating the groups array as you go
# for i in range(len(master_train_data)):
#     if i == 13 or i == 19: #neither had any rem sleep
#         continue

#     #Both yield same results, oversampler takes little longer to run, but shouldn't matter in implementation
#     # smote = SMOTE(sampling_strategy='auto', random_state=42)
#     # X_resampled, y_resampled = smote.fit_resample(master_train_data[i], master_train_labels[i])

#     oversampler = RandomOverSampler()
#     X_resampled, y_resampled = oversampler.fit_resample(master_train_data[i], master_train_labels[i])

#     # undersampler = RandomUnderSampler()
#     # X_resampled, y_resampled = undersampler.fit_resample(master_train_data[i], master_train_labels[i])
    
#     print(len(y_resampled), len(master_train_labels[i]))
#     for j in range(len(y_resampled)):
        
#         groups.append(group_num)
#         train_data.append(X_resampled[j])
#         train_labels.append(y_resampled[j])
#     group_num += 1



#add an SVC
#when hyperparameter optimizing SVC see how to add visualizations
# svc = svm.SVC(probability=True)

###############IDEA: I can use both mlpc2 and knn to make identifying non rem sleep better. I would then need to mess with
#the probability thresholds to know which to listen to when one says rem other says non rem

rfc = RandomForestClassifier(max_depth=20, random_state=0, n_estimators=1000, min_samples_leaf=32)

# mlpc2 = MLPClassifier(activation='logistic', hidden_layer_sizes=(15, 15, 15),
#                                                           max_iter=2000, alpha=0.01, solver='adam', verbose=False,
#                                                           n_iter_no_change=20, shuffle=True)

# mlpc = MLPClassifier(activation='relu', hidden_layer_sizes=(20, 20, 20),
#                                                           max_iter=2000, alpha=0.1, solver='sgd', verbose=False,
#                                                           n_iter_no_change=20, shuffle=True)

# knn = KNeighborsClassifier(weights='distance')

gbc = GradientBoostingClassifier(n_estimators=100, max_depth=3)
logo = LeaveOneGroupOut()
predictions = cross_val_predict(gbc, train_data, train_labels, groups=groups, cv=logo, verbose=2, n_jobs=-1)
print(accuracy_score(train_labels, predictions))


# #hyperparameter optimization 
# mlp = MLPClassifier(max_iter=2000, n_iter_no_change=20)

#rfc parameter grid
param_grid = {
    'max_depth': [None, 10, 20, 30, 50],
    'random_state': [None, 0],
    'n_estimators': [100, 500, 1000, 1200],
    'min_samples_leaf': [1, 16, 32, 48]
}
logo = LeaveOneGroupOut()
grid_search = GridSearchCV(rfc, param_grid, cv=logo.split(train_data, train_labels, groups=groups), verbose=2, n_jobs=-1)
grid_search.fit(train_data, train_labels, groups=groups)

# Print the best hyperparameters and corresponding accuracy
print("Best Hyperparameters: ", grid_search.best_params_)
print("Best Accuracy: ", grid_search.best_score_)

# Get the predictions on the test data using the best model
best_model = grid_search.best_estimator_
predictions = best_model.predict(train_data)

# Calculate the accuracy of the best model on the test data
accuracy = accuracy_score(train_labels, predictions)
print("Accuracy on Test Data: ", accuracy)

###################for plotting heatmap
# Extract results
mean_test_scores = grid_search.cv_results_['mean_test_score']
params = grid_search.cv_results_['params']

# Extract hyperparameters and their corresponding scores
param_names = list(param_grid.keys())
param_values = [list(params[i].values()) for i in range(len(params))]

# Create a grid of mean test scores
scores_grid = np.array(mean_test_scores).reshape(len(param_values), -1)

# Plot heatmap
plt.figure(figsize=(10, 6))
plt.imshow(scores_grid, cmap='viridis')
plt.colorbar()
plt.xticks(np.arange(len(param_names)), param_names, rotation=45)
plt.yticks(np.arange(len(param_values)), param_values)
plt.xlabel('Hyperparameters')
plt.ylabel('Parameter Values')
plt.title('Grid Search Results')
plt.show()
path = "rfc_heatmap"
plt.savefig(path)

# logo = LeaveOneGroupOut()
# predictions = cross_val_predict(gbc, train_data, train_labels, groups=groups, cv=logo, verbose=2, n_jobs=-1, method='predict')
# # print(predictions[0:1000])
# # print(len(predictions))


#using probabilities, change the thresholds to get optimal values
logo = LeaveOneGroupOut()
probabilities = cross_val_predict(rfc, train_data, train_labels, groups=groups, cv=logo, verbose=2, n_jobs=-1, method='predict_proba')
# #IDEA:
# #If the classifier thinks it is stage 2, and the second highest probability is stage 5, guess stage 5
# #if the stage 5 probability is at least 0.30

#manipulate probability thresholds
#if max probability is N2 and it is above 0.55, no matter the rem probabiltiy, keep it as 0.54
###################IDEA: If i just guessed that it is rem, boost the next probability by something like 0.05 since all
#rems are almost always in batches
new_predictions = np.zeros(len(probabilities))
for i in range(len(probabilities)):
    arr = np.sort(probabilities[i])
    if arr[3] == probabilities[i][1]: #max probability is N2
        if arr[2] == probabilities[i][3] and probabilities[i][1]: #second largest probability is rem and it is less than 0.55 probability
            if arr[2] >= 0.24:
                new_predictions[i] = 1
            else:
                new_predictions[i] = 0
        else: new_predictions[i] = 0
    elif arr[3] == probabilities[i][3]:
        new_predictions[i] = 1
    else:
        new_predictions[i] = 0

#replace all predictions with new_predictions
arr = np.zeros(len(new_predictions))
for i in range(len(arr)):
    if train_labels[i] == 1 or train_labels[i] == 2 or train_labels[i] == 3:
        arr[i] = 0
    else:
        arr[i] = 1

for i in range(1000):
    #print probabilities, prediction made, correct answer, and whether the prediction wass correct
    # print(probabilities[i], predictions[i], train_labels[i], predictions[i] == train_labels[i])
    # if (train_labels[i] == 5 and predictions[i] == 1) or (train_labels[i] != 5 and predictions[i] == 0):
    #     correct = True
    # else: correct = False
    print(probabilities[i], np.argmax(probabilities[i]), train_labels[i], new_predictions[i] == arr[i])

# for i in range(len(arr)):
#     if predictions[i] == 1 or predictions[i] == 2 or predictions[i] == 3:
#         predictions[i] = 0
#     else:
#         predictions[i] = 1

#print metrics
# print(predictions[0:1000])
# for i in range(1000):
#     #print probabilities, prediction made, correct answer, and whether the prediction wass correct
#     print(probabilities[i], train_labels[i], new_predictions[i], new_predictions[i] == arr[i])
#     # print(probabilities[i], train_labels[i], new_predictions[i])
accuracy = accuracy_score(arr, new_predictions)
precision = precision_score(arr, new_predictions, pos_label=1) #out of all the times it says it's rem, how many times is it actually rem
recall = recall_score(arr, new_predictions, pos_label=1) #out of all the times it is rem, how many times is it saying it is rem
#we want high recall, at the cost of low precision
print(accuracy)
print(precision)
print(recall)

print()
print()


accuracies = []
precisions = []
recalls = []

for g in np.unique(groups):
    indx = (groups == g)

    acc = accuracy_score(arr[indx], new_predictions[indx])
    accuracies.append(acc)

    prec = precision_score(arr[indx], new_predictions[indx], pos_label=1)
    precisions.append(prec)

    rec = recall_score(arr[indx], new_predictions[indx], pos_label=1)
    recalls.append(rec)

accuracies = np.array(accuracies)
mean_accuracy = accuracies.mean()
accuracy_error = accuracies.std()
print(mean_accuracy)
print(np.mean(precisions))
print(np.mean(recalls))

print()
print(accuracies)

categories = ['Average Accuracy']  # Categories or labels for the bars
accuracy_means = [mean_accuracy]  # Average accuracy values
accuracy_errors = [accuracy_error]  # Error values for each category

# Set the y-axis limit to 1
plt.ylim(0, 1)

# Plot the bar graph
plt.bar(categories, accuracy_means, yerr=accuracy_errors, capsize=4)

# Set labels and title
plt.xlabel('Categories')
plt.ylabel('Accuracy')
plt.title('Average Accuracy with Error Bars')

save_path = 'gbc_bar_graph.png'
# plt.savefig(save_path)

# Show the plot
plt.show()





#print the confusion matrix
# cm = confusion_matrix(arr, new_predictions)
# fig, ax = plt.subplots()
# im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
# classes = ['0', '1']  # Class labels
# ax.set(xticks=np.arange(cm.shape[1]),
#        yticks=np.arange(cm.shape[0]),
#        xticklabels=classes, yticklabels=classes,
#        title='Confusion Matrix',
#        ylabel='True label',
#        xlabel='Predicted label')

# plt.show()

def plot_normalized_confusion_matrix(confusion_matrix, classes, save_path):
    # Normalize the confusion matrix
    row_sums = confusion_matrix.sum(axis=1)
    normalized_matrix = confusion_matrix / row_sums[:, np.newaxis]

    # Create the figure and axis
    fig, ax = plt.subplots()
    
    # Plot the normalized confusion matrix
    im = ax.imshow(normalized_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    
    # Set axis labels and tick labels
    ax.set(xticks=np.arange(normalized_matrix.shape[1]),
           yticks=np.arange(normalized_matrix.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title='Normalized Confusion Matrix',
           ylabel='True label',
           xlabel='Predicted label')

    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)

    # Save the plot as an image file
    # plt.savefig(save_path)

    # Show the plot
    plt.show()

cm = confusion_matrix(arr, new_predictions)
classes = ['0', '1']  # Class labels

save_path = 'gbc_confusion_matrix.png' #where the matrix will be saved

# Plot the normalized confusion matrix
plot_normalized_confusion_matrix(cm, classes, save_path)






# """
# train model on each subject, one after the other, except for last subject
# Can't train on all but one at the same time because the data array for the whole thing isn't homogenous
# """
# lr = LogisticRegression(penalty='l1', solver='liblinear', verbose=0, warm_start=False)
# rfc = RandomForestClassifier(max_depth=20, random_state=0, warm_start=False, n_estimators=1000, min_samples_leaf=32)
# knn = KNeighborsClassifier(weights='distance')
# mlpc = MLPClassifier(activation='relu', hidden_layer_sizes=(15, 15, 15),
#                                                           max_iter=2000, alpha=0.01, solver='adam', verbose=False,
#                                                           n_iter_no_change=20)

# mlpc2 = MLPClassifier(activation='logistic', hidden_layer_sizes=(15, 15, 15),
#                                                           max_iter=2000, alpha=0.01, solver='adam', verbose=False,
#                                                           n_iter_no_change=20)

#use for real time predictions, predicts the same values as if all data were present at once 
# predicts = []
# for data in v2_test_data:
#     predicts.append(mlpc2.predict([data]))

# predicts = np.array(predicts)
# predicts = predicts.flatten()
# print(predicts[0:500])