from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import tempfile
import os
import librosa
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import language_tool_python
from mangum import Mangum
import boto3
import nltk
import subprocess

nltk.download('vader_lexicon', download_dir='/tmp/nltk_docs')

nltk.data.path.append('/tmp/nltk_docs')

os.environ["NLTK_DATA"] = '/tmp/nltk_docs'
# librosa.cache.clear()
os.environ["LIBROSA_CACHE_DIR"] = "/tmp"
librosa.cache.path = '/tmp'

current_directory = os.getcwd()

# List all files in the current directory
files = os.listdir(current_directory)

# Print the list of files
print("Files in the current directory:")
for file in files:
    print(file)


class AudioAnalysis:
    def __init__(self):
        self.speech_rate_threshold = 150  # Adjust as needed
        self.pitch_variation_threshold = 50  # Adjust as needed
        self.sid = SentimentIntensityAnalyzer()

    def check_grammar(self, text):
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)

        # Grammar score is calculated based on the number of grammar errors
        grammar_score = 1 - len(matches) / len(text.split())

        return grammar_score

    def analyze_audio(self, audio_file):
        # Load audio file using librosa
        waveform, sample_rate = librosa.load(audio_file, sr=None)

        # Analyze speech rate
        speech_rate = len(waveform) / sample_rate  # Speech rate in seconds

        # Analyze pitch variation
        pitches, magnitudes = librosa.core.piptrack(y=waveform, sr=sample_rate)
        mean_pitch = np.mean(pitches[pitches > 0])

        # Analyze sentiment (tone)
        spoken_text = self.transcribe_audio(audio_file)
        tone_score = self.analyze_sentiment(spoken_text)

        return speech_rate, mean_pitch, tone_score

    def transcribe_audio(self, audio_file):
        return "i'm winging its virgin tolentino you can call me john i'm twenty four years old i haven't the year work experience with the p. b. ewing the street doing inbound and outbound calling first i served as the technical consultant were in my multitasking skills has been definitely enhanced that eventually i switch to customer service were in how we're integrity lisa very big role definitely sales must always be on point ahead of the target and at the same time making sure that each and every customer will always be satisfied with my assistants and on top of all these skillfully also have the talent we're doing graphic design screening fly years business cards and social media advertisement which will really be helpful for clients marketing needs and i can assure you that i'm not just the libyan other number on your people but definitely a good addition to come and once again this is red john tolentino think you can get by"

    def analyze_sentiment(self, text):
        # Use NLTK's VADER sentiment analysis
        sentiment_score = self.sid.polarity_scores(text)
        return sentiment_score['compound']

    def assess_audio_quality(self, speech_rate, mean_pitch, tone_score):
        # Assess clarity, confidence, and tone based on thresholds
        clarity = "Clear"  # Placeholder for more sophisticated analysis
        confidence = "High" if speech_rate > self.speech_rate_threshold and mean_pitch > self.pitch_variation_threshold else "Low"
        tone = "Positive" if tone_score >= 0 else "Negative"

        return clarity, confidence, tone

    # save to s3


def save_to_s3(object_key, content):
    # AWS credentials setup (make sure you handle credentials securely)
    aws_bucket_name ="reckognitionnew"
    aws_access_key = 'AKIAZC3RQOWY2DXBO72Q'
    aws_secret_key = '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'

    # Initialize S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    # Upload content to S3
    s3.put_object(Bucket=aws_bucket_name, Key=object_key, Body=content)


app = FastAPI()
handler = Mangum(app)
audio_analyzer = AudioAnalysis()


@app.get("/testing")
def testing():
    return {"testing": 1}


@app.post("/process_data")
async def process_data(
        audio_file: UploadFile = File(...),
        text_data: Optional[str] = Form(None)
):
    try:
        # Save the uploaded audio file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(audio_file.file.read())
            temp_audio_path = temp_audio.name

        # Perform audio analysis
        speech_rate, mean_pitch, tone_score = audio_analyzer.analyze_audio(temp_audio_path)

        # Additional processing based on the provided text data (replace with your logic)
        if text_data:
            # Your text processing logic here
            grammer_score = audio_analyzer.check_grammar(text_data)
            grammer_score = round(grammer_score * 100, 2)
        else:
            processed_text = None

        # Construct the response JSON
        response_data = {
            "speech_rate": float(speech_rate),
            "mean_pitch": float(mean_pitch),
            "tone_score": float(tone_score),
            "grammer_score": float(grammer_score)
        }
        print(response_data)

        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        print(e)
        # Handle exceptions and return an appropriate error response
        return HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")
    finally:
        # Delete the temporary audio file
        os.remove(temp_audio_path)


@app.post('/download')
def download_stream():
    try:
        local_file_path = '/tmp/stream.WAV'
        ffmpeg_command = [
            'ffmpeg',
            '-i',
            "https://d8cele0fjkppb.cloudfront.net/ivs/v1/624618927537/y16bDr6BzuhG/2023/12/6/5/55/EWxpQleowffw/media/hls/master.m3u8",
            '-c', 'copy',
            '-f', 'WAV',
            local_file_path,
        ]
        subprocess.run(ffmpeg_command, check=True)
        with open(local_file_path, 'rb') as local_file:
            save_to_s3("saved_audio.WAV", local_file)

    except Exception as e:
        print(e)
        # Handle exceptions and return an appropriate error response
        return HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

# To run the application:
# uvicorn your_module_name:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
