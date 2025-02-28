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

    for (let i=1; i < results.question_list.length; i++) {
        const row = document.createElement("tr");

        const qid = document.createElement("td");
        qid.textContent = i;
        row.insertAdjacentElement("beforeend", qid);

        const correct = document.createElement("td");
        correct.textContent = results.result ? "Richtig" : "Falsch";
        row.insertAdjacentElement("beforeend", correct);

        const details = document.createElement("td");
        const details_link = document.createElement("a");
        details_link.href = `/quizresult/details/${i}`;
        details_link.target = "_blank";
        details_link.textContent = "Details";
        details.insertAdjacentElement("afterbegin", details_link);
        row.insertAdjacentElement("beforeend", details);

        document.querySelector("table").insertAdjacentElement("beforeend", row);
    }
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
