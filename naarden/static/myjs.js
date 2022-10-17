
// run the logic when the document is fully loaded
document.addEventListener("DOMContentLoaded", () => {

    // add anchor elements in each of the table row 
    const rows = document.querySelectorAll("td[data-href]");
    console.log(rows);

    rows.forEach(row => {
        row.addEventListener("click", () => {
            window.location.href = row.dataset.href;
        })
    })

    // load the searched text
    var searchedText = sessionStorage.getItem("searchedText");
    if (searchedText != null) {
        document.getElementById("search").value = searchedText;
    }
});

// Highlight function gets the text based on user's input
function highlight() {
    let rows = document.querySelectorAll("#text-highlight");
    rows.forEach(row => {
        row.outerHTML = row.innerHTML;
    })

    let textToHighlight = document.getElementById("search").value
    if (textToHighlight != '') {
        rows = document.querySelectorAll("#table-text");
        rows.forEach(row => {
            let str = row.innerHTML;
            //console.log("Search [" + textToHighlight + "] in text: " + str);
            let regex = new RegExp(textToHighlight, "ig");
            // return a list of all accurance (not case sensitive) and for each calls function addMarkelement
            // we use first match and then replace because we want to search non-case sensitive. Otherwise, replace func woudl be suficient
            let matchesFound = str.match(regex);
            if (matchesFound != null) {
                matchesFound.forEach(addMarkElement);
            }
            // gets a string value and add a mark element around it
            function addMarkElement(value) {
                let textHighlighted = str.replace(value, '<mark id="text-highlight">' + value + '</mark>');
                //console.log("Text highlighted: " + value);
                row.innerHTML = textHighlighted;
            }
        })
    } else {
        sessionStorage.searchedText = '';
    }

}

// insert by the user input back into the search bar
function storeTextToSearch() {
    sessionStorage.searchedText = document.getElementById("search").value;
    var searchedText = sessionStorage.getItem("searchedText");
}