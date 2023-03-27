from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import googletrans
from textblob import *

root = Tk()
root.title("")
root.geometry("1200x700")
root.configure(bg="#141414")
root.iconbitmap('logo.ico')

img = Image.open("tthk.png")
img = img.resize((900, 400))
img = ImageTk.PhotoImage(img)
img_label = Label(root, image=img, bg='#141414')
img_label.place(x=85, y=290) 


def translate_text():
    translated_text.delete(1.0, END)
    for key, value in languages.items(): 
        if (value == original_combo.get()):
            from_language_key = key
    for key, value in languages.items(): 
        if (value == translated_combo.get()):
            to_language_key = key
    words = TextBlob(original_text.get(1.0, END))
    words = words.translate(from_lang=from_language_key , to=to_language_key)
    translated_text.insert(1.0, words)


def ograni4enie():

    inputValue=original_text.get("1.0","end-1c")
    print(inputValue)
    string = inputValue
    count=0
    for char in string:
        count +=1
    print(count)


languages = googletrans.LANGUAGES
language_list = list(languages.values())

original_text = Text(root, height=10, width=40, bg='#141414', fg='#FFFFFF', font=("Helvetica", 14))
original_text.grid(row=0, column=0, pady=20, padx=10)

translate_button = Button(root, text="Translate!", font=("Helvetica", 24), bg='#141414', fg='#FFFFFF', command=lambda:[translate_text(), ograni4enie()])
translate_button.grid(row=0, column=1, padx=10)

translated_text = Text(root, height=10, width=40, bg='#141414', fg='#FFFFFF', font=("Helvetica", 14))
translated_text.grid(row=0, column=2, pady=20, padx=10)


style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox",fieldbackground='black', background= "#ffcc00",foreground='white')
root.option_add("*TCombobox*Listbox*Background", 'black')
root.option_add('*TCombobox*Listbox*Foreground', 'white')
original_combo = ttk.Combobox(root, width=50, value=language_list)
original_combo.current(21)
original_combo.grid(row=1, column=0)


translated_combo = ttk.Combobox(root, width=50, value=language_list)
translated_combo.current(23)
translated_combo.grid(row=1, column=2)


def clear():
	original_text.delete(1.0, END)
	translated_text.delete(1.0, END)

clear_button = Button(root, text="Clear", command=clear, bg='#141414', fg='#FFFFFF')
clear_button.grid(row=2, column=1)

root.mainloop()