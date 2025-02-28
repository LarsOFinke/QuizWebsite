from datetime import datetime
from ..db.crud import get_correct_answer, get_category_name, get_category_idref, get_topic_name, add_highscore



def compare_user_answers_with_correct(question_list: list[dict]) -> list[dict]:
    for question in question_list:
        correct_answer: int = int(get_correct_answer(question.get("questionID")))
        question["correctAnswer"] = correct_answer
        
        if int(question.get("answerUser")) == correct_answer:
            question["correctAnswered"] = True
            
        else:
            question["correctAnswered"] = False
            
    return question_list


def calculate_quiz_result(question_list) -> float:
    question_count: int = len(question_list)
    score: int = 0
    
    for question in question_list:
        if question["correctAnswered"]:
            score += 1
    
    return round(((score / question_count) * 100), 2)
    

def add_result_to_highscores(payload, result):
    match payload["game_mode"]:
        case "full":
            category_played: str = "full"
            topic_played: str = "full"
            
        case "categ":
            category_played: str = get_category_name(int(payload["category_id"]))
            topic_played: str = "all"
            
        case "topic":
            category_id: int = get_category_idref(int(payload['topic_id']))
            category_played: str = get_category_name(category_id)
            topic_played: str = get_topic_name(int(payload['topic_id']))
        
    current_date: str = datetime.now().strftime("%Y-%m-%d")
    
    add_highscore(payload["username"], payload["game_mode"], category_played, topic_played, result, current_date)