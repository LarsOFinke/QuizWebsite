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


function updateMode(event) {
    const new_mode = event.target.value;

    const old_options = document.querySelectorAll("#mode > option");
    old_options.forEach(e => e.remove());

    if (new_mode === "full") { document.getElementById("mode").innerHTML = html_mode_full; }
    else if (new_mode === "categ") { document.getElementById("mode").innerHTML = html_mode_categ; }
    else if (new_mode === "topic") { document.getElementById("mode").innerHTML = html_mode_topic; }
};



// {% if session.highscore_mode == "categ" or session.highscore_mode == "topic" %}
//     <form method="post">
//         <label for="category">Kategorie:</label>
//         <select name="category" id="mode" onchange="this.form.submit()">
    
//         {% if not session.highscore_category_name %}
//             <option value="">-- Wähle eine Kategorie --</option>
//         {% else %}
//             <option value="{{session.highscore_category_name}}">{{session.highscore_category_name}}</option>
//         {% endif %}

//         {% for category, category_id in categories.items() %}
//             <option value="{{category}}">{{category}}</option>
//         {% endfor %}
//         </select>
//     </form>
// {% endif %}


