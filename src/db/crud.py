import sqlite3, os, sys # FOR DB
from typing import Any, List, Tuple, Optional   # FOR "execute_query" FUNCTIONS
from .. import logging  # GET .ENV CONSTANTS AND LOGGING
from ..utils.utility import image_to_binary
from werkzeug.security import generate_password_hash, check_password_hash # LOGIN-SYSTEM SECURITY


# SET DB-Connection String
CONNECTIONSTRING_LOGIN = os.path.join(os.path.dirname(__file__), "LoginDB.db")
CONNECTIONSTRING_QUIZ = os.path.join(os.path.dirname(__file__), "QuizDB.db")
CONNECTIONSTRING_SCORES = os.path.join(os.path.dirname(__file__), "ScoresDB.db")


# SET DEFAULT RETURN VALUES FOR CRUD
DEFAULT_CATEGORY_ID = -1
DEFAULT_TOPIC_ID = -1
DEFAULT_QUESTION_ID = -1
DEFAULT_ANSWER_ID = -1



def create_login_db() -> bool:
    try:
        con = sqlite3.connect(CONNECTIONSTRING_LOGIN)
        cursor = con.cursor()
        with con:
            sql: str = "CREATE TABLE tblLogin(" \
                        "LoginID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                        "LoginUsername TEXT NOT NULL UNIQUE, " \
                        "LoginPassword TEXT NOT NULL, " \
                        "LoginType TEXT NOT NULL)"
            cursor.execute(sql)
            
        return True
    
    except:
        logging.error("Could not create login-database!")
        return False
    
def create_admins() -> bool:
    try:
        con = sqlite3.connect(CONNECTIONSTRING_LOGIN)
        cursor = con.cursor()
        with con:
            hashed_password = generate_password_hash("admin", method='pbkdf2:sha256')
            sql: str = "INSERT INTO tblLogin(LoginUsername, LoginPassword, LoginType) VALUES ('admin', ?, 'admin')"
            cursor.execute(sql, (hashed_password,))
        return True

    except sqlite3.Error as e:
        logging.error(e)

    except:
        logging.error("Could not create admins for some reason!")
        return False

def create_quiz_db() -> bool:
    try:
        con = sqlite3.connect(CONNECTIONSTRING_QUIZ)
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        con.commit()
    
        with con:
            sql: str = "CREATE TABLE tblCategory(" \
                        "CategoryID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                        "CategoryName TEXT NOT NULL UNIQUE)"
            cursor.execute(sql)
            
            sql: str = "CREATE TABLE tblTopic(" \
                        "TopicID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                        "TopicName TEXT NOT NULL," \
                        "CategoryIDRef INTEGER, " \
                        "FOREIGN KEY(CategoryIDRef) REFERENCES tblCategory(CategoryID))"
            cursor.execute(sql)
            
            sql: str = "CREATE TABLE tblQuestion(" \
                        "QuestionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                        "QuestionText TEXT NOT NULL, " \
                        "TopicIDRef INTEGER, " \
                        "ImageIDRef INTEGER" \
                        "FOREIGN KEY(TopicIDRef) REFERENCES tblTopic(TopicID))"
            cursor.execute(sql)
            
            sql: str = "CREATE TABLE tblAnswers(" \
                        "AnswerID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                        "Answer1 TEXT NOT NULL, " \
                        "Answer2 TEXT NOT NULL, " \
                        "Answer3 TEXT NOT NULL, " \
                        "Answer4 TEXT NOT NULL, " \
                        "AnswerCorrect INTEGER NOT NULL, " \
                        "QuestionIDRef INTEGER, " \
                        "FOREIGN KEY(QuestionIDRef) REFERENCES tblQuestion(QuestionID))"
            cursor.execute(sql)
            
            sql: str = "CREATE TABLE tblImages(" \
                        "ImageID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                        "ImageBinary BLOB)"
            cursor.execute(sql)
            
            return True
            
    except:
        return False

