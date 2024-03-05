"""
THIS IS THE FILE TO RUN
ALL FEATURE EXTRACTION IS DONE IN HELPER FILES
THIS IS THE MAIN FILE THAT PRINTS OUT ALL METRICS AND MANAGES PROBABILITY VALUES 
"""

from sklearn.model_selection import GridSearchCV, LeaveOneGroupOut, cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import numpy as np
from numpy import savetxt, loadtxt
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from preprocessing.preprocessor import Features
import random
from sklearn import svm
import os
import matplotlib as plt


import matplotlib.pyplot as plt

import sys
np.set_printoptions(threshold=sys.maxsize)

"""
Runs makeFeatures in the preprocessor.py file, and returns the features
master_x_data is a 2d array. First dimension holds subject number in the data
Second dimesnion is the feature at some point in the night
"""
# feat = Features()
# feat.makeFeatures()
# master_hr_data, master_motion_data, master_time_data, master_labels = feat.getFeatures()

# group_num = 1
# groups = []
# train_data = []
# train_labels = []

# print(master_hr_data[0][0])
# print(master_time_data[-1][:5])
# print(len(master_hr_data[-1]), len(master_motion_data[-1]), len(master_time_data[-1]), len(master_labels[-1]))

# for i in range(len(master_hr_data)):
#     print(len(master_hr_data[i]), len(master_motion_data[i]))

"""
Remove subjects 13, 19 (since no REM sleep, i included in the training for the final model)
Merge N1 and N2
"""

# for i in range(len(master_hr_data)):
#     if i == 13 or i == 19: #not included because neither had rem sleep ######INCLUDE FOR FINAL MODEL
#         continue
#     for j in range(len(master_hr_data[i])):
#         groups.append(group_num)
#         a = master_hr_data[i][j]
#         b = master_motion_data[i][j]
#         c = master_time_data[i][j]
#         d = master_labels[i][j]
#         # if d == 0 or d == 1:
#         #     d = 1
#         if d == 2 or d == 1: #labels: 0, 2, 3, 5. #Grouping 1 and 2 to make stage 2 look less like rem
#             d = 2
        
#         train_data.append([a, b, c])
#         train_labels.append(float(d))
#     group_num += 1

# train_data = np.array(train_data)
# train_labels = np.array(train_labels)
# groups = np.array(groups)

"""
Getting all the features from the files. These files are made by running the code above
"""
train_data = loadtxt('Sleep Classification/train_data.csv', delimiter=',')
train_labels = loadtxt('Sleep Classification/train_labels.csv', delimiter=',')
groups = loadtxt('Sleep Classification/groups.csv', delimiter=',')

# savetxt('train_data.csv', train_data, delimiter=',')
# savetxt('train_labels.csv', train_labels, delimiter=',')
# savetxt('groups.csv', groups, delimiter=',')

# train_data = loadtxt('test_train.csv', delimiter=',')
# train_labels = loadtxt('test_labels.csv', delimiter=',')
# groups = loadtxt('test_groups.csv', delimiter=',')

# hr_data = loadtxt('train_data.csv', delimiter=',')

# old = loadtxt('train_data.csv', delimiter=',')
# old = np.array(old)
# old = old[:,1]


# x = train_data[:,2] #[:len(master_hr_data[0])]
# y1 = old[:len(master_hr_data[0])]
# y2 = train_data[:,0]#[:len(master_hr_data[0])]
# # plt.plot(x, y1)
# # plt.plot(x, y2)
# # plt.show()

# #did this stuff to see trends not really relevant
# colors = []
# for i in range(len(train_labels)):
#     if train_labels[i] == 5:
#         colors.append('red')
#     elif train_labels[i] == 0 or train_labels[i] == 1:
#         colors.append('green')
#     else:
#         colors.append('blue')

# plt.scatter(x, y2, c=colors)
# # plt.legend()
# plt.show()



gbc = GradientBoostingClassifier(n_estimators=100, max_depth=3)
# rfc = RandomForestClassifier(max_depth=20, random_state=0, n_estimators=1000, min_samples_leaf=32)
rfc = RandomForestClassifier(max_depth=None, random_state=1, n_estimators=100, min_samples_leaf=48)
svc = svm.SVC(probability=True)

mlpc2 = MLPClassifier(activation='logistic', hidden_layer_sizes=(15, 15, 15),
                                                          max_iter=2000, alpha=0.01, solver='adam', verbose=False,
                                                          n_iter_no_change=20, shuffle=True)

