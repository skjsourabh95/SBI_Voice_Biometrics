from enroll import enroll,enroll_all
from recognize import recognize
import uuid
import os
from utility import clean_temp_audios

def main(audio_path,name=None,method= "enroll",enroll_dir = False):
    reponse = "Failed"
    audio_file_name = f"../Audio/{name}/{name}-{str(uuid.uuid4())}.wav"
    if not os.path.exists(f"../Audio/{name}/"):
        os.mkdir(f"../Audio/{name}/")
    try:
        if name:
            name = name.lower()
        if method and audio_path:
            print("Processing Audio!")
            if method.lower() == "enroll" and enroll_dir:
                # eroll from a given dir
                print("Staring Enrolling all Audios!")
                enroll_all(audio_path)
            elif method.lower() == "enroll" and not enroll_dir:
                # enroll a single voice sample
                print("Staring Enrolling!")
                enroll(name,audio_path,audio_file_name)
            else:
                # verify a audio sample with or without name
                reponse = recognize(name,audio_path)
                print(reponse)
                clean_temp_audios()
    except Exception as e:
        print(reponse,str(e))


if not os.path.exists(f"../Audio"):
    os.mkdir(f"../Audio")


# ENROLLING VOICES
# enroll from a dir
# all_audio_dir = "../sample_data/train"
# main(audio_path = all_audio_dir,method= "enroll",enroll_dir =True) 

# enroll single
# audio_path = "../sample_data/skj/voice_skj.wav"
name = "skj" # is a must to register a voice against a user!
# main(audio_path= audio_path,name = name,method= "enroll") 

# MATCHING VOICE
# verify against a name and sample
audio_path = "../sample_data/test/Obama.mp3" 
name = "Barack Obama"
main(audio_path= audio_path,name=name,method= "match") 

# verify against sample without name for an unknow voice sample - 
# audio_path = "../sample_data/test/voldemort.mp3" 
# main(audio_path = audio_path,method= "match") 

# CURRENT NAMES IN DIR
# Amitabh Bachan
# Barack Obama
# Morgan Freeman
# Oprah winfrey
# Voldemort
# skj