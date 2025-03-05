document.addEventListener("DOMContentLoaded", function () {
    let searchInput = document.getElementById("table-search");

    searchInput.addEventListener("keyup", function () {
        let searchValue = this.value.toLowerCase();
        let rows = document.querySelectorAll(".searchable-table tbody tr");

        rows.forEach((row) => {
            let rowText = row.textContent.toLowerCase();
            row.style.display = rowText.includes(searchValue) ? "" : "none";
        });
    });
});
