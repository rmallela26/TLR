# TLR_app
Targeted Lucidity Reactivation in an iOS/watchOS app

This repository includes the code for the iOS/watchOS application, and the code for the server used for data processing. All code relating to the classifier used to sleep stage is included in the server section. The paper associated with this work is available here [link]

## iOS/watchOS app
You can download the app (Dream Sage) as is from the App Store. To customize the app, download the files from the repository and open them in Xcode. To test the app, you can use the simulator, but if you want to test it on a physical device, you might get an error if you don't have an Apple Developer account. 

Note that you might need to change a few things in the code such as filepaths and the IP address for your server (if you create a different one). 

## Server
To create your own server, you will need to use Google Cloud Services. You may want to do this if you want to run an experiemnt yourself with this app. This application uses a Google Kubernetes Engine (https://cloud.google.com/kubernetes-engine?hl=en). To create your server, follow these directions: https://cloud.google.com/kubernetes-engine/docs/deploy-app-cluster. All files that need to be created (as described in the tutorial) are already created and are in the server folder in this repo. You only need to modify things like cluster location, server name, etc. Once you create the server, get the IP address and modify the link in the iOS/watchOS app in ServerCommunication file so that post requests are sent to your server. 

## Classifier
To modify the classifier, download the server folder. The main file that runs the classifier is processing.py. The specifications of the classifier are located in model.py. This is also where the classifier is trained. 