def create_scores_db() -> bool:
    try:
        with sqlite3.connect(CONNECTIONSTRING_SCORES) as con:
            cursor = con.cursor()
            sql: str = "CREATE TABLE tblScores(" \
                        "ScoreID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                        "ScoreUsername TEXT NOT NULL, " \
                        "ScoreMode TEXT NOT NULL, " \
                        "ScoreCategory TEXT NOT NULL, " \
                        "ScoreTopic TEXT NOT NULL, " \
                        "ScoreHighscore REAL NOT NULL, " \
                        "ScoreDate TEXT NOT NULL)"
            cursor.execute(sql)
            
            return True
    
    except:
        return False

if not os.path.exists(CONNECTIONSTRING_LOGIN):
    if not create_login_db():
        logging.error("Could not create login-database! Something went wrong...")
        sys.exit()
    if not create_admins():
        logging.error("Could not create admins! Something went wrong...")
        sys.exit()
 
if not os.path.exists(CONNECTIONSTRING_QUIZ):
    if not create_quiz_db():
        logging.error("Could not create quiz-database! Something went wrong...")
        sys.exit()

if not os.path.exists(CONNECTIONSTRING_SCORES):
    if not create_scores_db():
        logging.error("Could not create scores-database! Something went wrong...")
        sys.exit()

 
 
 
# EXECUTE SQL WITH PARAMS
def execute_query(sql: str, params: Tuple[Any, ...], connectionstring: str, fetch: bool = False) -> Optional[List[Tuple]]:
    """Executes a SQL command with the provided parameters.

    This function connects to the SQLite database, executes the specified SQL command with the given parameters,
    and optionally fetches the results based on the `fetch` argument. 

    Args:
        sql (str): The SQL-Command to be executed. This can be any valid SQL statement such as 
                   SELECT, INSERT, UPDATE, or DELETE.
                   
        connectionstring (str): The DB-Connection-String used for the query
                   
        params (Tuple[Any, ...]): A tuple containing the parameters to bind to the SQL command. 
                                The number and types of parameters should match the placeholders in the SQL statement.
                                
        fetch (bool, optional): If True, the function fetches and returns all rows of the result set as a list of tuples.
                                If False, it returns a boolean indicating whether any rows were affected by 
                                the SQL command (True for affected, False for none). Defaults to False.
    Returns:
        Optional[List[Tuple]]: 
            - If `fetch` is True, returns a list of tuples where each tuple represents a row fetched from the database. 
              Returns an empty list if no rows were returned.
            - If `fetch` is False, returns a boolean value:
              - True if the SQL command affected one or more rows.
              - False if no rows were affected.
            - Returns None if an error occurs during execution.

    """
    try:
        with sqlite3.connect(connectionstring) as con:
            cursor = con.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            con.commit()
            cursor.execute(sql, params)
            
            if fetch:
                return cursor.fetchall()  # Return fetched results
            
            else:
                return cursor.rowcount > 0  # Return True for insert/update/delete if any rows affected, else False
            
    except sqlite3.Error as e:
        logging.error(f"An error occurred: {e}")
        return None  # Return None in case of error

# EXECUTE SQL WITHOUT PARAMS
def execute_query_get_all(sql: str, connectionstring: str) -> dict:
    results: dict = {}  # {id: "name"} -> int: str
    try:
        with sqlite3.connect(connectionstring) as con:
            cursor = con.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            con.commit()
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            for row in rows:
                results[row[0]] = row[1]
                
            return results
        
    except sqlite3.error as e:
        logging.error(f"An error occured: {e}")
        return results




#-- CRUD FUNCTIONALITY LOGIN --#

def add_login(username: str, password: str) -> bool:
    """
    Returns:
        True: if successfully added
        False: if error happened
    """
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    sql: str = "INSERT INTO tblLogin(LoginUsername, LoginPassword, LoginType) VALUES (?, ?, 'user')"
    return execute_query(sql, (username, hashed_password), CONNECTIONSTRING_LOGIN)
    

