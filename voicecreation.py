from twilio.rest import Client
from flask import Flask, Response
import requests
import os
import time
import threading

# Twilio credentials (replace with your actual credentials)
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
DESTINATION_NUMBER = os.getenv("DESTINATION_NUMBER")
AUDIO_DIR = "audio"

# Ensure audio directory exists
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Flask app for dynamic TwiML hosting
app = Flask(__name__)
twiml_cache = {}

# Complete files list with 34 SSML scripts
files = [
    {
        "filename": "audio/intro_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>This is an interactive journey through the Forest of Disconnect storybook.<break time="0.5s"/> You will join five travelers as they learn to defuse the <emphasis level="moderate">emotional bombs</emphasis> of cynicism and judgment to find connection.<break time="0.5s"/> Click "Begin" to start.</speak>'
    },
    {
        "filename": "audio/chapter1_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>In a vast land, there was a dense, misty place called the <say-as interpret-as="characters">Forest of Disconnect</say-as>.<break time="0.7s"/> Five travelers arrived: Kai, who guarded his thoughts with sharp words;<break time="0.3s"/> Mara, quick to voice her worries;<break time="0.3s"/> Tomas, slow but wise;<break time="0.3s"/> Sana, quiet but observant;<break time="0.3s"/> and Eli, humming softly, seeking clarity.<break time="0.5s"/> Their guide, Lina, held a glowing lantern and a map: <say-as interpret-as="characters">Lina’s Compass of Connection</say-as>.</speak>'
    },
    {
        "filename": "audio/chapter1_lina_1.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">This forest holds <emphasis level="strong">emotional bombs</emphasis>—spiky barriers of cynicism and judgment that block our path to connection.<break time="0.5s"/> Defusing them means softening their power with understanding.<break time="0.5s"/> Will you join me with open minds and <emphasis level="moderate">kind hearts</emphasis>?</prosody></speak>'
    },
    {
        "filename": "audio/chapter1_narrator_2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>The travelers nodded, though some looked skeptical.<break time="0.4s"/> Eli hummed softly, eyeing the foggy path.<break time="0.5s"/> Lina smiled and shared the first rule: <prosody volume="soft">“We’ll create a Safe Zone by listening, speaking kindly, and assuming good intentions.”</prosody></speak>'
    },
    {
        "filename": "audio/reflection_1_q1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Why might the travelers feel hesitant to enter the forest?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/reflection_1_q2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">What does a <say-as interpret-as="characters">Safe Zone</say-as> mean to you in a group?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/chapter2_kai_1.mp3",
        "voice": "Polly.Brian-Standard",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.1" pitch="-10%">As the group walked, Kai kicked a stone and muttered,<break time="0.3s"/> <emphasis level="moderate">This is pointless.</emphasis><break time="0.3s"/> We’ll never find the Clearing.<break time="0.3s"/> It’s just a fairy tale.</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_lina_1.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">I notice frustration in your words, Kai.<break time="0.4s"/> Sounds like you’re doubting this journey can work.<break time="0.5s"/> Does that feel right?</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_lina_2.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Kai shrugged but didn’t snap back.<break time="0.4s"/> Lina continued, <emphasis level="moderate">Sounds like you need to feel sure our effort won’t be wasted?</emphasis></prosody></speak>'
    },
    {
        "filename": "audio/chapter2_lina_3.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Kai hesitated, then nodded slightly.<break time="0.4s"/> Lina shared, <prosody volume="soft">When I hear doubt, I feel a bit sad because I need hope for our group.</prosody><break time="0.5s"/> Kai, what would make this journey feel less pointless to you?</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_kai_2.mp3",
        "voice": "Polly.Brian-Standard",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.0" pitch="-5%">Kai mumbled, <prosody volume="soft">Maybe if we knew the path was real.</prosody><break time="0.5s"/> Lina nodded.<break time="0.3s"/> Let’s check <say-as interpret-as="characters">Lina’s Compass of Connection</say-as> together and take one step at a time.<break time="0.4s"/> How does that sound?</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>The spiky orb dissolved into a soft wisp of light.<break time="0.7s"/> Kai’s tense shoulders relaxed, and he gave a small nod.<break time="0.5s"/> The group moved forward, feeling a tiny spark of trust.</speak>'
    },
    {
        "filename": "audio/reflection_2_q1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">How did Lina respond to Kai’s cynicism without arguing?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/reflection_2_q2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">What’s an example of a time you felt cynical?<break time="0.5s"/> What helped you feel heard?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/chapter3_mara_1.mp3",
        "voice": "Polly.Amy-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.1" pitch="+10%">Deeper in the forest, Mara pointed at Tomas, who was walking slowly.<break time="0.4s"/> <emphasis level="strong">If he can’t keep up, we’ll never make it,</emphasis> she said sharply.</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_lina_1.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Mara, I notice a strong worry in your words, maybe about our progress.<break time="0.5s"/> Sounds like you need reassurance we’ll reach our goal?</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_lina_2.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Mara crossed her arms but nodded.<break time="0.4s"/> Lina turned to Tomas.<break time="0.3s"/> Tomas, how did Mara’s words land on you?</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_tomas_1.mp3",
        "voice": "Polly.Russell-Standard",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.8" pitch="-10%">Tomas sighed.<break time="0.7s"/> They make me feel like a burden.<break time="0.5s"/> I need to feel valued, even if I’m slow.</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_lina_3.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Lina nodded.<break time="0.4s"/> <prosody volume="soft">I feel a bit heavy hearing this because I need us all to feel included.</prosody><break time="0.5s"/> This judgment shows how much we all want to succeed.<break time="0.4s"/> Instead of blaming each other, can we face the disconnect as a team?<break time="0.5s"/> What could help us move forward together?</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>Mara softened.<break time="0.4s"/> <prosody volume="soft">Maybe we could take breaks so Tomas can rest.</prosody><break time="0.3s"/> Tomas smiled.<break time="0.3s"/> <prosody volume="soft">I’d appreciate that.</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_narrator_2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>The spiky orb dissolved into a soft wisp of light.<break time="0.7s"/> Mara’s tight grip on her arms loosened, and she met Tomas’s gaze with a shy smile.<break time="0.5s"/> The group agreed to walk at a pace that worked for all.</speak>'
    },
    {
        "filename": "audio/reflection_3_q1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">How did Lina help Mara and Tomas understand each other’s needs?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/reflection_3_q2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">When have you judged someone?<break time="0.5s"/> How could you reframe it to understand their needs?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/chapter4_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>As days passed, more bombs appeared—grumbles, doubts, and sharp words.<break time="0.5s"/> Each time, Lina used her <say-as interpret-as="characters">Compass of Connection</say-as>: acknowledge feelings, guess needs, share her heart, and invite curiosity.<break time="0.5s"/> Slowly, the travelers copied her.<break time="0.4s"/> One afternoon, Kai muttered, <prosody volume="soft">This path’s getting us nowhere.<break time="0.3s"/> I just don’t see the point anymore.</prosody></speak>'
    },
    {
        "filename": "audio/chapter4_eli_1.mp3",
        "voice": "Google.en-US-Standard-C",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.0" pitch="+5%">Eli, who sought clarity, stepped forward.<break time="0.4s"/> Kai, I hear frustration.<break time="0.3s"/> Am I hearing you right?<break time="0.5s"/> Maybe you need to know we’re making progress?</prosody></speak>'
    },
    {
        "filename": "audio/chapter4_eli_2.mp3",
        "voice": "Google.en-US-Standard-C",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.0" pitch="+5%">Kai nodded, surprised.<break time="0.4s"/> Eli continued, <prosody volume="soft">I feel a bit lost too, and I need to believe we’re moving forward.</prosody><break time="0.5s"/> Could we check <say-as interpret-as="characters">Lina’s Compass</say-as> together, just to see our next step?</prosody></speak>'
    },
    {
        "filename": "audio/chapter4_narrator_2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>Kai agreed.<break time="0.4s"/> The spiky orb dissolved into a soft wisp of light.<break time="0.7s"/> A quiet relief softened Kai’s frown, and a warmth spread through the group, their steps lighter.<break time="0.5s"/> Lina smiled.<break time="0.3s"/> <prosody volume="soft">Eli, you just defused a bomb!</prosody><break time="0.4s"/> Each time we listen and share, we build a stronger bridge.</speak>'
    },
    {
        "filename": "audio/chapter4_sana_1.mp3",
        "voice": "Polly.Salli-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9" volume="soft">That evening, Sana whispered, <emphasis level="moderate">I feel safer now.</emphasis></prosody></speak>'
    },
    {
        "filename": "audio/reflection_4_q1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">What small wins have you noticed in a group you’re part of?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/reflection_4_q2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">How can regular check-ins help a group stay connected?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/chapter5_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>At last, the forest opened to a golden meadow—the <say-as interpret-as="characters">Clearing of Connection</say-as>.<break time="0.7s"/> The air felt warm, and the travelers stood together, their faces glowing with relief and joy.<break time="0.5s"/> A shared warmth filled their hearts, as if the forest’s weight had lifted.</speak>'
    },
    {
        "filename": "audio/chapter5_lina_1.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">We didn’t erase the bombs, but we learned to defuse them.<break time="0.5s"/> Cynicism and judgment come from pain and unmet needs.<break time="0.5s"/> By creating safety and understanding, we found our way here.</prosody></speak>'
    },
    {
        "filename": "audio/chapter5_narrator_2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>The travelers vowed to share the <say-as interpret-as="characters">Compass’s</say-as> lessons with others, knowing connection is a journey, not a race.<break time="0.7s"/></speak>'
    },
    {
        "filename": "audio/outro_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>You have reached the <say-as interpret-as="characters">Clearing of Connection</say-as>.<break time="0.5s"/> The lessons from <say-as interpret-as="characters">Lina’s Compass</say-as> are now yours to carry into your own <emphasis level="moderate">forests</emphasis>.<break time="0.5s"/> How will you use these lessons in your life?<break time="0.7s"/> You can use the Journey Map to revisit any part of the story.</speak>'
    }
]

