from ..db.crud import get_answers, get_image_id
from random import shuffle

    

def create_question(questionID: int, questionText: str, answers: list[str], imageID: int) -> dict:
    """This function combines the data pulled from the database to a complete question.

    Args:
        questionID (int): The question_id from the database.
        questionText (str): Question text from the database.
        answers (list[str]): Answers 1-4 from the database for the question in a list.
        imageID (int): ID of the image in the database - 0 if doesnt exist.

    Returns:
        dict: Returns a dictionary resembling a question.
    """
    return {
        "questionID": questionID,
        "questionText": questionText,
        "answers": answers,
        "imageID": imageID,
        "answerUser": 0,
    }


def provide_questions(questions: dict) -> list[dict]:
    """Builds the questions pulled from the database and servers them in JSON-format to be used in the frontend.

    Args:
        questions (dict): Questions pulled from the database. {"question": id}

    Returns:
        list[dict]: Returns a list of dictionaries aka JSON containing the questions for the current quiz.
    """
    questions_provided: list = []
    for questionID, question in questions.items():
        questionText = question
        answers = get_answers(questionID)  # Get answers for the current question
        imageID = int(get_image_id(questionID))
        
        questions_provided.append(create_question(questionID, questionText, answers, imageID))
    
    return questions_provided
    

def prepare_question_list(question_list: list[dict], question_amount: int) -> list[dict]:
    shuffle(question_list)    
    
    return question_list




if __name__ == "__main__":    

    pass