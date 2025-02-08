from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .db.crud import (add_category, get_all_categories, get_category_name,
                  add_topic, get_topics_by_category, get_questions_by_topic, get_topic_name,
                  add_question, get_question, get_question_id, edit_question, delete_question, get_all_questions,
                  add_answers, get_answers_id, get_answers, get_correct_answer, edit_answers, delete_answers,
                  add_highscore, get_highscores_full, get_highscores_category, get_highscores_topic)
from .utils.questions import provide_questions
from datetime import datetime


views = Blueprint('views', __name__)


@views.route('/selection', methods=['GET', 'POST'])
def selection():
    topics = {}
    selected_category_id = None
    # Fetch all categories to display in the dropdown
    categories: dict = get_all_categories()  # {"name": id}

    if request.method == 'POST':
        action: str = request.form.get("start")
        
        if action:
            match action:
                case "full":
                    session["game_mode"] = "full"
                
                case "categ":
                    session["category_id"] = request.form.get('category')
                    session["game_mode"] = "categ"
                
                case "topic":
                    selected_topic_id = request.form.get('topic')
                    session['topic_id'] = selected_topic_id  # Save the selected topic-ID in the session
                    session["game_mode"] = "topic"
                    
            return redirect(url_for('views.quiz'))  # Start the quiz
        
        
        if 'category' in request.form:  # Category was selected
            selected_category_id = request.form.get('category')    # Get category_id from the form
            selected_category_id = int(selected_category_id)
            session["category_id"] = selected_category_id   # Save the selected category-ID in the session
            
            for category, categ_id in categories.items():   # Iterate over the categories-dictionary from the DB
                if categ_id == selected_category_id:   # Find the selected category name
                    selected_category = category
                    session["selected_category"] = selected_category    # Save the selected category-name in the session
                    break
            
            topics = get_topics_by_category(selected_category_id)  # Fetch topics based on selected category


    return render_template('selection.html', categories=categories, topics=topics, selected_category_id=selected_category_id)


@views.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'game_mode' not in session:  # Check if player went through the quiz-"selection"
        return redirect("/selection")
      
    match session["game_mode"]: # Match the selected game mode to receive questions from the database
        case "full":
            questions: dict = get_all_questions()  # {"Question": QuestionID} | str: int
            
        case "categ":
            questions: dict = {}    # {"Question": QuestionID} | str: int
            topics: dict = get_topics_by_category(session["category_id"])
            for topic, topic_id in topics.items():
                questions.update(get_questions_by_topic(topic_id))  

        case "topic":                          
            questions: dict = get_questions_by_topic(session['topic_id'])  # {"Question": QuestionID} | str: int
    
    if "question_count" not in session: # Initialize quiz-session       
        session.pop("questions_game", None)
        session["questions_game"] = provide_questions(questions) # Create the Questions (list containing dictionaries)
        session["question_count"] = len(session["questions_game"])
        session['current_question'] = 0
        session['score'] = 0
        
    if request.method == 'POST':    # User pressed an answer-button
        user_answer = int(request.form.get("user_answer"))
        if session["questions_game"][session['current_question']]["answerRight"] == user_answer:
            session['score'] += 1
            session["questions_game"][session['current_question']]["correctAnswered"] = True

        session["questions_game"][session['current_question']]["answerUser"] = user_answer
        session['current_question'] += 1    # Move to the next question

            
        if session['current_question'] >= session["question_count"]:   # If all questions have been answered, reset the session and calculate result
            result: float = round(((session['score'] / session["question_count"]) * 100), 2)
            
            match session["game_mode"]:
                case "full":
                    category_played: str = "full"
                    topic_played: str = "full"
                    
                case "categ":
                    category_played: str = get_category_name(session["category_id"])
                    topic_played: str = "all"
                    
                case "topic":
                    category_played: str = get_category_name(session["category_id"])
                    topic_played: str = get_topic_name(session['topic_id'])
                    
            current_date: str = datetime.now().strftime("%Y-%m-%d")
            
            add_highscore(session["username"], session["game_mode"], category_played, topic_played, result, current_date)
            
            questions_game: list = session["questions_game"]
            
            # Clear the session variables
            session.pop('category_id', None)
            session.pop('topic_id', None)
            session.pop('game_mode', None)
            session.pop("question_count", None)
            session.pop('current_question', None)  
            session.pop('score', None) 
            
            return render_template('quiz_result.html', result=result, questions_game=questions_game)  # Render the results page

    current_question = session["questions_game"][session['current_question']]

    
    return render_template('quiz.html', question=current_question)


@views.route('/quizresult')
def quiz_result():
    
    return render_template('quiz_result.html')