@app.route("/twiml/<filename>")
def serve_twiml(filename):
    """Serve TwiML for a given filename."""
    file_data = next((f for f in files if f["filename"] == filename), None)
    if not file_data:
        return Response("File not found", status=404, mimetype="text/plain")
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="{file_data['voice']}" language="{file_data['language']}">{file_data['ssml']}</Say>
        <Record maxLength="60" recordingStatusCallback="/recording-callback"/>
    </Response>"""
    return Response(twiml, mimetype="application/xml")

@app.route("/recording-callback", methods=["POST"])
def recording_callback():
    """Handle recording callback (placeholder for production)."""
    return Response("", status=200)

def create_tts_file(file_data):
    """Generate MP3 for a single file using Twilio."""
    filename = file_data["filename"]
    twiml_url = f"http://127.0.0.1:5000/twiml/{filename}"  # Update with ngrok URL in production
    
    try:
        # Initiate call
        call = client.calls.create(
            to=DESTINATION_NUMBER,
            from_=TWILIO_NUMBER,
            url=twiml_url
        )
        print(f"Started call for {filename} (Call SID: {call.sid})")
        
        # Poll for recording (max 30 seconds)
        for _ in range(30):
            recordings = client.recordings.list(call_sid=call.sid)
            if recordings:
                recording_url = f"https://api.twilio.com{recordings[0].uri.replace('.json', '.mp3')}"
                output_path = os.path.join(AUDIO_DIR, filename)
                response = requests.get(recording_url, auth=(ACCOUNT_SID, AUTH_TOKEN))
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
                return
            time.sleep(1)
        
        print(f"No recording found for {filename} after 30 seconds")
    except Exception as e:
        print(f"Error for {filename}: {e}")
    
    time.sleep(0.1)  # Respect CPS limit

def run_flask():
    """Run Flask server in a separate thread."""
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(2)  # Wait for Flask to start
    
    # Process all 34 files
    for file_data in files:
        create_tts_file(file_data)
    
    print("All files processed.")

from twilio.rest import Client
from flask import Flask, Response
import requests
import os
import time
import threading

# Twilio credentials (replace with your actual credentials)
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
DESTINATION_NUMBER = os.getenv("DESTINATION_NUMBER")
AUDIO_DIR = "audio"

# Ensure audio directory exists
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Flask app for dynamic TwiML hosting
app = Flask(__name__)
twiml_cache = {}

# Complete files list with 34 SSML scripts
files = [
    {
        "filename": "audio/intro_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>This is an interactive journey through the Forest of Disconnect storybook.<break time="0.5s"/> You will join five travelers as they learn to defuse the <emphasis level="moderate">emotional bombs</emphasis> of cynicism and judgment to find connection.<break time="0.5s"/> Click "Begin" to start.</speak>'
    },
    {
        "filename": "audio/chapter1_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>In a vast land, there was a dense, misty place called the <say-as interpret-as="characters">Forest of Disconnect</say-as>.<break time="0.7s"/> Five travelers arrived: Kai, who guarded his thoughts with sharp words;<break time="0.3s"/> Mara, quick to voice her worries;<break time="0.3s"/> Tomas, slow but wise;<break time="0.3s"/> Sana, quiet but observant;<break time="0.3s"/> and Eli, humming softly, seeking clarity.<break time="0.5s"/> Their guide, Lina, held a glowing lantern and a map: <say-as interpret-as="characters">Lina’s Compass of Connection</say-as>.</speak>'
    },
    {
        "filename": "audio/chapter1_lina_1.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">This forest holds <emphasis level="strong">emotional bombs</emphasis>—spiky barriers of cynicism and judgment that block our path to connection.<break time="0.5s"/> Defusing them means softening their power with understanding.<break time="0.5s"/> Will you join me with open minds and <emphasis level="moderate">kind hearts</emphasis>?</prosody></speak>'
    },
    {
        "filename": "audio/chapter1_narrator_2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>The travelers nodded, though some looked skeptical.<break time="0.4s"/> Eli hummed softly, eyeing the foggy path.<break time="0.5s"/> Lina smiled and shared the first rule: <prosody volume="soft">“We’ll create a Safe Zone by listening, speaking kindly, and assuming good intentions.”</prosody></speak>'
    },
    {
        "filename": "audio/reflection_1_q1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Why might the travelers feel hesitant to enter the forest?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/reflection_1_q2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">What does a <say-as interpret-as="characters">Safe Zone</say-as> mean to you in a group?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/chapter2_kai_1.mp3",
        "voice": "Polly.Brian-Standard",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.1" pitch="-10%">As the group walked, Kai kicked a stone and muttered,<break time="0.3s"/> <emphasis level="moderate">This is pointless.</emphasis><break time="0.3s"/> We’ll never find the Clearing.<break time="0.3s"/> It’s just a fairy tale.</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_lina_1.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">I notice frustration in your words, Kai.<break time="0.4s"/> Sounds like you’re doubting this journey can work.<break time="0.5s"/> Does that feel right?</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_lina_2.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Kai shrugged but didn’t snap back.<break time="0.4s"/> Lina continued, <emphasis level="moderate">Sounds like you need to feel sure our effort won’t be wasted?</emphasis></prosody></speak>'
    },
    {
        "filename": "audio/chapter2_lina_3.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Kai hesitated, then nodded slightly.<break time="0.4s"/> Lina shared, <prosody volume="soft">When I hear doubt, I feel a bit sad because I need hope for our group.</prosody><break time="0.5s"/> Kai, what would make this journey feel less pointless to you?</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_kai_2.mp3",
        "voice": "Polly.Brian-Standard",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.0" pitch="-5%">Kai mumbled, <prosody volume="soft">Maybe if we knew the path was real.</prosody><break time="0.5s"/> Lina nodded.<break time="0.3s"/> Let’s check <say-as interpret-as="characters">Lina’s Compass of Connection</say-as> together and take one step at a time.<break time="0.4s"/> How does that sound?</prosody></speak>'
    },
    {
        "filename": "audio/chapter2_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>The spiky orb dissolved into a soft wisp of light.<break time="0.7s"/> Kai’s tense shoulders relaxed, and he gave a small nod.<break time="0.5s"/> The group moved forward, feeling a tiny spark of trust.</speak>'
    },
    {
        "filename": "audio/reflection_2_q1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">How did Lina respond to Kai’s cynicism without arguing?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/reflection_2_q2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">What’s an example of a time you felt cynical?<break time="0.5s"/> What helped you feel heard?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/chapter3_mara_1.mp3",
        "voice": "Polly.Amy-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.1" pitch="+10%">Deeper in the forest, Mara pointed at Tomas, who was walking slowly.<break time="0.4s"/> <emphasis level="strong">If he can’t keep up, we’ll never make it,</emphasis> she said sharply.</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_lina_1.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Mara, I notice a strong worry in your words, maybe about our progress.<break time="0.5s"/> Sounds like you need reassurance we’ll reach our goal?</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_lina_2.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Mara crossed her arms but nodded.<break time="0.4s"/> Lina turned to Tomas.<break time="0.3s"/> Tomas, how did Mara’s words land on you?</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_tomas_1.mp3",
        "voice": "Polly.Russell-Standard",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.8" pitch="-10%">Tomas sighed.<break time="0.7s"/> They make me feel like a burden.<break time="0.5s"/> I need to feel valued, even if I’m slow.</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_lina_3.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">Lina nodded.<break time="0.4s"/> <prosody volume="soft">I feel a bit heavy hearing this because I need us all to feel included.</prosody><break time="0.5s"/> This judgment shows how much we all want to succeed.<break time="0.4s"/> Instead of blaming each other, can we face the disconnect as a team?<break time="0.5s"/> What could help us move forward together?</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>Mara softened.<break time="0.4s"/> <prosody volume="soft">Maybe we could take breaks so Tomas can rest.</prosody><break time="0.3s"/> Tomas smiled.<break time="0.3s"/> <prosody volume="soft">I’d appreciate that.</prosody></speak>'
    },
    {
        "filename": "audio/chapter3_narrator_2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>The spiky orb dissolved into a soft wisp of light.<break time="0.7s"/> Mara’s tight grip on her arms loosened, and she met Tomas’s gaze with a shy smile.<break time="0.5s"/> The group agreed to walk at a pace that worked for all.</speak>'
    },
    {
        "filename": "audio/reflection_3_q1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">How did Lina help Mara and Tomas understand each other’s needs?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/reflection_3_q2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">When have you judged someone?<break time="0.5s"/> How could you reframe it to understand their needs?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/chapter4_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>As days passed, more bombs appeared—grumbles, doubts, and sharp words.<break time="0.5s"/> Each time, Lina used her <say-as interpret-as="characters">Compass of Connection</say-as>: acknowledge feelings, guess needs, share her heart, and invite curiosity.<break time="0.5s"/> Slowly, the travelers copied her.<break time="0.4s"/> One afternoon, Kai muttered, <prosody volume="soft">This path’s getting us nowhere.<break time="0.3s"/> I just don’t see the point anymore.</prosody></speak>'
    },
    {
        "filename": "audio/chapter4_eli_1.mp3",
        "voice": "Google.en-US-Standard-C",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.0" pitch="+5%">Eli, who sought clarity, stepped forward.<break time="0.4s"/> Kai, I hear frustration.<break time="0.3s"/> Am I hearing you right?<break time="0.5s"/> Maybe you need to know we’re making progress?</prosody></speak>'
    },
    {
        "filename": "audio/chapter4_eli_2.mp3",
        "voice": "Google.en-US-Standard-C",
        "language": "en-US",
        "ssml": '<speak><prosody rate="1.0" pitch="+5%">Kai nodded, surprised.<break time="0.4s"/> Eli continued, <prosody volume="soft">I feel a bit lost too, and I need to believe we’re moving forward.</prosody><break time="0.5s"/> Could we check <say-as interpret-as="characters">Lina’s Compass</say-as> together, just to see our next step?</prosody></speak>'
    },
    {
        "filename": "audio/chapter4_narrator_2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>Kai agreed.<break time="0.4s"/> The spiky orb dissolved into a soft wisp of light.<break time="0.7s"/> A quiet relief softened Kai’s frown, and a warmth spread through the group, their steps lighter.<break time="0.5s"/> Lina smiled.<break time="0.3s"/> <prosody volume="soft">Eli, you just defused a bomb!</prosody><break time="0.4s"/> Each time we listen and share, we build a stronger bridge.</speak>'
    },
    {
        "filename": "audio/chapter4_sana_1.mp3",
        "voice": "Polly.Salli-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9" volume="soft">That evening, Sana whispered, <emphasis level="moderate">I feel safer now.</emphasis></prosody></speak>'
    },
    {
        "filename": "audio/reflection_4_q1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">What small wins have you noticed in a group you’re part of?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/reflection_4_q2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">How can regular check-ins help a group stay connected?</prosody><break time="1s"/></speak>'
    },
    {
        "filename": "audio/chapter5_narrator_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>At last, the forest opened to a golden meadow—the <say-as interpret-as="characters">Clearing of Connection</say-as>.<break time="0.7s"/> The air felt warm, and the travelers stood together, their faces glowing with relief and joy.<break time="0.5s"/> A shared warmth filled their hearts, as if the forest’s weight had lifted.</speak>'
    },
    {
        "filename": "audio/chapter5_lina_1.mp3",
        "voice": "Polly.Joanna-Neural",
        "language": "en-US",
        "ssml": '<speak><prosody rate="0.9">We didn’t erase the bombs, but we learned to defuse them.<break time="0.5s"/> Cynicism and judgment come from pain and unmet needs.<break time="0.5s"/> By creating safety and understanding, we found our way here.</prosody></speak>'
    },
    {
        "filename": "audio/chapter5_narrator_2.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>The travelers vowed to share the <say-as interpret-as="characters">Compass’s</say-as> lessons with others, knowing connection is a journey, not a race.<break time="0.7s"/></speak>'
    },
    {
        "filename": "audio/outro_1.mp3",
        "voice": "Polly.Matthew-Neural",
        "language": "en-US",
        "ssml": '<speak>You have reached the <say-as interpret-as="characters">Clearing of Connection</say-as>.<break time="0.5s"/> The lessons from <say-as interpret-as="characters">Lina’s Compass</say-as> are now yours to carry into your own <emphasis level="moderate">forests</emphasis>.<break time="0.5s"/> How will you use these lessons in your life?<break time="0.7s"/> You can use the Journey Map to revisit any part of the story.</speak>'
    }
]

@app.route("/twiml/<filename>")
def serve_twiml(filename):
    """Serve TwiML for a given filename."""
    file_data = next((f for f in files if f["filename"] == filename), None)
    if not file_data:
        return Response("File not found", status=404, mimetype="text/plain")
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="{file_data['voice']}" language="{file_data['language']}">{file_data['ssml']}</Say>
        <Record maxLength="60" recordingStatusCallback="/recording-callback"/>
    </Response>"""
    return Response(twiml, mimetype="application/xml")

