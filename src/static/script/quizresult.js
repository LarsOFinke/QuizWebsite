"use strict";



function get_results_from_local_storage() {
    const storedQuestions = localStorage.getItem('question_list');
    const question_list = storedQuestions ? JSON.parse(storedQuestions) : null;

    const storedResult = localStorage.getItem('result');
    const result = storedResult ? JSON.parse(storedResult) : null;

    return {"question_list": question_list, "result": result};
};


function show_results() {
    const results = get_results_from_local_storage();
    document.getElementById("result").textContent = `${results.result} %`;
}

show_results();




// <table class="centered">
//     <tr>
//         <th>Frage Nr.</th>
//         {% if session.is_admin %}
//             <td>Datenbank ID</td>
//         {% endif %}
//         <th>Richtig / Falsch</th>
//         <th>Quiz-Fragen</th>
//     </tr>

//     {% for question in questions_game %}
//         <tr>
//             <td>{{ loop.index }}</td>
//             {% if session.is_admin %}
//                 <td>{{ question["questionID"] }}</td>
//             {% endif %}
//             <td>{% if question["correctAnswered"] %} Richtig {% else %} Falsch {% endif %}</td>
//             <td><a href="/quizresult/details/{{ loop.index }}" target="_blank">Details</a></td>
//         </tr>
//     {% endfor %}
// </table>
