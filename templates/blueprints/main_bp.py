from flask import Blueprint, render_template, request, redirect, url_for, session
from src.language_modifier.language_translator import *
from src.language_modifier.language_code_resource import *
from src.user.user_login import create_login, create_signup
from src.user.user_translations import text_history_query
from datetime import datetime
from src.db.db_functions import *
import asyncio

main_bp = Blueprint("main", __name__, template_folder='../pages')

@main_bp.route('/signin')
def signin():
    if not session.get("username"):
        return redirect(url_for("main.login"))
    return redirect(url_for("main.process_text"))

@main_bp.route('/signup', methods=['GET','POST'])
def signup():
    errors = {}

    if request.method == "POST":
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        user, errors = create_signup(username,first_name,last_name, email, password)

        if user:
            session['username'] = user
            return redirect(url_for('main.signup'))
        if errors:
            return render_template('signup.html', errors=errors)
        
    return render_template('signup.html', errors = errors)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login_result = create_login(username, password)
        if login_result:
            session['username'] = login_result
            return redirect(url_for('main.signin'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@main_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main_bp.route('/', methods=['GET', 'POST'])

def process_text():
    lang_codes = create_lang_codes()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_text =''
    transformed_text= ''
    target_language =''
    target_language_name =''
    
    if request.method == "POST":
        user_text = request.form['user_text']
        target_language_code = request.form['target_language']
        target_language_name = lang_codes[target_language_code].capitalize()


        if user_text and target_language_code:
            transformed_text = asyncio.run(translate_text(user_text, target_language_code))
            print(transformed_text)
    
    username = session.get('username')
    
    if username:
        values = (username, user_text, transformed_text, target_language_name, timestamp)
        query = text_history_query()

        insert_data(query,values)
        pass

    return render_template(
        'home.html',
        user_text=user_text,
        transformed_text=transformed_text,
        target_language=target_language,
        languages=lang_codes
    )


