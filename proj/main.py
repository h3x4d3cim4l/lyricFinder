from flask import Flask, render_template, request
import lyricsgenius
genius = lyricsgenius.Genius("euzZWGNwXagg61U3uPMjlPbdf-QcsATRZ2AKxe7m7bVpqVJ9CRBRlZHDkQqCV_2R")
app = Flask(__name__)


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/bytext/", methods=['GET','POST'])
def bytext():
    x = ""
    if request.method == "POST":
        x = request.form['wartosc']
    return render_template("bytext.html", xy=x)



@app.route("/byname/", methods=['GET', 'POST'])
def byname():
    song_title = ""
    songs = ""
    if request.method == "POST":
        title = request.form['title']
        songs = genius.search_songs(title,50,1)
    return render_template("byname.html", songs=songs)



if __name__ == "__main__":
   app.run() 