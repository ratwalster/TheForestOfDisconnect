import boto3
import os

# Create a directory to store audio files if it doesn't exist
output_directory = "audio"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize Polly client
polly = boto3.client('polly', region_name='us-east-1')

# List containing ONLY the three files that previously failed,
# with their SSML adjusted to remove Unsupported Neural features.
files = [
    {
        "filename": "audio/intro_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        # Removed <emphasis level="moderate">emotional bombs</emphasis>
        "ssml": '<speak>This is an interactive journey through the Forest of Disconnect storybook.<break time="0.5s"/> You will join five travelers as they learn to defuse the emotional bombs of cynicism and judgment to find connection.<break time="0.5s"/> Click "Begin" to start.</speak>'
    },
    {
        "filename": "audio/chapter1_lina_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        # Removed <emphasis level="strong">emotional bombs</emphasis>
        # Removed <emphasis level="moderate">kind hearts</emphasis>
        "ssml": '<speak><prosody rate="0.9">This forest holds emotional bombs—spiky barriers of cynicism and judgment that block our path to connection.<break time="0.5s"/> Defusing them means softening their power with understanding.<break time="0.5s"/> Will you join me with open minds and kind hearts?</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_kai_3.mp3",
        "voice": "Matthew",
        "language": "en-US",
        # Removed prosody pitch, kept only the text
        "ssml": '<speak>It... it must be hard to feel so hopeless.</speak>'
    },
]

# This list will store details of files that failed
failed_files = []

for file_info in files:
    filename = file_info["filename"]
    try:
        raw_voice_name = file_info["voice"]
        engine_type = file_info.get("engine") # Check if 'engine' is explicitly set in the dict

        if engine_type is None: # If no explicit engine was set, infer based on voice name
            if raw_voice_name.endswith('-Neural'):
                cleaned_voice_id = raw_voice_name.rsplit('-Neural', 1)[0]
                engine_type = 'neural'
            # This 'elif' block is simplified now, assuming you've cleaned the names manually.
            # It primarily ensures that voices you want as neural (like Matthew, Joanna) are marked as such.
            elif raw_voice_name in ['Matthew', 'Joanna', 'Amy', 'Kendra', 'Joey', 'Salli', 'Justin', 'Ivy']:
                engine_type = 'neural'
                cleaned_voice_id = raw_voice_name
            else:
                cleaned_voice_id = raw_voice_name
                engine_type = 'standard'
        else: # An explicit engine was already set (e.g., "standard")
            cleaned_voice_id = raw_voice_name # Use the voice name as is

        print(f"DEBUG: Processing {filename}")
        print(f"DEBUG: Using VoiceId: {cleaned_voice_id}, Engine: {engine_type}, SSML length: {len(file_info['ssml'])}")

        response = polly.synthesize_speech(
            Text=file_info["ssml"],
            VoiceId=cleaned_voice_id,
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
                error_message = f"Polly returned an empty audio stream (0 bytes). Check SSML for issues (SSML snippet: {file_info['ssml'][:100]}...)"
                print(f"ERROR: {filename}: {error_message}")
                failed_files.append({"filename": filename, "error": error_message, "ssml": file_info['ssml']})
        else:
            error_message = "No 'AudioStream' key in Polly response. Request might have failed silently."
            print(f"ERROR: {filename}: {error_message}")
            failed_files.append({"filename": filename, "error": error_message, "ssml": file_info['ssml']})

    except Exception as e:
        error_message = f"An unhandled error occurred: {e}"
        print(f"CRITICAL ERROR: {filename}: {error_message}")
        failed_files.append({"filename": filename, "error": error_message, "ssml": file_info['ssml']})

print("\n--- Summary of Failures ---")
if failed_files:
    for fail in failed_files:
        print(f"File: {fail['filename']}")
        print(f"  Error: {fail['error']}")
        print("-" * 30)
    print(f"\n{len(failed_files)} file(s) failed to generate. Check SSML for specific errors.")
else:
    print("All audio files generated successfully!")
    