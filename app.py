import json
from flask import Flask, request, jsonify
import time

#main
app = Flask(__name__)

def json_file():
    with open("database/anime.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
    
def get_html(page_name):
    try:
        with open(page_name + ".html") as html_file:
            return html_file.read()
    except FileNotFoundError:
        return f"<h1>Page {page_name} not found.</h1>"

def logs(email ,password):
    if not (email and password):
        return get_html("login")
    
    with open("database/register.txt", "r") as registers_db:
        for line in registers_db:
            parts = line.strip().split("|")
            username, registered_email, registered_password = parts
            if registered_email ==  email and registered_password == password: 
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                with open("database/logs.txt", "a") as log:
                    log.write(f"{username}|{email}|{current_time}\n")
                    return get_html("myList")

def registeration(username, email, password):
        if not (username and email and password and len(password) >= 8):
            return get_html("register")
        
        with open("database/register.txt", "r") as db:
            for line in db:
                if email in line:
                    return get_html("register")
        with open("database/register.txt", "a") as db:
            db.write(f"{username}|{email}|{password}\n")
        return get_html("login")

@app.route("/")
def Home():
    return get_html("index")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        return logs(email, password)
    return get_html("login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        return registeration(username, email, password)
    return get_html("register")

@app.route("/api/shows", methods = ["GET"])
def get_shows():
    return(jsonify(json_file()))

@app.route("/shows", methods=["GET", "POST"])
def shows():
    return get_html("shows")

@app.route("/shows/details")
def details():
    name = request.args.get("name").strip()
    if not name:
        return "<h1> No anime specified</h1>"
    anime_data = json_file()
    for anime in anime_data:
        if anime["name"] == name:
            html = get_html("details")
            html = html.replace("$$name$$", anime["name"])
            html = html.replace("$$img$$", anime["img"])
            html = html.replace("$$rating$$", str(anime.get("Rating", "N/A")))
            html = html.replace("$$episodes$$", str(anime.get("episode", "N/A")))
            html = html.replace("$$genre$$", anime.get("categorie", "N/A"))
            html = html.replace("$$studio$$", anime.get("studio", "N/A"))
            html = html.replace("$$desc$$", anime.get("description", "No description."))
            return html
    return "<h1>Anime not found</h1>"

@app.route("/search")
def search():
    data = json_file()
    query =request.args.get("query", "").lower()
    results = [anime for anime in data
                if query in anime["name"].lower()]
    return jsonify(results)
        
if __name__ == "__main__":
    app.run(debug=True)