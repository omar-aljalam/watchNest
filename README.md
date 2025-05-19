# MY FINAL PROJECT: WatchNest

WatchNest is a web application for anime fans to track and manage their personal watchlist.  
Users can log in, browse shows, and organize their watch history by status, rating, and notes.

- What does it do?  
  It allows users to browse animes and manage a personalized list using Flask, localStorage, and file-based storage.

- What is the "new feature" you've implemented?  


---

## Prerequisites

- Before running the project, make sure you have Python installed.
- You will also need to install Flask:
    pip install flask

---

## Project Checklist

- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.  
  - Module name: `datetime`
- [x] It contains at least one class written by you that has both properties and methods.  
  - File name for the class definition: `users_list.py`  
  - Line number(s) for the class definition: Line 2  
  - Name of two properties: `name`, `status`  
  - Name of two methods: `add_shows()`, `edit_shows()`  
  - File name and line numbers where the methods are used: `app.py` — lines 254, 273
- [x] It makes use of JavaScript in the front end and uses the `localStorage` of the web browser.
- [x] It uses modern JavaScript (for example, `let` and `const` rather than `var`).
- [x] It makes use of the reading and writing to the same file feature.  
  Files: `database/register.txt`, `database/logs.txt`, `database/user_shows.json`
- [x] It contains conditional statements.  
  - File name: `app.py`  
  - Line number(s):  74, 236
- [x] It contains loops.  
  - File name: `app.py`  
  - Line number(s): 217
- [x] It lets the user enter a value in a text box at some point.  
- [x] It doesn't generate any error message even if the user enters a wrong input.  
- [x] It is styled using your own CSS.  
- [x] The code follows code and style conventions as introduced in the course, is fully documented, and contains no unused code.  
  User feedback is shown in-browser via HTML, not via `print()` or `console.log()`.
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.

---

## How to Run

1. Requirements
Make sure you have the following installed:

Python 3.7+

Flask (pip install flask)

2. Project Structure
Ensure the folder structure looks like this:

| File                    | Destination folder     |
| ----------------------- | ---------------------- |
| `app.py`                | `watchnest/`           |
| `users_list.py`         | `watchnest/`           |
| All `.html` files       | `watchnest/templates/` |
| All `.css`, `.js` files | `watchnest/static/`    |
| All `.json`, `.txt`     | `watchnest/database/`  |

3. Run:
set FLASK_APP=app.py
flask run