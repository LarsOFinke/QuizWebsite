from flask import Blueprint, request, jsonify, Response
from .db.crud import (get_all_categories, get_category_name,
                    get_all_topics, get_topic_name,
                    get_highscores_full, get_highscores_category, get_highscores_topic,
                    add_image, get_image, edit_image, delete_image)
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


@api.route("/image/<image_id>", methods=["GET"])
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



@api.route("/get-highscores", methods=["POST", "GET"])
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