@views.route("/quizresult/details/<question_index>")
def quiz_result_details(question_index: str):
    question = session["questions_game"][int(question_index)-1]
    
    return render_template("quiz_result_details.html", question=question)


@views.route("/quizdb/addcatstops", methods=["GET", "POST"])
def quizdb_catstops():
    if "is_admin" not in session or not session["is_admin"]:
        return redirect("/")
        
    selected_category_id = None
    categories: dict = get_all_categories()  # {"name": id}   # Fetch all categories to display in the dropdown
    
    if request.method == 'POST':
        action: str = request.form.get('catstops')
        match action:
            case "category":
                new_category: str = request.form.get("new_category")
                add_category(new_category)
                flash("Successfully added new category!", "info")
                
            case "topic":
                new_topic: str = request.form.get("new_topic")
                add_topic(new_topic, session["db_category_id"])
                flash("Successfully added new topic!", "info")
                    
            case _:
                if 'category' in request.form:  # Category was selected
                    selected_category_id = request.form.get('category')    # Get category_id from the form
                    selected_category_id = int(selected_category_id)
                    session["db_category_id"] = selected_category_id   # Save the selected category-ID in the session
                        
                    for category, categ_id in categories.items():   # Iterate over the categories-dictionary from the DB
                        if categ_id == selected_category_id:   # Find the selected category name
                            selected_category = category
                            session["db_selected_category"] = selected_category    # Save the selected category-name in the session
                            break
        
        
    return render_template("quizdb_add_catstops.html", categories=categories)


@views.route('/quizdb/addquestions', methods=['GET','POST'])
def quizdb_addquestions():
    if "is_admin" not in session or not session["is_admin"]:
        return redirect("/")
    
    topics = {}
    
    selected_category_id = None
    categories: dict = get_all_categories()  # {"name": id}   # Fetch all categories to display in the dropdown
    
    if request.method == 'POST':
        if 'category' in request.form:  # Category was selected
            selected_category_id = request.form.get('category')    # Get category_id from the form
            selected_category_id = int(selected_category_id)
            session["db_category_id"] = selected_category_id   # Save the selected category-ID in the session
            
            for category, categ_id in categories.items():   # Iterate over the categories-dictionary from the DB
                if categ_id == selected_category_id:   # Find the selected category name
                    session["db_selected_category"] = category    # Save the selected category-name in the session
                    break
            
            topics = get_topics_by_category(selected_category_id)  # Fetch topics based on selected category # {"name": id} -> str: int
            
        elif 'topic' in request.form:   # Topic was selected
            selected_topic_id = request.form.get('topic')
            session['db_topic_id'] = selected_topic_id  # Save the selected topic-ID in the session
            
            question: str = request.form.get('question')
            answer_1: str = request.form.get('answer1')
            answer_2: str = request.form.get('answer2')
            answer_3: str = request.form.get('answer3')
            answer_4: str = request.form.get('answer4')
            answer_Correct: int = request.form.get('correct')

            topics = get_topics_by_category(session["db_category_id"])
            for topic, topic_id in topics.items():
                if topic_id == int(selected_topic_id):
                    session["db_selected_topic"] = topic
                    break
            
            action: str = request.form.get('quiz_db')
        
            match action:
                case "add":
                    add_question(question, int(session["db_topic_id"]))
                    question_id: int = get_question_id(question)
                    add_answers(answer_1, answer_2, answer_3, answer_4, answer_Correct, question_id)
                    flash("Question successfully added!", "info")
        
        
    return render_template('quizdb_add_questions.html', categories=categories, topics=topics)


