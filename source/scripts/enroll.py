import torchaudio
from speechbrain.pretrained import EncoderClassifier
from pydub import AudioSegment
from utility import clean_temp_audios
from utility import upload_blob,download_blob
import pickle
import uuid
import glob
import os

def enroll(speaker,audio_path,audio_file_name):
    """Enroll a user with an audio file
        inputs: str (Name of the person to be enrolled and registered)
                str (Path to the audio file of the person to enroll)
        outputs: None"""
    if speaker:
        new_ebm = {}
        try:
            classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-xvect-voxceleb", savedir="../pretrained_models/spkrec-xvect-voxceleb")
        except:
            print("Failed to model weights ")
            return f"Failed: {str(e)}"
        try:
            print("Processing enroll sample....")
            sound = AudioSegment.from_file(audio_path)
            sound = sound.set_channels(1)
            sound.export(audio_file_name, format="wav")
            signal, rate_of_sample = torchaudio.load(audio_file_name)
            embeddings = classifier.encode_batch(signal)
            embeddings = embeddings.flatten() 
            new_ebm[speaker] = [embeddings]
        except Exception as e:
            print("Error processing the input audio file. Make sure the path.")
            print(str(e))
            return f"Failed: {str(e)}"
        try:
            print("Uploading Sample for the user to register")
            # upload to bucket
            upload_blob(audio_file_name,speaker)
            print("Succesfully enrolled the user")
        except Exception as e:
            print(str(e))
            print("Unable to save the user into the database.")
            return f"Failed: {str(e)}"
        try:
            print("Re-creating the authentication embedding")
            embeddings_path  = download_blob()
            if embeddings_path:
                # embeddings exists
                with open(embeddings_path, 'rb') as handle:
                    embeddings_data = pickle.load(handle)
                print(f"embedding length- {len(embeddings_data)}")
                if speaker in embeddings_data:
                    embeddings_data[speaker].append(embeddings)
                else:
                    embeddings_data.update(new_ebm)
                with open(embeddings_path, 'wb') as handle:
                    pickle.dump(embeddings_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                # no embeddings exists (First registration)
                with open('../pretrained_models/embeddings.pickle', 'wb') as handle:
                    pickle.dump(new_ebm, handle, protocol=pickle.HIGHEST_PROTOCOL)

            print(f"Downloaded:{embeddings_path}")
            upload_blob("../pretrained_models/embeddings.pickle")
            print("Succesfully created the new embedding")
           
        except Exception as e:
            print(str(e))
            print("Unable to create the new embedding.")
        clean_temp_audios(path='../Audio',rmv_dir=True)
    else:
        print(f"Failed: Please give the name for the voice to register")
        

def enroll_all(dir_path):
    """Enroll a user with an audio file
        inputs: str (Name of the person to be enrolled and registered)
                str (Path to the audio file of the person to enroll)
        outputs: None"""
    
    classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-xvect-voxceleb", savedir="../pretrained_models/spkrec-xvect-voxceleb")
    new_ebm = {}
    print("Grabing All Files")
    types = (
        glob.glob(f"{dir_path}/**/*.mp3", recursive=True), 
        glob.glob(f"{dir_path}/**/*.flac", recursive=True),
        glob.glob(f"{dir_path}/**/*.wav", recursive=True)
    ) # the tuple of file types

    files_grabbed = []
    for files in types:
        files_grabbed.extend(files)
    print("No of audio samples",len(files_grabbed))
    
    for audio_path in files_grabbed:
        speaker = audio_path.split(os.sep)[-2].lower()
        print(speaker)
        if not os.path.exists(f"../Audio/{speaker}/"):
            os.mkdir(f"../Audio/{speaker}/")
        audio_file_name = f"../Audio/{speaker}/{speaker}-{str(uuid.uuid4())}.wav"
        sound = AudioSegment.from_file(audio_path)
        sound = sound.set_channels(1)
        sound.export(audio_file_name, format="wav")
        signal, rate_of_sample = torchaudio.load(audio_file_name)
        embeddings = classifier.encode_batch(signal)
        embeddings = embeddings.flatten() 
        if speaker in new_ebm:
             new_ebm[speaker].append(embeddings)
        else:
            new_ebm[speaker] = [embeddings]
        upload_blob(audio_file_name,speaker)
    
    
    if len(new_ebm) > 0:
        print("Re-creating the authentication embedding")
        embeddings_path  = download_blob()
        if embeddings_path:
            # embeddings exists
            with open(embeddings_path, 'rb') as handle:
                embeddings_data = pickle.load(handle)
            print(f"embedding length- {len(embeddings_data)}")
            for key,emb in new_ebm.items():
                if key in embeddings_data:
                    embeddings_data[key].extend(emb)
                else:
                    embeddings_data.update({key:emb})
            with open(embeddings_path, 'wb') as handle:
                pickle.dump(embeddings_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            # no embeddings exists (First registration)
            with open('../pretrained_models/embeddings.pickle', 'wb') as handle:
                pickle.dump(new_ebm, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print(f"Downloaded:{embeddings_path}")
        upload_blob("../pretrained_models/embeddings.pickle")
        print("Succesfully created the new embedding")
    else:
        print("No audio found in path")
    clean_temp_audios(path='../Audio',rmv_dir=True)