
from scipy.spatial.distance import  euclidean
import torchaudio
from speechbrain.pretrained import EncoderClassifier
from pydub import AudioSegment
from utility import download_blob,download_files_from_folder
import pickle
from speechbrain.pretrained import SpeakerRecognition
import glob
import os
from utility import clean_temp_audios


def get_score_from_audio_matching(speaker,verification,audio_file_name):
    root = download_files_from_folder(speaker)
    print(f"root:{root}")
    max_score = -1
    for path in glob.glob(f"{root}/*.wav"):
        # print(path)
        score, prediction = verification.verify_files(audio_file_name, path)
        # print(f"{prediction,score}")
        prediction = bool(prediction[0]) 
        score = float(score[0])
        if prediction == True and score > max_score:
            max_score = score
        os.remove(path)
    return max_score
    

def recognize(speaker,audio_file_name):
    """Recognize the input audio file by comparing to saved users' voice prints
        inputs: str (Path to audio file of unknown person to recognize)
        outputs: matched: bool (True or False)
                 score: flaot(matched score)
    """
    # two scores - one distance and another the model scoring
    try:
        classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-xvect-voxceleb", savedir="../pretrained_models/spkrec-xvect-voxceleb")
        verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="../pretrained_models/spkrec-ecapa-voxceleb")
    except Exception as e:
        print("Failed to model weights ")
        return f"Failed: {str(e)}"
    
    print("Processing enroll sample....")
    sound = AudioSegment.from_file(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")
    signal, rate_of_sample = torchaudio.load(audio_file_name)
    embeddings = classifier.encode_batch(signal)
    embeddings = embeddings.flatten() 
    
    print("Downloading the latest Embedding!")
    embeddings_path  = download_blob()
    with open(embeddings_path, 'rb') as handle:
        test_embs = pickle.load(handle)
    
    print("Comparing sample against enrolled samples....")
    distances = {}
    for key,embs in test_embs.items():
        for emb in embs:
            distance = euclidean(emb, embeddings)
            if key in distances:
                if distance < distances[key]:
                    distances.update({key:distance})
            else:
                distances.update({key:distance})
    min_dist_speaker = min(distances, key=distances.get)
    min_dist_score = distances[min_dist_speaker]
    print("DISTANCE SIMILARITY SCORE(MIN BETTER) : ",f"{min_dist_speaker,min_dist_score}")
    print("Comparing sample voice against matched name voice samples....")
    if speaker:
        # name of the user to verify given
        if min_dist_speaker.lower() == speaker.lower():
            # dist matching gives the same name - check for the name
            print("dist matching gives the same name - check for the name")
            max_score = get_score_from_audio_matching(speaker,verification,audio_file_name)   
            if max_score == -1:
                max_score = min_dist_score
            print("FINAL RECOGNITION(MAX BETTER) : ",f"{speaker,max_score}")
        else:
            # dist matching gives a different name - check for both names
            print("dist matching gives a different name - check for both names")
            max_score_1 = get_score_from_audio_matching(speaker,verification,audio_file_name)
            max_score_2 = get_score_from_audio_matching(min_dist_speaker,verification,audio_file_name)
            if max_score_1 >= max_score_2:
                 print("FINAL RECOGNITION(MAX BETTER) : ",f"{speaker,max_score_1}") 
            else:
                print("FINAL RECOGNITION(MAX BETTER) : ",f"{min_dist_speaker,max_score_2}")
    else:   
        # no speaker name given - check for the name taken from dist matching
        print("no speaker name given - check for the name taken from dist matching")
        max_score = get_score_from_audio_matching(min_dist_speaker,verification,audio_file_name)
        print("FINAL RECOGNITION(MAX BETTER) : ",f"{min_dist_speaker,max_score}")
    clean_temp_audios(path='../Audio',rmv_dir=True)