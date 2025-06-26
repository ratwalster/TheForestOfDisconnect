import boto3
import os

# Create a directory to store audio files if it doesn't exist
output_directory = "audio"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize Polly client
# Ensure you have your AWS credentials configured correctly (e.g., via environment variables, IAM roles, or a credentials file)
polly = boto3.client('polly', region_name='us-east-1') # Ensure us-east-1 supports Matthew and Joanna neural voices

files = [
    {
        "filename": "audio/intro_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>This is an interactive journey through the forest of disconnect storybook.<break time="0.5s"/> You will join five travelers as they learn to defuse the <emphasis level="moderate">emotional bombs</emphasis> of cynicism and judgment to find connection.<break time="0.5s"/> Click "Begin" to start.</speak>'
    },
    {
        "filename": "audio/chapter1_narrator_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>In a vast land, there was a dense, misty place called the <say-as interpret-as="characters">Forest of Disconnect</say-as>.<break time="0.7s"/> Five travelers arrived: Kai, who guarded his thoughts with sharp words;<break time="0.3s"/> Mara, quick to voice her worries;<break time="0.3s"/> Tomas, slow but wise;<break time="0.3s"/> Sana, quiet but observant;<break time="0.3s"/> and Eli, humming softly, seeking clarity.<break time="0.5s"/> Their guide, Lina, held a glowing lantern and a map: <say-as interpret-as="characters">Lina’s Compass of Connection</say-as>.</speak>'
    },
    {
        "filename": "audio/chapter1_lina_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">This forest holds <emphasis level="strong">emotional bombs</emphasis>—spiky barriers of cynicism and judgment that block our path to connection.<break time="0.5s"/> Defusing them means softening their power with understanding.<break time="0.5s"/> Will you join me with open minds and <emphasis level="moderate">kind hearts</emphasis>?</prosody></speak>'
    },
    {
        "filename": "audio/chapter1_narrator_2.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>The travelers nodded, though some looked skeptical.<break time="0.4s"/> Eli hummed softly, eyeing the foggy path.</speak>'
    },
    {
        "filename": "audio/chapter1_kai_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>See? I told you this was a waste of time!</speak>'
    },
    {
        "filename": "audio/chapter1_mara_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Are you sure we should go in? What if something bad happens?</speak>'
    },
    {
        "filename": "audio/chapter1_lina_2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Fear and doubt are natural, but they can be the first "bombs" to disarm.<break time="0.5s"/> Let my compassion be your guide as you explore your own hearts and minds.</speak>'
    },
    {
        "filename": "audio/chapter2_narrator_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>They walked deeper, the mist clinging to them.<break time="0.4s"/> A large, thorny bush blocked the way.<break time="0.5s"/> From it emerged a thorny ball of negativity—a Cynicism Bomb.<break time="0.8s"/> It crackled with defensive energy.</speak>'
    },
    {
        "filename": "audio/chapter2_cynicism_bomb_1.mp3",
        "voice": "Salli",
        "language": "en-US",
        "ssml": '<speak>Bah! What\'s the point? This is hopeless!</speak>'
    },
    {
        "filename": "audio/chapter2_kai_2.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>See? I told you this was a waste of time!</speak>'
    },
    {
        "filename": "audio/chapter2_lina_3.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>This bomb feeds on our negativity, Kai.<break time="0.5s"/> Try speaking to it with understanding instead of judgment.</speak>'
    },
    {
        "filename": "audio/chapter2_kai_3.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak><prosody pitch="-10%">It... it must be hard to feel so hopeless.</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_narrator_2.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>The Cynicism Bomb’s thorns softened slightly.<break time="0.5s"/> Lina smiled.</speak>'
    },
    {
        "filename": "audio/chapter2_lina_4.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Well done, Kai! Understanding is the first step to defusing cynicism.</speak>'
    },
    {
        "filename": "audio/chapter3_narrator_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>Further on, they encountered a rigid wall of disapproval.<break time="0.6s"/> A Judgment Bomb radiated icy critiques.<break time="0.8s"/> It spoke with harsh, critical words.</speak>'
    },
    {
        "filename": "audio/chapter3_judgment_bomb_1.mp3",
        "voice": "Amy",
        "language": "en-US",
        "ssml": '<speak>You\'re not doing it right! You\'ll never succeed!</speak>'
    },
    {
        "filename": "audio/chapter3_mara_2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>It knows my deepest fears!</speak>'
    },
    {
        "filename": "audio/chapter3_lina_5.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>This bomb thrives on our self-doubt, Mara.<break time="0.5s"/> Try speaking with self-compassion.</speak>'
    },
    {
        "filename": "audio/chapter3_mara_3.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.8">I am doing my best, and that is enough.</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_narrator_2.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>The Judgment Bomb’s icy surface cracked.<break time="0.5s"/> Lina nodded encouragingly.</speak>'
    },
    {
        "filename": "audio/chapter3_lina_6.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Excellent, Mara! Self-compassion melts the ice of judgment.</speak>'
    },
    {
        "filename": "audio/chapter4_narrator_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>Tomas, the thoughtful traveler, noticed a dense fog of confusion.<break time="0.6s"/> Within it swirled a bomb of Uncertainty.<break time="0.8s"/> It pulsed with hesitant energy.</speak>'
    },
    {
        "filename": "audio/chapter4_uncertainty_bomb_1.mp3",
        "voice": "Joey",
        "language": "en-US",
        "ssml": '<speak>What if I make the wrong choice? I don\'t know what to do!</speak>'
    },
    {
        "filename": "audio/chapter4_tomas_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>This bomb speaks to my own hesitations.</speak>'
    },
    {
        "filename": "audio/chapter4_lina_7.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Uncertainty stems from seeking perfect answers, Tomas.<break time="0.5s"/> Speak to it with gentle acceptance of the unknown.</speak>'
    },
    {
        "filename": "audio/chapter4_tomas_2.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak><prosody volume="soft">It is okay not to know everything.</prosody></speak>'
    },
    {
        "filename": "audio/chapter4_narrator_2.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>The Uncertainty Bomb\'s fog thinned.<break time="0.5s"/> Lina smiled.</speak>'
    },
    {
        "filename": "audio/chapter4_lina_8.mp3", # Corrected from .mply
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Wisely spoken, Tomas! Acceptance clears the fog of uncertainty.</speak>'
    },
    {
        "filename": "audio/chapter5_narrator_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>Sana, the quiet one, felt a chill from a distant Isolation Bomb.<break time="0.6s"/> It vibrated with a lonely hum.<break time="0.8s"/> It seemed to say nothing, but its silence was a heavy weight.</speak>'
    },
    {
        "filename": "audio/chapter5_isolation_bomb_1.mp3",
        "voice": "Kendra",
        "language": "en-US",
        "ssml": '<speak><prosody rate="x-slow">No one understands. I am alone.</prosody></speak>'
    },
    {
        "filename": "audio/chapter5_sana_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Its silence speaks of deep sadness.</speak>'
    },
    {
        "filename": "audio/chapter5_lina_9.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Isolation thrives in silence, Sana.<break time="0.5s"/> Speak to it with connection, even if it feels small.</speak>'
    },
    {
        "filename": "audio/chapter5_sana_2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak><prosody rate="x-slow" volume="loud">You are not alone.</prosody></speak>'
    },
    {
        "filename": "audio/chapter5_narrator_2.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>The Isolation Bomb\'s hum faded.<break time="0.5s"/> Lina smiled gently.</speak>'
    },
]

