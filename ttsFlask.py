from flask import Flask, request, send_file
from dotenv import load_dotenv
import os
import openai
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
load_dotenv()
openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate_audio', methods=['POST'])
@cross_origin()
def generate_audio():
    input_text = request.form('input_text')

    if input_text is None or input_text.strip() == '':
        return 'Input text cannot be empty', 400

    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=input_text,
    )
    
    audio_data = response['audio']  

    with open('output.mp3', 'wb') as audio_file:
        audio_file.write(audio_data)

    return send_file('output.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
