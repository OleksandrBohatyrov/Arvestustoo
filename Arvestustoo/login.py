from tkinter import *
import mysql.connector
from tkinter import Tk
from tkinter.simpledialog import *
from subprocess import *

welcome_form = Tk()
welcome_form.title("Welcome to Translator")
welcome_form.geometry("700x500")
welcome_form.configure(bg="#141414")
welcome_form.iconbitmap('logo.ico')


welcome_message = Label(welcome_form, text="Welcome to Translate!", font=("Arial", 16), bg='#141414', fg='#FFFFFF')
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

    labelUser = Label(parent,text="Nimi: ", background = "dark slate gray",
                              foreground = "White", font=("Arial", 16), bg='#141414', fg='#FFFFFF')
    labelUser.place(x=25,y=20)

    entryUser = Entry(parent,textvariable=username)
    entryUser.place(x=100,y=25)

    labelPass = Label(parent,text="Parool: ", background = "dark slate gray",
                              foreground = "White", font=("Arial", 16), bg='#141414', fg='#FFFFFF')
    labelPass.place(x=25,y=57)

    LabelSwitch = Label(parent,text="Lülitus hele/tume teema ==>>", font=("Arial", 10), bg='#141414', fg='#FFFFFF')
    LabelSwitch.place(x=400, y=150)

    entryPass = Entry(parent,textvariable=password, show="*")
    entryPass.place(x=100,y=60)

    buttonLogin = Button(parent,text="LOGIN", font = "Arial 14 bold",command=login, bg='#141414', fg='#FFFFFF')
    buttonLogin.place(height=45,width=79 ,x=250,y=29)

    buttonRegister = Button(parent, text="REGISTER", font = "Arial 14 bold", bg='#141414', fg='#FFFFFF', command=register)
    buttonRegister.place(height=45,width=119, x=340, y=29)
    
    global message_label
    message_label = Label(parent, text="", background="#141414", foreground="#FFFFFF", font="Arial 8 bold")
    message_label.place(x=25, y=89)


    buttonResetPass = Button(parent, text="RESET PASSWORD", font="Arial 14 bold", bg='#141414', fg='#FFFFFF', command=reset_password)
    buttonResetPass.place(height=45,width=200, x=475, y=29)


    image = PhotoImage(file="tthk.png")
    smaller_image = image.subsample(3)  
    label = Label(parent, image=smaller_image, bg="#141414")
    label.image = smaller_image  
    label.pack(side=BOTTOM, pady=10)

 
    #nightmode-------------------
    image = PhotoImage(file="nightmode.png")
    smaller_image = image.subsample(7)  
    label = Label(parent, image=smaller_image, bg="#141414")
    label.image = smaller_image  
    label.pack(side=BOTTOM, pady=10)
    label.place(x=570, y=100)

    
    #daymode------------------------
    image = PhotoImage(file="daymode.png")
    smaller_dayimage = image.subsample(7)  
    label = Label(parent, image=smaller_dayimage, bg="#141414")
    label.image = smaller_dayimage  
    label.pack(side=BOTTOM, pady=10)
    label.place(x=585, y=120)

    def switch_theme():
        current_theme = parent.cget('bg')
        if current_theme == "#FFFFFF":
            parent.configure(bg="#141414")
            theme_button.configure(image=smaller_dayimage)
        else:
            parent.configure(bg="#FFFFFF")
            theme_button.configure(image=smaller_image)

    theme_button = Button(parent, image=smaller_image, bg="#141414", fg='#FFFFFF', borderwidth=0, command=switch_theme)
    theme_button.place(x=570, y=120)


def register():
    mycursor = mydb.cursor()

    # Проверка на наличие ника в базе данных
    sql = "SELECT * FROM login WHERE BINARY username = %s"
    val = (username.get(),)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result:
        message_label.config(text="Kasutajanimi on juba olemas.")
        return

    # Добавляем новую запись в базу данных
    sql = "INSERT INTO login (username, Password) VALUES (%s, %s)"
    val = (username.get(), password.get())
    mycursor.execute(sql, val)
    mydb.commit()

    message_label.config(text="Kirje sisestatud.")

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
        message_label.config(text="Kasutajanimi ei eksisteeri.")
        return

    new_password = askstring("Uus parool", "Sisesta uus parool", show="*")

    if not new_password:
        message_label.config(text="Uus parool on nõutav.")
        return

    sql = "UPDATE login SET Password = %s WHERE BINARY username = %s"
    val = (new_password, username.get())
    mycursor.execute(sql, val)
    mydb.commit()

    message_label.config(text="Parool muudetud.")

def login():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM login WHERE BINARY username = '%s' AND BINARY password = '%s'" % (username.get(),password.get())
    mycursor.execute(sql)
    if mycursor.fetchone():
        open_file()
    else:

         message_label.config(text="Kehtetud volikirjad")

def main():

    root = Tk()
    initialize_interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
