"use strict";



async function fetch_categories() {
    let categories = {};

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


fetch_categories().then( cats => {
    Object.values(cats).forEach(category => {
        console.log(category);
    });
})


