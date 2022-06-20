import os
import glob
from azure.storage.blob import BlobServiceClient, BlobClient
from azurebatchload import Download
import json

with open('config.json','r') as f:
    config = json.load(f)

blob_service_client = BlobServiceClient.from_connection_string(config['connect_str'])

os.environ["AZURE_STORAGE_CONNECTION_STRING"] = config['connect_str']

def upload_blob(local_file_path,speaker=None):
    local_file_name = local_file_path.split(os.sep)[-1]
    if speaker:
        upload_file_path = f"{speaker}/{local_file_name}"
    else:
        upload_file_path = local_file_name

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=config['container_name'], blob=upload_file_path)
    # print("\nUploading to Azure Storage as blob:\n\t" + upload_file_path)
    # Upload the created file
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data,overwrite=True)
    # print("File Uploaded Successfully!")

def download_blob():
    download_file_path = '../pretrained_models/embeddings.pickle'
    download_file_name = 'embeddings.pickle'
    blob = BlobClient.from_connection_string(conn_str=config['connect_str'], container_name=config['container_name'], blob_name=download_file_name)
    exists = blob.exists()
    print(exists)
    if exists:
        blob_client = blob_service_client.get_container_client(container= config['container_name']) 
        print("\nDownloading blob to \n\t" + download_file_path)
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob(download_file_name).readall())
        return download_file_path
    else:
        return None

def download_files_from_folder(speaker): 
    try:
        Download(
            destination=f"../Audio/",
            source= config['container_name'],
            folder=f"{speaker}",
            extension='.wav',
            method='single'
            ).download()
        return f"../Audio/{speaker}"
    except Exception as e:
        print(str(e))
        print("Unable to create audio files")

def clean_temp_audios(path='.',rmv_dir=False):
    print("Cleaning audio files")
    types = (
        glob.glob(f"{path}/**/*.mp3", recursive=True), 
        glob.glob(f"{path}/**/*.flac", recursive=True),
        glob.glob(f"{path}/**/*.wav", recursive=True)
    ) # the tuple of file types

    files_grabbed = []
    for files in types:
        files_grabbed.extend(files)

    for pa in files_grabbed:
        # print(pa)
        os.remove(pa)
    if rmv_dir:
        for pa in glob.glob(f"{path}/*/",recursive=True):
            # print()
            os.rmdir(pa)