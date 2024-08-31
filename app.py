from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.exceptions import YouTubeTranscriptApiException
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

    except YouTubeTranscriptApiException as e:
        error_message = str(e)
        if "Too Many Requests" in error_message:
            # Retry after delay if rate limit error
            time.sleep(60)  # Wait 60 seconds before retrying
            return jsonify(error="Rate limit exceeded. Please try again later."), 429
        else:
            return jsonify(error=error_message), 500

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
