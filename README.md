# [SBI - Voice Biometrics](https://www.techgig.com/hackathon/voice-biometrics)

## Objective
```
Customers interact with the Bank via various channels such as Contact Centre & Video based Customer Identification Process Calls. Authentication measures of Caller ID / PIN / Security Questions / Device Signatures are often inadequate and intrusive.
```

## Solution Expected:
```
For a sample voice clip, develop a voice signature for authentication with other voice samples & further develop the Voice signature as per repeated voice samples.
The following are the expectations from the prototype:
    1. To Authenticate & continuously enhance Voice Signatures of Customers for interaction with the Bank via following channels:
            Contact Centre
            Mobile App
            Video Customer Identification Process
    2.Voice as additional factor of authentication
    3.Response as a Percentage of model of Voice
```

## Solution Architecture - POC

![alt text](./images/final_arch.png)

## Solution Architecture - PROD

![alt text](./idea/images/arch.png)

## Solution Samples

### Enroll Voices from a Directory

![alt text](./images/enroll_vocies_from_a_dir.png)

![alt text](./images/output_enroll_all.png)

![alt text](./images/buucket_all.png)

![alt text](./images/bucket_inside.png)

### Enroll a single vocie with a name

![alt text](./images/enroll_single.png)

![alt text](./images/output_single.png)

![alt text](./images/bucket_single.png)


### Match Voice with a given name - when Distance Scoring Output matches with given name

![alt text](./images/match_with_name.png)

![alt text](./images/output_with_name.png)

![alt text](./images/match_with_name1.png)

![alt text](./images/output_match_with_name_1.png)

### Match Voice with a given name - when Distance Scoring Output do not match with given name

![alt text](./images/match_with_name_no_dist.png)

![alt text](./images/output_match_with_name_no_dist.png)


### Match Voice without a given name

![alt text](./images/match_without_name.png)

![alt text](./images/output_match_without_name.png)

![alt text](./images/output_match_without_name_1.png)
