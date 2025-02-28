from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .db.crud import (add_category, get_all_categories,
                  add_topic, get_topics_by_category, get_questions_by_topic,
                  add_question, get_question, get_question_id, edit_question, delete_question,
                  add_answers, get_answers_id, get_answers, get_correct_answer, edit_answers, delete_answers)



views = Blueprint('views', __name__)



@views.route("/")
def home():
    if "username" in session:
        return redirect(url_for("views.selection"))
    
    return render_template("login.html")


@views.route('/selection')
def selection():
    return render_template('selection.html')


@views.route('/quiz')
def quiz():
    #         match session["game_mode"]:
    #             case "full":
    #                 category_played: str = "full"
    #                 topic_played: str = "full"
                    
    #             case "categ":
    #                 category_played: str = get_category_name(session["category_id"])
    #                 topic_played: str = "all"
                    
    #             case "topic":
    #                 category_played: str = get_category_name(session["category_id"])
    #                 topic_played: str = get_topic_name(session['topic_id'])
              
    #         current_date: str = datetime.now().strftime("%Y-%m-%d")
    #         add_highscore(session["username"], session["game_mode"], category_played, topic_played, result, current_date)

    return render_template('quiz.html')


@views.route('/quizresult')
def quiz_result(): 
    return render_template('quiz_result.html')


@views.route("/quizresult/details/<question_index>")
def quiz_result_details(question_index: str):
    question_id: int = int(question_index)-1
    return render_template("quiz_result_details.html", question_id=question_id)


@views.route("/quizdb/addcatstops", methods=["GET", "POST"])
def quizdb_catstops():
    if "is_admin" not in session or not session["is_admin"]:
        return redirect("/")
        
    categories: dict = get_all_categories()  # Fetch all categories to display in the dropdown - {"name": id}   
    
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
                   
            # If no add-button has been pressed, the category must have been selected for a topic to be added 
            case _:
                if 'category' in request.form:  # Category was selected
                    session["db_category_id"] = int(request.form.get('category'))   # Save the selected category-ID in the session
                        
                    for category, categ_id in categories.items():   # Iterate over the categories-dictionary from the DB
                        if categ_id == session["db_category_id"]:   # Find the selected category name
                            session["db_selected_category"] = category    # Save the selected category-name in the session
                            break
        
        
    return render_template("quizdb_add_catstops.html", categories=categories)


@views.route('/quizdb/addquestions', methods=['GET','POST'])
def quizdb_addquestions():
    ### CHECK IF ADMIN, if not --> redirect back to Login-Page ###
    if "is_admin" not in session or not session["is_admin"]:
        return redirect("/")
    
    categories: dict = get_all_categories()  # Fetch all categories to display in the dropdown - {"name": id} 
    
    if request.method == 'POST':
        if 'category' in request.form:
            ### RESET SESSION VALUES ###
            if "db_topic_id" in session:
                session.pop("db_topic_id"); session.pop("db_selected_topic")
            
            session["db_category_id"] = int(request.form.get('category') )      # Get category_id from the form and save it in the session
            
            for category, categ_id in categories.items():       # Iterate over the topics-dictionary from the DB
                if categ_id == session["db_category_id"]:       # Find the selected topic name
                    session["db_selected_category"] = category  # Save the selected topic-name in the session
                    break
            
            topics: dict = get_topics_by_category(session["db_category_id"])    # Fetch topics based on selected category - {"name": id}
            
            return render_template('quizdb_add_questions.html', categories=categories, topics=topics)
        
            
        elif 'topic' in request.form:
            ### FETCH DATA FROM THE FORM ###
            session['db_topic_id'] = int(request.form.get('topic'))
            question: str = request.form.get('question')
            answer_1: str = request.form.get('answer1')
            answer_2: str = request.form.get('answer2')
            answer_3: str = request.form.get('answer3')
            answer_4: str = request.form.get('answer4')
            answer_Correct: int = request.form.get('correct')

            topics: dict = get_topics_by_category(session["db_category_id"])    # Fetch topics based on selected category - {"name": id}
            for topic, topic_id in topics.items():          # Iterate over the topics-dictionary from the DB
                if topic_id == session['db_topic_id']:      # Find the selected topic name
                    session["db_selected_topic"] = topic    # Save the selected topic-name in the session
                    break
            
            action: str = request.form.get('quiz_db')
            match action:
                case "add":
                    question_id: int = get_question_id(question)
                    add_question(question, int(session["db_topic_id"]))
                    add_answers(answer_1, answer_2, answer_3, answer_4, answer_Correct, question_id)
                    flash("Question successfully added!", "info")
                    
            return render_template('quizdb_add_questions.html', categories=categories, topics=topics)
        
        
    return render_template('quizdb_add_questions.html', categories=categories)


