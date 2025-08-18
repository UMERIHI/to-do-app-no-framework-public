import datetime
import pickle
import re
from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import Calendar
import socket
from PIL import Image, ImageTk

info_img = "info.png"
ask_yes_no_img = "ask_yes_no.png"
error_img = "error.png"

client = socket.socket()
client.connect(("localhost", 65432))

window = Tk()

window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
window.title("Todo App")
window.config(background='#0D0527')

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

def login(frame):
    if frame and frame.winfo_exists():
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

    window.grab_set()
    window.wait_window()

def login_work(frame, username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    result = out_communication(f"check_login_user|{username}|{password}")
    if result is True:
        show_info_msg("Login Success","You have successfully logged in")
        dashboard(frame, username)
    elif result is False:
        show_error_msg("Login Failed", "login Failed Check Please Username and Password")
    else:
        show_error_msg("Login Failed", "login Failed Due to an Error")
        login(frame)

def signup(frame):
    if frame and frame.winfo_exists():
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

    window.grab_set()
    window.wait_window()

def signup_work(frame, email_entry, username_entry, password_entry):
    email = str(email_entry.get())
    username = str(username_entry.get())
    password = str(password_entry.get())

    if " " in username:
        show_error_msg("Incorrect Username", "Username should not contain spaces")
        return

    if " " in email:
        show_error_msg("Incorrect Email", "Email should not contain spaces")
        return

    if len(username) < 4:
        show_error_msg("Username Length Error", "Username should be at least 4 characters")
        return

    if len(password) < 8:
        show_error_msg("Password Length Error", "Password must be at least 8 characters")
        return

    domain = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(domain, email):
        show_error_msg("Incorrect Email", "Please Check Your Email Again Wrong Domain")
        return
    result = out_communication(f"otp_send|{email}|{username}")
    if result is False:
        show_error_msg("Signup Error"," Sign up Failed Username or Email Already Exist")
    elif result is None:
        show_error_msg("Signup Error"," Sign up Failed due to an Error")
    else:
        otp_verify(frame, result, email, username, password)

def otp_verify(frame, given_otp, email, username, password):
    if frame and frame.winfo_exists():
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

    dont_get_otp_button = Button(dont_get_otp_frame, text="Send Again", font=("Ariel", 15, "bold"), fg='black', bg='#4ECDC4', activebackground="#292F36", activeforeground="#F5EEDC",command=lambda: out_communication(f"otp_send|{email}|{username}"))
    dont_get_otp_button.grid(row=0, column=1)

    otp_verify_button = Button(otp_verify_frame, text="Verify Email", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda: save_user(otp_verify_frame, given_otp, otp_entry, email, username, password))
    otp_verify_button.grid(row=4,column=1, padx=10, pady=10)

    window.grab_set()
    window.wait_window()

def save_user(frame, otp_input, otp_entry, email, username, password):
    otp = otp_entry.get()
    if otp_input == otp:
        result = out_communication(f"insert_user|{email}|{username}|{password}")
        if result is True:
            show_info_msg("User Created",f"User with username: {username}\nhas Been Successfully Created")
            login(frame)
        else:
            show_error_msg("User Creation Failed", "User Creation has been Failed Due to an Error")
    else:
        show_error_msg("Email Verification Failed", "Email Verification Failed due to Wrong OTP Entered returning to Sign Up")
        signup(frame)

def dashboard(frame, username):
    if frame and frame.winfo_exists():
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

    search_button = Button(search_add_task_frame, text="Search", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4', activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda: search_task(dashboard_frame, mainframe, username, search_entry,priority_combobox,status_combobox, type_combobox))
    search_button.grid(row=0, column=4, padx=10, pady=10, sticky="e")

    add_task_button = Button(search_add_task_frame, text="Add Task", font=("Ariel", 20, "bold"), fg='black',bg='#4ECDC4', activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda: add_task(dashboard_frame, username))
    add_task_button.grid(row=0, column=5, padx=10, pady=10, sticky="e")

    mainframe = Frame(dashboard_frame)
    mainframe.pack()
    scroll_canvas = Canvas(mainframe, width=1120, height=400)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollable_frame = Scrollbar(mainframe, orient=VERTICAL, command=scroll_canvas.yview)
    scrollable_frame.pack(side=RIGHT, fill=Y)
    scroll_canvas.configure(yscrollcommand=scrollable_frame.set)
    scroll_canvas.bind('<Configure>', lambda scroll: scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all')))
    all_task_frame = Frame(scroll_canvas)
    scroll_canvas.create_window((0, 0), window=all_task_frame)
    result = get_task(f"fetch_tasks|{username}")
    if result is None:
        show_error_msg("Task Fetching Failed", "Fetching tasks failed due to an Error")
    else:
        for task in result:
            task_show_frame = Frame(all_task_frame)
            show_edit_task_button = Button(task_show_frame, text=(
                f"Title: {task.title} Due Date: {task.due_date} Status: {task.status}\nDescription: {task.description}"),
                                           width=50, height=3, font=("Ariel", 25, "bold"), fg='black', bg='#4ECDC4',
                                           activebackground="#292F36", activeforeground="#F5EEDC", padx=20, pady=10,
                                           command=lambda o=task: show_edit_task(dashboard_frame, username, o))
            show_edit_task_button.grid(row=0, column=0, sticky='e')

            delete_task_button = Button(task_show_frame, text="Delete\nTask", width=5, height=3,
                                        font=("Ariel", 25, "bold"), fg='black', bg='#4ECDC4',
                                        activebackground="#292F36", activeforeground="#F5EEDC", padx=20, pady=10,
                                        command=lambda o=task: delete_task_work(dashboard_frame, username, o))
            delete_task_button.grid(row=0, column=1, sticky='w')
            task_show_frame.pack(padx=10, pady=10, anchor="center")

    scroll_canvas.update_idletasks()
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    scroll_canvas.yview_moveto(0)

    window.grab_set()
    window.wait_window()

def search_task(frame, mainframe, username, search_entry, priority_combobox, status_combobox, type_combobox):
    if frame and frame.winfo_exists():
        for widget in mainframe.winfo_children():
            widget.destroy()

    scroll_canvas = Canvas(mainframe, width=1120, height=400)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollable_frame = Scrollbar(mainframe, orient=VERTICAL, command=scroll_canvas.yview)
    scrollable_frame.pack(side=RIGHT, fill=Y)
    scroll_canvas.configure(yscrollcommand=scrollable_frame.set)
    scroll_canvas.bind('<Configure>', lambda scroll: scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all')))
    all_task_frame = Frame(scroll_canvas)
    scroll_canvas.create_window((0, 0), window=all_task_frame, anchor="nw")
    result = get_task(f"fetch_tasks|{username}")
    for task in result:
        if (not search_entry.get() or search_entry.get().lower() in task.title.lower()) and (
                not priority_combobox.get() or task.priority == priority_combobox.get()) and (
                not status_combobox.get() or task.status == status_combobox.get()) and (
                not type_combobox.get() or task.task_type == type_combobox.get()):
            task_show_frame = Frame(all_task_frame)
            show_edit_task_button = Button(task_show_frame, text=(
                f"Title: {task.title} Due Date: {task.due_date} Status: {task.status}\nDescription: {task.description}"),
                                           width=50, height=3, font=("Ariel", 25, "bold"), fg='black', bg='#4ECDC4',
                                           activebackground="#292F36", activeforeground="#F5EEDC", padx=20, pady=10,
                                           command=lambda obj=task: show_edit_task(frame, username, obj))
            show_edit_task_button.grid(row=0, column=0, sticky='e')

            delete_task_button = Button(task_show_frame, text="Delete\nTask", width=5, height=3,
                                        font=("Ariel", 25, "bold"), fg='black', bg='#4ECDC4',
                                        activebackground="#292F36",
                                        activeforeground="#F5EEDC", padx=20, pady=10,
                                        command=lambda obj=task: delete_task_work(frame, username, obj))
            delete_task_button.grid(row=0, column=1, sticky='w')
            task_show_frame.pack(padx=10, pady=10, anchor="nw")

    scroll_canvas.update_idletasks()
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    scroll_canvas.yview_moveto(0)

    window.grab_set()
    window.wait_window()

def add_task(frame, username):
    if frame and frame.winfo_exists():
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

    add_task_button = Button(add_task_frame, text="Add Task", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda :add_task_work(add_task_frame, username, title_entry, description_text, due_date_entry, due_time_hr_combobox, due_time_min_combobox, due_time_am_pm_combobox, priority_combobox, status_combobox, task_type_combobox))
    add_task_button.grid(row=8,column=1, padx=10, pady=10, sticky="w")

    window.grab_set()
    window.wait_window()

def add_task_work(frame, username, title_entry, description_text, due_date_entry, due_time_hr_combobox, due_time_min_combobox, due_time_am_pm_combobox, priority_combobox, status_combobox, task_type_combobox):
    if title_entry.get() == "":
        show_error_msg("Title Empty", "Please enter a title in the Title field. It cannot be empty.")
        return
    else:
        title = title_entry.get()

    if description_text.get("1.0", "end-1c") == "":
        show_error_msg("Description Empty", "Please enter a Description in the Description field. It cannot be empty.")
        return
    else:
        description = description_text.get("1.0", "end-1c")

    if due_date_entry.get_date() == "":
        show_error_msg("Due Date Empty", "Please enter a Due Date in the Due Date field. It cannot be empty.")
        return
    else:
        due_date = due_date_entry.get_date()

    if due_time_hr_combobox.get() == "":
        show_error_msg("Due Time Hour Empty", "Please enter a Due Time Hour in the Due Time Hour field. It cannot be empty")
        return
    else:
        due_time_hr = f"{due_time_hr_combobox.get()}"

    if due_time_min_combobox.get() == "":
        show_error_msg("Due Time minute Empty", "Please enter a Due Time minute in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_min = due_time_hr_combobox.get()

    if due_time_am_pm_combobox.get() == "":
        show_error_msg("Due Time AM/PM Empty", "Please enter a Due Time AM/PM in the Due Time Hour field. It cannot be empty.")
        return
    elif due_time_am_pm_combobox.get() not in ['AM', 'PM', 'am', 'pm', 'Am','Pm','pM','aM']:
        show_error_msg("Due Time AM/PM Wrong","Please enter Correct Due Time AM/PM in the Due Time AM/PM field.")
        return
    else:
        due_time_am_pm = due_time_am_pm_combobox.get().upper()

    due_time = f"{due_time_hr}:{due_time_min} {due_time_am_pm}"
    if priority_combobox.get() == "":
        show_error_msg("Priority Empty", "Please enter a Priority in the Priority field. It cannot be empty.")
        return
    else:
        priority = priority_combobox.get()
    if status_combobox.get() == "":
        show_error_msg("Status Empty", "Please enter a Status in the Status field. It cannot be empty.")
        return
    else:
        status = status_combobox.get()
    if task_type_combobox.get() == "":
        show_error_msg("Task Type Empty", "Please Enter Title in the Title Entry")
        return
    else:
        task_type = task_type_combobox.get()

    result = out_communication(f"insert_task|{title}|{description}|{due_date}|{due_time}|{priority}|{status}|{task_type}|{username}")
    if result is True:
        show_info_msg("Task Saved", f"Task\n'{title}'\nSaved successfully.")
        dashboard(frame, username)
    else:
        show_error_msg("Task Creation Failed", f"Task creation has been failed due to an Error")
        return

def show_edit_task(frame, username, obj):
    if frame and frame.winfo_exists():
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

    save_changes_task_button = Button(show_edit_task_frame, text="Save Changes", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4', activebackground="#292F36", activeforeground="#F5EEDC", padx=10, pady=10, command=lambda: save_change_work(show_edit_task_frame, username, title_entry, description_text, due_date_entry, due_time_hr_combobox, due_time_min_combobox, due_time_am_pm_combobox, priority_combobox, status_combobox, task_type_combobox, obj))
    save_changes_task_button.grid(row=8, column=0, pady=10, sticky="w")

    window.grab_set()
    window.wait_window()

def save_change_work(frame, username, title_entry, description_text, due_date_entry, due_time_hr_combobox, due_time_min_combobox, due_time_am_pm_combobox, priority_combobox, status_combobox, task_type_combobox, obj):
    if title_entry.get() == "":
        show_error_msg("Title Empty", "Please enter a title in the Title field. It cannot be empty.")
        return
    else:
        title = title_entry.get()
    if description_text.get("1.0", "end-1c") == "":
        show_error_msg("Description Empty", "Please enter a Description in the Description field. It cannot be empty.")
        return
    else:
        description = description_text.get("1.0", "end-1c")
    if due_date_entry.get_date() == "":
        show_error_msg("Due Date Empty", "Please enter a Due Date in the Due Date field. It cannot be empty.")
        return
    else:
        due_date = due_date_entry.get_date()
    if due_time_hr_combobox.get() == "":
        show_error_msg("Due Time Hour Empty", "Please enter a Due Time Hour in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_hr = due_time_hr_combobox.get()
    if due_time_min_combobox.get() == "":
        show_error_msg("Due Time minute Empty", "Please enter a Due Time minute in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_min = due_time_min_combobox.get()
    if due_time_am_pm_combobox.get() == "":
        show_error_msg("Due Time AM/PM Empty", "Please enter a Due Time AM/PM in the Due Time Hour field. It cannot be empty.")
        return
    else:
        due_time_am_pm = due_time_am_pm_combobox.get()
    due_time = str(f"{due_time_hr}:{due_time_min} {due_time_am_pm}")
    if priority_combobox.get() == "":
        show_error_msg("Priority Empty", "Please enter a Priority in the Priority field. It cannot be empty.")
        return
    else:
        priority = priority_combobox.get()
    if status_combobox.get() == "":
        show_error_msg("Status Empty", "Please enter a Status in the Status field. It cannot be empty.")
        return
    else:
        status = status_combobox.get()
    if task_type_combobox.get() == "":
        show_error_msg("Task Type Empty", "Please Enter Title in the Title Entry")
        return
    else:
        task_type = task_type_combobox.get()

    result = get_task(f"fetch_tasks|{username}")
    if result is None:
        show_error_msg("Task Fetching Failed", f"Fetching tasks failed due to an Error")
    else:
        for task in result:
            if task.task_id == obj.task_id:
                obj.title = title
                obj.description = description
                obj.due_date = due_date
                obj.due_time = due_time
                obj.priority = priority
                obj.status = status
                obj.task_type = task_type
                break
    result = out_communication(f"update_task|{obj.task_id}|{title}|{description}|{due_date}|{due_time}|{priority}|{status}|{task_type}")
    if result is True:
        show_info_msg("Task Updated", f"Task\n{title}\nupdated successfully.")
    else:
        show_error_msg("Task Update Failed", "Task update failed due to an Error")
    dashboard(frame, username)

def delete_task_work(frame, username, obj):
    if frame and frame.winfo_exists():
        frame.pack_forget()
    try:
        answer = show_yes_no_msg("Confirm Remove Task", f"Do You want to Remove Task\n{obj.title}")
        if frame and frame.winfo_exists():
            if answer:
                result = out_communication(f"delete_task|{obj.task_id}")
                if result is True:
                    show_info_msg("Task Deleted", "Task has been Deleted successfully.")
                else:
                    show_error_msg("Task Deletion Failed", "Task deletion failed due to an Error")
            else:
                show_info_msg("Operation Cancelled", f"Operation to Remove Task\n{obj.title}\nhas been Cancelled")
        else:
            window.destroy()
    except Exception:
        return

    dashboard(frame, username)

def get_task(message):
    client.send(message.encode())
    size_data = client.recv(4)  # first 4 bytes = size
    size = int.from_bytes(size_data, 'big')  # convert back to int
    data = b""
    while len(data) < size:
        part = client.recv(4096)
        if not part:
            break
        data += part
    return pickle.loads(data)

def in_communication():
    response = client.recv(1024).decode()
    if response == "True":
        return True
    elif response == "False":
        return False
    elif response == "None":
        return None
    else:
        return response

def out_communication(message):
    client.send(message.encode())
    return in_communication()

def show_info_msg(title, message):
    msg_window = Toplevel(window)
    msg_window.title("Message")
    msg_window.config(background='#0D0527')

    width, height = 600, 350
    screen_w = msg_window.winfo_screenwidth()
    screen_h = msg_window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    msg_window.geometry(f"{width}x{height}+{x}+{y}")

    img = Image.open(info_img)
    img = img.resize((150, 150))
    icon = ImageTk.PhotoImage(img)

    icon_label = Label(msg_window, image=icon, bg="#0D0527")
    icon_label.pack()

    title_label = Label(msg_window, text=title, font=("Ariel", 25, "bold"), fg='white', bg="#0D0527")
    title_label.pack()

    msg_label = Label(msg_window, text=message, font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    msg_label.pack()

    ok_button = Button(msg_window, text="Ok", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC",width=12 ,height=2, command=lambda: msg_window.destroy())
    ok_button.pack(pady=20)
    msg_window.grab_set()
    msg_window.wait_window()

def show_error_msg(title, message):
    msg_window = Toplevel(window)
    msg_window.title("Message")
    msg_window.config(background='#0D0527')

    width, height = 600, 350
    screen_w = msg_window.winfo_screenwidth()
    screen_h = msg_window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    msg_window.geometry(f"{width}x{height}+{x}+{y}")

    img = Image.open(error_img)
    img = img.resize((150, 150))
    icon = ImageTk.PhotoImage(img)

    icon_label = Label(msg_window, image=icon, bg="#0D0527")
    icon_label.pack()

    title_label = Label(msg_window, text=title, font=("Ariel", 25, "bold"), fg='white', bg="#0D0527")
    title_label.pack()

    msg_label = Label(msg_window, text=message, font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    msg_label.pack()

    ok_button = Button(msg_window, text="Ok", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',activebackground="#292F36", activeforeground="#F5EEDC",width=12 ,height=2, command=lambda: msg_window.destroy())
    ok_button.pack(pady=20)
    msg_window.grab_set()
    msg_window.wait_window()

def show_yes_no_msg(title, message):
    msg_window = Toplevel(window)
    msg_window.title("Message")
    msg_window.config(background='#0D0527')

    width, height = 600, 350
    screen_w = msg_window.winfo_screenwidth()
    screen_h = msg_window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    msg_window.geometry(f"{width}x{height}+{x}+{y}")

    img = Image.open(ask_yes_no_img)
    img = img.resize((150, 150))
    icon = ImageTk.PhotoImage(img)

    icon_label = Label(msg_window, image=icon, bg="#0D0527")
    icon_label.pack()

    title_label = Label(msg_window, text=title, font=("Ariel", 25, "bold"), fg='white', bg="#0D0527")
    title_label.pack()

    msg_label = Label(msg_window, text=message, font=("Ariel", 20, "bold"), fg='white', bg="#0D0527")
    msg_label.pack()

    result = {"value": None}
    def on_yes():
        result["value"] = True
        msg_window.destroy()
    def on_no():
        result["value"] = False
        msg_window.destroy()

    button_frame = Frame(msg_window, bg='#0D0527')
    button_frame.pack()

    no_button = Button(button_frame, text="No", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',
                       activebackground="#292F36", activeforeground="#F5EEDC", width=8 ,height=2, command=on_no)
    no_button.grid(row=0, column=0,padx=10, pady=20)

    yes_button = Button(button_frame, text="Yes", font=("Ariel", 20, "bold"), fg='black', bg='#4ECDC4',
                       activebackground="#292F36", activeforeground="#F5EEDC",width=8 ,height=2, command=on_yes)
    yes_button.grid(row=0, column=1, padx=10, pady=20, sticky='w')

    msg_window.grab_set()
    msg_window.wait_window()

    return result["value"]

myframe = Frame()
login(myframe)
window.mainloop()