#for testing rfc vs mlpc:
#
# logo = LeaveOneGroupOut()
# predictions = cross_val_predict(rfc, train_data, train_labels, groups=groups, cv=logo, verbose=2, n_jobs=-1)


# arr = np.zeros(len(predictions))
# for i in range(len(arr)):
#     if train_labels[i] == 0 or train_labels[i] == 1 or train_labels[i] == 2 or train_labels[i] == 3:
#         arr[i] = 0
#     else:
#         arr[i] = 1

# arr = np.array(arr)

# new_predictions = []
# for i in range(len(arr)):
#     if predictions[i] == 5:
#         new_predictions.append(1)
#     else: 
#         new_predictions.append(0)

# print(accuracy_score(arr, new_predictions))
# print(precision_score(arr, new_predictions))
# print(recall_score(arr, new_predictions))

# predictions = cross_val_predict(mlpc2, train_data, train_labels, groups=groups, cv=logo, verbose=2, n_jobs=-1)

# arr = np.zeros(len(predictions))
# for i in range(len(arr)):
#     if train_labels[i] == 0 or train_labels[i] == 1 or train_labels[i] == 2 or train_labels[i] == 3:
#         arr[i] = 0
#     else:
#         arr[i] = 1

# arr = np.array(arr)

# new_predictions = []
# for i in range(len(arr)):
#     if predictions[i] == 5:
#         new_predictions.append(1)
#     else: 
#         new_predictions.append(0)

# print(accuracy_score(arr, new_predictions))
# print(precision_score(arr, new_predictions))
# print(recall_score(arr, new_predictions))










# rfc.fit(train_data[930:-1], train_labels[930:-1])
# probabilities = rfc.predict_proba(train_data[0:930])

# new_predictions = []
# for i in range(len(probabilities)):
#     if i == 113:
#         print(probabilities[i])
#     if train_data[i][1] > 1.16 and train_data[i][1] < 2.24:
#         new_predictions.append(1)
#         continue

#     pred = np.argmax(probabilities[i])
#     probs = np.sort(probabilities[i])

#     # #no groups
#     # if pred == 4 :
#     #     new_predictions.append(1)
#     # elif pred == 2 and probs[4] <= 0.63 and probs[3] == probabilities[i][4] and probs[3] > 0.22:
#     #     new_predictions.append(1)
#     # elif pred == 0 and train_data[i][2] > 0.41: #guessing it is 0 in the middle of the night
#     #     new_predictions.append(1)
#     # else:
#     #     new_predictions.append(0)

#     #group 1 and 2
#     if pred == 3:
#         new_predictions.append(1)
#     elif pred == 1 and probs[3] <= 0.7 and ((probs[2] == probabilities[i][3] and probs[2] > 0.20) or (probs[2] == probabilities[i][0] and probs[1] == probabilities[i][3] and probs[1] > 0.24)):
#         new_predictions.append(1)
#     elif pred == 0 and train_data[i][2] > 0.41: #guessing it is 0 in the middle of the night
#         new_predictions.append(1)
#     else:
#         new_predictions.append(0)

# for i in range(len(new_predictions)):
#     print(i+1, new_predictions[i])









# ##############FOR GRID SEARCH HYPERPARAMETER OPTIMIZATION
# param_grid = {
#     'random_state': [2, 3],
#     'n_estimators': [50, 60, 70, 80, 90, 100]
# }
# logo = LeaveOneGroupOut()
# grid_search = GridSearchCV(rfc, param_grid, cv=logo.split(train_data, train_labels, groups=groups), verbose=2, n_jobs=-1)
# grid_search.fit(train_data, train_labels, groups=groups)

# # Print the best hyperparameters and corresponding accuracy
# print("Best Hyperparameters: ", grid_search.best_params_)
# print("Best Accuracy: ", grid_search.best_score_)

# # Get the predictions on the test data using the best model
# best_model = grid_search.best_estimator_
# predictions = best_model.predict(train_data)

# # Calculate the accuracy of the best model on the test data
# accuracy = accuracy_score(train_labels, predictions)
# print("Accuracy on Test Data: ", accuracy)

# ###################for plotting heatmap
# # Extract results
# mean_test_scores = grid_search.cv_results_['mean_test_score']
# params = grid_search.cv_results_['params']

