import librosa
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import language_tool_python

#import nltk
#nltk.download('vader_lexicon')
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

if __name__ == "__main__":
    audio_analyzer = AudioAnalysis()

    # Example audio file (replace with your actual audio file)
    audio_file = "output_audio.wav"
    text = "i'm winging its virgin tolentino you can call me john i'm twenty four years old i haven't the year work experience with the p. b. ewing the street doing inbound and outbound calling first i served as the technical consultant were in my multitasking skills has been definitely enhanced that eventually i switch to customer service were in how we're integrity lisa very big role definitely sales must always be on point ahead of the target and at the same time making sure that each and every customer will always be satisfied with my assistants and on top of all these skillfully also have the talent we're doing graphic design screening fly years business cards and social media advertisement which will really be helpful for clients marketing needs and i can assure you that i'm not just the libyan other number on your people but definitely a good addition to come and once again this is red john tolentino think you can get by"


    # Analyze audio features
    speech_rate, mean_pitch, tone_score = audio_analyzer.analyze_audio(audio_file)
    grammar_score = audio_analyzer.check_grammar(text)
    print(f"Speech Rate: {speech_rate} seconds")
    print(f"Mean Pitch: {mean_pitch}")
    print(f"Tone Score: {tone_score}")

    # Assess audio quality
    clarity, confidence, tone = audio_analyzer.assess_audio_quality(speech_rate, mean_pitch, tone_score)
    print(f"Clarity: {clarity}")
    print(f"Confidence: {confidence}")
    print(f"Tone: {tone}")
    print(round(grammar_score*100, 2))