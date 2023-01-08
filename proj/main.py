from flask import Flask, render_template, request, url_for
import lyricsgenius
genius = lyricsgenius.Genius("euzZWGNwXagg61U3uPMjlPbdf-QcsATRZ2AKxe7m7bVpqVJ9CRBRlZHDkQqCV_2R")
from jinja2.utils import markupsafe
from PIL import Image
from PIL.ImageStat import Stat
import requests
from io import BytesIO


app = Flask(__name__)

def bold(text, search):
    text = text.replace(search, f"<b>{search}</b>")
    text = text.replace(search.capitalize(), f"<b>{search.capitalize()}</b>")
    text = text.replace(search.lower(), f"<b>{search.lower()}</b>")
    text = text.replace(search.upper(), f"<b>{search.upper()}</b>")
    return markupsafe.Markup(text)

app.jinja_env.filters['bold'] = bold  

with app.app_context(), app.test_request_context():
    from articles import articles

@app.route("/")
def index():
    global articles
    return render_template("index.html", articles = articles)



@app.route("/bytext/", methods=['GET','POST'])
def bytext():
    return render_template("bytext.html")
    



@app.route("/search/", methods=['GET', 'POST'])
def search():
    song_title = ""
    songs = ""
    if request.method == "POST":
        title = request.form['title']
        songs = genius.search_songs(title,50,1)
    return render_template("search.html", songs=songs)





@app.route("/showsong/", methods=['GET', 'POST'])
def showsong():
    song = genius.search_song(song_id=request.form['id'])
    json = song.to_dict()
    feats = [artist['name'] for artist in json['featured_artists']]
    lyrics = json['lyrics'].replace(f"{song.title} Lyrics", "").replace("Embed", "")
    fi = lyrics.index("[")
    lyrics = lyrics[fi:]
    lyrics = lyrics.replace("[", "\n[")
    lyrics = lyrics.split("\n")

    response = requests.get(song.header_image_thumbnail_url)
    img = Image.open(BytesIO(response.content))
    colorsx = Stat(img).mean
    colors = []
    for val in colorsx:
        val = int(val)
        if val > 200:
            val = 200
        colors.append(val)


    

    album_name = json["album"]["name"]
    album_id = json['album']['id']


    return render_template("showsong.html", song = song, feats = feats, lyrics = lyrics, colors = colors, album_name = album_name, album_id = album_id) 


@app.route("/showalbum/", methods=["GET", "POST"])
def showalbum():
    albumid = ""
    if request.method == "POST":
        albumid = request.form['albumid']
    album = genius.album(albumid)

    response = requests.get(album['album']['cover_art_thumbnail_url'])
    img = Image.open(BytesIO(response.content))
    colorsx = Stat(img).mean
    colors = []
    for val in colorsx:
        val = int(val)
        if val > 200:
            val = 200
        colors.append(val)

    tracks = genius.album_tracks(albumid, per_page=50)

    return render_template("showalbum.html", album_id = albumid, album=album, colors = colors, tracks=tracks)

@app.route("/showarticle/", methods=["GET", "POST"])
def showarticle():
    artid = ""
    if request.method == "POST":
        artid = request.form['id']
    
    article = {}
    global articles
    for art in articles:
        if art['id'] == artid:
            article = art
    return render_template('showarticle.html', article = article)



if __name__ == "__main__":
   app.run() 