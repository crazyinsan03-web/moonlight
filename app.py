from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

def get_song_info(query):
   ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'cookiefile': 'youtube.com_cookies.txt', # YE LINE ADD KARNI HAI
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
