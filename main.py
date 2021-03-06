import tkinter
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for l in range(nr_letters)]
    password_symbols = [random.choice(symbols) for s in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for n in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_to_file():
    website = website_input.get()
    mail = mail_input.get()
    password = password_input.get()
    new_data = {website: {
        "email": mail,
        "password": password
    }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)

        else:
            # Updating old data with new dat
            data.update(new_data)
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)

        finally:
            website_input.delete(0, tkinter.END)
            password_input.delete(0, tkinter.END)


# ---------------------------- FIND DATA ------------------------------- #
def find_password():
    website = website_input.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Email:{data[website]['email']}\n"
                                                       f"Password:{data[website]['password']}")
        else:
            messagebox.showerror(title="Error", message=f"No details for the {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Password Manager")
window.minsize(width=500, height=400)
window.config(padx=50, pady=50)

# Canvas
canvas = tkinter.Canvas(width=200, height=200)
logo = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_label = tkinter.Label(text="Website:")
website_label.grid(column=0, row=1)

mail_label = tkinter.Label(text="Email/Username:")
mail_label.grid(column=0, row=2)

password_label = tkinter.Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_input = tkinter.Entry(width=33)
website_input.grid(column=1, row=1)
website_input.focus()

mail_input = tkinter.Entry(width=52)
mail_input.grid(column=1, row=2, columnspan=2)

password_input = tkinter.Entry(width=33)
password_input.grid(column=1, row=3)

# Buttons
gen_pass_button = tkinter.Button(text="Generate Password", command=generate_password)
gen_pass_button.grid(column=2, row=3)

add_button = tkinter.Button(text="Add", width=44, command=save_to_file)
add_button.grid(column=1, row=4, columnspan=2)

search_button = tkinter.Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
