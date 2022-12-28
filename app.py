from flask import Flask, render_template, request, session, redirect
from user import *
from flask_session import Session


# Configure app
app = Flask(__name__)


# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["POST", "GET"])
def index():

    # Добавление нового таска в базу данных
    if request.form.get("new_task"):
        # Получение информации о пользователи
        user_data = get_personal_data(session["username"])

        # Получения user_id и других, далее добавляние данных в базу данных
        user_id = user_data[0]
        task_name = request.form.get("task_name")
        task_info = request.form.get("task_info")
        add_task_to_db(user_id, task_name, task_info)
    
    # Удаление таска из базы данных
    if request.form.get("complete_task"):
        task_id = request.form.get("complete_task")
        remove_task_from_db(task_id)

    # Проверка, есть ли в сессии значению "username",
    # если нет, то перенаправляет в на страницу login
    # Иначе возвращает страницу пользователя с username
    if not session.get("username"):
        return redirect("/login")
    
    # Вывод главной страницы пользователя
    personal_data = get_personal_data(session["username"])
    task_data = get_task_data(session["username"])
    return render_template("index.html", personal_data = personal_data, task_data = task_data)


@app.route("/login", methods=["POST", "GET"])
def login():
    # Запускается, когда пользователь нажимает Login в навбаре
    if request.form.get("login"):
        return render_template("login.html")

    # Запускается, когда пользователь логиниться
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if get_to_page(username, password):
            # Инициализация пользователя
            session["username"] = request.form.get("username")
            return redirect("/")
        else:
            return render_template("failure.html")
    
    # По умолчанию
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    # Запускается, когда пользователь нажимает Registration в навбаре
    if request.form.get("user_register"):
        surname = request.form.get("surname")
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")

        if not check_user_input(surname, name, username, password):
            return render_template("failure.html")
        
        if insert_into_db(surname, name, username, password):
            return render_template("success.html")
        return render_template("failure.html")
    
    # По умолчанию
    return render_template("register.html")

    
@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")


@app.route("/remove", methods=["POST", "GET"])
def remove():
    username = session["username"]
    session["username"] = None
    remove_from_db(username)
    return render_template("remove.html", username=username)