def validate_login(username: str, password: str) -> bool:
    """Validates whether a Login is successfull or not

    Args:
        username (str): Username from Frontend
        password (str): Password from Frontend

    Returns:
        True: if Password matches that from the database for the called user
        False: if user not found in the Database OR password does NOT match that from the database for the called user 
    """
    sql: str = "SELECT LoginPassword FROM tblLogin WHERE LoginUsername = ?"
    result = execute_query(sql, (username,), CONNECTIONSTRING_LOGIN, fetch=True)
    
    if not result:
        return False    # No matches for the username
    
    password_db = result[0][0]
    
    if check_password_hash(password_db, password):
        return True # Passwords match
    
    return False    # Password doesn't match with database


def get_all_usernames() -> list:
    """Returns a list containing all usernames in the database"""
    sql: str = "SELECT LoginUsername FROM tblLogin"
    
    with sqlite3.connect(CONNECTIONSTRING_LOGIN) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        usernames: list = [user[0] for user in results]
        
    return usernames




#-- CRUD FUNCTIONALITY QUIZ --#

def add_category(category_name: str) -> bool:
    """
    Returns:
        True: if successfully added
        False: if error happened
    """
    sql: str = "INSERT INTO tblCategory(CategoryName) VALUES (?)"
    return execute_query(sql, (category_name,), CONNECTIONSTRING_QUIZ)


def edit_category(new_category_name: str, category_id: int) -> bool:
    """
    Returns:
        True: if successfully edited
        False: if error happened
    """
    sql: str = "UPDATE tblCategory SET CategoryName = ? WHERE CategoryID = ?"
    return execute_query(sql, (new_category_name, category_id), CONNECTIONSTRING_QUIZ)


def delete_category(category_id: int) -> bool:
    """
    Returns:
        True: if successfully deleted
        False: if error happened
    """
    sql: str = "DELETE FROM tblCategory WHERE CategoryID = ?"
    return execute_query(sql, (category_id,), CONNECTIONSTRING_QUIZ)


def get_all_categories() -> dict:
    """Returns a dictionary containing all categories in the database

    Returns:
        dict: {category_id: "category"} -> int: str
    """
    sql: str = "SELECT CategoryID, CategoryName FROM tblCategory"
    return execute_query_get_all(sql, CONNECTIONSTRING_QUIZ)


def get_category_id(category_name: str) -> int:
    """
    Returns:
        int: ID of the category in the database
    """
    sql = "SELECT CategoryID FROM tblCategory WHERE CategoryName = ?"
    result = execute_query(sql, (category_name,), CONNECTIONSTRING_QUIZ, fetch=True)
    return result[0][0] if result else DEFAULT_CATEGORY_ID  # Returns the ID if results have been found, else -1


def get_category_name(category_id: int) -> str:
    """
    Returns:
        str: name of the category in the database
    """
    sql: str = "SELECT CategoryName FROM tblCategory WHERE CategoryID = ?"
    return execute_query(sql, (category_id,), CONNECTIONSTRING_QUIZ, fetch=True)[0][0]



def add_topic(topic_name: str, category_id: int) -> bool:
    """
    Returns:
        True: if successfully added
        False: if error happened
    """
    sql: str = "INSERT INTO tblTopic(TopicName, CategoryIDRef) VALUES (?, ?)"
    return execute_query(sql, (topic_name, category_id), CONNECTIONSTRING_QUIZ)


def get_all_topics() -> dict:
    """Returns a dictionary containing all topics in the database

    Returns:
        dict: {topic_id: "topic"} -> int: str
    """
    sql: str = "SELECT TopicID, TopicName FROM tblTopic"
    return execute_query_get_all(sql, CONNECTIONSTRING_QUIZ)


