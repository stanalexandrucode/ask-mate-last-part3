import bcrypt
from psycopg2.extras import RealDictCursor
import os

import database_common


@database_common.connection_handler
def get_table_question(cursor: RealDictCursor) -> list:
    """
    :return:
    all data from table question
    """
    query = """
        SELECT *
        FROM question
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_table_comment(cursor: RealDictCursor) -> list:
    """
    :return:
    all data from table comment
    """
    query = """
        SELECT *
        FROM comment
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_from_question_by_id(cursor: RealDictCursor, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param id:
    select the id for the delete
    :return:
    deletes line for chosen id
    """
    query = """
        DELETE FROM question
        WHERE id = %(id)s
    """
    args = {'id': id}
    cursor.execute(query, args)
    return "Id deleted"


@database_common.connection_handler
def delete_from_answer_by_id(cursor: RealDictCursor, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param id:
    select the id for the delete
    :return:
    deletes line for chosen id
    """
    query = """
        DELETE FROM answer
        WHERE id = %(id)s
    """
    args = {'id': id}
    cursor.execute(query, args)
    return "Id deleted"


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, id: int) -> list:
    """
    :param id:
    enter id for desired data
    :return:
    data from question table by selected id
    """
    query = """
            SELECT *
            FROM question
            WHERE id = %(id)s
            """
    args = {'id': id}
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_id(cursor: RealDictCursor, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param id:
    enter answer id
    :return:
    data from answer table by selected id
    """
    query = """
            SELECT *
            FROM answer
            WHERE id = %(id)s
            """
    args = {'id': id}
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param question_id:
    enter id for question_id
    :return:
    data from answer table by selected id
    """
    query = """
            SELECT *
            FROM answer
            WHERE question_id = %(question_id)s
            ORDER BY submission_time DESC
            """
    args = {'question_id': question_id}
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor: RealDictCursor, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param id:
    enter id for the comment
    :return:
    data from comment table by selected id
    """
    query = """
            SELECT *
            FROM comment
            WHERE id = %(id)s
            """
    data = {'id': id}
    cursor.execute(query, data)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param question_id:
    enter question_id for the comment
    :return:
    data from comment table by selected id
    """
    query = """
            SELECT *
            FROM comment
            WHERE question_id = %(question_id)s
            """
    args = {'question_id': question_id}
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def write_question(cursor: RealDictCursor, submission_time: str,user_id:int, view_number: int,
                   vote_number: int, title: str, message: str, image: str) -> list:
    """
    :param cursor:
    RealDictCursor
    :param submission_time:
    submission_time for inserting data
    :param view_number:
    number of views of the question
    :param vote_number:
    votes status of the question
    :param title:
    title text
    :param message:
    the message for the title
    :param image:
    url for the image
    :return:
    inserts values for columns indicated
    """
    query = """
            INSERT INTO question (submission_time,user_id, view_number, vote_number, title, message, image)
            VALUES (%(submission_time)s,%(user_id)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)
            """
    args = {'submission_time': submission_time,'user_id':user_id, 'view_number': view_number, 'vote_number': vote_number,
            'title': title, 'message': message, 'image': image
            }
    cursor.execute(query, args)
    return "New value added"


@database_common.connection_handler
def write_answer(cursor: RealDictCursor, submission_time: str, user_id: int, vote_number: int,
                 question_id: int, message: str, image: str, valid: bool) -> list:
    """
    :param cursor:
    RealDictCursor
    :param submission_time:
    submission_time for inserting data
    :param vote_number:
    votes status of the question
    :param question_id:
    id of the question
    :param message:
    the message for the title
    :param image:
    url for the image
    :return:
    inserts values for columns indicated
    """
    query = """
            INSERT INTO answer (submission_time,user_id, vote_number,question_id,message,image,valid)
            VALUES (%(submission_time)s,%(user_id)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s,%(valid)s)
            """
    args = {'submission_time': submission_time, 'user_id': user_id, 'vote_number': vote_number,
            'question_id': question_id, 'message': message, 'image': image, 'valid': valid
            }
    cursor.execute(query, args)
    return "New value added"


@database_common.connection_handler
def write_comment(cursor: RealDictCursor, question_id: int,user_id:int, message: str,
                  submission_time: str, edited_count: int) -> list:
    query = """
            INSERT INTO comment (question_id,user_id, message, submission_time, edited_count)
            VALUES (%(question_id)s,%(user_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
            """
    args = {'question_id': question_id,'user_id':user_id, 'message': message,
            'submission_time': submission_time, 'edited_count': edited_count
            }
    cursor.execute(query, args)
    return "New value added"


@database_common.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id: int) -> str:
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s
    """
    args = {'comment_id': comment_id}
    cursor.execute(query, args)
    return "Comment deleted"


@database_common.connection_handler
def update_data_question(cursor: RealDictCursor, title: str, message: str, image: str, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param title:
    update title
    :param message:
    update message
    :param image:
    update image
    :param id:
    :return:
    """
    query = """
            UPDATE question
            SET title = %(title)s, message = %(message)s, image = %(image)s
            WHERE id = %(id)s
            """
    args = {'title': title, 'message': message, 'image': image, 'id': id}
    cursor.execute(query, args)
    updated_query = f"""
            SELECT *
            FROM question
            WHERE id = %(id)s
            """
    args = {'id': id}
    cursor.execute(updated_query, args)
    return cursor.fetchall()


