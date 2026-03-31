from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

def get_song_info(query):
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
            info = ydl.extract_info(f"scsearch1:{query}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                res = info['entries'][0]
                return {
                    'title': res.get('title'),
                    'thumbnail': res.get('thumbnail'),
                    'audio_url': res.get('url')
                }
    except Exception as e:
        print(f"Error logic: {e}")
    return None

# Yahan humne POST method allow kar diya hai taaki error na aaye
@app.route('/', methods=['GET', 'POST'])
def index():
    song_info = None
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            song_info = get_song_info(query)
    
    return render_template('index.html', song=song_info)

# Isko bhi update kar diya safety ke liye
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query') or request.form.get('query')
    if not query:
        return "Search box khali hai bhai!", 400
    
    song_info = get_song_info(query)
    if song_info:
        return render_template('index.html', song=song_info)
    else:
        return "Gaana nahi mila, spelling check karle.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
