from flask import Blueprint, request, jsonify, Response
from .db.crud import (get_all_categories, get_category_name,
                    get_all_topics, get_topic_name, get_topics_by_category,
                    get_highscores_full, get_highscores_category, get_highscores_topic,
                    get_all_questions, get_questions_by_topic,
                    add_image, get_image, edit_image, delete_image)
from .models.questions import provide_questions, prepare_question_list
from .utils.utility_quiz_result import compare_user_answers_with_correct, calculate_quiz_result, add_result_to_highscores
from io import BytesIO

api = Blueprint('api', __name__)


@api.route("/get-categories", methods=["GET"])
def get_categories():
    categories: list[dict] = get_all_categories()   # {
                                                    # "category_id": category_id, -> str: int
                                                    # "category": category        -> str: str
                                                    # }

    return jsonify({"categories": categories}), 200


@api.route("/get-topics", methods=["GET"])
def get_topics():
    topics: list[dict] = get_all_topics()   # {
                                            # "topic_id": topic_id,   -> str: int
                                            # "topic": topic, -> str: str
                                            # "category_id", category_id  -> str: int
                                            # } 

    return jsonify({"topics": topics}), 200


@api.route("/get-questions", methods=["POST"])
def get_questions():
    data: dict = request.get_json() # {
                                    # "mode": "mode",   -> str: str
                                    # "id": id  - > str: int
                                    # }

    question_amount: int = data.get("question_amount") 
    
    match data.get("mode"):
        case "full":
            questions: dict = get_all_questions()
            question_list: list[dict] = provide_questions(questions)
        
        case "category":    ### IMPLEMENT THIS ###
            topics: dict = get_topics_by_category(data.get("id"))
        
        case "topic":
            questions: dict = get_questions_by_topic(data.get("id"))
            question_list: list[dict] = provide_questions(questions)
        
    question_list = prepare_question_list(question_list, question_amount)
    
    return jsonify({"questions": question_list}), 200


@api.route("/serve-image/<image_id>", methods=["GET", "POST"])
def serve_image(image_id: str):
    """This route serves to return an image to HTML. Implement it as a src={{ url_for('serve_image', question_id=XXX) }}.

    Args:
        image_id (str): String of the image_id from the database.

    Returns:
        A HTML-readable response of an images binary data.
    """
    image_binary = get_image(int(image_id))    # Retreive the image-binary from the database
    image_stream = BytesIO(image_binary) # Use io.BytesIO to wrap binary data
    return Response(image_stream, mimetype='image/jpeg')    # Return the image as a response with the correct MIME type


@api.route("/process-quiz-result", methods=["POST"])
def process_quiz_result():
    data: dict = request.get_json()
    
    question_list: list[dict] = data.get("question_list")
    question_list = compare_user_answers_with_correct(question_list)

    result: float = calculate_quiz_result(question_list)
    
    add_result_to_highscores(data, result)

    return jsonify({ "question_list": question_list, "result": result }), 200


@api.route("/get-highscores", methods=["POST"])
def get_highscores():
    data: dict = request.get_json() # {
                                    # "mode": mode,
                                    # "category": category,
                                    # "topic": topic
                                    # }
                                    
    highscores: list[dict] = [] # {
                                # "name": name,
                                # "score": score,
                                # "date": date
                                # }
    
    mode: str = data.get("mode")
    match mode:
        case "full":
            highscores = get_highscores_full()  

        case "categ":
            category: str = data.get("category");
            category = get_category_name(category)
            highscores = get_highscores_category(category)
        
        case "topic":
            category: str = data.get("category");
            category = get_category_name(int(category))
            topic: str = data.get("topic")
            topic = get_topic_name(int(topic))
            highscores = get_highscores_topic(category, topic)

    
    return jsonify({"highscores": highscores}), 200
