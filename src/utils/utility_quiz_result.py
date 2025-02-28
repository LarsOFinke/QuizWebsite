from ..db.crud import get_correct_answer



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
    question_count = len(question_list)
    score = 0
    
    for question in question_list:
        if question["correctAnswered"]:
            score += 1
    
    return round(((score / question_count) * 100), 2)
    
    