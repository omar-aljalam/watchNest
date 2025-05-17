const username = localStorage.getItem("username");
const links = document.getElementsByClassName("nav_links");

if (username){
    links[0].textContent = "My List";
    links[0].setAttribute("href", "/mylist");

    links[1].textContent = "Logout";
    links[1].setAttribute("href", "/logout");
} else {
    links[0].textContent = "Login";
    links[0].setAttribute("href", "/login");

    links[1].textContent = "Register";
    links[1].setAttribute("href", "/register");
}


function loadSHows() {
    fetch("/api/shows")
    .then(responseJS)
    .then(dataJS)
    .catch(function () {});
}

function responseJS (response){
    return response.json();
}
function dataJS (data){
    let container = document.querySelector(".catalog-container");
    container.innerHTML = "";
    for (let i = 0; i < data.length; i++){
        let anime = data[i];
        let animeCard = document.createElement("div");
        animeCard.className = "anime-card";
        let link = document.createElement("a")
        link.href = "/shows/details?name=" + encodeURIComponent(anime.name);
        let img = document.createElement("img");
            img.src = anime.img;
            img.alt = anime.name;
            img.className = "anime-img"

            let name = document.createElement("h2");
            name.textContent = anime.name;
            link.appendChild(img);
            animeCard.appendChild(link);
            animeCard.appendChild(name);
            container.appendChild(animeCard);
        }
}

function search() {
    let query = document.getElementById("query").value.trim();
    fetch("/search?query=" + encodeURIComponent(query))
    .then(responseJS)
    .then(dataJS)
    .catch(function () {});
}

document.addEventListener("DOMContentLoaded", loadSHows);

document.getElementById("search_form").addEventListener("input", function (e) {
    e.preventDefault();
    search();
});

