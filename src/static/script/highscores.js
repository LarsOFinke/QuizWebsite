"use strict";



const html_mode_full = `
<option value="full">Alle Bereiche</option> 
<option value="categ">Kategorie</option>
<option value="topic">Thema</option>
`

const html_mode_categ = `
<option value="categ">Kategorie</option>
<option value="full">Alle Bereiche</option>
<option value="topic">Thema</option>
`

const html_mode_topic = `
<option value="topic">Thema</option>
<option value="full">Alle Bereiche</option> 
<option value="categ">Kategorie</option>
`


function clearHighscores() {
    const old_highscores = document.querySelectorAll(".highscore");
    old_highscores.forEach(e => e.remove());
};


let new_mode = "";

function updateMode(event) {
    new_mode = event.target.value;

    const old_options = document.querySelectorAll("#mode > option");
    old_options.forEach(e => e.remove());

    if (new_mode === "full") { 
        document.getElementById("mode").innerHTML = html_mode_full; 
        removeCategoryOptions();
        removeTopicOptions();
        updateHighscores();
    } else if (new_mode === "categ") { 
        document.getElementById("mode").innerHTML = html_mode_categ; 
        addEmptyCategoryOption();
        get_categories();
        clearHighscores();
    } else if (new_mode === "topic") { 
        document.getElementById("mode").innerHTML = html_mode_topic; 
        removeCategoryOptions();
        addEmptyCategoryOption();
        get_categories();
        clearHighscores();
    }
};


function updateTopics(event) {
    clearHighscores();
    if (new_mode === "topic") { addEmptyTopicOption(); createTopicOptions(event); }
    else if (new_mode === "categ") { updateHighscores(event.target.value); }
};


function getTopicHighscores(event) {
    updateHighscores(document.getElementById("category").value, event.target.value);
}


async function fetch_highscores(mode, category, topic) {
    let highscores = [];

    return fetch("http://127.0.0.1:5000/api/get-highscores", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({mode, category, topic})
    })
    .then(response => response.json())
    .then(data => {
        highscores = data.highscores;
        return highscores;
    })
    .catch(error => {
        createErrorBox("Highscores konnten nicht gefetcht werden!");
        console.error('Error:', error);
        return highscores
    });
};

function updateHighscores(category = "", topic = "") {
    clearHighscores();

    fetch_highscores(new_mode, category, topic).then(highscores => {
        highscores.forEach(highscore => {
            const table_row = document.createElement("tr");
            table_row.className = "highscore";

            const td_player = document.createElement("td");
            td_player.textContent = highscore.name;
            table_row.insertAdjacentElement("afterbegin", td_player);
            const td_score = document.createElement("td");
            td_score.textContent = highscore.score;
            table_row.insertAdjacentElement("beforeend", td_score);
            const td_date = document.createElement("td");
            td_date.textContent = highscore.date;
            table_row.insertAdjacentElement("beforeend", td_date);

            const table = document.querySelector("tbody")
            table.insertAdjacentElement("beforeend", table_row);
        })
    })
}