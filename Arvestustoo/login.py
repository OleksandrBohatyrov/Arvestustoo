from tkinter import *
import mysql.connector
from tkinter import Tk
from tkinter.simpledialog import *
from subprocess import *

welcome_form = Tk()
welcome_form.title("Welcome to Translator")
welcome_form.geometry("700x500")
welcome_form.configure(bg="#141414")
welcome_form.iconbitmap("logo.ico")


welcome_message = Label(welcome_form, text="Tere tulemast tõlkima!", font=("Arial", 16), bg='#141414', fg='#FFFFFF')
welcome_message.pack(pady=20)
def start_game():
    welcome_form.destroy() 

start_button = Button(welcome_form, text="Start", font=("Arial", 12),bg='#141414', fg='#FFFFFF',borderwidth=0, command=start_game)
start_button.pack()


welcome_form.mainloop()


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    database = "login"
)


def initialize_interface(parent):

    parent.title("Login")
    parent.configure(bg="#141414")
    parent.geometry("690x500")
    parent.resizable(False,False)

    global username
    global password

    username = StringVar()
    password = StringVar()

    labelUser = Label(parent,text="Nimi: ", font=("Arial", 16), bg='#141414', fg='#FFFFFF')
    labelUser.place(x=25,y=20)

    entryUser = Entry(parent,textvariable=username)
    entryUser.place(x=100,y=25)


    labelPass = Label(parent,text="Parool: ", font=("Arial", 16), bg='#141414', fg='#FFFFFF')
    labelPass.place(x=25,y=57)

    entryPass = Entry(parent,textvariable=password, show="*")
    entryPass.place(x=100,y=60)


    global message_label
    message_label = Label(parent, text="", bg="#141414", fg="#FFFFFF", font="Arial 8 bold")
    message_label.place(x=25, y=89)


    buttonLogin = Button(parent,text="LOGIN", font = "Arial 14 bold", command=login, bg='#141414', fg='#FFFFFF')
    buttonLogin.place(height=45,width=79 ,x=250,y=29)

    buttonRegister = Button(parent, text="REGISTER", font = "Arial 14 bold", bg='#141414', fg='#FFFFFF', command=register)
    buttonRegister.place(height=45,width=119, x=340, y=29)

    buttonResetPass = Button(parent, text="RESET PASSWORD", font="Arial 14 bold", bg="#141414", fg="#FFFFFF", command=reset_password)
    buttonResetPass.place(height=45,width=200, x=475, y=29)


    image = PhotoImage(file="tthk.png")
    smaller_image = image.subsample(3)  
    label = Label(parent, image=smaller_image, bg="#141414")
    label.image = smaller_image  
    label.pack(side=BOTTOM, pady=10)


    def dark():
        parent.configure(bg="#141414")
        labelUser.config(bg="#141414", fg="#FFFFFF")
        labelPass.config(bg="#141414", fg="#FFFFFF")
        buttonLogin.config(bg="#141414", fg="#FFFFFF")
        buttonRegister.config(bg="#141414", fg="#FFFFFF")
        buttonResetPass.config(bg="#141414",fg="#FFFFFF")
        message_label.config(bg="#141414", fg="#FFFFFF")
        label.config(bg="#141414")

    def light():
        parent.configure(bg="#FFFFFF")
        labelUser.config(bg="#FFFFFF", fg="BLACK")
        labelPass.config(bg="#FFFFFF",fg="BLACK")
        buttonLogin.config(bg="#FFFFFF",fg="BLACK")
        buttonRegister.config(bg="#FFFFFF",fg="BLACK")
        buttonResetPass.config(bg="#FFFFFF",fg="BLACK")
        label.config(bg="#FFFFFF",fg="#121212")
        message_label.config(bg="#FFFFFF", fg="BLACK")

    dark_btn = Button(parent, text="Tume",bg="#141414",fg="#FFFFFF",command=dark)
    dark_btn.place(y=120, x=100)
    
    light_btn = Button(parent, text="Hele",bg="#FFFFFF",fg="#121212",command=light)
    light_btn.place(y=120, x=27)



    def estonian():
        labelUser.config(text="Nimi: ")
        labelPass.config(text="Parool: ")
        buttonLogin.config(text="LOGIN")
        buttonRegister.config(text="REGISTER")
        buttonRegister.place(height=45,width=119, x=340, y=29)
        buttonResetPass.config(text="RESET PASSWORD")
        buttonResetPass.place(height=45,width=200, x=475, y=29)
        dark_btn.config(text="Tume")
        light_btn.config(text="Hele")

    def russian():
        labelUser.config(text="Имя: ")
        labelPass.config(text="Пароль: ")
        buttonLogin.config(text="ЛОГИН")
        buttonRegister.config(text="РЕГИСТРАЦИЯ")
        buttonRegister.place(height=45,width=150)
        buttonResetPass.config(text="Смена пароля")
        buttonResetPass.place(height=45,width=150, x=500, y=29)
        dark_btn.config(text="Темная")
        light_btn.config(text="Светлая")
    
    est_btn = Button(parent, text="Eesti keeles",bg='#141414',fg='#FFFFFF',command=estonian)
    est_btn.place(y=120, x=270)

    rus_btn = Button(parent, text="На русском",bg='#141414',fg='#FFFFFF',command=russian)
    rus_btn.place(y=120,x=160)




def register():
    mycursor = mydb.cursor()

    # Проверка на наличие ника в базе данных
    sql = "SELECT * FROM login WHERE BINARY username = %s"
    val = (username.get(),)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result:
        h=message_label.config(text="Kasutajanimi on juba olemas.")
        return

    # Добавляем новую запись в базу данных
    sql = "INSERT INTO login (username, Password) VALUES (%s, %s)"
    val = (username.get(), password.get())
    mycursor.execute(sql, val)
    mydb.commit()

    g=message_label.config(text="Kirje sisestatud.")

    print(mycursor.rowcount, "Kirje sisestatud.")


def open_file():
    filename2 = "trans.py"
    call(['python', filename2])

def reset_password():
    mycursor = mydb.cursor()

    sql = "SELECT * FROM login WHERE BINARY username = %s"
    val = (username.get(),)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if not result:
        d=message_label.config(text="Kasutajanimi ei eksisteeri.")
        return

    new_password = askstring("Uus parool", "Sisesta uus parool", show="*")

    if not new_password:
        c=message_label.config(text="Uus parool on nõutav.")
        return

    sql = "UPDATE login SET Password = %s WHERE BINARY username = %s"
    val = (new_password, username.get())
    mycursor.execute(sql, val)
    mydb.commit()

    a=message_label.config(text="Parool muudetud.")


def login():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM login WHERE BINARY username = '%s' AND BINARY password = '%s'" % (username.get(),password.get())
    mycursor.execute(sql)
    if mycursor.fetchone():
        open_file()

    else:

         b=message_label.config(text="Kehtetud volikirjad")


def main():

    root = Tk()
    initialize_interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
