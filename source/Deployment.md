# [SBI - Voice Biometrics](https://www.techgig.com/hackathon/voice-biometrics)

## Scope of Work of the PoC

The POC curently is restricted to handling only 
- Enroll and Match Voice samples 
- Azure Functions for parallel processing of videos and scaling
- A TDNN classifier (xvector) and a custom model called ECAPA-TDNN from [speechbrain](https://github.com/speechbrain/speechbrain) to extract voice embeddings
- Azure Containers to store voices

Features - 
- Enroll vocies with names from a directory
- Enroll a single voice with name
- Identification of a given voice with name
- Identification of a given voice without name

Post POC Work - 
1. Train Custom Models with better domain data and voices.
2. Creating a model rather than similarity compairiosn of embeddings to filter out initial voices.

## Pre-requisites from the Bank’s side
1. Azure Account
2. Works with both CPU and GPU
3. Setup & Deployment will not require more than a week.

## Infrastructure required for setting up the PoC. 
1. The audios can be uploaded to a container storage.
2. An Azure function to deploy this code and call it using REST API's.

## Setting up the PoC infrastructure on Microsoft Azure cloud setup
1. [Creating a resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal#create-resource-groups)
2. [Creating a storage account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)
3. [Creating a container](https://docs.microsoft.com/en-us/azure/storage/blobs/blob-containers-cli#create-a-container)
4. [Creating a function app](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal#create-a-function-app)
5. [Deploy code in azure function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal#create-function)
6. [Writing scipts to download and upload images to the azure function for processing in azure](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=environment-variable-windows#upload-blobs-to-a-container)

## High level PoC Key Performance Indicators (KPIs) 
- Samples Processed are provide in the [sample_data](./sample_data/) directory and Video of execution can be found [here](https://drive.google.com/file/d/1c69mpH_fLMXZxh01kAhQWJvdAOeyKc3e/view?usp=sharing) 

- Used the best xvector model (trained on Voxceleb and stored on HuggingFace) From Speechbrian to compute voice embeddings and perform a speaker classification based on similairty scores to get a name of speaker

- Used a Connectionist Temporal Classification (CTC) which is the simplest speech recognition system available in SpeechBrain and used it pretarined models to get the images of the speaker identified from before and so a verification

- We can keep adding new voices for a given user that increases the chances of being matched thus increasing confidence score and then after we have enough samples we can train a custom classifier model.

- Using a similarity to match a audio to get recommended names and then verifying voices for those names seems a good idea since we can't do an online trainig of the model for each voice added, can be too costly.

- A custom trained model can be craeted and be used in production once we have enough samples by following the guide [here](https://colab.research.google.com/drive/1aFgzrUv3udM_gNJNUoLaHIm78QHtxdIz?usp=sharing#scrollTo=yXy6DhQmhrYA) and [here](https://colab.research.google.com/drive/1UwisnAjr8nQF3UnrkIJ4abBMAWzVwBMh?usp=sharing#scrollTo=4LnRq1_cpPXZ) depending on the cost and requirement.

## Deployment Guide
Local Deployment
- [Python](https://www.python.org/downloads/release/python-390/)
- First Run will install all the required custom models being used.
- The Credentails and keys provided with this POC will be avilable till the challenge duration
- FFMPEG will be required

```cmd
pip3 install vitualenv
virtualenv vio_bio
source "vio_bio/bin/activate"
pip3 install -r requirements.txt
python process_audio.py
```


