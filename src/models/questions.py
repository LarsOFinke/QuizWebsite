from ..db.crud import get_answers, get_correct_answer, get_all_questions, get_image



def check_if_has_image(question_id: int) -> bool:
    try:
        get_image(question_id)
        return True
    
    except:
        return False
    

def create_question(questionID: int, questionText: str, answer1: str, answer2: str, answer3: str, answer4: str, answerRight: int, has_image: bool):
    return {
        "questionID": questionID,
        "questionText": questionText,
        "answer1": answer1,
        "answer2": answer2,
        "answer3": answer3,
        "answer4": answer4,
        "answerRight": answerRight,
        "hasImage": has_image,
        "answerUser": 0,
        "correctAnswered": False
    }


def provide_questions(questions: dict) -> list[dict]:
    questions_provided: list = []
    for question, questionID in questions.items():
        questionText = question
        answers = get_answers(questionID)  # Get answers for the current question
        answer1 = answers[0]
        answer2 = answers[1]
        answer3 = answers[2]
        answer4 = answers[3]
        answerRight = get_correct_answer(questionID)
        has_image = check_if_has_image(questionID)
        
        questions_provided.append(create_question(questionID, questionText, answer1, answer2, answer3, answer4, answerRight, has_image))
    
    return questions_provided
    



if __name__ == "__main__":    
    # print(provide_questions(get_all_questions()))
    # print(check_if_has_image(1))
    # print(check_if_has_image(2))
    pass