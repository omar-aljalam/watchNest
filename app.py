import json
from flask import Flask, request, jsonify, session, redirect, url_for
import time
from users_list import UserShows

app = Flask(__name__)
app.secret_key = "Xx_secret_key_xX"

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
                session["user_email"] = email
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
               
                with open("database/logs.txt", "a") as log:
                    log.write(f"{username}|{email}|{current_time}\n")
                
                return redirect(url_for("my_list"))
                   

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
    if session.get("user_email"):
        return redirect(url_for("my_list"))
    
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

@app.route("/logout")
def logout():
    session.pop("user_email", None)

    html = get_html('login')
    html += """"
    <script>
        localStorage.clear();
    </script>
    """
    return html

@app.route("/mylist")
def my_list():
    if "user_email" not in session:
        return get_html("login")

    email = session["user_email"]
    username = ""

    with open("database/register.txt") as db:
        for line in db:
            parts = line.strip().split("|")
            if parts[1] == email:
                username = parts[0]
                break
    try:
        with open("database/user_shows.json", encoding="utf-8") as f:
            data = json.load(f)
            user_shows = data.get(email, [])
    except FileNotFoundError:
        user_shows = []

    html = get_html("list") 
    table_rows = ""
    for show in user_shows:
        table_rows += f"""
        <tr>
            <td>
                <div class="anime-info">
                    <img src="{show.get('img', '')}" alt="{show['name']}">
                    <span>{show['name']}</span>
                </div>
            </td>
            <td>{show.get('status', '')}</td>
            <td>{show.get('rating', '')}</td>
            <td>{show.get('category', '')}</td>
            <td>{show.get('studio', '')}</td>
            <td><input type="text" class="notes-input" value="{show.get('notes', '')}" placeholder="Add note..."></td>
            <td><button class="action-btn">Edit</button></td>
            <td><button class="action-btn delete-btn">Delete</button></td>
        </tr>
        """
    html = html.replace("$$table$$", table_rows)

    html += f"""
    <script>
        localStorage.setItem("username", "{username}");
        localStorage.setItem("email", "{email}");
    </script>
    """     
    return html
          


@app.route("/api/shows", methods = ["GET"])
def get_shows():
    return(jsonify(json_file()))

@app.route("/shows")
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