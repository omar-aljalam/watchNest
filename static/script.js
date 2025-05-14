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



