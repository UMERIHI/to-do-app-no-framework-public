import datetime
import os
import pickle
import random
import smtplib
import re
from email.message import EmailMessage
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import Calendar

data_file_path = "data.pkl"
data = {}
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('user@gmail.com','abcd abcd abcd abcd')

window = Tk()

window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
window.title("Todo App")
window.config(background='#0D0527')

class Task:
    def __init__(self, title, description, due_date, due_time, priority, status, task_type, username):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.due_time = due_time
        self.priority = priority
        self.status = status
        self.task_type = task_type
        self.creation_date = datetime.datetime.now()
        self.last_Updated_date = datetime.datetime.now()
        self.owner = username


class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

def read_file(file_path, data):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            loaded_data = pickle.load(file)
            data.clear()
            data.update(loaded_data)
    else:
        pass

def write_file(file_path, data):
    if data is None:
        pass
    else:
        with open(file_path, "wb") as file:
            pickle.dump(data, file)

def login(frame):
    frame.pack_forget()
    login_frame = Frame(window,bg='#0D0527')
    login_frame.pack(expand=True, anchor='center')

    login_label = Label(login_frame, text="Login", font=("Ariel", 40, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    login_label.grid(row=0,column=1, padx=10, pady=10)

    username_label = Label(login_frame, text="Username", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    username_label.grid(row=1,column=0, padx=10, pady=10, sticky="w")

    username_entry = Entry(login_frame, font=("Ariel", 20, "bold"), fg='black', bg='#FFE66D', width=25)
    username_entry.grid(row=1,column=1, padx=10, pady=10, sticky="w")

    password_label = Label(login_frame, text="Password", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    password_label.grid(row=2,column=0, padx=10, pady=10, sticky="w")

    password_entry = Entry(login_frame, font=("Ariel", 20, "bold"), fg='black', bg='#FFE66D', width=25, show="*")
    password_entry.grid(row=2,column=1, padx=10, pady=10, sticky="w")

    dont_have_account_frame = Frame(login_frame, bg='#0D0527')
    dont_have_account_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    dont_have_account_label = Label(dont_have_account_frame, text="Don't have a Account?", font=("Ariel", 15, "bold"), fg='white',bg="#0D0527")
    dont_have_account_label.grid(row=0, column=0, sticky="w")

    dont_have_account_button = Button(dont_have_account_frame, text="Sign Up", font=("Ariel", 15, "bold"), fg='black', bg='#4ECDC4', activebackground="#292F36", activeforeground="#F5EEDC",command=lambda: signup(login_frame))
    dont_have_account_button.grid(row=0, column=1, sticky="w")

    login_button = Button(login_frame, text="Log In", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda: login_work(login_frame, username_entry, password_entry))
    login_button.grid(row=4,column=1, padx=10, pady=10, sticky="w")

def login_work(frame, username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    for user in data.keys():
        if user.username.lower() == username.lower():
            if user.password == password:
                messagebox.showinfo(title="Login Success", message="You successfully logged in")
                dashboard(frame, user)
            else:
                messagebox.showwarning(title="Login Error", message="Wrong Username and Password")
            return
    messagebox.showwarning(title="Login Error", message="User not found")
    return

def signup(frame):
    frame.pack_forget()
    signup_frame = Frame(window,bg='#0D0527')
    signup_frame.pack(expand=True, anchor='center')

    signup_label = Label(signup_frame, text="Sign Up", font=("Ariel", 40, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    signup_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    email_label = Label(signup_frame, text="Email", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527",padx=10, pady=10)
    email_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    email_entry = Entry(signup_frame, font=("Ariel", 20, "bold"), fg='black', bg='#FFE66D', width=25)
    email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    username_label = Label(signup_frame, text="Username", font=("Ariel", 20, "bold"),  fg='white', bg="#0D0527", padx=10,pady=10)
    username_label.grid(row=2,column=0, padx=10, pady=10, sticky="w")

    username_entry = Entry(signup_frame, font=("Ariel", 20, "bold"), fg='black', bg='#FFE66D', width=25)
    username_entry.grid(row=2,column=1, padx=10, pady=10, sticky="w")

    password_label = Label(signup_frame, text="Password", font=("Ariel", 20, "bold"),  fg='white', bg="#0D0527", padx=10,pady=10)
    password_label.grid(row=3,column=0, padx=10, pady=10, sticky="w")

    password_entry = Entry(signup_frame, font=("Ariel", 20, "bold"), fg='black', bg='#FFE66D', width=25, show="*")
    password_entry.grid(row=3,column=1, padx=10, pady=10, sticky="w")

    already_a_user_frame = Frame(signup_frame, bg='#0D0527')
    already_a_user_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    already_a_user_label =  Label(already_a_user_frame, text="Already a User?", font=("Ariel", 15, "bold"), fg='white', bg="#0D0527")
    already_a_user_label.grid(row=0, column=0, sticky="w")

    already_a_user_button = Button(already_a_user_frame, text="Log in", font=("Ariel", 15, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC", command=lambda : login(signup_frame))
    already_a_user_button.grid(row=0,column=1, sticky="w")

    signup_button = Button(signup_frame, text="Sign Up", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda : signup_work(signup_frame, email_entry, username_entry, password_entry))
    signup_button.grid(row=5,column=1, padx=10, pady=10, sticky="w")

def signup_work(frame, email_entry, username_entry, password_entry):
    email = str(email_entry.get())
    username = str(username_entry.get())
    password = str(password_entry.get())

    if username.find(" ") != -1:
        messagebox.showwarning(title="Incorrect Username", message="Please Check Your Username Again")
        return
    if email.find(" ") != -1:
        messagebox.showwarning(title="Incorrect Email", message="Please Check Your Email Again")
        return
    if len(username) < 3:
        messagebox.showwarning(title="Username Length Error",message="Please Check Your Username Again Username should be higher than 4 character")
        return
    if len(password) < 1:
        messagebox.showwarning(title="Password Length Error",message="Please Check Your Password Again Password Less than 8 Character")
        return

    for user in data.keys():
        if user.email.lower() == email.lower():
            messagebox.showwarning(title="Email Already Exist", message="Your Given Email Already Exist in System")
            return
        elif user.username.lower() == username.lower():
            messagebox.showwarning(title="Email Already Exist", message="Your Given Email Already Exist in System")
            return

    domain = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(domain, email):
        messagebox.showwarning(title="Incorrect Email", message="Please Check Your Email Again Wrong Domain")
        return
    otp_send(frame, email, username, password)

def otp_send(frame, email, username, password):
    from_mail = 'user@gmail.com'
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
    server.send_message(msg)
    messagebox.showinfo(title="OTP Message Sent",message="OTP Verification Code has been sent to the mail")
    otp_verify(frame, otp, email, username, password)

def otp_verify(frame, given_otp, email, username, password):
    frame.pack_forget()
    otp_verify_frame = Frame(window,bg='#0D0527')
    otp_verify_frame.pack(expand=True, anchor='center')

    otp_verification_label = Label(otp_verify_frame, text="OTP Verification", font=("Ariel", 40, "bold"), fg='white', bg="#0D0527", padx=10, pady=10)
    otp_verification_label.grid(row=0, column=1)

    otp_verify_label = Label(otp_verify_frame, text="OTP has been Sent to Your Email\nPlease Enter OTP Below", font=("Ariel", 15, "bold"), fg='white', bg="#0D0527", padx=10, pady=10)
    otp_verify_label.grid(row=1, column=1)

    otp_label = Label(otp_verify_frame, text="OTP", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    otp_label.grid(row=2,column=0, padx=10, pady=10)

    otp_entry = Entry(otp_verify_frame, font=("Ariel", 20, "bold"), fg='black', bg='#FFE66D', width=25)
    otp_entry.grid(row=2,column=1, padx=10, pady=10)

    dont_get_otp_frame = Frame(otp_verify_frame, bg='#0D0527')
    dont_get_otp_frame.grid(row=3, column=1, padx=10, pady=10)

    dont_get_otp_label = Label(dont_get_otp_frame, text="Didn't get OTP?", font=("Ariel", 15, "bold"), fg='white',bg="#0D0527")
    dont_get_otp_label.grid(row=0, column=0)

    dont_get_otp_button = Button(dont_get_otp_frame, text="Send Again", font=("Ariel", 15, "bold"), fg='black', bg='#4ECDC4', activebackground="#292F36", activeforeground="#F5EEDC",command=lambda: otp_send(otp_verify_frame, email, username, password))
    dont_get_otp_button.grid(row=0, column=1)

    otp_verify_button = Button(otp_verify_frame, text="Verify Email", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda: otp_verification(otp_verify_frame, given_otp, otp_entry, email, username, password))
    otp_verify_button.grid(row=4,column=1, padx=10, pady=10)

def otp_verification(frame, otp_input, otp_entry, email, username, password):
    otp = int(otp_entry.get())
    if otp_input == otp:
        save_user(frame, email, username, password)
        return
    else:
        messagebox.showwarning(title="Email Verification Failed", message="Email Verification Failed Due to Error")
        return

def save_user(frame, email, username, password):
    user = User(email, username, password)
    data[user] = []
    write_file(data_file_path, data)
    messagebox.showinfo(title="User Created",message="User has Been Successfully Created")
    login(frame)

def dashboard(frame, user):
    frame.pack_forget()
    dashboard_frame = Frame(window, bg='#0D0527')
    dashboard_frame.pack(expand=True, anchor='center')

    to_do_app_label = Label(dashboard_frame, text="To Do App", font=("Ariel", 40, "bold"), fg='white', bg="#0D0527")
    to_do_app_label.pack(padx=20, pady=20)

    search_add_task_frame = Frame(dashboard_frame, bg='#1b6187')
    search_add_task_frame.pack(padx=20, pady=20)

    search_frame = Frame(search_add_task_frame, bg='#1b6187')
    search_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    search_label = Label(search_frame, text="Search by Title", font=("Ariel", 20, "bold"), fg='white', bg="#1b6187")
    search_label.grid(row=0, column=0, sticky='w')
    search_entry = Entry(search_frame, font=("Ariel", 20), fg='black', bg='#FFE66D', width=30)
    search_entry.grid(row=1, column=0, sticky='w')

    priority_frame = Frame(search_add_task_frame, bg='#1b6187')
    priority_frame.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    priority_label = Label(priority_frame, text="Priority", font=("Ariel", 20, "bold"), fg='white', bg="#1b6187")
    priority_label.grid(row=0, column=0, sticky='w')
    priority_combobox = Combobox(priority_frame, values=['','Low', 'Medium', 'High'], state="readonly", width=8, background="#1b6187")
    priority_combobox.grid(row=1, column=0, sticky='w')

    status_frame = Frame(search_add_task_frame, bg='#1b6187')
    status_frame.grid(row=0, column=2, padx=10, pady=10, sticky='w')
    status_label = Label(status_frame, text="Status", font=("Ariel", 20, "bold"), fg='white', bg="#1b6187")
    status_label.grid(row=0, column=0, sticky='w')
    status_combobox = Combobox(status_frame, values=['', 'Pending', 'In Progress', 'Done'], state="readonly", width=10, background="#1b6187")
    status_combobox.grid(row=1, column=0, sticky='w')

    type_frame = Frame(search_add_task_frame, bg='#1b6187')
    type_frame.grid(row=0, column=3, padx=10, pady=10, sticky='w')
    type_label = Label(type_frame, text="Type", font=("Ariel", 20, "bold"), fg='white', bg="#1b6187")
    type_label.grid(row=0, column=0, sticky='w')
    type_combobox = Combobox(type_frame, values=['', 'Home', 'Work', 'Education', 'Miscellaneous'], state="readonly", width=12,background="#1b6187")
    type_combobox.grid(row=1, column=0, sticky='w')

    add_task_button = Button(search_add_task_frame, text="Add Task", font=("Ariel", 20, "bold"), fg='black',bg='#4ECDC4', activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda: add_task(dashboard_frame, user))
    add_task_button.grid(row=0, column=5, padx=10, pady=10, sticky="e")

    mainframe = Frame(dashboard_frame)
    mainframe.pack()
    scroll_canvas = Canvas(mainframe, width=1120, height=400)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollable_frame = Scrollbar(mainframe, orient=VERTICAL, command=scroll_canvas.yview)
    scrollable_frame.pack(side=RIGHT, fill=Y)
    scroll_canvas.configure(yscrollcommand=scrollable_frame.set)
    scroll_canvas.bind('<Configure>', lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all')))
    all_task_frame = Frame(scroll_canvas)
    scroll_canvas.create_window((0, 0), window=all_task_frame)

    for task in data[user]:
        task_show_frame = Frame(all_task_frame)
        show_edit_task_button = Button(task_show_frame,
                                       text=f"Title: {task.title}                     Due Date: {task.due_date}\nStatus: {task.status}",
                                       width=50, height=3, font=("Ariel", 25, "bold"), fg='black', bg='#4ECDC4',
                                       activebackground="#292F36", activeforeground="#F5EEDC", padx=20, pady=10,
                                       command=lambda o=task: show_edit_task(dashboard_frame, user, o))
        show_edit_task_button.grid(row=0, column=0, sticky='e')

        delete_task_button = Button(task_show_frame, text="Delete\nTask", width=5, height=3,
                                    font=("Ariel", 25, "bold"), fg='black', bg='#4ECDC4', activebackground="#292F36",
                                    activeforeground="#F5EEDC", padx=20, pady=10,
                                    command=lambda o=task: delete_task(dashboard_frame, user, o))
        delete_task_button.grid(row=0, column=1, sticky='w')
        task_show_frame.pack(padx=10, pady=10, anchor="center")

    scroll_canvas.update_idletasks()
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    scroll_canvas.yview_moveto(0)

    search_button = Button(search_add_task_frame, text="Search", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',
                           activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10,
                           command=lambda: search_task(dashboard_frame, mainframe, user, search_entry,priority_combobox,status_combobox, type_combobox))
    search_button.grid(row=0, column=4, padx=10, pady=10, sticky="e")

def search_task(frame, mainframe, user, search_entry, priority_combobox, status_combobox, type_combobox):
    for widget in mainframe.winfo_children():
        widget.destroy()

    scroll_canvas = Canvas(mainframe, width=1120, height=400)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollable_frame = Scrollbar(mainframe, orient=VERTICAL, command=scroll_canvas.yview)
    scrollable_frame.pack(side=RIGHT, fill=Y)
    scroll_canvas.configure(yscrollcommand=scrollable_frame.set)
    scroll_canvas.bind('<Configure>', lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all')))
    all_task_frame = Frame(scroll_canvas)
    scroll_canvas.create_window((0, 0), window=all_task_frame, anchor="nw")

    for task in data[user]:
        if (not search_entry.get() or search_entry.get().lower() in task.title.lower()) and (not priority_combobox.get() or task.priority == priority_combobox.get()) and (not status_combobox.get() or task.status == status_combobox.get()) and (not type_combobox.get() or task.task_type == type_combobox.get()):
            task_show_frame = Frame(all_task_frame)
            show_edit_task_button = Button(task_show_frame,
                                           text=f"Title: {task.title}                     Due Date: {task.due_date}\nStatus: {task.status}",
                                           width=50, height=3, font=("Ariel", 25, "bold"), fg='black', bg='#4ECDC4',
                                           activebackground="#292F36", activeforeground="#F5EEDC", padx=20, pady=10,
                                           command=lambda obj=task: show_edit_task(frame, user, obj))
            show_edit_task_button.grid(row=0, column=0, sticky='e')

            delete_task_button = Button(task_show_frame, text="Delete\nTask", width=5, height=3,
                                        font=("Ariel", 25, "bold"), fg='black', bg='#4ECDC4',
                                        activebackground="#292F36",
                                        activeforeground="#F5EEDC", padx=20, pady=10,
                                        command=lambda obj=task: delete_task(frame, user, obj))
            delete_task_button.grid(row=0, column=1, sticky='w')
            task_show_frame.pack(padx=10, pady=10, anchor="nw")
    scroll_canvas.update_idletasks()
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    scroll_canvas.yview_moveto(0)

def add_task(frame, user):
    frame.pack_forget()
    add_task_frame = Frame(window, bg='#0D0527')
    add_task_frame.pack(expand=True, anchor='center')

    add_task_label = Label(add_task_frame, text="Add Task", font=("Ariel", 40, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    add_task_label.grid(row=0, column=1, padx=10, pady=10)

    title_label = Label(add_task_frame, text="Title", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    title_label.grid(row=1,column=0, padx=10, pady=10, sticky="w")

    title_entry = Entry(add_task_frame, font=("Ariel", 20), fg='black', bg='#FFE66D', width=25)
    title_entry.grid(row=1,column=1, padx=10, pady=10, sticky="w")

    description_label = Label(add_task_frame, text="Description", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    description_label.grid(row=2,column=0, padx=10, pady=10, sticky="w")

    description_text = Text(add_task_frame, font=("Ariel", 20), fg='black', bg='#FFE66D', width=30, height= 5)
    description_text.grid(row=2,column=1, padx=10, pady=10, sticky="w")

    due_date_label = Label(add_task_frame, text="Due Date", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    due_date_label.grid(row=3,column=0, padx=10, pady=10, sticky="w")

    due_date_entry = Calendar(add_task_frame)
    due_date_entry.grid(row=3,column=1, padx=10, pady=10, sticky="w")

    due_time_label = Label(add_task_frame, text="Due Time", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    due_time_label.grid(row=4,column=0, padx=10, pady=10, sticky="w")

    due_time_frame = Frame(add_task_frame, bg='#0D0527')
    due_time_frame.grid(row=4,column=1, padx=10, pady=10, sticky="w")

    hour_list = [f"{i:02d}" for i in range(1, 13)]
    due_time_hr_combobox = Combobox(due_time_frame, values=hour_list,state="readonly", width=3)
    due_time_hr_combobox.grid(row=0, column=0, sticky="w")

    minute_list = [f"{i:02d}" for i in range(0, 60)]
    due_time_min_combobox = Combobox(due_time_frame, values=minute_list,state="readonly", width=3)
    due_time_min_combobox.grid(row=0, column=1, sticky="w")

    due_time_am_pm_combobox = Combobox(due_time_frame, values=['AM', 'PM'],state="readonly", width=3)
    due_time_am_pm_combobox.grid(row=0, column=2, sticky="w")

    priority_label = Label(add_task_frame, text="Priority", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    priority_label.grid(row=5,column=0, padx=10, sticky="w")

    priority_combobox = Combobox(add_task_frame, values=['Low','Medium','High'], state="readonly", width=8)
    priority_combobox.grid(row=5,column=1, padx=10, sticky="w")

    status_label = Label(add_task_frame, text="Status", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    status_label.grid(row=6,column=0, padx=10, sticky="w")

    status_combobox = Combobox(add_task_frame, values=['Pending','In Progress','Done'],state="readonly", width=10)
    status_combobox.grid(row=6, column=1, padx=10, sticky="w")

    type_label = Label(add_task_frame, text="Type", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527", padx=10,pady=10)
    type_label.grid(row=7,column=0, padx=10, sticky="w")

    task_type_combobox = Combobox(add_task_frame, values=['Home', 'Work', 'Education', 'Miscellaneous'],state="readonly", width=12)
    task_type_combobox.grid(row=7, column=1, padx=10 ,sticky="w")

    add_task_button = Button(add_task_frame, text="Add Task", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda :add_task_work(add_task_frame, user, title_entry, description_text, due_date_entry, due_time_hr_combobox, due_time_min_combobox, due_time_am_pm_combobox, priority_combobox, status_combobox, task_type_combobox))
    add_task_button.grid(row=8,column=1, padx=10, pady=10, sticky="w")

def add_task_work(frame, user, title_entry, description_text, due_date_entry, due_time_hr_combobox, due_time_min_combobox, due_time_am_pm_combobox, priority_combobox, status_combobox, task_type_combobox):
    if title_entry.get() == "":
        messagebox.showwarning(title="Title Empty", message="Please enter a title in the Title field. It cannot be empty.")
        return
    else:
        title = title_entry.get()

    if description_text.get("1.0", "end-1c") == "":
        messagebox.showwarning(title="Description Empty", message="Please enter a Description in the Description field. It cannot be empty.")
        return
    else:
        description = description_text.get("1.0", "end-1c")

    if due_date_entry.get_date() == "":
        messagebox.showwarning(title="Due Date Empty", message="Please enter a Due Date in the Due Date field. It cannot be empty.")
        return
    else:
        due_date = due_date_entry.get_date()

    if due_time_hr_combobox.get() == "":
        messagebox.showwarning(title="Due Time Hour Empty", message="Please enter a Due Time Hour in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_hr = f"0{due_time_hr_combobox.get()}"

    if due_time_min_combobox.get() == "":
        messagebox.showwarning(title="Due Time minute Empty", message="Please enter a Due Time minute in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_min = due_time_hr_combobox.get()

    if due_time_am_pm_combobox.get() == "":
        messagebox.showwarning(title="Due Time AM/PM Empty", message="Please enter a Due Time AM/PM in the Due Time Hour field. It cannot be empty.")
        return
    elif due_time_am_pm_combobox.get() not in ['AM', 'PM', 'am', 'pm', 'Am','Pm','pM','aM']:
        messagebox.showwarning(title="Due Time AM/PM Wrong",message="Please enter Correct Due Time AM/PM in the Due Time AM/PM field.")
        return
    else:
        due_time_am_pm = due_time_am_pm_combobox.get().upper()

    due_time = f"{due_time_hr}:{due_time_min} {due_time_am_pm}"
    if priority_combobox.get() == "":
        messagebox.showwarning(title="Priority Empty", message="Please enter a Priority in the Priority field. It cannot be empty.")
        return
    else:
        priority = priority_combobox.get()
    if status_combobox.get() == "":
        messagebox.showwarning(title="Status Empty", message="Please enter a Status in the Status field. It cannot be empty.")
        return
    else:
        status = status_combobox.get()
    if task_type_combobox.get() == "":
        messagebox.showwarning(title="Task Type Empty", message="Please Enter Title in the Title Entry")
        return
    else:
        task_type = task_type_combobox.get()

    task = Task(title, description, due_date, due_time, priority, status, task_type, user.username)
    data[user].append(task)
    write_file(data_file_path, data)
    messagebox.showinfo(title="Task Saved", message="Your Task has been Saved Successfully")
    dashboard(frame, user)

def show_edit_task(frame, user, obj):
    frame.pack_forget()
    show_edit_task_frame = Frame(window, bg='#0D0527')
    show_edit_task_frame.pack(expand=True, anchor='center')

    add_task_label = Label(show_edit_task_frame, text="Task", font=("Ariel", 40, "bold"), fg='white', bg="#0D0527")
    add_task_label.grid(row=0, column=0)

    title_frame = Frame(show_edit_task_frame, bg='#0D0527')
    title_frame.grid(row=1, column=0, pady=5, sticky='w')

    title_label = Label(title_frame, text="Title", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    title_label.pack(anchor="w")

    title_entry = Entry(title_frame, font=("Ariel", 20), fg='black', bg='#FFE66D', width=30)
    title_entry.insert(0,obj.title)
    title_entry.pack(anchor="w")

    description_frame = Frame(show_edit_task_frame, bg='#0D0527')
    description_frame.grid(row=2, column=0, pady=5, sticky='w')

    description_label = Label(description_frame, text="Description", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    description_label.pack(anchor="w")

    description_text = Text(description_frame, font=("Ariel", 20), fg='black', bg='#FFE66D', width=40, height=5)
    description_text.insert("1.0",obj.description)
    description_text.pack(anchor="w")

    due_date_frame = Frame(show_edit_task_frame, bg='#0D0527')
    due_date_frame.grid(row=3, column=0, pady=10, sticky='w')

    due_date_label = Label(due_date_frame, text="Due Date", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    due_date_label.pack(anchor="w")

    due_date_entry = Calendar(due_date_frame)
    due_date_entry.selection_set(obj.due_date)
    due_date_entry.pack(anchor="w")

    due_time_frame = Frame(show_edit_task_frame, bg='#0D0527')
    due_time_frame.grid(row=4, column=0, pady=10, sticky='w')

    due_time_label = Label(due_time_frame, text="Due Time", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    due_time_label.pack(anchor="w")

    due_time_entry_frame = Frame(due_time_frame, bg='#0D0527')
    due_time_entry_frame.pack(anchor="w")
    due_time = str(obj.due_time)
    due_time_hr = due_time[:due_time.find(":")]
    due_time_min = due_time[due_time.find(":")+1:due_time.find(" ")]
    due_time_am_pm = due_time[due_time.find(" ")+1:]
    hour_list = [f"{i:02d}" for i in range(1, 13)]
    due_time_hr_combobox = Combobox(due_time_entry_frame, values=hour_list, state="readonly", width=3)
    due_time_hr_combobox.set(due_time_hr)
    due_time_hr_combobox.grid(row=0, column=0, sticky="w")

    minute_list = [f"{i:02d}" for i in range(0, 60)]
    due_time_min_combobox = Combobox(due_time_entry_frame, values=minute_list, state="readonly", width=3)
    due_time_min_combobox.set(due_time_min)
    due_time_min_combobox.grid(row=0, column=1, sticky="w")

    due_time_am_pm_combobox = Combobox(due_time_entry_frame, values=['AM', 'PM'], state="readonly", width=3)
    due_time_am_pm_combobox.set(due_time_am_pm)
    due_time_am_pm_combobox.grid(row=0, column=2, sticky="w")

    priority_frame = Frame(show_edit_task_frame, bg='#0D0527')
    priority_frame.grid(row=5, column=0, pady=5, sticky='w')

    priority_label = Label(priority_frame, text="Priority", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    priority_label.pack(anchor="w")

    priority_combobox = Combobox(priority_frame, values=['Low', 'Medium', 'High'], state="readonly", width=8)
    priority_combobox.set(obj.priority)
    priority_combobox.pack(anchor="w")

    status_frame = Frame(show_edit_task_frame, bg='#0D0527')
    status_frame.grid(row=6, column=0, pady=2, sticky='w')

    status_label = Label(status_frame, text="Status", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    status_label.pack(anchor="w")

    status_combobox = Combobox(status_frame, values=['Pending', 'In Progress', 'Done'], state="readonly", width=10)
    status_combobox.set(obj.status)
    status_combobox.pack(anchor="w")

    type_frame = Frame(show_edit_task_frame, bg='#0D0527')
    type_frame.grid(row=7, column=0, pady=5, sticky='w')

    type_label = Label(type_frame, text="Type", font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    type_label.pack(anchor="w")

    task_type_combobox = Combobox(type_frame, values=['Home', 'Work', 'Education', 'Miscellaneous'], state="readonly", width=12)
    task_type_combobox.set(obj.task_type)
    task_type_combobox.pack(anchor="w")

    save_changes_task_button = Button(show_edit_task_frame, text="Save Changes", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4', activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda: save_change_work(show_edit_task_frame, user, title_entry, description_text, due_date_entry, due_time_hr_combobox, due_time_min_combobox, due_time_am_pm_combobox, priority_combobox, status_combobox, task_type_combobox, obj))
    save_changes_task_button.grid(row=8, column=0, pady=10, sticky="w")

def save_change_work(frame, user, title_entry, description_text, due_date_entry, due_time_hr_combobox, due_time_min_combobox, due_time_am_pm_combobox, priority_combobox, status_combobox, task_type_combobox, obj):
    if title_entry.get() == "":
        messagebox.showwarning(title="Title Empty", message="Please enter a title in the Title field. It cannot be empty.")
        return
    else:
        title = title_entry.get()
    if description_text.get("1.0", "end-1c") == "":
        messagebox.showwarning(title="Description Empty", message="Please enter a Description in the Description field. It cannot be empty.")
        return
    else:
        description = description_text.get("1.0", "end-1c")
    if due_date_entry.get_date() == "":
        messagebox.showwarning(title="Due Date Empty", message="Please enter a Due Date in the Due Date field. It cannot be empty.")
        return
    else:
        due_date = due_date_entry.get_date()
    if due_time_hr_combobox.get() == "":
        messagebox.showwarning(title="Due Time Hour Empty", message="Please enter a Due Time Hour in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_hr = due_time_hr_combobox.get()
    if due_time_min_combobox.get() == "":
        messagebox.showwarning(title="Due Time minute Empty", message="Please enter a Due Time minute in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_min = due_time_min_combobox.get()
    if due_time_am_pm_combobox.get() == "":
        messagebox.showwarning(title="Due Time AM/PM Empty", message="Please enter a Due Time AM/PM in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_am_pm = due_time_am_pm_combobox.get()
    due_time = str(f"{due_time_hr}:{due_time_min} {due_time_am_pm}")
    if priority_combobox.get() == "":
        messagebox.showwarning(title="Priority Empty", message="Please enter a Priority in the Priority field. It cannot be empty.")
        return
    else:
        priority = priority_combobox.get()
    if status_combobox.get() == "":
        messagebox.showwarning(title="Status Empty", message="Please enter a Status in the Status field. It cannot be empty.")
        return
    else:
        status = status_combobox.get()
    if task_type_combobox.get() == "":
        messagebox.showwarning(title="Task Type Empty", message="Please Enter Title in the Title Entry")
        return
    else:
        task_type = task_type_combobox.get()

    for task in data[user]:
        if task == obj:
            obj.title = title
            obj.description = description
            obj.due_date = due_date
            obj.due_time = due_time
            obj.priority = priority
            obj.status = status
            obj.task_type = task_type
            obj.username = user.username
            break
    write_file(data_file_path, data)
    messagebox.showinfo(title="Task Saved", message="Your Task has been Saved Successfully")
    dashboard(frame, user)

def delete_task(frame, user, obj):
    frame.pack_forget()
    result = messagebox.askyesno(title="Confirm Remove Task",message=f"Do You want to Remove Task\n{obj.title}")
    if result:
        data[user].remove(obj)
        write_file(data_file_path, data)
        messagebox.showinfo(title="Task Removed",message="Given Task has been Removed")
        dashboard(frame, user)
    else:
        messagebox.showinfo(title="Operation Cancelled",message=f"Operation to Remove Task\n{obj.title}\nhas been Cancelled")

read_file(data_file_path, data)
myframe = Frame()
login(myframe)
window.mainloop()