def get_topics_by_category(category_id: int) -> dict:
    """Returns a dictionary containing all topics in the database for a given category

    Returns:
        dict: {"topic": topic_id} -> str: int
    """
    topics: dict = {}
    sql: str = "SELECT * FROM tblTopic WHERE CategoryIDRef = ?"
    results = execute_query(sql, (category_id,), CONNECTIONSTRING_QUIZ, fetch=True)
    
    for result in results:
        topics[result[1]] = result[0]
        
    return topics


def get_topic_id(topic_name: str) -> int:
    """
    Returns:
        int: ID of the topic in the database
    """
    sql: str ="SELECT TopicID FROM tblTopic WHERE TopicName = ?"
    result = execute_query(sql, (topic_name,), CONNECTIONSTRING_QUIZ, fetch=True)
    return result[0][0] if result else DEFAULT_TOPIC_ID


def get_topic_name(topic_id: int) -> str:
    """
    Returns:
        str: name of the topic in the database
    """
    sql: str = "SELECT TopicName FROM tblTopic WHERE TopicID = ?"
    return execute_query(sql, (topic_id,), CONNECTIONSTRING_QUIZ, fetch=True)[0][0]


def edit_topic(new_topic_name: str, topic_id: int, category_id: int) -> bool:
    """
    Returns:
        True: if successfully edited
        False: if error happened
    """
    sql: str = "UPDATE tblTopic SET TopicName = ?, CategoryIDRef = ? WHERE TopicID = ?"
    return execute_query(sql, (new_topic_name, category_id, topic_id), CONNECTIONSTRING_QUIZ)


def delete_topic(topic_id: int) -> bool:
    """
    Returns:
        True: if successfully deleted
        False: if error happened
    """
    sql: str = "DELETE FROM tblTopic WHERE TopicID = ?"
    return execute_query(sql, (topic_id,), CONNECTIONSTRING_QUIZ)



def add_question(question: str, topic_id: int, image_id: int = 0) -> bool:
    """
    Returns:
        True: if successfully added
        False: if error happened
    """
    sql: str = "INSERT INTO tblQuestion(QuestionText, TopicIDRef, ImageIDRef) VALUES (?, ?, ?)"
    return execute_query(sql, (question, topic_id, image_id), CONNECTIONSTRING_QUIZ)


def get_question(question_id: int) -> str:
    """
    Returns:
        str: question text
    """
    sql: str = "SELECT QuestionText FROM tblQuestion WHERE QuestionID = ?"
    return execute_query(sql, (question_id,), CONNECTIONSTRING_QUIZ, fetch=True)[0][0]


def get_all_questions() -> dict:
    """Returns a dictionary containing all questions in the database

    Returns:
        dict: {question_id: "question"} -> int: str
    """
    questions: dict = {}
    sql: str = "SELECT QuestionID, QuestionText FROM tblQuestion"
    questions = execute_query_get_all(sql, CONNECTIONSTRING_QUIZ)
        
    return questions


def get_questions_by_topic(topic_id: int) -> dict:
    """Returns a dictionary containing all questions in the database for a given topic

    Returns:
        dict: {"question": question_id} -> str: int
    """
    questions: dict = {}
    sql: str = "SELECT QuestionID, QuestionText FROM tblQuestion WHERE TopicIDRef = ?"
    results = execute_query(sql, (topic_id,), CONNECTIONSTRING_QUIZ, fetch=True)
    
    for result in results:
        questions[result[1]] = result[0]
        
    return questions


def get_question_id(question: str) -> int:
    """
    Returns:
        int: ID of the question in the database
    """
    sql: str = "SELECT QuestionID FROM tblQuestion WHERE QuestionText = ?"
    result = execute_query(sql, (question,), CONNECTIONSTRING_QUIZ, fetch=True)
    return result[0][0] if result else DEFAULT_QUESTION_ID


def edit_question(new_question: str, topic_id: int, question_id: int) -> bool:
    """
    Returns:
        True: if successfully edited
        False: if error happened
    """
    sql: str = "UPDATE tblQuestion SET QuestionText = ?, TopicIDRef = ? WHERE QuestionID = ?"
    return execute_query(sql, (new_question, topic_id, question_id), CONNECTIONSTRING_QUIZ)


