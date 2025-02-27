"use strict";



function createErrorBox(message) {
    const errorbox = document.getElementById("error_box");
    if (errorbox !== null) {
        errorbox.remove();
    }
    
    const error_box = document.createElement("div");
    error_box.id = "error_box";
    const error_message = document.createElement("p");
    error_message.textContent = message;
    error_box.insertAdjacentElement("afterbegin", error_message);
    const error_anchor = document.querySelector(".wrapper h1");
    error_anchor.insertAdjacentElement("afterend", error_box);
};


function removeCategoryOptions() {
    const category_options = document.querySelectorAll("#category > option");
    category_options.forEach(e => e.remove());
};

function removeTopicOptions() {
    const topic_options = document.querySelectorAll("#topic > option");
    topic_options.forEach(e => e.remove());
};


function addEmptyCategoryOption() {
    const new_option = document.createElement("option");
    document.getElementById("category").insertAdjacentElement("afterbegin", new_option);
};

function addEmptyTopicOption() {
    const new_option = document.createElement("option");
    document.getElementById("topic").insertAdjacentElement("afterbegin", new_option);
};


async function fetch_categories() {
    let categories = [];

    return fetch("http://127.0.0.1:5000/api/get-categories", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })
    .then(response => response.json())
    .then(data => {
        categories = data.categories;
        return categories;  // Return the categories here
    })
    .catch(error => {
        createErrorBox("Kategorien konnten nicht gefetcht werden! Verbindung zum Server steht?");
        console.error('Error:', error);
        return categories;  // Return an empty object or default value in case of error
    });
};

function get_categories() {
    fetch_categories().then( categories => {
        categories.forEach(entry => {
            let category = entry.category;
            let category_id = entry.category_id; 

            let new_option = document.createElement("option");
            new_option.textContent = category;
            new_option.value = category_id;
            document.getElementById("category").insertAdjacentElement("beforeend", new_option);
        });
    });
};


let topics = [];

async function fetch_topics() {
    topics = [];

    return fetch("http://127.0.0.1:5000/api/get-topics", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })
    .then(response => response.json())
    .then(data => {
        topics = data.topics;
    })
    .catch(error => {
        createErrorBox("Themen konnten nicht gefetcht werden! Verbindung zum Server steht?");
        console.error('Error:', error);
    });
};

fetch_topics();


function createTopicOptions(event) {
    const cat_def_opt = document.getElementById("cat_def_opt");
    if (cat_def_opt !== null) { cat_def_opt.remove(); }

    const category_id = event.target.value;

    const old_options = document.querySelectorAll("#topic > option");
    old_options.forEach(e => e.remove());

    addEmptyTopicOption();
    
    topics.forEach(entry => {
        if (entry.category_id === parseInt(category_id)) {
            let new_option = document.createElement("option");
            new_option.textContent = entry.topic;
            new_option.value = entry.topic_id;
            document.getElementById("topic").insertAdjacentElement("beforeend", new_option);
        }
    });
};
