from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

def get_song_info(query):
  ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    # YouTube ki jagah SoundCloud search use karega
    'default_search': 'scsearch', 
    'nocheckcertificate': True
}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info and len(info['entries']) > 0:
            res = info['entries'][0]
            return {
                'title': res.get('title'),
                'thumbnail': res.get('thumbnail'),
                'audio_url': res.get('url')
            }
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    song = None
    if request.method == 'POST':
        query = request.form.get('song_name')
        if query:
            song = get_song_info(query)
    return render_template('index.html', song=song)

if __name__ == "__main__":
    app.run(debug=True)
