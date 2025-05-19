const filterSelect = document.getElementById("status-filter");
const tableBody = document.getElementById("anime-table");
const notif = document.getElementById("noAnime");

function filterRows() {
    const rows = tableBody.querySelectorAll("tr");
    let count = 0;
    
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        if (filterRow(row)) {
            count++;
        }
    }
    
    if (count === 0) {
        notif.style.display = "";
    } else {
        notif.style.display = "none";
    }
}

function filterRow(row) {
    const selected = filterSelect.value.toLowerCase();
    const statusCell = row.querySelector("select[name='status']");
    const status = statusCell.value.toLowerCase();
    
    if (selected === "all" || selected === status) {
        row.style.display = "";
        return true; 
    } else {
        row.style.display = "none";
        return false; 
    }
}


filterRows();

filterSelect.addEventListener("change", filterRows);