def delete_question(question_id: int) -> bool:
    """
    Returns:
        True: if successfully deleted
        False: if error happened
    """
    sql: str = "DELETE FROM tblQuestion WHERE QuestionID = ?"
    return execute_query(sql, (question_id,), CONNECTIONSTRING_QUIZ)



def add_answers(answer1: str, answer2: str, answer3: str, answer4: str, answer_correct: str, question_id: int) -> bool:
    """
    Returns:
        True: if successfully added
        False: if error happened
    """
    sql: str = "INSERT INTO tblAnswers(Answer1, Answer2, Answer3, Answer4, AnswerCorrect, QuestionIDRef) VALUES (?, ?, ?, ?, ?, ?)"
    return execute_query(sql, (answer1, answer2, answer3, answer4, answer_correct, question_id), CONNECTIONSTRING_QUIZ)


def get_answers(question_id: int) -> list:
    """Returns a list containing the possible answers for a given question (by ID in the database)
    Returns:
        list: [answer1, answer2, answer3, answer4]
    """
    answers: list = []
    try:
        with sqlite3.connect(CONNECTIONSTRING_QUIZ) as con:
            cursor = con.cursor()
            sql: str = "SELECT Answer1, Answer2, Answer3, Answer4 FROM tblAnswers WHERE QuestionIDRef = ?"
            
            cursor.execute(sql, (question_id,))
            rows = cursor.fetchall()
            
            for answer in rows:
                answers: list = [answer[0], answer[1], answer[2], answer[3]]
                
            return answers

    except sqlite3.Error as e:
        logging.error(f"An error occured: {e}")
        return answers
    

def get_correct_answer(question_id: int) -> int:
    """Get the correct answer number relevant to the list (answer1 = 1 | answer2 = 2 | answer3 = 3 | answer4 = 4)
    Returns:
        int: correct answer number
    """
    sql: str = "SELECT AnswerCorrect FROM tblAnswers WHERE QuestionIDRef = ?"
    result = execute_query(sql, (question_id,), CONNECTIONSTRING_QUIZ, fetch=True)
    return result[0][0] if result else DEFAULT_ANSWER_ID


def get_answers_id(answer1: str, answer2: str, answer3: str, answer4: str, answer_correct: int) -> int:
    """
    Returns:
        int: ID of the answers in the database
    """
    sql: str = "SELECT AnswerID FROM tblAnswers WHERE Answer1 = ? AND Answer2 = ? AND Answer3 = ? AND Answer4 = ? AND AnswerCorrect = ?"
    result = execute_query(sql, (answer1, answer2, answer3, answer4, answer_correct), CONNECTIONSTRING_QUIZ)
    return result[0][0] if result else DEFAULT_ANSWER_ID


def edit_answers(new_answer1: str, new_answer2: str, new_answer3: str, new_answer4: str, new_answer_correct: str, answer_id: int) -> bool:
    """
    Returns:
        True: if successfully edited
        False: if error happened
    """
    sql: str = "UPDATE tblAnswers SET Answer1 = ?, Answer2 = ?, Answer3 = ?, Answer4 = ?, AnswerCorrect = ? WHERE AnswerID = ?"
    return execute_query(sql, (new_answer1, new_answer2, new_answer3, new_answer4, new_answer_correct, answer_id), CONNECTIONSTRING_QUIZ)


def delete_answers(question_id: int) -> bool:
    """
    Returns:
        True: if successfully deleted
        False: if error happened
    """
    sql: str = "DELETE FROM tblAnswers WHERE QuestionIDRef = ?"
    return execute_query(sql, (question_id,), CONNECTIONSTRING_QUIZ)