@views.route("/quizdb/editquestions", methods=["GET", "POST"])
def quizdb_editquestions():
    if "is_admin" not in session or not session["is_admin"]:
        return redirect("/")
    
    if "topics" not in session:
        session["topics"] = {} # {"topic": id}
    
    if "question_ids" not in session:
        session["question_ids"]= {} # {question_id: db_question_id}
        
    if "quest" not in session:
        session["quest"] = ""
        
    if "answers" not in session:
        session["answers"] = []
    
    if "correct_answer" not in session:
        session["correct_answer"] = 0
        
    selected_category_id = None
    categories: dict = get_all_categories()  # {"category": id}   # Fetch all categories to display in the dropdown
    
    if request.method == 'POST':
        if 'category' in request.form:  # Category was selected
            # RESET SESSION VALUES
            session["topics"] = {}
            session["question_ids"]= {}
            session["quest"] = ""
            session["answers"] = []
            session["correct_answer"] = 0
            
            selected_category_id = request.form.get('category')    # Get category_id from the form
            selected_category_id = int(selected_category_id)
            session["db_category_id"] = selected_category_id   # Save the selected category-ID in the session
            
            for category, categ_id in categories.items():   # Iterate over the categories-dictionary from the DB
                if categ_id == selected_category_id:   # Find the selected category name
                    selected_category = category
                    session["db_selected_category"] = selected_category    # Save the selected category-name in the session
                    break
            
            topics = get_topics_by_category(selected_category_id)  # Fetch topics based on selected category
            session["topics"] = topics
            
        elif 'topic' in request.form:   # Topic was selected
            selected_topic_id = request.form.get('topic')
            selected_topic_id = int(selected_topic_id)
            session['db_topic_id'] = selected_topic_id  # Save the selected topic-ID in the session
            
            for topic, topic_id in session["topics"].items():   # Iterate over the categories-dictionary from the DB
                if topic_id == selected_topic_id:   # Find the selected category name
                    selected_topic = topic
                    session["db_selected_topic"] = selected_topic    # Save the selected topic-name in the session
                    break
            
            questions:dict = get_questions_by_topic(selected_topic_id) # Get all questions for selected topic -> {"question": id}
            i: int = 0
            for question, db_question_id in questions.items():
                i += 1
                session["question_ids"][i] = db_question_id # {frontend_id: db_id}
                
        elif "question_nr" in request.form:
            selected_question_nr = request.form.get("question_nr")
            selected_question_nr = int(selected_question_nr)
            session["db_question_number"] = selected_question_nr
            question_id: int = session["question_ids"][str(selected_question_nr)]

            session["quest"] = get_question(question_id) 
            session["answers"] = get_answers(question_id)
            session["correct_answer"] = get_correct_answer(question_id)

            action: str = request.form.get('quiz_db')
            match action:       
                case "edit":
                    question: str = request.form.get('question')
                    answer_1: str = request.form.get('answer1')
                    answer_2: str = request.form.get('answer2')
                    answer_3: str = request.form.get('answer3')
                    answer_4: str = request.form.get('answer4')
                    answer_Correct: int = request.form.get('correct')
                    
                    edit_question(question, session['db_topic_id'], question_id)
                    
                    answer_id: int = get_answers_id(answer_1, answer_2, answer_3, answer_4, answer_Correct)
                    edit_answers(answer_1, answer_2, answer_3, answer_4, answer_Correct, answer_id)
                    # RESET SESSION VALUES
                    session["topics"] = {}
                    session["question_ids"]= {}
                    session["quest"] = ""
                    session["answers"] = []
                    session["correct_answer"] = 0
                    session["db_question_number"] = 0
                    flash("Question successfully edited!", "info")
                    
                case "delete":
                    delete_answers(question_id)
                    delete_question(question_id)
                    # RESET SESSION VALUES
                    session["topics"] = {}
                    session["question_ids"]= {}
                    session["quest"] = ""
                    session["answers"] = []
                    session["correct_answer"] = 0
                    session["db_question_number"] = 0
                    flash("Question successfully deleted!", "info")
        
        
    return render_template('quizdb_edit_questions.html', categories=categories, topics=session["topics"], question_ids=session["question_ids"], quest=session["quest"], answers=session["answers"], correct=session["correct_answer"])


@views.route('/highscores', methods=['GET', 'POST'])
def highscores():
    highscores: list = []
    
    if "highscore_mode" not in session:
        session["highscore_categories"] = {}
        session["highscore_topics"] = {}      
    
    # Handle POST request
    if request.method == 'POST':
        if "mode" in request.form:
            session["highscore_mode"] = request.form.get("mode")
            
            if session["highscore_mode"] != "full":
                session["highscore_categories"] = get_all_categories()  # Update categories from the function      

            else:   # Reset dictionaries if the mode is 'full'
                highscores = get_highscores_full()
                session["highscore_categories"] = {}
                session["highscore_topics"] = {}  
        

        if "category" in request.form:
            session["highscore_category_name"] = request.form.get("category")

            # Update the category ID based on the selected category
            if session["highscore_category_name"] in session["highscore_categories"]:
                session["highscore_category_id"] = session["highscore_categories"][session["highscore_category_name"]]
                
                if session["highscore_mode"] == "topic":
                    session["highscore_topics"] = get_topics_by_category(session["highscore_category_id"])
                    session["highscore_topic_name"] = None
                
                else:
                    highscores = get_highscores_category(session["highscore_category_name"])
                    
        if "topic" in request.form:
            session["highscore_topic_name"] = request.form.get("topic") 
            highscores = get_highscores_topic(session["highscore_category_name"], session["highscore_topic_name"])
    
    # Render the template with default categories and topics
    return render_template('highscores.html', categories=session["highscore_categories"], topics=session["highscore_topics"], highscores=highscores)