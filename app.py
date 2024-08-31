from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.exceptions import (
    TranscriptsDisabled,
    VideoUnavailable,
    NoTranscriptFound,
    CouldNotRetrieveTranscript
)
import time

app = Flask(__name__)

@app.route('/transcript', methods=['POST'])
def get_transcript():
    if 'video_id' not in request.form:
        return jsonify(error="No video ID provided"), 400

    video_id = request.form['video_id']
    
    try:
        # Fetch the transcript with timestamps
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatted_transcript = []

        for entry in transcript:
            formatted_entry = {
                "start_time": entry['start'],
                "duration": entry['duration'],
                "text": entry['text']
            }
            formatted_transcript.append(formatted_entry)

        return jsonify(transcript=formatted_transcript), 200

    except TranscriptsDisabled:
        return jsonify(error="Transcripts are disabled for this video."), 403
    except VideoUnavailable:
        return jsonify(error="The video is unavailable."), 404
    except NoTranscriptFound:
        return jsonify(error="No transcript found for this video."), 404
    except CouldNotRetrieveTranscript:
        # Handle cases where the transcript couldn't be retrieved
        return jsonify(error="Could not retrieve transcript. Please try again later."), 500
    except Exception as e:
        # Handle other exceptions
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