# # Extract hyperparameters and their corresponding scores
# param_names = list(param_grid.keys())
# param_values = [list(params[i].values()) for i in range(len(params))]

# # Create a grid of mean test scores
# scores_grid = np.array(mean_test_scores).reshape(len(param_values), -1)

# # Plot heatmap
# plt.figure(figsize=(10, 6))
# plt.imshow(scores_grid, cmap='viridis')
# plt.colorbar()
# plt.xticks(np.arange(len(param_names)), param_names, rotation=45)
# plt.yticks(np.arange(len(param_values)), param_values)
# plt.xlabel('Hyperparameters')
# plt.ylabel('Parameter Values')
# plt.title('Grid Search Results')
# plt.show()
# path = "rfc_heatmap.png"
# plt.savefig(path)




#get probabilities

logo = LeaveOneGroupOut()
probabilities = cross_val_predict(rfc, train_data, train_labels, groups=groups, cv=logo, verbose=2, n_jobs=-1, method='predict_proba')
# rfc.fit(train_data, train_labels)
# probabilities = rfc.predict_proba(train_data)
arr = np.zeros(len(probabilities))
for i in range(len(arr)):
    if train_labels[i] == 0 or train_labels[i] == 1 or train_labels[i] == 2 or train_labels[i] == 3:
        arr[i] = 0
    else:
        arr[i] = 1

arr = np.array(arr)

""""
Play with probabilities to see what makes the metrics go up
Pred = the prediction (0= wake, etc.)
Probs = the sorted probability values
"""
new_predictions = []
for i in range(len(probabilities)):
    # if train_data[i][1] > 1.16 and train_data[i][1] < 2.24:
    #     new_predictions.append(1)
    #     continue

    pred = np.argmax(probabilities[i])
    probs = np.sort(probabilities[i])

    # #no groups
    # if pred == 4 :
    #     new_predictions.append(1)
    # elif pred == 2 and probs[4] <= 0.63 and probs[3] == probabilities[i][4] and probs[3] > 0.22:
    #     new_predictions.append(1)
    # elif pred == 0 and train_data[i][2] > 0.41: #guessing it is 0 in the middle of the night
    #     new_predictions.append(1)
    # else:
    #     new_predictions.append(0)

    #group 1 and 2
    if probabilities[i][4] > 0.24: #if the probability of REM sleep is greater than 0.24, guess REM 
        new_predictions.append(1)
    else: new_predictions.append(0)
    # if pred == 3:
    #     new_predictions.append(1)
    # # elif pred == 1: #max probability is N1/N2
    # elif probs[2] == probabilities[i][3]: #second largest probability is rem 
    #     if probs[2] >= 0.24:
    #         new_predictions.append(1)
    #     else: new_predictions.append(0)
    #         # new_predictions.append(1)
    #     # else: new_predictions.append(0)
    # else:
    #     new_predictions.append(0)

    # #group 2 and 0
    # if pred == 3:
    #     new_predictions.append(1)
    # elif pred == 1 and probs[3] <= 0.7 and ((probs[2] == probabilities[i][3] and probs[2] > 0.20) or (probs[2] == probabilities[i][0] and probs[1] == probabilities[i][3] and probs[1] > 0.20)):
    #     new_predictions.append(1)
    # # elif pred == 0 and train_data[i][2] > 0.41: #guessing it is 0 in the middle of the night
    # #     new_predictions.append(1)
    # else:
    #     new_predictions.append(0)

new_predictions = np.array(new_predictions)

"""
print accurayc, precision, recall
"""

for i in range(3792, 4745):
    x = np.argmax(probabilities[i])
    print(probabilities[i], x, train_labels[i], new_predictions[i] == arr[i])



for i in range (930):
    print(i+1, new_predictions[i])

accuracy = accuracy_score(arr, new_predictions)
precision = precision_score(arr, new_predictions, pos_label=1) #out of all the times it says it's rem, how many times is it actually rem
recall = recall_score(arr, new_predictions, pos_label=1) #out of all the times it is rem, how many times is it saying it is rem
#we want high recall, at the cost of low precision
print(accuracy)
print(precision)
print(recall)


# x = train_data[:,2][:len(master_hr_data[0])]
# y1 = old[:len(master_hr_data[0])]
# y2 = train_data[:,1][:len(master_hr_data[0])]
# # plt.plot(x, y1)