@views.route("/quizdb/editquestions", methods=["GET", "POST"])
def quizdb_editquestions():
    ### CHECK IF ADMIN, if not --> redirect back to Login-Page ###
    if "is_admin" not in session or not session["is_admin"]:
        return redirect("/")
        
    categories: dict = get_all_categories()     # Fetch all categories to display in the dropdown - {"category": id}
    
    if request.method == 'POST':
        if 'category' in request.form:
            ### RESET SESSION VALUES ###
            if "db_topic_id" in session:
                session.pop("db_topic_id"); session.pop("db_selected_topic")
            if "db_question_ids" in session:
                session.pop("db_question_ids")
            if "db_question_number" in session:
                session.pop("db_question_number")
            
            session["db_selected_category_id"] = int(request.form.get('category')) # Get category_id from the form and save it in the session
            for category, categ_id in categories.items():                       # Iterate over the categories-dictionary from the DB
                if categ_id == session["db_selected_category_id"]:                 # Find the selected category name
                    session["db_selected_category"] = category                  # Save the selected category-name in the session
                    break
            
            topics: dict = get_topics_by_category(session["db_selected_category_id"])  # Fetch topics based on selected category - {"topic_name" : topic_id}
            
            return render_template('quizdb_edit_questions.html', categories=categories, topics=topics)
                                   
            
        elif 'topic' in request.form:
            ### RESET SESSION VALUES ###
            if "db_question_ids" in session:
                session.pop("db_question_ids")
            if "db_question_number" in session:
                session.pop("db_question_number")
            
            session['db_topic_id'] = int(request.form.get('topic'))  # Save the selected topic-ID in the session
            
            topics: dict = get_topics_by_category(session["db_selected_category_id"])  # Fetch topics based on selected category - {"topic_name" : topic_id}
            for topic, topic_id in topics.items():          # Iterate over the topics-dictionary from the DB
                if topic_id == session['db_topic_id']:      # Find the selected topic name
                    session["db_selected_topic"] = topic    # Save the selected topic-name in the session
                    break
            
            i: int = 1
            session["db_question_ids"] = {}
            questions: dict = get_questions_by_topic(session['db_topic_id']) # Get all questions for selected topic -> {"question": id}
            for question, db_question_id in questions.items():
                session["db_question_ids"][i] = db_question_id # {frontend_id : db_id}
                i += 1
                
            return render_template('quizdb_edit_questions.html', categories=categories, topics=topics)
                
                
        elif "question_nr" in request.form:
            ### FETCH FORM AUTOFILL INFORMATION FROM THE DB ###
            session["db_question_number"] = int(request.form.get("question_nr"))
            question_id: int = session["db_question_ids"][session["db_question_number"]]
            question: str = get_question(question_id) 
            answers: list = get_answers(question_id)
            correct_answer = get_correct_answer(question_id)
            
            topics: dict = get_topics_by_category(session["db_selected_category_id"])  # Fetch topics based on selected category - {"topic_name" : topic_id}
            for topic, topic_id in topics.items():          # Iterate over the topics-dictionary from the DB
                if topic_id == session['db_topic_id']:      # Find the selected topic name
                    session["db_selected_topic"] = topic    # Save the selected topic-name in the session
                    break

            action: str = request.form.get('quiz_db')
            match action:       
                
                case "edit":
                    ### FETCH DATA FROM THE FORM ###
                    question: str = request.form.get('question')
                    answer_1: str = request.form.get('answer1')
                    answer_2: str = request.form.get('answer2')
                    answer_3: str = request.form.get('answer3')
                    answer_4: str = request.form.get('answer4')
                    answer_Correct: int = request.form.get('correct')
                    answer_id: int = get_answers_id(answer_1, answer_2, answer_3, answer_4, answer_Correct)
                    
                    edit_answers(answer_1, answer_2, answer_3, answer_4, answer_Correct, answer_id)
                    edit_question(question, session['db_topic_id'], question_id)
                    flash("Question successfully edited!", "info")
                    
                    ### RESET SESSION VALUES ###
                    session.pop("db_selected_category_id"); session.pop("db_selected_category"); session.pop("db_topic_id")
                    session.pop("db_selected_topic"); session.pop("db_question_ids"); session.pop("db_question_number")
                    
                case "delete":
                    delete_answers(question_id)
                    delete_question(question_id)
                    flash("Question successfully deleted!", "info")
                    
                    ### RESET SESSION VALUES ###
                    session.pop("db_selected_category_id"); session.pop("db_selected_category"); session.pop("db_topic_id")
                    session.pop("db_selected_topic"); session.pop("db_question_ids"); session.pop("db_question_number")
        
            return render_template('quizdb_edit_questions.html', categories=categories, topics=topics, question=question, answers=answers, correct=correct_answer)


    return render_template('quizdb_edit_questions.html', categories=categories)


@views.route('/highscores')
def highscores():
    return render_template('highscores.html')

