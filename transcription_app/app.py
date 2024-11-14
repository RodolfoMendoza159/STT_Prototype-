from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)
recognizer = sr.Recognizer()

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Add debug log to check the request path
    print(f"Incoming request path: {request.path}")
    
    if 'audio' not in request.files:
        print("Audio file not provided in request.")
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    
    try:
        # Use AudioFile to read the .wav file directly
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return jsonify({"transcription": text}), 200

    except sr.RequestError as e:
        print(f"RequestError: {e}")
        return jsonify({"error": "STT service request failed."}), 500
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return jsonify({"error": "Could not understand the audio."}), 400

if __name__ == '__main__':
    app.run(debug=True)