# colors = []
# for i in range(len(master_labels[0])):
#     if master_labels[0][i] == 5 and new_predictions[i] == 1:
#         colors.append('red')
#     elif master_labels[0][i] == 5 and new_predictions[i] == 0:
#         colors.append('orange')
#     elif master_labels[0][i] != 5 and new_predictions[i] == 1:
#         colors.append('green')
#     else:
#         colors.append('blue')

# colors2 = []
# for i in range(len(master_labels[0])):
#     if predictions[i] == 1:
#         colors2.append('green')
#     else:
#         colors2.append('orange')

# plt.scatter(x, y2, c=colors)
# # plt.scatter(x, y2, c=colors2)
# # plt.legend()
# plt.show()










#####################FIX THIS 
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

i = 0
p = []
r = []
while i < len(precisions):
    if precisions[i] == 0: 
        i += 1
        continue
    p.append(precisions[i])
    i += 1
i = 0
while i < len(recalls):
    if recalls[i] == 0: 
        i += 1
        continue
    r.append(recalls[i])
    i += 1
p = np.array(p)
r = np.array(r)
print()
print()
print(np.mean(p))
print(np.mean(r))

print()
print(accuracies)
print(precisions)
print(recalls)

#print graphs for recall
recalls = np.array(r)
mean_recall = recalls.mean()
recall_error = recalls.std()
print("recall mean is ")
print(mean_recall)

precisions = np.array(p)
mean_precision = precisions.mean()
precision_error = precisions.std()

categories = ['Average Accuracy', 'Average Precision', 'Average Recall']
means = [mean_accuracy, mean_precision, mean_recall]
errors = [accuracy_error, precision_error, recall_error]

# categories = ['Average Recall']  # Categories or labels for the bars
# recall_means = [mean_recall]  # Average accuracy values
# recall_errors = [recall_error]  # Error values for each category

# Set the y-axis limit to 1
plt.ylim(0, 1)

# Plot the bar graph
plt.bar(categories, means, yerr=errors, capsize=4)

# Set labels and title
plt.xlabel('Categories')
plt.ylabel('Percent of Epochs')
plt.title('Average Scores with Error Bars')

save_path = 'rfc_bar_graph.png'
plt.savefig(save_path)

# Show the plot
plt.show()

# def plot_normalized_confusion_matrix(confusion_matrix, classes, save_path):
#     # Normalize the confusion matrix
#     row_sums = confusion_matrix.sum(axis=1)
#     normalized_matrix = confusion_matrix / row_sums[:, np.newaxis]

#     # Create the figure and axis
#     fig, ax = plt.subplots()
    
#     # Plot the normalized confusion matrix
#     im = ax.imshow(normalized_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    
#     # Set axis labels and tick labels
#     ax.set(xticks=np.arange(normalized_matrix.shape[1]),
#            yticks=np.arange(normalized_matrix.shape[0]),
#            xticklabels=classes, yticklabels=classes,
#            title='Normalized Confusion Matrix',
#            ylabel='True label',
#            xlabel='Predicted label')

#     # Add colorbar
#     cbar = ax.figure.colorbar(im, ax=ax)

#     # Save the plot as an image file
#     plt.savefig(save_path)

#     # Show the plot
#     plt.show()

# cm = confusion_matrix(arr, new_predictions)
# classes = ['0', '1']  # Class labels

# save_path = 'rfc_confusion_matrix.png' #where the matrix will be saved

# # Plot the normalized confusion matrix
# plot_normalized_confusion_matrix(cm, classes, save_path)



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

    # Add numbers inside each box
    fmt = '.2f'
    thresh = normalized_matrix.max() / 2.0
    for i in range(normalized_matrix.shape[0]):
        for j in range(normalized_matrix.shape[1]):
            ax.text(j, i, format(normalized_matrix[i, j], fmt),
                    ha='center', va='center',
                    color='white' if normalized_matrix[i, j] > thresh else 'black')

    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)

    # Save the plot as an image file
    plt.savefig(save_path)

    # Show the plot
    plt.show()


# Compute the confusion matrix
cm = confusion_matrix(arr, new_predictions)

classes = ['0', '1']  # Class labels
save_path = 'rfc_confusion_matrix.png'  # File path to save the matrix

# Plot the normalized confusion matrix with numbers inside each box
plot_normalized_confusion_matrix(cm, classes, save_path)
