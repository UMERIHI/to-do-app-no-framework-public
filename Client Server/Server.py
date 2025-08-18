import datetime
import pickle
import random
import smtplib
from email.message import EmailMessage
import sqlite3
import socket

database_file = "todo.db"
connection = sqlite3.connect(database_file)
variable = []
email_server = smtplib.SMTP('smtp.gmail.com', 587)
email_server.starttls()
email_server.login('user@gmail.com','abcd abcd abcd abcd')

query_user = """
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
"""

query_task = """
CREATE TABLE IF NOT EXISTS task (
    task_id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL, 
    description TEXT NOT NULL, 
    due_date DATE NOT NULL, 
    due_time TEXT NOT NULL, 
    priority TEXT NOT NULL, 
    status TEXT NOT NULL, 
    task_type TEXT NOT NULL,
    owner TEXT NOT NULL,
    FOREIGN KEY (owner) REFERENCES user(username)
);
"""

def insert_user(email, username, password):
    query = "INSERT INTO user(email, username, password) VALUES (?,?,?)"
    try:
        with connection:
            connection.execute(query, (email, username, password))
        return True
    except Exception as error:
        print("Database Error:", error)
        return None

def check_login_user(username, password):
    query = "SELECT 1 FROM user WHERE LOWER(username) = LOWER(?) AND password = ?"
    try:
        with connection:
            response = connection.execute(query, (username, password)).fetchone()
        return response is not None
    except Exception as error:
        print("Database Error:", error)
        return None

def check_user_exist(email, username):
    query = "SELECT 1 FROM user WHERE LOWER(email) = LOWER(?) OR LOWER(username) = LOWER(?)"
    try:
        with connection:
            response = connection.execute(query, (email, username)).fetchone()
        return response is None
    except Exception as error:
        print("Database Error:", error)
        return None

def insert_task(title, description, due_date, due_time, priority, status, task_type, owner):
    query = """
    INSERT INTO task(title, description, due_date, due_time, priority, status, task_type, owner)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        with connection:
            connection.execute(query, (title, description, due_date, due_time, priority, status, task_type, owner))
        return True
    except Exception as error:
        print("Database Error:", error)
        return None

def update_task(task_id, title, description, due_date, due_time, priority, status, task_type):
    query = """
    UPDATE task
    SET title = ?, description = ?, due_date = ?, due_time = ?, priority = ?, status = ?, task_type = ? WHERE task_id = ?
    """
    try:
        with connection:
            connection.execute(query, (title, description, due_date, due_time, priority, status, task_type, task_id))
        return True
    except Exception as error:
        print("Database Error:", error)
        return None

def fetch_tasks(username):
    query = "SELECT * FROM task WHERE owner = ?"
    try:
        with connection:
            rows = connection.execute(query, (username,)).fetchall()
        return send_task([Task(*row) for row in rows])
    except Exception as error:
        print("Database Error:", error)
        return None

def send_task(response):
    data = pickle.dumps(response)
    size = len(data).to_bytes(4, 'big')
    conn.sendall(size + data)
    in_communication()

def delete_task(task_id):
    query = "DELETE FROM task WHERE task_id = ?"
    try:
        with connection:
            connection.execute(query, (task_id, ))
        return True
    except Exception as error:
        print("Database Error:", error)
        return None

class Task:
    def __init__(self, task_id, title, description, due_date, due_time, priority, status, task_type, owner):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.due_time = due_time
        self.priority = priority
        self.status = status
        self.task_type = task_type
        self.creation_date = datetime.datetime.now()
        self.last_updated_date = datetime.datetime.now()
        self.owner = owner

def otp_send(email, username):
    response = check_user_exist(email, username)
    if response is True:
        try:
            from_mail = 'mumerihi@gmail.com'
            to_mail = email.lower()
            msg = EmailMessage()
            msg['Subject'] = "OTP Verification"
            msg['From'] = from_mail
            msg['To'] = to_mail
            otp = ""
            for j in range(6):
                otp += str(random.randint(1, 9))
            otp = int(otp)
            msg.set_content(f"Your OTP is: {otp}")
            email_server.send_message(msg)
            return otp
        except Exception as error:
            print("Database Error:", error)
            return None

    elif result is None:
        return None
    else:
        return False

def main():
    try:
        connection.execute(query_user)
        connection.execute(query_task)
        return True
    except Exception as e:
        print("Database Error:", e)
        return None

def in_communication():
    response = conn.recv(1024).decode()
    parts = response.split('|')
    method = parts[0]
    arguments = parts[1:]
    if method in globals():
        func = globals()[method]
        response = func(*arguments)
        out_communication(response)

def out_communication(response):
    conn.send(str(response).encode())
    in_communication()

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 65432))
server.listen()
while True:
    conn, add = server.accept()
    with conn:
        result = main()
        if result is True:
            in_communication()
        else:
            conn.send(str(result).encode())