@app.route("/recording-callback", methods=["POST"])
def recording_callback():
    """Handle recording callback (placeholder for production)."""
    return Response("", status=200)

def create_tts_file(file_data):
    """Generate MP3 for a single file using Twilio."""
    filename = file_data["filename"]
    twiml_url = f"http://127.0.0.1:5000/twiml/{filename}"  # Update with ngrok URL in production
    
    try:
        # Initiate call
        call = client.calls.create(
            to=DESTINATION_NUMBER,
            from_=TWILIO_NUMBER,
            url=twiml_url
        )
        print(f"Started call for {filename} (Call SID: {call.sid})")
        
        # Poll for recording (max 30 seconds)
        for _ in range(30):
            recordings = client.recordings.list(call_sid=call.sid)
            if recordings:
                recording_url = f"https://api.twilio.com{recordings[0].uri.replace('.json', '.mp3')}"
                output_path = os.path.join(AUDIO_DIR, filename)
                response = requests.get(recording_url, auth=(ACCOUNT_SID, AUTH_TOKEN))
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
                return
            time.sleep(1)
        
        print(f"No recording found for {filename} after 30 seconds")
    except Exception as e:
        print(f"Error for {filename}: {e}")
    
    time.sleep(0.1)  # Respect CPS limit

def run_flask():
    """Run Flask server in a separate thread."""
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(2)  # Wait for Flask to start
    
    # Process all 34 files
    for file_data in files:
        create_tts_file(file_data)
    
    print("All files processed.")