@database_common.connection_handler
def update_data_comment(cursor: RealDictCursor, message: str, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param message:
    value for the message column
    :param id:
    id for the comment
    :return:
    """
    query = """
            UPDATE comment
            SET message = %(message)s
            WHERE id = %(id)s
            """
    args = {'message': message, 'id': id}
    cursor.execute(query, args)

    updated_query = """
            SELECT *
            FROM comment
            WHERE id = %(id)s
            """
    args = {'id': id}
    cursor.execute(updated_query, args)
    return cursor.fetchall()


@database_common.connection_handler
def update_edit_number(cursor: RealDictCursor, edited_count: int, id: int) -> list:
    query = """
        UPDATE comment
        SET edited_count = %(edited_count)s + 1
        WHERE id = %(id)s
    """
    args = {'edited_count': edited_count, 'id': id}
    cursor.execute(query, args)
    return "DONE"


@database_common.connection_handler
def get_edit_number(cursor: RealDictCursor, id: int) -> list:
    query = """
        SELECT edited_count
        FROM comment
        WHERE id = %(id)s
    """
    args = {'id': id}
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def update_view_number_qu(cursor: RealDictCursor, view_number: str, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param view_number:
    new value for the the view_number
    :param id:
    id of the question
    :return:
    """
    query = """
            UPDATE question
            SET view_number = %(view_number)s
            WHERE id = %(id)s
            """
    args = {'view_number': view_number, 'id': id}
    cursor.execute(query, args)

    updated_query = """
            SELECT *
            FROM question
            WHERE id = %(id)s
            """
    args = {'id': id}
    cursor.execute(updated_query, args)
    return cursor.fetchall()


@database_common.connection_handler
def update_vote_number_qu(cursor: RealDictCursor, vote_number: str, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param vote_number:
    new value for the the view_number
    :param id:
    id of the question
    :return:
    """
    query = """
            UPDATE question
            SET vote_number = %(vote_number)s
            WHERE id = %(id)s
            """
    args = {'vote_number': vote_number, 'id': id}
    cursor.execute(query, args)

    updated_query = """
            SELECT *
            FROM question
            WHERE id = %(id)s
            """
    args = {'vote_number': vote_number, 'id': id}
    cursor.execute(updated_query, args)
    return cursor.fetchall()


@database_common.connection_handler
def update_vote_number_an(cursor: RealDictCursor, vote_number: str, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param vote_number:
    new value for the the view_number
    :param id:
    id of the question
    :return:
    """
    query = """
            UPDATE answer
            SET vote_number = %(vote_number)s
            WHERE id = %(id)s
            """
    args = {'vote_number': vote_number, 'id': id}
    cursor.execute(query, args)
    updated_query = """
            SELECT *
            FROM answer
            WHERE id = %(id)s
            """
    args = {'id': id}
    cursor.execute(updated_query, args)
    return cursor.fetchall()


@database_common.connection_handler
def search(cursor: RealDictCursor, phrase: str) -> list:
    query = """
            SELECT DISTINCT question.id AS id, question.submission_time AS submission_time ,
question.view_number AS view_number, question.vote_number AS vote_number, question.title AS title,
question.message AS message, question.image AS image, answer.id AS answer_id,
answer.question_id AS answer_question_id, answer.submission_time AS answer_submission_time,
answer.vote_number AS answer_vote_number, answer.message AS answer_message, answer.image AS answer_image
            FROM question
            LEFT OUTER JOIN answer
            ON question.id = answer.question_id
            WHERE question.title LIKE %(phrase)s
            OR question.message LIKE %(phrase)s
            OR answer.message LIKE %(phrase)s;
            """
    args = ({'phrase': '%' + phrase + '%'})
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def comment_answer(cursor: RealDictCursor, answer_id: int,user_id:int, message: str, submission_time: str,
                   edited_count: int) -> list:
    query = """
            INSERT INTO comment (answer_id,user_id, message,submission_time,edited_count)
            VALUES (%(answer_id)s,%(user_id)s,%(message)s,%(submission_time)s,%(edited_count)s)
            """
    args = {'answer_id': answer_id,'user_id':user_id, 'message': message, 'submission_time': submission_time,
            'edited_count': edited_count}
    cursor.execute(query, args)
    return "New value added"


@database_common.connection_handler
def get_latest_questions(cursor: RealDictCursor) -> list:
    query = """SELECT *
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_question_tags(cursor: RealDictCursor, question_id: int, tag_id: int) -> list:
    query = """
        INSERT INTO question_tag (question_id, tag_id)
        VALUES (%(question_id)s, %(tag_id)s)
    """
    args = {'question_id': question_id, 'tag_id': tag_id}
    cursor.execute(query, args)
    return "Tags Updated"


@database_common.connection_handler
def tags(cursor: RealDictCursor, question_id: int) -> list:
    query = """
            SELECT question_tag.question_id,question_tag.tag_id,tag.name
            FROM question_tag JOIN tag
            ON question_tag.tag_id=tag.id
            WHERE question_tag.question_id = %(question_id)s
            """
    args = {'question_id': question_id}
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_tags(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag(cursor: RealDictCursor, question_id: int, tag_id: int) -> list:
    query = """
        DELETE FROM question_tag
        WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
    """
    args = {'question_id': question_id, 'tag_id': tag_id}
    cursor.execute(query, args)
    return "Tag deleted"


@database_common.connection_handler
def add_new_tag(cursor: RealDictCursor, new_tag: str) -> list:
    query = """ 
        INSERT INTO tag (name)
        VALUES (%(new_tag)s)
    """
    args = {'new_tag': new_tag}
    cursor.execute(query, args)
    return "DONE"


@database_common.connection_handler
def username_exists(cursor: RealDictCursor, username: str):
    query = """
        SELECT *
        FROM users
        WHERE username = %(username)s;
         """
    args = {'username': username}
    cursor.execute(query, args)
    return cursor.fetchone()


@database_common.connection_handler
def register_user(cursor: RealDictCursor, username: str, text_password: str, submission_time: int):
    """
    Checks for valid username.
    If username is valid, inserts the new user into the database
    """
    if username_exists(username):
        return False
    query = """
    INSERT INTO users (username,password,submission_time,count_questions,count_answers,count_comments,reputation)
    VALUES (%(username)s,%(password)s,%(submission_time)s,0,0,0,0)
           """
    args = {"username": username, "password": encrypt_password(text_password), "submission_time": submission_time}
    return cursor.execute(query, args)


def encrypt_password(password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pass.decode('utf-8')


def verify_password(text_password, hashed_pass):
    return bcrypt.checkpw(text_password.encode('utf-8'), hashed_pass.encode('utf-8'))


@database_common.connection_handler
def users_data(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM users
            """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def check_user(cursor, username):
    query = """
        SELECT id, password
        FROM users
        WHERE username ILIKE %(username)s;
    """
    data = {
        "username": username
    }
    cursor.execute(query, data)
    return cursor.fetchone()

@database_common.connection_handler
def update_question_count(cursor: RealDictCursor, user_id: int) -> list:
    query="""
        UPDATE users
        SET count_questions = count_questions+1
        WHERE id = %(user_id)s
        """
    args={'user_id': user_id}
    return cursor.execute(query, args)


@database_common.connection_handler
def update_answer_count(cursor: RealDictCursor, user_id: int) -> list:
    query="""
        UPDATE users
        SET count_answers = count_answers+1
        WHERE id = %(user_id)s
        """
    args={'user_id': user_id}
    return cursor.execute(query, args)


@database_common.connection_handler
def update_comment_count(cursor: RealDictCursor,user_id: int) -> list:
    query="""
        UPDATE users
        SET count_comments = count_comments+1
        WHERE id = %(user_id)s
        """
    args={'user_id': user_id}
    return cursor.execute(query, args)


@database_common.connection_handler
def gain_reputation(cursor: RealDictCursor, user_id: int, points: int) -> list:
    query="""
        UPDATE users
        SET reputation = reputation+%(points)s
        WHERE id = %(user_id)s
        """
    args={'user_id': user_id, 'points': points}
    return cursor.execute(query, args)


@database_common.connection_handler
def lose_reputation(cursor: RealDictCursor, user_id: int) -> list:
    query = """
        UPDATE users
        SET reputation = reputation-2
        WHERE id = %(user_id)s
        """
    args={'user_id':user_id}
    return cursor.execute(query, args)


def random_api_key():
    """
    :return: salt in secret key
    """
    return os.urandom(100)


@database_common.connection_handler
def show_tags(cursor: RealDictCursor) -> list:
    query = """
            SELECT tag.name, count(question_tag.question_id) as question_number
            FROM question_tag JOIN tag
            ON question_tag.tag_id=tag.id
            GROUP BY tag.name
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def valid_answer(cursor: RealDictCursor, valid: bool, id: int) -> list:
    query = """
            UPDATE answer
            SET valid = %(valid)s
            WHERE id = %(id)s
            """
    args = {'valid': valid, 'id': id}
    cursor.execute(query, args)


@database_common.connection_handler
def edit_answer(cursor: RealDictCursor, message: str, id: int) -> list:
    query = """
            UPDATE answer
            SET message = %(message)s
            WHERE id = %(id)s
            """
    args = {'message': message, 'id': id}
    cursor.execute(query, args)


@database_common.connection_handler
def questions_by_id(cursor: RealDictCursor, user_id: int) -> list:
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question
            WHERE id = %(user_id)s
    """
    args = {'user_id': user_id}
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def answers_for_question_id(cursor: RealDictCursor, user_id: int) -> list:
    query = """
            SELECT answer.*, question.id, question.title
            FROM answer
            LEFT JOIN question
            ON answer.question_id = question.id
            WHERE answer.user_id = %(user_id)s
    """
    args = {'user_id': user_id}
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def comments_for_question_id(cursor: RealDictCursor, user_id: int) -> list:
    query = """
            SELECT comment.*, question.id, question.title
            FROM comment
            LEFT JOIN question
            ON comment.question_id = question.id
            WHERE comment.user_id = %(user_id)s AND comment.answer_id IS NULL 
    """
    args = {'user_id': user_id}
    cursor.execute(query, args)
    return cursor.fetchall()
