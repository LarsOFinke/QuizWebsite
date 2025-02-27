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


let new_mode = "";

function updateMode(event) {
    new_mode = event.target.value;

    const old_options = document.querySelectorAll("#mode > option");
    old_options.forEach(e => e.remove());

    if (new_mode === "full") { 
        document.getElementById("mode").innerHTML = html_mode_full; 
        const category_options = document.querySelectorAll("#category > option");
        category_options.forEach(e => e.remove());
        const topic_options = document.querySelectorAll("#topic > option");
        topic_options.forEach(e => e.remove());
    } else if (new_mode === "categ") { 
        document.getElementById("mode").innerHTML = html_mode_categ; 
        get_categories();
    } else if (new_mode === "topic") { 
        document.getElementById("mode").innerHTML = html_mode_topic; 
        const category_options = document.querySelectorAll("#category > option");
        category_options.forEach(e => e.remove());
        const new_option = document.createElement("option");
        document.getElementById("category").insertAdjacentElement("afterbegin", new_option)
        get_categories();
    }
};


function updateTopics(event) {
    if (new_mode === "topic") { createTopicOptions(event); }
};


