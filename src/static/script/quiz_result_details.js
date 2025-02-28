"use strict";



function get_questions_from_local_storage() {
    const storedQuestions = localStorage.getItem('question_list');
    const question_list = storedQuestions ? JSON.parse(storedQuestions) : null;

    return {"question_list": question_list};
};


function show_question_summary() {
    let result = get_questions_from_local_storage();
    const question_list = result.question_list;

    const question = document.getElementById("question");
    question.textContent = question_list[question_id].questionText;
    
    const answer1 = document.getElementById("answer1");
    answer1.textContent = question_list[question_id].answers[0];

    const answer2 = document.getElementById("answer2");
    answer2.textContent = question_list[question_id].answers[1];

    const answer3 = document.getElementById("answer3");
    answer3.textContent = question_list[question_id].answers[2];
    
    const answer4 = document.getElementById("answer4");
    answer4.textContent = question_list[question_id].answers[3];

    const answerRight = document.getElementById("answerRight");
    answerRight.textContent = question_list[question_id].correctAnswer;

    const answerUser = document.getElementById("answerUser");
    answerUser.textContent = question_list[question_id].answerUser;
};

show_question_summary();

