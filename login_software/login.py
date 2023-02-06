import database as db
import local_database as ld
from google_drive_downloader import GoogleDriveDownloader as gdd
from tkinter import messagebox
import random
import urllib.request
import uuid
import requests
import datetime
import smtplib
import ssl
from socket import gaierror
from requests import get
from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import csv
import re

width = 450
height = 550
clicks = 0
text = ""
past_loc = []
rand_num = random.randint(10000000, 99999999)


class login_manager(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=False)
        container.configure(width=450, height=550)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login_screen, Sign_up, Select_room, Star_wars_pre_memes, Star_wars_se_memes, Lord_of_the_ring_memes,
                  Marvel_memes, Users_marvel, Users_pre, Users_ring, Users_se, Rank, Confirm_log_in, Settings,
                  Change_info):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.place(relwidth=1, relheight=1)

        self.show_frame("Login_screen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if not page_name == "Rank":
            past_loc.append(page_name)

    def show_password(self, pw):
        global clicks
        clicks += 1
        if clicks % 2 == 1:
            pw.configure(show="")
        else:
            pw.configure(show="*")

    def choose_page(self):
        if past_loc[-1] == "Users_pre" or past_loc[-1] == "Star_wars_pre_memes":
            self.show_frame("Star_wars_pre_memes")
        if past_loc[-1] == 'Users_se' or past_loc[-1] == 'Star_wars_se_memes':
            self.show_frame("Star_wars_se_memes")
        if past_loc[-1] == 'Users_ring' or past_loc[-1] == 'Lord_of_the_ring_memes':
            self.show_frame("Lord_of_the_ring_memes")
        if past_loc[-1] == 'Users_marvel' or past_loc[-1] == 'Marvel_memes':
            self.show_frame("Marvel_memes")

    def choose_users(self):
        if past_loc[-1] == 'Users_pre' or past_loc[-1] == 'Star_wars_pre_memes':
            self.show_frame("Users_pre")
        if past_loc[-1] == 'Users_se' or past_loc[-1] == 'Star_wars_se_memes':
            self.show_frame("Users_se")
        if past_loc[-1] == 'Users_ring' or past_loc[-1] == 'Lord_of_the_ring_memes':
            self.show_frame("Users_ring")
        if past_loc[-1] == 'Users_marvel' or past_loc[-1] == 'Marvel_memes':
            self.show_frame("Users_marvel")

    def secede(self):
        order = db.users[2].index(ld.pw)
        db.users[0].pop(order)
        db.users[1].pop(order)
        db.users[2].pop(order)
        db.users[3].pop(order)
        db.users[4].pop(order)
        del db.users[5][order]

    def download_image(self, url, url2, directory, dir2, notice):
        gdd.download_file_from_google_drive(file_id=url, dest_path=directory)
        gdd.download_file_from_google_drive(file_id=url2, dest_path=dir2)
        notice.place(x=360, y=40)


class Login_screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        global clicks

        logo = Label(self, text="Login UI", font=("Comic Sans", 26, "bold"), fg="green")
        logo.place(x=170, y=15)

        sign_in = Label(self, text="Sign In", font=("Comic Sans", 12, "bold"))
        sign_in.place(x=210, y=60)

        id_text = Label(self, text="ID:", font=("Comic Sans", 13))
        id_text.place(x=60, y=115)

        ID = Entry(self, font=("Comic Sans", 13))
        ID.place(x=50, y=140, width=350, height=45)

        ID_error = Label(self, text="ID with such name does not exist", font=("Comic Sans", 8), fg="red")

        pw_text = Label(self, text="Password:", font=("Comic Sans", 13))
        pw_text.place(x=60, y=210)

        pw = Entry(self, font=("Comic Sans", 13), show="*")
        pw.place(x=50, y=235, width=350, height=45)

        pw_error = Label(self, text="Password is incorrect, please try again", font=("Comic Sans", 8), fg="red")

        clicks = 0
        show_pw = Button(self, font=("Comic Sans", 8, "bold"), fg="#0099ff", highlightthickness=0, bd=0,
                         text="Show Password", command=lambda: controller.show_password(pw))
        show_pw.place(x=50, y=300, width=93, height=25)

        guest_mode = Label(self, text="Not your computer? Use Guest mode.(Not a feature)", font=("Comic Sans", 9),
                           fg="#808080")
        guest_mode.place(x=40, y=370)

        learn_more = Button(self, text="Learn more", font=("Comic Sans", 9, "bold"), fg="#0099ff", highlightthickness=0,
                            bd=0)
        learn_more.place(x=40, y=387, width=75, height=20)

        sign_up = Button(self, text="Sign up", font=("Comic Sans", 16, "bold"), fg="#0099ff", highlightthickness=0,
                         bd=0, command=lambda: controller.show_frame("Sign_up"))
        sign_up.place(x=40, y=470, width=80, height=30)

        def enter(id, pw):
            global user_mail
            cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            mac_address = ":".join(re.findall('..', "%12x" % uuid.getnode())).upper()

            if not id in db.users[1]:
                ID_error.place(x=50, y=185)
                pw_error.place(x=50, y=280)
            else:
                ID_error.place(x=6000, y=2300)
                pw_error.place(x=50, y=280)
                index = db.users[1].index(id)
            try:
                if not pw == db.users[2][index]:
                    pw_error.place(x=50, y=280)
                else:
                    pw_error.place(x=5000, y=3000)
            except UnboundLocalError:
                pw_error.place(x=50, y=280)
            if id in db.users[1] and pw in db.users[2]:
                ld.pw = pw
                for i in db.users[1]:
                    if i == id:
                        index = db.users[1].index(i)
                        ld.index = int(index)
                        if len(db.users[5][index]) == 0:
                            ip = get("https://api.ipify.org").text
                            db.users[5][index].append(str(mac_address))
                            db.users[6][index].append(ip)
                            ld.IP_add = ip
                            ld.MAC_ID = mac_address
                            controller.show_frame("Select_room")
                        elif mac_address in db.users[5][index]:
                            controller.show_frame("Select_room")
                        else:
                            ip = get("https://api.ipify.org").text
                            ld.IP_add = ip
                            ld.MAC_ID = mac_address
                            user_mail = db.users[3][index]

                            url = 'http://ip-api.com/json/'
                            params = {'query': ld.IP_add}
                            response = requests.get(url, params=params)
                            ip_info = response.json()

                            ip_address = ip_info['query']
                            country = ip_info['country']
                            region = ip_info['regionName']
                            network_provider = ip_info['org']

                            port = 465
                            smtp_server = "smtp.gmail.com"
                            login = "muengsun1964@gmail.com"
                            password = "vczoszkakvnvawlz"
                            subject = "Login UI Account Log-in Attempt From New Device"
                            context = ssl.create_default_context()
                            sender = "muengsun1964@gmail.com"
                            receiver = user_mail
                            message = f"""\
                           To: {receiver}
                           From: {sender}
                           Subject: {subject}

                           Your Login UI account had a log-in attempt from a new device.
                           For your security, Login UI wants to make sure it's really you.
                           Do you recognize this device? If you don't, someone else has your password.
                           It is highly recommended to change your password immediately.

                               MAC address: %s
                               Public IP address: %s
                               Location: %s, %s
                               Time: %s
                               Network provider: %s

                           If you recognize this device, please copy this code needed to login to the account %s:

                           %s""" % (mac_address, ip_address, region, country, cur_time, network_provider, id, rand_num)

                            try:
                                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                    server.login(login, password)
                                    server.sendmail(sender, receiver, message)
                                    controller.show_frame("Confirm_log_in")
                            except (gaierror, ConnectionRefusedError):
                                print("Failed to connect to the server. Bad connection settings")
                            except smtplib.SMTPServerDisconnected:
                                print("Failed to connect to the server. Wrong user/password")
                            except smtplib.SMTPException as e:
                                print("SMTP error occurred: " + str(e))

        log_in = Button(self, bg="#0099ff", font=("Comic Sans", 10, "bold"), fg="white", bd=0, text="Log In",
                        command=lambda: enter(ID.get(), pw.get()))
        log_in.place(x=310, y=460, width=90, height=40)


class Confirm_log_in(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Users", font=("Comic Sans", 30, "bold"), fg="grey")
        title.place(x=30, y=0)

        verify = Entry(self, font=("Comic Sans", 48, "bold"), fg="#0099ff", justify=CENTER)
        verify.place(x=50, y=200, width=330, height=100)

        ver_button = Button(self, font=("Comic Sans", 8), text="Verify", bg="#0099ff", bd=0,
                            command=lambda: check_code(int(verify.get())))
        ver_button.place(x=50, y=320, width=50, height=20)

        def check_code(code):
            if not code == rand_num:
                verify_error = Label(self, font=("Comic Sans", 8), fg="red",
                                     text="Wrong verification Code. Please try again")
                verify_error.place(y=300, x=50)
            else:
                controller.show_frame("Select_room")

                db.users[5][ld.index].append(ld.MAC_ID)
                if ld.IP_add not in db.users[6][ld.index]:
                    db.users[6][ld.index].append(ld.IP_add)


class Sign_up(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        global clicks

        def register(first_name, last_name, id, password, password_confirm, month, day, year, email, checkbox):
            name = first_name + " " + last_name
            birthday = month + " " + day + ", " + year
            if len(first_name) == 0:
                first_name_error.place(x=30, y=100)
            else:
                first_name_error.place(x=5600, y=50000)
            if len(last_name) == 0:
                last_name_error.place(x=240, y=100)
            else:
                last_name_error.place(x=5000, y=5000)
            if len(id) == 0:
                id_create_error.place(x=30, y=240)
            else:
                id_create_error.place(x=45000, y=29023)
            if len(password) == 0:
                pw_create_error.place(x=30, y=335)
            else:
                pw_create_error.place(x=4095, y=2345)
            if len(password_confirm) == 0:
                pw_confirm_error.place(x=240, y=335)
            else:
                pw_confirm_error.place(x=4346, y=3456)
            if len(month) == 0:
                month_error.place(x=30, y=460)
            else:
                month_error.place(x=54000, y=34000)
            if len(day) == 0:
                day_error.place(x=230, y=460)
            else:
                day_error.place(x=4000, y=34000)
            if len(year) == 0:
                year_error.place(x=320, y=460)
            else:
                year_error.place(x=5000, y=5000)
            if len(email) == 0:
                email_error.place(x=30, y=165)
            else:
                email_error.place(x=50000, y=34000)
            if id in db.users[1]:
                id_create_error2.place(x=30, y=240)
            else:
                id_create_error2.place(x=40000, y=40000)
            if email in db.users[3]:
                email_error2.place(x=30, y=165)
            else:
                email_error2.place(x=5000, y=54000)
            if 0 < len(password) < 8 or len(password) > 50:
                pw_create_error1.place(x=30, y=335)
            else:
                pw_create_error1.place(x=3000, y=4000)
            if not password == password_confirm:
                pw_confirm_error2.place(x=240, y=335)
            else:
                pw_confirm_error2.place(x=4000, y=4000)
            if checkbox == 0:
                agree_error.place(x=30, y=500)
            else:
                agree_error.place(x=5000, y=70000)
            if len(first_name) > 0 and len(last_name) > 0 and len(id) > 0 and len(password) > 0 and len(
                    password_confirm) > 0 \
                    and len(month) > 0 and len(day) > 0 and len(year) > 0 and len(email) > 0 and id not in db.users[1] \
                    and email not in db.users[3] and 7 < len(
                password) < 51 and password == password_confirm and checkbox == 1:
                db.users[0].append(name)
                db.users[1].append(id)
                db.users[2].append(password)
                db.users[3].append(email)
                db.users[4].append(birthday)
                db.users[5].append([])
                db.users[6].append([])
                print(db.users)
                controller.show_frame("Login_screen")

        titles = Label(self, text="Create your Login UI account", font=("Comic Sans", 14, "bold"))
        titles.place(x=55, y=0)

        first_name = Label(self, font=("Comic Sans", 8, "bold"), text="First Name")
        first_name.place(x=30, y=45)

        last_name = Label(self, font=("Comic Sans", 8, "bold"), text="Last Name")
        last_name.place(x=240, y=45)

        first_name_txt = Entry(self, font=("Comic Sans", 12,))
        first_name_txt.place(x=30, y=65, width=190, height=35)

        first_name_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        last_name_txt = Entry(self, font=("Comic Sans", 12))
        last_name_txt.place(x=240, y=65, width=190, height=35)

        last_name_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        id_create = Label(self, font=("Comic Sans", 8, "bold"), text="ID")
        id_create.place(x=30, y=185)

        id_create_txt = Entry(self, font=("Comic Sans", 12))
        id_create_txt.place(x=30, y=205, width=400, height=35)

        id_create_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        id_create_error2 = Label(self, font=("Comic Sans", 8), fg="red", text="The same ID already exists")

        id_create_info = Label(self, font=("Comic Sans", 8), text="You can use letters, numbers, & periods")
        id_create_info.place(x=30, y=260)

        email = Label(self, font=("Comic Sans", 8, "bold"), text="e-mail")
        email.place(x=30, y=110)

        email_txt = Entry(self, font=("Comic Sans", 12))
        email_txt.place(x=30, y=130, width=400, height=35)

        email_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        email_error2 = Label(self, font=("Comic Sans", 8), fg="red",
                             text="An account was already registered with this email")

        pw_create = Label(self, font=("Comic Sans", 8, "bold"), text="Password")
        pw_create.place(x=30, y=280)

        pw_create_txt = Entry(self, font=("Comic Sans", 12), show="*")
        pw_create_txt.place(x=30, y=300, width=190, height=35)

        pw_create_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        pw_create_error1 = Label(self, font=("Comic Sans", 6), fg="red",
                                 text="Password has to be between 8-50 characters")

        pw_confirm = Label(self, font=("Comic Sans", 8, "bold"), text="Password Confirm")
        pw_confirm.place(x=240, y=280)

        pw_confirm_txt = Entry(self, font=("Comic Sans", 12), show="*")
        pw_confirm_txt.place(x=240, y=300, width=190, height=35)

        pw_confirm_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        pw_confirm_error2 = Label(self, font=("Comic Sans", 6), fg="red", text="Confirm does not match with password")

        clicks = 0
        pw_register_show = Button(self, font=("Comic Sans", 8, "bold"), text="Show Password", bd=0, fg="#0099ff",
                                  command=lambda: controller.show_password(pw_create_txt))
        pw_register_show.place(x=30, y=350, height=25)

        pw_create_info = Label(self, font=("Comic Sans", 8),
                               text="Use 8 to 50 characters with a mix of letters, numbers, & symbols")
        pw_create_info.place(x=30, y=372)

        birthday = Label(self, font=("Comic Sans", 8, "bold"), text="Birthday")
        birthday.place(x=30, y=390)

        month = Label(self, font=("Comic Sans", 8, "bold"), text="Month")
        month.place(x=30, y=410)

        day = Label(self, font=("Comic Sans", 8, "bold"), text="Day")
        day.place(x=230, y=410)

        year = Label(self, font=("Comic Sans", 8, "bold"), text="Year")
        year.place(x=310, y=410)

        month_txt = Combobox(self, font=("Comic Sans", 12),
                             values=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                     'September', 'October', 'November', 'December'], state="readonly")
        month_txt.place(x=30, y=430, width=180, height=30)

        month_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        day_txt = Entry(self, font=("Comic Sans", 12))
        day_txt.place(x=230, y=430, width=60, height=30)

        day_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        year_txt = Entry(self, font=("Comic Sans", 12))
        year_txt.place(x=310, y=430, width=120, height=30)

        year_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")

        var = IntVar()
        agree = Checkbutton(self, text="I agree to Login UI's terms of service and privacy policy",
                            font=("Comic Sans", 9), variable=var)
        agree.place(x=30, y=480)

        agree_error = Label(self, font=("Comic Sans", 7), fg="red", text="You have to agree in order to sign up")

        sign_in_instead = Button(self, text="Sign in instead", font=("Comic Sans", 10, "bold"), bd=0, fg="#0099ff",
                                 command=lambda: controller.show_frame("Login_screen"))
        sign_in_instead.place(x=30, y=510, height=25)

        sign_up_confirm = Button(self, text="Sign Up", font=("Comic Sans", 10, "bold"), fg="white", bg="#0099ff", bd=0,
                                 command=lambda: register(first_name_txt.get(), last_name_txt.get(),
                                                          id_create_txt.get(), pw_create_txt.get(),
                                                          pw_confirm_txt.get(), month_txt.get(), day_txt.get(),
                                                          year_txt.get(), email_txt.get(), var.get()))
        sign_up_confirm.place(x=360, y=510, height=30, width=70)


class Select_room(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        sign_out = Button(self, text="Sign Out", font=("Comic Sans", 10, "bold"), bg="#0099ff",
                          command=lambda: controller.show_frame("Login_screen"), bd=0, fg="white")
        sign_out.place(x=20, y=85, width=70, height=25)

        self.img = Image.open("setting.png")
        self.img = self.img.resize((30, 30), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.img)

        settings = Button(self, image=self.image, bd=0, command=lambda: controller.show_frame("Settings"))
        settings.place(y=75, x=390)

        titles = ["Star Wars Sequel Memes", "Star Wars Prequel Memes", "Lord of the Ring Memes", "Marvel Memes",
                  "Empty"]

        room = Label(self, text="Rooms", font=("Comic Sans", 36, "bold"), fg="grey")
        room.place(x=155, y=15)

        uf_club = Frame(self, bg="white")
        uf_club.place(x=20, y=120, width=410, height=80)

        uf_titles = Label(uf_club, font=("Comic Sans", 14, "bold"), text=titles[0], bg="white", fg='grey')
        uf_titles.place(x=20, y=10)

        uf_pop = Label(uf_club, font=("Comic Sans", 8, "bold"), text="Members:  97/150                 Status: Active",
                       bg="white", fg="green")
        uf_pop.place(x=40, y=60)

        uf_join = Button(uf_club, font=("Comic Sans", 8, "bold"), text="Join", bg="#0099ff", fg="white", bd=0,
                         command=lambda: controller.show_frame("Star_wars_se_memes"))
        uf_join.place(x=320, y=40, height=30, width=70)

        mf1_club = Frame(self, bg="white")
        mf1_club.place(x=20, y=205, width=410, height=80)

        mf1_titles = Label(mf1_club, font=("Comic Sans", 14, "bold"), text=titles[1], bg="white", fg='grey')
        mf1_titles.place(x=20, y=10)

        mf1_pop = Label(mf1_club, font=("Comic Sans", 8, "bold"),
                        text="Members:  487/500                 Status: Active", bg="white", fg="green")
        mf1_pop.place(x=40, y=60)

        mf1_join = Button(mf1_club, font=("Comic Sans", 8, "bold"), text="Join", bg="#0099ff", fg="white", bd=0,
                          command=lambda: controller.show_frame("Star_wars_pre_memes"))
        mf1_join.place(x=320, y=40, height=30, width=70)

        mf2_club = Frame(self, bg="white")
        mf2_club.place(x=20, y=290, width=410, height=80)

        mf2_titles = Label(mf2_club, font=("Comic Sans", 14, "bold"), text=titles[2], bg="white",
                           fg='grey')
        mf2_titles.place(x=20, y=10)

        mf2_pop = Label(mf2_club, font=("Comic Sans", 8, "bold"),
                        text="Members:  218/300                 Status: Active", bg="white", fg="green")
        mf2_pop.place(x=40, y=60)

        mf2_join = Button(mf2_club, font=("Comic Sans", 8, "bold"), text="Join", bg="#0099ff", fg="white", bd=0,
                          command=lambda: controller.show_frame("Lord_of_the_ring_memes"))
        mf2_join.place(x=320, y=40, height=30, width=70)

        mf3_club = Frame(self, bg="white")
        mf3_club.place(x=20, y=375, width=410, height=80)

        mf3_titles = Label(mf3_club, font=("Comic Sans", 14, "bold"), text=titles[3], bg="white",
                           fg='grey')
        mf3_titles.place(x=20, y=10)

        mf3_pop = Label(mf3_club, font=("Comic Sans", 8, "bold"),
                        text="Members:  218/300                 Status: Active", bg="white", fg="green")
        mf3_pop.place(x=40, y=60)

        mf3_join = Button(mf3_club, font=("Comic Sans", 8, "bold"), text="Join", bg="#0099ff", fg="white", bd=0,
                          command=lambda: controller.show_frame("Marvel_memes"))
        mf3_join.place(x=320, y=40, height=30, width=70)

        bf_club = Frame(self, bg="white")
        bf_club.place(x=20, y=460, width=410, height=80)

        bf_titles = Label(bf_club, font=("Comic Sans", 14, "bold"), text=titles[4], bg="white",
                          fg='grey')
        bf_titles.place(x=20, y=10)


class Settings(Frame):
    def __init__(self, parent, controller):
        global clicks
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Settings", font=("Comic Sans", 30, "bold"), fg="grey")
        title.place(x=30, y=0)

        change_info = Label(self, text="Change account information", font=("Comic Sans", 18, "bold"))
        change_info.place(x=20, y=70)

        change_account_info = Button(self, text="Change account information", font=("Comic Sans", 10), fg="#0099ff",
                                     bd=0, command=lambda: change(password.get()))
        change_account_info.place(x=20, y=205)

        pw_create = Label(self, font=("Comic Sans", 8, "bold"), text="Password")
        pw_create.place(x=30, y=110)

        password = Entry(self, font=("Comic Sans", 12), show="*")
        password.place(x=30, y=130, width=390, height=35)

        clicks = 0
        pw_show = Button(self, font=("Comic Sans", 8, "bold"), text="Show Password", bd=0, fg="#0099ff",
                         command=lambda: controller.show_password(password))
        pw_show.place(x=30, y=183, height=25)

        pw_create_error = Label(self, text="No entry", font=("Comic Sans", 8), fg="red")
        pw_error = Label(self, text="Password is incorrect, please try again", font=("Comic Sans", 8), fg="red")

        change_info = Label(self, text="Secession", font=("Comic Sans", 18, "bold"))
        change_info.place(x=20, y=260)

        warning_txt = """This procedure will erase all information of this account.
You will not be able to to log in with this account again."""

        warning = Label(self, text=warning_txt, font=("Comic Sans", 10))
        warning.place(x=30, y=300)

        secession = Button(self, text="Secede", font=("Comic Sans", 10), bg="#0099ff", bd=0,
                           command=lambda: controller.secede())
        secession.place(x=30, y=340, width=70, height=30)

        back = Button(self, text="return to room selection", font=("Comic Sans", 10), bd=0, fg="#0099ff",
                      command=lambda: controller.show_frame('Select_room'))
        back.place(x=30, y=400, )

        def change(password):
            if len(password) == 0:
                pw_create_error.place(x=30, y=165)
            else:
                pw_create_error.place(x=4095, y=2345)

            if not password == ld.pw and len(password) > 1:
                pw_error.place(x=30, y=165)
            else:
                pw_error.place(x=50000, y=20000)
            if password == ld.pw:
                controller.show_frame("Change_info")


class Change_info(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        global clicks

        def register(first_name, last_name, id, password, password_confirm, month, day, year, email):
            num = db.users[2].index(ld.pw)
            if len(first_name) > 0 and len(last_name) > 0:
                com_name = first_name + " " + last_name
                db.users[0][num] = com_name
            if len(id) > 0 and id not in db.users[1]:
                db.users[1][num] = id
            if len(password) > 0 and password not in db.users[2]:
                db.users[2][num] = password
            if len(email) > 0 and email not in db.users[3]:
                db.users[3][num] = email
            if len(month) > 0 and len(day) > 0 and len(year) > 0:
                birday = month + " " + day + ", " + year
                db.users[4][num] = birday
            if id in db.users[1]:
                id_create_error2.place(x=30, y=240)
            else:
                id_create_error2.place(x=40000, y=40000)
            if email in db.users[3]:
                email_error2.place(x=30, y=165)
            else:
                email_error2.place(x=5000, y=54000)
            if 0 < len(password) < 8 or len(password) > 50:
                pw_create_error1.place(x=30, y=335)
            else:
                pw_create_error1.place(x=3000, y=4000)
            if not password == password_confirm:
                pw_confirm_error2.place(x=240, y=335)
            else:
                pw_confirm_error2.place(x=4000, y=4000)
            if password in db.users[2]:
                pw_create_error.place(x=30, y=335)
            if id not in db.users[1] \
                    and email not in db.users[3] and 7 < len(
                password) < 51 and password == password_confirm and password not in db.users[2]:
                controller.show_frame("Settings")

        titles = Label(self, text="Create your Login UI account", font=("Comic Sans", 14, "bold"))
        titles.place(x=55, y=0)

        first_name = Label(self, font=("Comic Sans", 8, "bold"), text="First Name")
        first_name.place(x=30, y=45)

        last_name = Label(self, font=("Comic Sans", 8, "bold"), text="First Name")
        last_name.place(x=240, y=45)

        first_name_txt = Entry(self, font=("Comic Sans", 12,))
        first_name_txt.place(x=30, y=65, width=190, height=35)

        last_name_txt = Entry(self, font=("Comic Sans", 12))
        last_name_txt.place(x=240, y=65, width=190, height=35)

        id_create = Label(self, font=("Comic Sans", 8, "bold"), text="ID")
        id_create.place(x=30, y=185)

        id_create_txt = Entry(self, font=("Comic Sans", 12))
        id_create_txt.place(x=30, y=205, width=400, height=35)

        id_create_error2 = Label(self, font=("Comic Sans", 8), fg="red", text="The same ID already exists")

        id_create_info = Label(self, font=("Comic Sans", 8), text="You can use letters, numbers, & periods")
        id_create_info.place(x=30, y=260)

        email = Label(self, font=("Comic Sans", 8, "bold"), text="e-mail")
        email.place(x=30, y=110)

        email_txt = Entry(self, font=("Comic Sans", 12))
        email_txt.place(x=30, y=130, width=400, height=35)

        email_error2 = Label(self, font=("Comic Sans", 8), fg="red",
                             text="An account was already registered with this email")

        pw_create = Label(self, font=("Comic Sans", 8, "bold"), text="Password")
        pw_create.place(x=30, y=280)

        pw_create_txt = Entry(self, font=("Comic Sans", 12), show="*")
        pw_create_txt.place(x=30, y=300, width=190, height=35)

        pw_create_error = Label(self, font=("Comic Sans", 6), fg="red",
                                text="An account was already registered with this password")

        pw_create_error1 = Label(self, font=("Comic Sans", 6), fg="red",
                                 text="Password has to be between 8-50 characters")

        pw_confirm = Label(self, font=("Comic Sans", 8, "bold"), text="Password Confirm")
        pw_confirm.place(x=240, y=280)

        pw_confirm_txt = Entry(self, font=("Comic Sans", 12), show="*")
        pw_confirm_txt.place(x=240, y=300, width=190, height=35)

        pw_confirm_error2 = Label(self, font=("Comic Sans", 6), fg="red", text="Confirm does not match with password")

        clicks = 0
        pw_register_show = Button(self, font=("Comic Sans", 8, "bold"), text="Show Password", bd=0, fg="#0099ff",
                                  command=lambda: controller.show_password(pw_create_txt))
        pw_register_show.place(x=30, y=350, height=25)

        pw_create_info = Label(self, font=("Comic Sans", 8),
                               text="Use 8 to 50 characters with a mix of letters, numbers, & symbols")
        pw_create_info.place(x=30, y=372)

        birthday = Label(self, font=("Comic Sans", 8, "bold"), text="Birthday")
        birthday.place(x=30, y=390)

        month = Label(self, font=("Comic Sans", 8, "bold"), text="Month")
        month.place(x=30, y=410)

        day = Label(self, font=("Comic Sans", 8, "bold"), text="Day")
        day.place(x=230, y=410)

        year = Label(self, font=("Comic Sans", 8, "bold"), text="Year")
        year.place(x=310, y=410)

        month_txt = Combobox(self, font=("Comic Sans", 12),
                             values=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                     'September', 'October', 'November', 'December'], state="readonly")
        month_txt.place(x=30, y=430, width=180, height=30)

        day_txt = Entry(self, font=("Comic Sans", 12))
        day_txt.place(x=230, y=430, width=60, height=30)

        year_txt = Entry(self, font=("Comic Sans", 12))
        year_txt.place(x=310, y=430, width=120, height=30)

        sign_in_instead = Button(self, text="Go back to settings", font=("Comic Sans", 10, "bold"), bd=0, fg="#0099ff",
                                 command=lambda: controller.show_frame("Settings"))
        sign_in_instead.place(x=30, y=510, height=25)

        sign_up_confirm = Button(self, text="Sign Up", font=("Comic Sans", 10, "bold"), fg="white", bg="#0099ff", bd=0,
                                 command=lambda: register(first_name_txt.get(), last_name_txt.get(),
                                                          id_create_txt.get(), pw_create_txt.get(),
                                                          pw_confirm_txt.get(), month_txt.get(), day_txt.get(),
                                                          year_txt.get(), email_txt.get()))
        sign_up_confirm.place(x=360, y=510, height=30, width=70)


class Star_wars_pre_memes(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Star Wars Prequel Memes", font=("Comic Sans", 18, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.show_frame("Users_pre"))
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Star_wars_pre_memes"))
        room.place(x=20, y=165)

        images = ["star_wars_meme1.png", "star_wars_meme2.png"]

        self.img = Image.open(images[0])
        self.img = self.img.resize((360, 200), Image.ANTIALIAS)
        self.resized_img = ImageTk.PhotoImage(self.img)

        meme1 = Label(self, image=self.resized_img)
        meme1.place(x=75, y=60, width=360, height=200)

        self.img2 = Image.open(images[1])
        self.img2 = self.img2.resize((360, 280), Image.ANTIALIAS)
        self.resized_img2 = ImageTk.PhotoImage(self.img2)

        meme1 = Label(self, image=self.resized_img2)
        meme1.place(x=75, y=265, width=360, height=280)

        download = Button(self, text="Download", font=("Comic Sans", 10, "bold"), fg="white", bg="#0099ff", bd=0,
                          command=lambda: controller.download_image("1b79seWZZB3FmCN9qeB7IQsnhmRXH8fOf",
                                                                    "1Z3d976H8IrxsVUGE906f2RhjdNuVgWX4",
                                                                    "C:/Users/mueng/Downloads/Star Wars Prequel Meme 1.png",
                                                                    "C:/Users/mueng/Downloads/Star Wars Prequel Meme 2.png",
                                                                    download_complete))
        download.place(x=360, y=10, height=30, width=70)

        download_complete = Label(self, text="Complete!", font=("Comic Sans", 8), fg="red")


class Star_wars_se_memes(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Star Wars Sequel Memes", font=("Comic Sans", 18, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.show_frame("Users_se"))
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Star_wars_se_memes"))
        room.place(x=20, y=165)

        images = ["star_wars_se_meme1.png", "star_wars_se_meme2.png"]

        self.img = Image.open(images[0])
        self.img = self.img.resize((360, 200), Image.ANTIALIAS)
        self.resized_img = ImageTk.PhotoImage(self.img)

        meme1 = Label(self, image=self.resized_img)
        meme1.place(x=75, y=60, width=360, height=200)

        self.img2 = Image.open(images[1])
        self.img2 = self.img2.resize((360, 280), Image.ANTIALIAS)
        self.resized_img2 = ImageTk.PhotoImage(self.img2)

        meme1 = Label(self, image=self.resized_img2)
        meme1.place(x=75, y=265, width=360, height=280)

        download = Button(self, text="Download", font=("Comic Sans", 10, "bold"), fg="white", bg="#0099ff", bd=0,
                          command=lambda: controller.download_image("1RjwPs2mB0ZA3mxSI-g1H1CWIsp4ySjJL",
                                                                    "1DRHAjuuVH2W-wPDsOO0AHa-YXif5qj9Z",
                                                                    "C:/Users/mueng/Downloads/Star Wars Sequel Meme 1.png",
                                                                    "C:/Users/mueng/Downloads/Star Wars Sequel Meme 2.png",
                                                                    download_complete))
        download.place(x=360, y=10, height=30, width=70)

        download_complete = Label(self, text="Complete!", font=("Comic Sans", 8), fg="red")


class Lord_of_the_ring_memes(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Lord of the Ring Memes", font=("Comic Sans", 18, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.show_frame("Users_ring"))
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Lord_of_the_ring_memes"))
        room.place(x=20, y=165)

        empty1 = Label(self, text="Empty", font=("Comic Sans", 10))
        empty1.place(x=75, y=60)


class Marvel_memes(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Marvel Memes", font=("Comic Sans", 18, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.show_frame("Users_marvel"))
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Marvel_memes"))
        room.place(x=20, y=165)

        empty2 = Label(self, text="Empty", font=("Comic Sans", 10))
        empty2.place(x=75, y=60)


class Users_pre(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Users", font=("Comic Sans", 30, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.show_frame("Users_pre"))
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Star_wars_pre_memes"))
        room.place(x=20, y=165)

        global text
        i = 0
        user = Text(self, font=("Comic Sans", 8), bd=0)
        while i < len(db.star_wars_pre[0]):
            text = "Nickname: %s\nRank: %s\n" % (db.star_wars_pre[0][i], db.star_wars_pre[1][i])
            user.insert("end", text)
            i += 1

        user.configure(state=DISABLED)
        user.place(x=75, y=60, width=350, height=480)


class Users_se(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Users", font=("Comic Sans", 30, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.show_frame("Users_se"))
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Star_wars_se_memes"))
        room.place(x=20, y=165)

        global text
        user = Text(self, font=("Comic Sans", 8), bd=0)
        i = 0
        while i < len(db.star_wars_se[0]):
            text = "Nickname: %s\nRank: %s\n" % (db.star_wars_se[0][i], db.star_wars_se[1][i])
            user.insert("end", text)
            i += 1

        user.configure(state=DISABLED)
        user.place(x=75, y=60, width=350, height=480)


class Users_ring(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Users", font=("Comic Sans", 30, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.show_frame("Users_ring"))
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Lord_of_the_ring_memes"))
        room.place(x=20, y=165)

        global text
        user = Text(self, font=("Comic Sans", 8), bd=0)
        i = 0
        while i < len(db.lord_of_the_ring[0]):
            text = "Nickname: %s\nRank: %s\n" % (db.lord_of_the_ring[0][i], db.lord_of_the_ring[1][i])
            user.insert("end", text)
            i += 1

        user.configure(state=DISABLED)
        user.place(x=75, y=60, width=350, height=480)


class Users_marvel(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Users", font=("Comic Sans", 30, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.show_frame("Users_marvel"))
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Marvel_memes"))
        room.place(x=20, y=165)

        global text
        i = 0
        user = Text(self, font=("Comic Sans", 8), bd=0)
        while i < len(db.marvel[0]):
            text = "Nickname: %s\nRank: %s\n" % (db.marvel[0][i], db.marvel[1][i])
            user.insert("end", text)
            i += 1

        user.configure(state=DISABLED)
        user.place(x=75, y=60, width=350, height=480)


class Rank(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        title = Label(self, text="Rank", font=("Comic Sans", 30, "bold"), fg="grey")
        title.place(x=30, y=0)

        home = Button(self, text="home", font=("Comic Sans", 10), bd=0,
                      command=lambda: controller.show_frame("Select_room"))
        home.place(x=20, y=60)

        users = Button(self, text="users", font=("Comic Sans", 10), bd=0,
                       command=lambda: controller.choose_users())
        users.place(x=20, y=95)

        rank = Button(self, text="rank", font=("Comic Sans", 10), bd=0, command=lambda: controller.show_frame("Rank"))
        rank.place(x=20, y=130)

        room = Button(self, text="room", font=("Comic Sans", 10), bd=0, command=lambda: controller.choose_page())
        room.place(x=20, y=165)

        description = """1. Leader: Has all access to room.\n\n\n
2. Co-leader: Has all characteristics of manager and can \nalso post notices.\n\n\n
3. Manager: Has all characteristics of co-manager and \ncan also send private messages to leader.\n\n\n
4. Co-manager: Has all characteristics of elder and can \nalso write comments.\n\n\n
5. Elder: Has all characteristics of supporter and can also \npost photos.\n\n\n
6. Supporter: Has all characteristics of member and can \nalso post texts and can be hidden from others in the room.\n\n\n
7. Member: Can view and download posts. """

        desc1 = Label(self, text=description, font=("Comic Sans", 10), justify=LEFT)
        desc1.place(x=75, y=60)


if __name__ == "__main__":
    def callback():
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            with open('data.csv', 'w') as data:
                csv_writer = csv.writer(data)
                csv_writer.writerow(['name', 'id', 'pw', 'email', 'birthday', 'mac id', 'ip address'])
                for i in range(len(db.users[0])):
                    csv_writer.writerow([db.users[0][i], db.users[1][i], db.users[2][i], db.users[3][i], db.users[4][i], db.users[5][i], db.users[6][i]])
            app.destroy()

    app = login_manager()
    app.protocol("WM_DELETE_WINDOW", callback)
    app.resizable(False, False)
    app.mainloop()



