"use strict";



get_categories();
fetch_topics();


function updateTopics(event) {
    createTopicOptions(event);
};


const qamount = document.getElementById("qamount");
const qamount_label = document.getElementById("qamount-label");

function updateAmountLabel() {
    qamount_label.textContent = qamount.value;
};

updateAmountLabel();


async function fetchQuestions(mode, id=0) {
    let questions = [];
    localStorage.setItem("game_mode", mode);
    let question_amount = qamount.value;

    return fetch(`${api_url}get-questions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({mode, id, question_amount})
    })
    .then(response => response.json())
    .then(data => {
        questions = data.questions;
        return questions;
    })
    .catch(error => {
        console.error('Error:', error);
        return questions;
    });
};


function startCategory(event) {
    event.preventDefault();

    let category_id = document.getElementById("category").value;
    localStorage.setItem("category_id", category_id);
    category_id = parseInt(category_id);

    fetchQuestions("category", category_id).then(question_list => {
        localStorage.setItem("question_list", JSON.stringify(question_list));
        window.location.href = "/quiz";
    });
};


function startTopic(event) {
    event.preventDefault();

    let topic_id = document.getElementById("topic").value;
    localStorage.setItem("topic_id", topic_id);
    topic_id = parseInt(topic_id);

    fetchQuestions("topic", topic_id).then(question_list => {
        localStorage.setItem("question_list", JSON.stringify(question_list));
        window.location.href = "/quiz";
    });
};


function startFull(event) {
    event.preventDefault();

    fetchQuestions("full").then(question_list => {
        localStorage.setItem("question_list", JSON.stringify(question_list));
        window.location.href = "/quiz";
    });
};
