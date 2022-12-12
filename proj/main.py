from flask import Flask, render_template, request

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



@app.route("/byname/")
def byname():
    return render_template("byname.html")


if __name__ == "__main__":
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)