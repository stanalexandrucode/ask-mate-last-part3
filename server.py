from flask import Flask, request, redirect, render_template, url_for, flash, session
import data_manager
from datetime import datetime

app = Flask(__name__)
# app.secret_key = b'123'
app.secret_key = data_manager.random_api_key()


@app.route("/")
def main_page():
    file_data = data_manager.get_latest_questions()
    return render_template('main_page.html', data=file_data)


@app.route("/list")
def all_questions():
    questions = data_manager.get_table_question()
    ordered_direction = "desc"
    ordered_by = "submission_time"
    args = request.args
    if "ordered_direction" in args and "ordered_by" in args:
        ordered_direction = args.get('ordered_direction')
        ordered_by = args.get('ordered_by')
    if ordered_direction == "desc":
        try:
            questions = sorted(questions, key=lambda k: int(k[ordered_by]), reverse=True)
        except:
            questions = sorted(questions, key=lambda k: k[ordered_by], reverse=True)
    elif ordered_direction == "asc":
        try:
            questions = sorted(questions, key=lambda k: int(k[ordered_by]))
        except:
            questions = sorted(questions, key=lambda k: k[ordered_by])

    return render_template("all_questions.html", questions=questions,
                           ordered_direction=ordered_direction, ordered_by=ordered_by)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def question(question_id):
    if request.method == 'POST':
        tag = request.form.get('add_tag')
        try:
            data_manager.update_question_tags(question_id, tag)
        except:
            return redirect('/question/' + str(question_id) + '/new-tag')
    comment_id_answer = data_manager.get_table_comment()
    comment_id_question = data_manager.get_comment_by_question_id(question_id)
    file_data = data_manager.get_question_by_id(question_id)[0]
    new = file_data.get('view_number', '') + 1
    data_manager.update_view_number_qu(new, question_id)
    answers = data_manager.get_answer_by_question_id(question_id)
    tags = data_manager.tags(question_id)
    return render_template('question.html', id=question_id, data=file_data, answers=answers,
                           comment_id_question=comment_id_question, comment_id_answer=comment_id_answer, tags=tags)


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def new_comment(question_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    if request.method == 'POST':
        question_id = question_id
        user_id = session['user_id']
        data_manager.update_comment_count(user_id)
        message = request.form.get('add-comment')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edited_count = 0
        data_manager.write_comment(question_id,user_id, message, submission_time, edited_count)
        return redirect('/question/' + str(question_id))
    return render_template('new-comment.html', id=question_id)


@app.route('/question/<question_id>/new_answer', methods=["GET", "POST"])
def post_new_answer(question_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = session['user_id']
        data_manager.update_answer_count(user_id)
        vote_number = 0
        question_id = question_id
        message = request.form.get('message')
        image = request.form.get('image')
        valid = False
        data_manager.write_answer(submission_time, user_id, vote_number, question_id, message, image, valid)
        return redirect('/question/' + str(question_id))
    return render_template('new_answer.html', id=question_id)


@app.route("/question/<question_id>/vote_up")
def Q_vote_up(question_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    file_data = data_manager.get_question_by_id(question_id)[0]
    new = file_data.get('vote_number', '') + 1
    user_id = file_data.get('user_id', '')
    data_manager.gain_reputation(user_id, 5)
    data_manager.update_vote_number_qu(new, question_id)
    return redirect(request.referrer)


@app.route("/question/<question_id>/vote_down")
def Q_vote_down(question_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    file_data = data_manager.get_question_by_id(question_id)[0]
    new = file_data.get('vote_number', '') - 1
    user_id = file_data.get('user_id', '')
    data_manager.lose_reputation(user_id)
    data_manager.update_vote_number_qu(new, question_id)
    return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote_up")
def A_vote_up(answer_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    file_data = data_manager.get_answer_by_id(answer_id)[0]
    new = file_data.get('vote_number', '') + 1
    user_id=file_data.get('user_id', '')
    data_manager.gain_reputation(user_id, 10)
    question_id = file_data.get('question_id', '')
    data_manager.update_vote_number_an(new, answer_id)
    question_data = data_manager.get_question_by_id(question_id)[0]
    new_view = question_data.get('view_number', '') - 1
    data_manager.update_view_number_qu(new_view, question_id)
    return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote_down")
def A_vote_down(answer_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    file_data = data_manager.get_answer_by_id(answer_id)[0]
    new = file_data.get('vote_number', '') - 1
    user_id = file_data.get('user_id', '')
    data_manager.lose_reputation(user_id)
    question_id = file_data.get('question_id', '')
    data_manager.update_vote_number_an(new, answer_id)
    question_data = data_manager.get_question_by_id(question_id)[0]
    new_view = question_data.get('view_number', '') - 1
    data_manager.update_view_number_qu(new_view, question_id)
    return redirect(request.referrer)


@app.route('/add_question', methods=["GET", "POST"])
def add_question():
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['user_id']
        data_manager.update_question_count(user_id)
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        view_number = 0
        vote_number = 0
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        data_manager.write_question(submission_time,user_id, view_number, vote_number, title, message, image)
        return redirect("/list")
    return render_template("add_question.html")


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    data_manager.delete_from_question_by_id(question_id)
    return redirect("/list")


@app.route('/question/<question_id>/edit', methods=["GET", "POST"])
def edit_question(question_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    file_data = data_manager.get_question_by_id(question_id)[0]
    if request.method == 'POST':
        data_manager.update_data_question(request.form.get('title'), request.form.get('message'),
                                          request.form.get('image'), question_id)
        return redirect('/list')
    return render_template('edit.html', id=question_id, data=file_data)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    file_data = data_manager.get_answer_by_id(answer_id)[0]
    question_id = file_data.get('question_id', '')
    data_manager.delete_from_answer_by_id(answer_id)
    return redirect("/question/" + str(question_id))


@app.route('/search')
def search():
    phrase = request.args.get('search_text')
    search_text = data_manager.search(phrase)
    return render_template('search.html', search_text=search_text, phrase=phrase)


@app.route("/answer/<answer_id>/new-comment", methods=['POST', 'GET'])
def new_comment_answer(answer_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    if request.method == 'POST':
        message = request.form.get('comment-answer')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = session['user_id']
        data_manager.update_comment_count(user_id)
        edited_count = 0
        data_manager.comment_answer(answer_id,user_id, message, submission_time, edited_count)
        file_data = data_manager.get_answer_by_id(answer_id)[0]
        question_id = file_data.get('question_id', '')
        return redirect('/question/' + str(question_id))
    return render_template('comment-answer.html', id=answer_id)


@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_tags(question_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    tags = data_manager.get_all_tags()
    if request.method == 'POST':
        if request.form.get('new_tag'):
            new_tag = request.form.get('new_tag')
            data_manager.add_new_tag(new_tag)
            return redirect('/question/' + str(question_id) + '/new-tag')
    return render_template('add_tags.html', question_id=question_id, tags=tags)


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    data_manager.delete_tag(question_id, tag_id)
    return redirect('/question/' + str(question_id))


@app.route("/comment/<comment_id>/edit", methods=['POST', 'GET'])
def edit_comment(comment_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    file_data = data_manager.get_comment_by_id(comment_id)[0]
    question_id = file_data.get('question_id', '')
    if question_id is None:
        answer_id = file_data.get('answer_id', '')
        data2 = data_manager.get_answer_by_id(answer_id)[0]
        question_id = data2.get('question_id', '')
    if request.method == 'POST':
        data = data_manager.get_edit_number(comment_id)[0]
        value = data.get('edited_count', '')
        data_manager.update_edit_number(value, comment_id)
        data_manager.update_data_comment(request.form.get('edit-comment-answer'), comment_id)
        return redirect('/question/' + str(question_id))
    return render_template('edit_comment.html', comment_id=comment_id, data=file_data)


@app.route("/comment/<comment_id>/delete", methods=['POST', 'GET'])
def delete_comment(comment_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    data = data_manager.get_comment_by_id(comment_id)[0]
    question_id = data.get('question_id', '')
    if question_id is None:
        answer_id = data.get('answer_id', '')
        data2 = data_manager.get_answer_by_id(answer_id)[0]
        question_id = data2.get('question_id', '')
    data_manager.delete_comment(comment_id)
    return redirect('/question/' + str(question_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for("main_page"))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if data_manager.register_user(username, password, submission_time) is False:
            flash('Not registered')
        data_manager.register_user(username, password, submission_time)
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for("main_page"))
    if request.method == 'POST':
        username, typed_password = request.form.get('username'), request.form.get('password')
        user = data_manager.check_user(username)
        if user and data_manager.verify_password(typed_password, user['password']):
            session['user_id'] = user['id']
            session['username'] = username
            flash('User logged in!')
            return redirect('/')
        else:
            flash('User or Password do not match')
    return render_template('login.html')


@app.route('/logout', methods= ['GET', 'POST'])
def logout():
    if 'user_id' not in session:
        flash('You are not logged in!')
    else:
        session.pop('user_id', None)
        session.pop('username', None)
    return redirect(url_for('main_page'))


@app.route("/users")
def users():
    users_data = data_manager.users_data()
    return render_template("users.html", users=users_data)


@app.route("/tags")
def show_tags():
    tags = data_manager.show_tags()
    return render_template('tags.html', tags=tags)


@app.route("/answer/<answer_id>/False")
def valid_answer_Flase(answer_id):
    file_data = data_manager.get_answer_by_id(answer_id)[0]
    valid = False
    question_id = file_data.get('question_id', '')
    data_manager.valid_answer(valid, answer_id)
    return redirect('/question/' + str(question_id))


@app.route("/answer/<answer_id>/True")
def valid_answer_True(answer_id):
    file_data = data_manager.get_answer_by_id(answer_id)[0]
    valid = True
    question_id = file_data.get('question_id', '')
    data_manager.valid_answer(valid, answer_id)
    user_id = file_data.get('user_id', '')
    data_manager.gain_reputation(user_id, 15)
    return redirect('/question/' + str(question_id))


@app.route("/answer/<answer_id>/edit", methods=['POST', 'GET'])
def edit_answer(answer_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    file_data = data_manager.get_answer_by_id(answer_id)[0]
    question_id = file_data.get('question_id', '')
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.edit_answer(message, answer_id)
        return redirect('/question/' + str(question_id))
    return render_template("edit_answer.html", data=file_data,answer_id=answer_id)


@app.route("/users/<user_id>")
def user_page(user_id):
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    questions_asked = data_manager.questions_by_id(user_id)
    answers = data_manager.answers_for_question_id(user_id)
    comments = data_manager.comments_for_question_id(user_id)
    print(comments)
    users_data = data_manager.users_data()
    return render_template("user_id.html", users=users_data, questions_asked=questions_asked, answers=answers, comments=comments)


if __name__ == '__main__':
    app.run(
        port=8000,
        debug=True,
    )
