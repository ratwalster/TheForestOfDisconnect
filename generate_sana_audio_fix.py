import boto3
import os

# Create a directory to store audio files if it doesn't exist
output_directory = "audio"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize Polly client
# Ensure you have your AWS credentials configured correctly
polly = boto3.client('polly', region_name='us-east-1')

# This list contains only the file that failed generation in the previous run.
files_to_generate = [
    {
        "filename": "audio/chapter4_sana_1.mp3",
        "voice": "Salli",
        "language": "en-US",
        # Original SSML caused "Unsupported Neural feature" error with Salli Neural voice.
        # "ssml": '<speak><prosody rate="0.9" volume="soft">That evening, Sana whispered, <emphasis level="moderate">I feel safer now.</emphasis></prosody></speak>',
        # Simplified SSML to be compatible with Salli Neural voice.
        "ssml": '<speak>That evening, Sana whispered, I feel safer now.</speak>',
        "engine": "neural"
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

