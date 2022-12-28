import hashlib
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///users.db")
db = scoped_session(sessionmaker(bind=engine))

def main():
    insert_into_db("surname", "name", "username", "password")


def insert_into_db(surname, name, username, password):
    hashed_password = hash_password(password)
    lower_username = username.lower()
    try:
        db.execute("INSERT INTO users (surname, name, username, hashed_password) VALUES (:surname, :name, :lower_username, :hashed_password)", 
                    {"surname": surname, "name": name, "lower_username": lower_username, "hashed_password": hashed_password})
        db.commit()
        return True
    except ValueError:
        return False
    

def hash_password(password):
        password = password.encode("utf-8")
        hashed_password = hashlib.sha256(password).hexdigest()
        return hashed_password


def check_user_input(surname, name, username, password):
    user_data = [surname, name, username, password]

    for data in user_data:
        if not re.search(r"^[^ ]{1,30}$", data):
            return False
        return True


def get_to_page(username, password):
    hashed_password = hash_password(password)
    lower_username = username.lower()
    db_hashed_password = db.execute("SELECT hashed_password FROM users WHERE username = :lower_username", {"lower_username": lower_username}).fetchone()[0]

    if db_hashed_password == []:
        return False

    if hashed_password == db_hashed_password:
        return True
    return False


def remove_from_db(username):
    db.execute("DELETE FROM tasks WHERE task_id IN (SELECT task_id FROM tasks WHERE user_id IN (SELECT user_id FROM users WHERE username = :username))", {"username": username})
    db.execute("DELETE FROM users WHERE username = :username", {"username": username})
    db.commit()


def get_personal_data(username):
    personal_data = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    return personal_data


def get_task_data(username):
    task_data = db.execute("SELECT * FROM tasks WHERE user_id = (SELECT user_id FROM users WHERE username = :username)", {"username": username}).fetchall()
    return task_data


def add_task_to_db(user_id, task_name, task_info):
    db.execute("INSERT INTO tasks (user_id, task_name, task_info) VALUES (:user_id, :task_name, :task_info)", 
                {"user_id": user_id, "task_name": task_name, "task_info": task_info})
    db.commit()


def remove_task_from_db(task_id):
    db.execute("DELETE FROM tasks WHERE task_id = :task_id", {"task_id": task_id})
    db.commit()


if __name__ == "__main__":
    main()