def add_image(image_path: str) -> bool :
    """Adds an image in binary form to the database.

    Args:
        image_path (str): Path of the image location to convert.

    Returns:
        True: if successfully deleted
        False: if error happened
    """
    sql: str = "INSERT INTO tblImages(ImageBinary) VALUES (?)"
    image_binary: bytes = image_to_binary(image_path)
    return execute_query(sql=sql, params=(image_binary,), connectionstring=CONNECTIONSTRING_QUIZ)


def get_image(image_id: int) -> bytes:
    """Acces saved images in the SQLite3-database.

    Args:
        image_id (int): ID in the database the image belongs to.

    Returns:
        bytes: Returns the binary data of an image from the DB.
    """
    sql: str = "SELECT ImageBinary FROM tblImages WHERE ImageID = ?"
    return execute_query(sql=sql, params=(image_id,), connectionstring=CONNECTIONSTRING_QUIZ, fetch=True)[0][0]


def get_image_id(question_id: int) -> int:
    """_summary_

    Args:
        question_id (int): Question ID in the database the image belongs to.

    Returns:
        int: The ImageID in the database.
    """
    sql: str = "SELECT ImageIDRef FROM tblQuestion WHERE QuestionID = ?"
    return execute_query(sql=sql, params=(question_id,), connectionstring=CONNECTIONSTRING_QUIZ, fetch=True)[0][0]


def edit_image(image_path: str, question_id: int) -> bool:
    """Updates the image for a question in the database.

    Args:
        image_path (str): Path of the image location to convert.
        question_id (int): The question_id from the database.

    Returns:
        True: if successfully deleted
        False: if error happened
    """
    sql: str = "UPDATE tblImages SET ImageBinary = ? WHERE QuestionIDRef = ?"
    image_binary: bytes = image_to_binary(image_path)
    return execute_query(sql=sql, params=(image_binary, question_id), connectionstring=CONNECTIONSTRING_QUIZ)


def delete_image(question_id: int) -> bool:
    """Delets the image of a question in the database.

    Args:
        question_id (int): The question_id from the database.

    Returns:
        True: if successfully deleted
        False: if error happened
    """
    sql: str = "DELETE FROM tblImages WHERE QuestionIDRef = ?"
    return execute_query(sql=sql, params=(question_id,), connectionstring=CONNECTIONSTRING_QUIZ)




#-- CRUD FUNCTIONALITY SCORES --#

def add_highscore(username: str, mode: str, category: str, topic: str, highscore: float, date: str) -> bool:
    """
    Returns:
        True: if successfully added
        False: if error happened
    """
    sql: str = "INSERT INTO tblScores(ScoreUsername, ScoreMode, ScoreCategory, ScoreTopic, ScoreHighscore, ScoreDate) VALUES (?, ?, ?, ?, ?, ?)"
    return execute_query(sql, (username, mode, category, topic, highscore, date), CONNECTIONSTRING_SCORES)


def get_highscores_full() -> list[tuple]:
    """Get Highscores played with "Full Quiz"-Mode 
    ordered by Highscore in descending order (highest scores first)

    Returns:
        list[tuple]: Returns a list of tuples -> ("name", score, "date")
    
    Example return:
        [('guest', 60.0, '2024-11-11')]
    """
    sql: str = "SELECT ScoreUsername, ScoreHighscore, ScoreDate FROM tblScores WHERE ScoreMode = 'full' ORDER BY ScoreHighscore DESC"
    with sqlite3.connect(CONNECTIONSTRING_SCORES) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        results: list = cursor.fetchall()
        return results


def get_highscores_category(category: str) -> list[tuple]:
    """Get Highscores played with "Category"-Mode 
    ordered by Highscore in descending order (highest scores first)

    Args:
        category (str): Name of the Category

    Returns:
        list[tuple]: Returns a list of tuples -> ("name", score, "date")
        
    Example return:
        [('guest', 60.0, '2024-11-11')]
    """
    sql: str = "SELECT ScoreUsername, ScoreHighscore, ScoreDate FROM tblScores WHERE ScoreMode = 'categ' AND ScoreCategory = ? ORDER BY ScoreHighscore DESC"
    return execute_query(sql, (category,), CONNECTIONSTRING_SCORES, fetch=True)


