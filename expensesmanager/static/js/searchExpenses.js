const searchField = document.getElementById("searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tableBody = document.querySelector(".table-body");

tableOutput.style.display = "none";
searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    tableBody.innerHTML=""
    paginationContainer.style.display="none"
    console.log("searchValue", searchValue);
    fetch("/search-expenses", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);

        tableOutput.style.display = "block";
        appTable.style.display = "none";
        paginationContainer.style.display = "none";
        if (data.length === 0) {
          tableOutput.innerHTML = `<p>No results found</p>`;
        } else {
          data.forEach((item) => {
            tableBody.innerHTML += ` <tr> <td>${item.amount}</td>
                  <td>${item.category}</td>
                  <td>${item.description}</td>
                  <td>${item.date}</td>

                  </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
