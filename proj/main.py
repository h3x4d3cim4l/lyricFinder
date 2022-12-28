from flask import Flask, render_template, request
import lyricsgenius
genius = lyricsgenius.Genius("euzZWGNwXagg61U3uPMjlPbdf-QcsATRZ2AKxe7m7bVpqVJ9CRBRlZHDkQqCV_2R")
app = Flask(__name__)
from jinja2.utils import markupsafe

def bold(text, search):
    text = text.replace(search, f"<b>{search}</b>")
    text = text.replace(search.capitalize(), f"<b>{search.capitalize()}</b>")
    text = text.replace(search.lower(), f"<b>{search.lower()}</b>")
    text = text.replace(search.upper(), f"<b>{search.upper()}</b>")
    return markupsafe.Markup(text)

app.jinja_env.filters['bold'] = bold  

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/bytext/", methods=['GET','POST'])
def bytext():
    lista = ["Jakub", "Przemek", "Oskar"]
    return render_template("bytext.html", lista=lista)
    



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
    return render_template("showsong.html", song = song, feats = feats, lyrics = json['lyrics'].replace(f"{song.title} Lyrics", "").replace("Embed", "").split("\n")) 



if __name__ == "__main__":
   app.run() 