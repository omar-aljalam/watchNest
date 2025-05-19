import json
from flask import Flask, request, jsonify, session, redirect, url_for
from datetime import datetime
from users_list import UserShows

app = Flask(__name__)
app.secret_key = "Xx_secret_key_xX"

def get_html(page_name):
    path = f"templates/{page_name}.html"
    with open(path) as html_file:
        return html_file.read()
    
def json_file():
    with open("database/anime.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data

def is_authenticated():
    if "user_email" not in session:
        return redirect(url_for("login"))
    return True
     
def logs(email ,password):
    if not (email and password):
        return False, None
    
    with open("database/register.txt", "r") as registers_db:
        for line in registers_db:
            parts = line.strip().split("|")
            username, registered_email, registered_password = parts
            if registered_email ==  email and registered_password == password: 
                session["user_email"] = email
                current_time = datetime.now().isoformat(sep=" ", timespec="seconds")
               
                with open("database/logs.txt", "a") as log:
                    log.write(f"{username}|{email}|{current_time}\n")
                
                return True, current_time
    return False, None
                   

def registration(username, email, password):
    html = get_html("register")
    if not (username and email and password and len(password) >= 8):
        return html.replace("$$error$$", "Invaild email or password.")
    
    with open("database/register.txt") as db:
        for line in db:
            if email in line:
                return html.replace("$$error$$", "Email already exists.")

    with open("database/register.txt", "a") as db:
            db.write(f"{username}|{email}|{password}\n")
    return redirect(url_for("login"))

@app.route("/")
def Home():
    return get_html("index")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_email"):
        return redirect(url_for("my_list"))
    
    html = get_html("login")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        success, login_time = logs(email, password)
        if success:
            return f"""
            <script>
                    localStorage.setItem("login_time", "{login_time}");
                    window.location.href = "/mylist";
            </script>
            """
        else:
            return html.replace("$$error$$", "Invalid email or password.")
        
    return html.replace("$$error$$", "")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        return registration(username, email, password)
    
    return get_html("register").replace("$$error$$", "")

@app.route("/logout")
def logout():
    session.pop("user_email", None)

    html = """"
    <script>
        localStorage.clear();
        window.location.href = '/login';
    </script>
    """
    return html

@app.route("/mylist")
def my_list():
    auth = is_authenticated()
    if auth is not True:
        return auth
    
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
                    <img src="{show.get('img')}" alt="{show['name']}">
                    <span>{show['name']}</span>
                </div>
            </td>
                <form action="/edit_show" method="post">
                <input type="hidden" name="name" value="{show['name']}">
                <td>
                    <select name="status">
                        <option {'selected' if show['status'] == 'Watching' else ''}>Watching</option>
                        <option {'selected' if show['status'] == 'Completed' else ''}>Completed</option>
                        <option {'selected' if show['status'] == 'Plan to Watch' else ''}>Plan to Watch</option>
                        <option {'selected' if show['status'] == 'Dropped' else ''}>Dropped</option>
                    </select>
                </td>
                <td>
                    <input type="number" class="number" step="0.5" min="1" max="10" name="rating" value="{show['rating']}">
                </td>
                <td>
                    <textarea name="notes">{show.get('notes', '')}</textarea>
                </td>
                <td>
                    <button type="submit" class="action-btn" onclick="alert('Changes has been made!')">Save</button>
                </td>
            </form>
            <form action="/delete_show" method="post">
                <input type="hidden" name="name" value="{show['name']}">
                <td>
                    <button type="submit" class="action-btn delete-btn" onclick="return confirm('Are you sure you want to delete this show?')">Delete</button>
                </td>
            </form>
        </tr>
        """
    html = html.replace("$$table$$", table_rows)

    html += f"""
    <script>
        const username = "{username}";
        localStorage.setItem("username", "{username}");
        localStorage.setItem("email", "{email}");
        document.getElementById("welcome").textContent = "Welcome " + username;
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

    anime_data = json_file()
    for anime in anime_data:
        if anime["name"] == name:
            html = get_html("details")
            html = html.replace("$$name$$", anime["name"])
            html = html.replace("$$img$$", anime["img"])
            html = html.replace("$$rating$$", str(anime.get("Rating")))
            html = html.replace("$$episodes$$", str(anime.get("episode")))
            html = html.replace("$$genre$$", anime.get("categorie"))
            html = html.replace("$$studio$$", anime.get("studio"))
            html = html.replace("$$desc$$", anime.get("description"))

            email = session.get("user_email")

            with open("database/user_shows.json", encoding="utf-8") as f:
                data = json.load(f)
                user_shows = data.get(email, [])

            in_list = False
            for show in user_shows:
                if show["name"] == name:
                    in_list = True
                    break

            if in_list:
                html += """
                <script>
                    const btn = document.getElementById("btn");
                    btn.textContent = "Update!";   
                </script>
                """
            return html


@app.route("/search")
def search():
    data = json_file()
    query =request.args.get("query", "").lower()
    results = [anime for anime in data
                if query in anime["name"].lower()]
    return jsonify(results)

@app.route("/add_show", methods=["GET", "POST"])
def add_show():
    auth = is_authenticated()
    if auth is not True:
        return auth
        
    email = session ["user_email"]
    
    name = request.form.get("name")
    img = request.form.get("img")
    status = request.form.get("status")
    notes =  request.form.get("notes")
    rating =  request.form.get("rating")

    show = UserShows(name, img, status, rating, notes)
    UserShows.add_shows(email, show)
    return redirect(url_for("my_list"))

@app.route("/edit_show", methods=["GET", "POST"])
def edit_show():
    auth = is_authenticated()
    if auth is not True:
        return auth

    
    email = session["user_email"]
    name = request.form.get("name")

    updates = {
        "status": request.form.get("status"),
        "rating": request.form.get("rating"),
        "notes": request.form.get("notes")
    }

    UserShows.edit_shows(name, email, updates)
    return redirect(url_for("my_list"))

@app.route("/delete_show", methods=["GET", "POST"])
def delete_show():
    auth = is_authenticated()
    if auth is not True:
        return auth
    
    email = session["user_email"]
    name = request.form.get("name")
    
    UserShows.delete_shows(name, email)

    return redirect(url_for("my_list"))
    
@app.after_request
def head(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response


if __name__ == "__main__":
    app.run(debug=True)