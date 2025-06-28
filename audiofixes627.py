import boto3
import os

# Create a directory to store audio files if it doesn't exist
output_directory = "audio"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize Polly client
# Ensure you have your AWS credentials configured correctly
polly = boto3.client('polly', region_name='us-east-1')

files_to_generate = [
    {
        "filename": "audio/chapter3_tomas_1.mp3",
        "voice": "Russell", # Based on voicecreation.py
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.8" pitch="-10%">Tomas sighed.<break time="0.7s"/> They make me feel like a burden.<break time="0.5s"/> I need to feel valued, even if I’m slow.</prosody></speak>',
        "engine": "standard" # Based on voicecreation.py mapping
    },
    {
        "filename": "audio/chapter4_sana_1.mp3",
        "voice": "Salli", # Based on voicecreation.py
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9" volume="soft">That evening, Sana whispered, <emphasis level="moderate">I feel safer now.</emphasis></prosody></speak>',
        "engine": "neural" # Based on voicecreation.py mapping
    },
    {
        "filename": "audio/chapter2_kai_2.mp3", # The file with the problematic text
        "voice": "Brian", # Based on voicecreation.py
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.0" pitch="-5%">Kai mumbled, <prosody volume="soft">Maybe if we knew the path was real.</prosody><break time="0.5s"/> Lina nodded.<break time="0.3s"/> Let’s check Lina’s <say-as interpret-as="words">Compass of Connection</say-as> together and take one step at a time.<break time="0.4s"/> How does that sound?</prosody></speak>',
        "engine": "standard" # Based on voicecreation.py mapping
    }
]

for file_info in files_to_generate:
    filename = file_info["filename"]
    try:
        voice_id = file_info["voice"]
        engine_type = file_info["engine"]
        ssml_text = file_info["ssml"]

        print(f"Attempting to generate: {filename} with voice {voice_id} ({engine_type})")

        response = polly.synthesize_speech(
            Text=ssml_text,
            VoiceId=voice_id,
            OutputFormat='mp3',
            TextType='ssml',
            Engine=engine_type
        )

        audio_stream = response.get('AudioStream')
        if audio_stream:
            audio_content = audio_stream.read()
            if audio_content:
                with open(filename, 'wb') as audio_file:
                    audio_file.write(audio_content)
                print(f"SUCCESS: Generated {filename}")
            else:
                print(f"WARNING: Polly returned an empty audio stream for {filename}.")
        else:
            print(f"ERROR: No 'AudioStream' in response for {filename}.")

    except Exception as e:
        print(f"ERROR generating {filename}: {e}")

print("\nGeneration process finished.")

