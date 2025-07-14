from flask import Flask, request, jsonify, send_from_directory
import speech_recognition as sr
from pydub import AudioSegment
import os




app = Flask(__name__)


app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'error': 'No audio file uploaded'}), 400

    # Save the uploaded file first
    temp_input_path = os.path.join('/tmp', audio_file.filename)
    audio_file.save(temp_input_path)

    # Convert to wav
    wav_path = convert_to_wav(temp_input_path)

    # Transcribe
    transcription = your_speech_to_text_function(wav_path)

    # Clean up temp files
    try:
        os.remove(temp_input_path)
        os.remove(wav_path)
    except Exception as e:
        print(f"Failed to delete temp files: {e}")

    return jsonify({'transcription': transcription})




def convert_to_wav(input_path, output_path=None):
    if not output_path:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".wav"
    
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")
    return output_path

def your_speech_to_text_function(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)  # read the whole audio file

    try:
        text = r.recognize_google(audio)  # Google Web Speech API
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"API error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
