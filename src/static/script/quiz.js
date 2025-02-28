"use strict";



// <form method="POST" class="centered">
//     <h2>{{ question.questionText }}</h2>
    
//     {% if question.imageID != 0 %}
//         <hr>
//         <div class="centered">
//             <img src="{{ url_for('views.serve_image', image_id=question.imageID) }}" alt="Bild zur Frage">
//         </div>
//     {% endif %}
//         <hr>
    
//         <button class="btn-medium" name="user_answer" value="1">{{question.answer1}}</button>
//         <button class="btn-medium" name="user_answer" value="2">{{question.answer2}}</button>
//         <button class="btn-medium" name="user_answer" value="3">{{question.answer3}}</button>
//         <button class="btn-medium" name="user_answer" value="4">{{question.answer4}}</button>   
// </form>

// // Retrieve the string from localStorage
// const storedData = localStorage.getItem('question_list');
// // Convert the string back into a JSON object
// const jsonObject = storedData ? JSON.parse(storedData) : null;
// console.log(jsonObject);



// function fetchImage(imageId) {
//     const imageUrl = `/serve-image/${imageId}`;  // Flask route URL
    
//     // Use fetch to get the image
//     fetch(imageUrl)
//       .then(response => {
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         return response.blob();  // Convert the response to a Blob (binary data)
//       })
//       .then(blob => {
//         // Create a URL for the Blob and set it as the src of the <img> tag
//         const imgUrl = URL.createObjectURL(blob);
//         document.getElementById('image').src = imgUrl;
//       })
//       .catch(error => {
//         console.error('There was a problem with the fetch operation:', error);
//       });
// };