def get_highscores_topic(category: str, topic: str) -> list[tuple]:
    """Get Highscores played with "Topic"-Mode 
    ordered by Highscore in descending order (highest scores first)

    Args:
        category (str): Name of the Category played
        topic (str): Name of the Topic played

    Returns:
        list[tuple]: Returns a list of tuples -> ("name", score, "date")
        
    Example return:
        [('guest', 60.0, '2024-11-11')]
    """
    sql: str = "SELECT ScoreUsername, ScoreHighscore, ScoreDate FROM tblScores WHERE ScoreMode = 'topic' AND ScoreCategory = ? AND ScoreTopic = ? ORDER BY ScoreHighscore DESC"
    return execute_query(sql, (category, topic), CONNECTIONSTRING_SCORES, fetch=True)




# FOR TESTING FUNCTIONS ONLY
if __name__ == "__main__":
    ### Login ###
    
    # print(get_correct_answer(1))
    # print(add_login("Name", "Password"))
    # print(validate_login("Name", "Password"))
    # print(get_all_usernames())
    
    
    
    ### Quiz ###
    
    # add_category("Python")
    # add_category("SQL")
    # add_category("Projektmanagement")
    # add_category("Wirtschaft")
    
    # add_topic("Grundlagen", 1)
    # add_topic("CRUD-Grundlagen", 2)
    # add_topic("Grundlagen", 3)
    # add_topic("Unternehmensformen", 4)
    
    # print(add_question("Frage1 Python1", 1))
    # print(add_answers("Frage1 Python1 Antwort1", "Frage1 Python1 Antwort2", "Frage1 Python1 Antwort3", "Frage1 Python1 Antwort4", 2, 1))
    # print(add_question("Frage2 Python1", 1))
    # print(add_answers("Frage2 Python1 Antwort1", "Frage2 Python1 Antwort2", "Frage2 Python1 Antwort3", "Frage2 Python1 Antwort4", 2, 2))
    # print(add_question("Frage3 Python1", 1))
    # print(add_answers("Frage3 Python1 Antwort1", "Frage3 Python1 Antwort2", "Frage3 Python1 Antwort3", "Frage3 Python1 Antwort4", 2, 3))
    # print(add_question("Frage4 Python1", 1))
    # print(add_answers("Frage4 Python1 Antwort1", "Frage4 Python1 Antwort2", "Frage4 Python1 Antwort3", "Frage4 Python1 Antwort4", 2, 4))
    
    # print(add_question("Frage1 SQL1", 2))
    # print(add_answers("Frage1 SQL1 Antwort1", "Frage1 SQL1 Antwort2", "Frage1 SQL1 Antwort3", "Frage1 SQL1 Antwort4", 2, 5))
    # print(add_question("Frage2 SQL1", 2))
    # print(add_answers("Frage2 SQL1 Antwort1", "Frage2 SQL1 Antwort2", "Frage2 SQL1 Antwort3", "Frage2 SQL1 Antwort4", 2, 6))
    # print(add_question("Frage3 SQL1", 2))
    # print(add_answers("Frage3 SQL1 Antwort1", "Frage3 SQL1 Antwort2", "Frage3 SQL1 Antwort3", "Frage3 SQL1 Antwort4", 2, 7))
    # print(add_question("Frage4 SQL1", 2))
    # print(add_answers("Frage4 SQL1 Antwort1", "Frage4 SQL1 Antwort2", "Frage4 SQL1 Antwort3", "Frage4 SQL1 Antwort4", 2, 8))
    
    # print(add_question("Frage1 Projektmanagement1", 3))
    # print(add_answers("Frage1 Projektmanagement1 Antwort1", "Frage1 Projektmanagement1 Antwort2", "Frage1 Projektmanagement1 Antwort3", "Frage1 Projektmanagement1 Antwort4", 2, 9))
    # print(add_question("Frage2 Projektmanagement1", 3))
    # print(add_answers("Frage2 Projektmanagement1 Antwort1", "Frage2 Projektmanagement1 Antwort2", "Frage2 Projektmanagement1 Antwort3", "Frage2 Projektmanagement1 Antwort4", 2, 10))
    # print(add_question("Frage3 Projektmanagement1", 3))
    # print(add_answers("Frage3 Projektmanagement1 Antwort1", "Frage3 Projektmanagement1 Antwort2", "Frage3 Projektmanagement1 Antwort3", "Frage3 Projektmanagement1 Antwort4", 2, 11))
    # print(add_question("Frage4 Projektmanagement1", 3))
    # print(add_answers("Frage4 Projektmanagement1 Antwort1", "Frage4 Projektmanagement1 Antwort2", "Frage4 Projektmanagement1 Antwort3", "Frage4 Projektmanagement1 Antwort4", 2, 12))
    
    # print(add_question("Frage1 Wirtschaft", 4))
    # print(add_answers("Frage1 Wirtschaft Antwort1", "Frage1 Wirtschaft Antwort2", "Frage1 Wirtschaft Antwort3", "Frage1 Wirtschaft Antwort4", 2, 13))
    # print(add_question("Frage2 Wirtschaft", 4))
    # print(add_answers("Frage2 Wirtschaft Antwort1", "Frage2 Wirtschaft Antwort2", "Frage2 Wirtschaft Antwort3", "Frage2 Wirtschaft Antwort4", 2, 14))
    # print(add_question("Frage3 Wirtschaft", 4))
    # print(add_answers("Frage3 Wirtschaft Antwort1", "Frage3 Wirtschaft Antwort2", "Frage3 Wirtschaft Antwort3", "Frage3 Wirtschaft Antwort4", 2, 15))
    # print(add_question("Frage4 Wirtschaft", 4))
    # print(add_answers("Frage4 Wirtschaft Antwort1", "Frage4 Wirtschaft Antwort2", "Frage4 Wirtschaft Antwort3", "Frage4 Wirtschaft Antwort4", 2, 16))
    
    
    
    # print(get_topics_by_category(1))
    # print(get_questions_by_topic(1))
    
    # print(get_all_categories())
    # print(get_all_topics())
    # print(get_all_questions())
    # print(get_answers(1))
    # print(get_question(1))
    
    # print(get_category_id("Categ1"))
    # print(get_topic_id("Topic1"))
    # print(get_question_id("Question1"))
    
    # print(get_category_name(1))
    # print(get_topic_name(1))
    
    # print(edit_category("Categ1_New", 1))
    # print(edit_topic("Topic1_new", 1, 1))
    # print(edit_question("Question1_new", 1, 1))
    # print(edit_answers("Answer1_new", "Answer2_new", "Answer3_new", "Answer4_new", "1", 1))
    
    # print(delete_answers(2))
    # print(delete_question(2))
    
    # questions:dict = get_questions_by_topic(1) # Get all questions for selected topic -> {"question": id}
    # question_count = len(questions) # Get count for questions in selected topic
    # question_ids: dict = {} # {question_id: db_question_id}
    
    # i: int = 0
    # for question, question_id in questions.items():
    #     i += 1
    #     question_ids[i] = question_id
            
    # print(question_ids)
    # # quest_ids:list = []
    # # for i in range(1, (question_count+1)):
    # #     quest_ids.append(i)
    # # print(quest_ids)
    
    # quest_ids:list = [i for i in range(1, (question_count+1))]
    # print(quest_ids)
    
    
    ## IMAGES ##
    
    # print(add_image("src\static\images\python-logo.png", 1))
    # print(get_image(1))
    # print(edit_image("src\static\images\image.png", 1))
    # print(delete_image(1))
    
    
    
    ### SCORES ###
    
    # print(get_highscores_category("Python"))
    # print(get_highscores_topic("Python", "Grundlagen"))
    # print(get_highscores_full())
    
    
    pass