# This list will store details of files that failed
failed_files = []

for file_info in files:
    filename = file_info["filename"] # Get filename outside the try block for clearer error messages
    try:
        raw_voice_name = file_info["voice"]

        # This logic handles both neural and standard voices automatically.
        # If you've manually cleaned all names to 'Matthew' or 'Joanna',
        # this block will primarily ensure `engine_type` is correctly set to 'neural'
        # for those voices. For Salli, Amy, Kendra, Joey, if they are standard,
        # they will correctly get 'standard'.
        if raw_voice_name.endswith('-Neural'):
            cleaned_voice_id = raw_voice_name.rsplit('-Neural', 1)[0]
            engine_type = 'neural'
        elif raw_voice_name in ['Matthew', 'Joanna', 'Amy', 'Kendra', 'Joey', 'Salli', 'Justin', 'Ivy']: # Add all neural voices you use
            # Assuming these voices are always intended to be neural if their raw name doesn't have -Neural
            engine_type = 'neural'
            cleaned_voice_id = raw_voice_name # Use the name as is
        else:
            cleaned_voice_id = raw_voice_name
            engine_type = 'standard' # Default to standard for other voices (like 'Salli' if she's standard)

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
                error_message = f"Polly returned an empty audio stream (0 bytes). Check SSML: {file_info['ssml'][:100]}..."
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
        # print(f"  SSML: {fail['ssml'][:200]}...") # Uncomment for full SSML in summary
        print("-" * 30)
    print(f"\n{len(failed_files)} file(s) failed to generate. Check SSML for specific errors.")
else:
    print("All audio files generated successfully!")
