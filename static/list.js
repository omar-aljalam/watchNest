const filterSelect = document.getElementById("status-filter");
const tableBody = document.getElementById("anime-table");

function filterRows (){
    const rows = tableBody.querySelectorAll("tr");

    for (let i = 0; i < rows.length; i++){
        const row = rows[i];
        filterRow(row);
    }
}

function filterRow (row) {
    const selected = filterSelect.value.toLowerCase();

    const statusCell = row.querySelector("select[name='status']");
    const status = statusCell.value.toLowerCase();
    
    if (selected === "all" || status === selected){
        row.style.display = ""; 
    } else {
        row.style.display = "none";
    }
}

filterSelect.addEventListener("change", filterRows);