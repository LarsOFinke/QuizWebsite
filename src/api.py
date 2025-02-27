from flask import Blueprint, request, jsonify, Response
from .db.crud import (get_all_categories, get_all_topics,
                    add_image, get_image, edit_image, delete_image)
from io import BytesIO

api = Blueprint('api', __name__)


@api.route("/get-categories", methods=["GET"])
def get_categories():
    categories: list[dict] = get_all_categories()   # Fetch all categories to display in the dropdown 
                                                    # {
                                                    # "category_id": category_id, -> str: int
                                                    # "category": category        -> str: str
                                                    # }

    return jsonify({"categories": categories}), 200


@api.route("/get-topics", methods=["GET"])
def get_topics():
    topics: list[dict] = get_all_topics()   # Fetch all topics to display in the dropdown
                                            # {
                                            # "topic_id": topic_id,   -> str: int
                                            # "topic": topic, -> str: str
                                            # "category_id", category_id  -> str: int
                                            # } 

    return jsonify({"topics": topics}), 200


@api.route("/image/<image_id>")
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
