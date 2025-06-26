import boto3
import os

# Create a directory to store audio files if it doesn't exist
output_directory = "audio"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize Polly client
polly = boto3.client('polly', region_name='us-east-1')

files = [
    {
        "filename": "audio/intro_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>This is an interactive journey through the forest of disconnect storybook.<break time="0.5s"/> You will join five travelers as they learn to defuse the emotional bombs of cynicism and judgment to find connection.<break time="0.5s"/> Click "Begin" to start.</speak>'
    },
    {
        "filename": "audio/chapter1_lina_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">This forest holds emotional bombs—spiky barriers of cynicism and judgment that block our path to connection.<break time="0.5s"/> Defusing them means softening their power with understanding.<break time="0.5s"/> Will you join me with open minds and kind hearts?</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_kai_3.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>It... it must be hard to feel so hopeless.</speak>'
    },
    {
        "filename": "audio/reflection_1_q1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Why might the travelers feel hesitant to enter the forest?</speak>'
    },
    {
        "filename": "audio/reflection_1_q2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>What does a “Safe Zone” mean to you in a group?</speak>'
    },
    {
        "filename": "audio/chapter2_kai_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>As the group walked, Kai kicked a stone and muttered, “This is pointless. We’ll never find the Clearing. It’s just a fairy tale.”</speak>'
    },
    {
        "filename": "audio/chapter2_lina_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>I notice frustration in your words, Kai. Sounds like you’re doubting this journey can work. Does that feel right?</speak>'
    },
    {
        "filename": "audio/chapter2_lina_2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Kai shrugged but didn’t snap back. Lina continued, “Sounds like you need to feel sure our effort won’t be wasted?”</speak>'
    },
    {
        "filename": "audio/reflection_2_q1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>How did Lina respond to Kai’s cynicism without arguing?</speak>'
    },
    {
        "filename": "audio/reflection_2_q2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>What’s an example of a time you felt cynical? What helped you feel heard?</speak>'
    },
    {
        "filename": "audio/chapter3_mara_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Deeper in the forest, Mara pointed at Tomas, who was walking slowly. “If he can’t keep up, we’ll never make it,” she said sharply.</speak>'
    },
    {
        "filename": "audio/chapter3_lina_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Mara, I notice a strong worry in your words, maybe about our progress. Sounds like you need reassurance we’ll reach our goal?</speak>'
    },
    {
        "filename": "audio/chapter3_lina_2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Mara crossed her arms but nodded. Lina turned to Tomas. “Tomas, how did Mara’s words land on you?”</speak>'
    },
    {
        "filename": "audio/chapter3_lina_3.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Lina nodded. “I feel a bit heavy hearing this because I need us all to feel included. This judgment shows how much we all want to succeed. Instead of blaming each other, can we face the disconnect as a team? What could help us move forward together?”</speak>'
    },
    {
        "filename": "audio/reflection_3_q1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>How did Lina help Mara and Tomas understand each other’s needs?</speak>'
    },
    {
        "filename": "audio/reflection_3_q2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>When have you judged someone? How could you reframe it to understand their needs?</speak>'
    },
    {
        "filename": "audio/chapter4_eli_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Eli, who sought clarity, stepped forward. “Kai, I hear frustration. Am I hearing you right? Maybe you need to know we’re making progress?”</speak>'
    },
    {
        "filename": "audio/chapter4_eli_2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>Kai nodded, surprised. Eli continued, “I feel a bit lost too, and I need to believe we’re moving forward. Could we check Lina’s Compass of Connection together, just to see our next step?”</speak>'
    },
    {
        "filename": "audio/reflection_4_q1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>What small wins have you noticed in a group you’re part of?</speak>'
    },
    {
        "filename": "audio/reflection_4_q2.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>How can regular check-ins help a group stay connected?</speak>'
    },
    {
        "filename": "audio/chapter5_lina_1.mp3",
        "voice": "Joanna",
        "language": "en-US",
        "ssml": '<speak>We didn’t erase the bombs, but we learned to defuse them. Cynicism and judgment come from pain and unmet needs. By creating safety and understanding, we found our way here.</speak>'
    },
    {
        "filename": "audio/outro_1.mp3",
        "voice": "Matthew",
        "language": "en-US",
        "ssml": '<speak>You have reached the Clearing of Connection. The lessons from Lina’s Compass are now yours to carry into your own "forests". How will you use these lessons in your life? You can use the Journey Map to revisit any part of the story.</speak>'
    },
]

# This list will store details of files that failed
failed_files = []

for file_info in files:
    filename = file_info["filename"]
    try:
        raw_voice_name = file_info["voice"]
        if raw_voice_name in ['Matthew', 'Joanna']:
            engine_type = 'neural'
            cleaned_voice_id = raw_voice_name
        else:
            cleaned_voice_id = raw_voice_name
            engine_type = 'standard'

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
        print("-" * 30)
    print(f"\n{len(failed_files)} file(s) failed to generate. Check SSML for specific errors.")
else:
    print("All audio files generated successfully!")
