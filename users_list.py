import json
class UserShows:
    def __init__(self, name, img, status, rating, category, studio, notes):
        self.name = name
        self.img = img
        self.status = status
        self.rating = rating
        self.category = category
        self.studio = studio
        self.notes = notes

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "rating": self.rating,
            "category": self.category,
            "studio": self.studio,
            "notes": self.notes,
            "img": self.img
        }
    def add_shows(email, show, path="database/user_shows.json"):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    
        if email not in data:
            data[email] = []
        
        data[email].append(show.to_dict())

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def delete_shows(name, email, path="database/user_shows.json"):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        data[email] = [show 
                       for show in data[email]
                            if show["name"] != name]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def edit_shows(name, email, updates, path="database/user_shows.json"):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

            for show in data[email]:
                if show["name"] == name:
                    for key, value in updates.items():
                        if key in show:
                            show[key]= value
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        