from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

def get_song_info(query):
    # SoundCloud search wala easy method
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'scsearch',
        'nocheckcertificate': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Query ko search kar raha hai
            info = ydl.extract_info(f"scsearch1:{query}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                res = info['entries'][0]
                return {
                    'title': res.get('title'),
                    'thumbnail': res.get('thumbnail'),
                    'audio_url': res.get('url')
                }
    except Exception as e:
        print(f"Error: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return "Please enter a song name", 400
    
    song_info = get_song_info(query)
    if song_info:
        return render_template('index.html', song=song_info)
    else:
        return "Song not found or blocked", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
