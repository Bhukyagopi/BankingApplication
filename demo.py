from tkinter import *
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import messagebox
import os
import mysql.connector
from tkinter import ttk
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gopi@123",
    database="SAFE_BANK_OF_INDIA"
)
cursor = db.cursor()
main = Tk()

main.title("SAFE BANKING OF INDIA")
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
main.geometry(f"{screen_width}x{screen_height}")

# Global variables for CAPTCHA
captcha_text = ""
entry = None
image_label = None
name_entry=""
pass_entry=""
email_entry=""
fullname_entry=""
mobile_entry=""

def image(logo_path):

    if os.path.exists(logo_path):
        image = Image.open(logo_path)
        image = image.resize((1550, 800))  # Resize the image with LANCZOS filter
        logo_image = ImageTk.PhotoImage(image)
        label2 = Label(main, image=logo_image)
        label2.image = logo_image  # Keep a reference to the image to prevent garbage collection
        label2.place(x=0, y=0)
    else:
        messagebox.showerror("Error", f"Logo image not found at {logo_path}")

def start_page():
    global name_entry,pass_entry
    for widget in main.winfo_children():
        widget.destroy()
    # Heading
    logo_path = "C:\\Users\\gopin\\Downloads\\background2.webp"
    image(logo_path)

    label1 = Label(main, text="SAFE BANK OF INDIA", font=('Comfort', 45), fg="red")
    label1.place(x=400, y=50)

    # Adjust the path to your logo image

    # Username
    username1 = Label(main, text="USERNAME:", font=('arial', 15))
    username1.place(x=450, y=250)
    username2 = Entry(main, width=30, font=('arial', 15))
    username2.place(x=600, y=250)

    # Password
    password1 = Label(main, text="PASSWORD", font=('arial', 15))
    password1.place(x=450, y=300)
    password2 = Entry(main, width=30, font=('arial', 15), show='*')
    password2.place(x=600, y=300)

    # Login button
    login = Button(main, text="LOGIN", font=('arial', 15), width=30,command=lambda:login_page(username2.get(),password2.get()))
    login.place(x=600, y=350)
    # Register button
    reg = Button(main, text="REGISTER", font=('arial', 15), width=30, command=register)
    reg.place(x=600, y=400)

def register():
    global entry, image_label, captcha_text,name_entry,pass_entry,email_entry,fullname_entry,mobile_entry

    # Clear previous widgets
    for widget in main.winfo_children():
        widget.destroy()
    logo_path = "C:\\Users\\gopin\\Downloads\\reg3.jpg"
    image(logo_path)
    heading = Label(main, text="REGISTRATION PAGE", font=('Comfort', 25), fg="red")
    heading.place(x=500, y=100)

    name_label = Label(main, text="USERNAME:", font=('arial', 15))
    name_label.place(x=450, y=150)
    name_entry = Entry(main, width=30, font=('arial', 15))
    name_entry.place(x=600, y=150)

    pass_label = Label(main, text="PASSWORD:", font=('arial', 15))
    pass_label.place(x=450, y=200)
    pass_entry = Entry(main, width=30, font=('arial', 15), show='*')
    pass_entry.place(x=600, y=200)

    email_label = Label(main, text="EMAIL:", font=('arial', 15))
    email_label.place(x=450, y=250)
    email_entry = Entry(main, width=30, font=('arial', 15))
    email_entry.place(x=600, y=250)

    fullname_label = Label(main, text="FULLNAME:", font=('arial', 15))
    fullname_label.place(x=450, y=300)
    fullname_entry = Entry(main, width=30, font=('arial', 15))
    fullname_entry.place(x=600, y=300)

    mobile_label=Label(main,text="MOBILE", font=('arial', 15))
    mobile_label.place(x=450,y=350)
    mobile_entry=Entry(main,width=30,font=('arial', 15))
    mobile_entry.place(x=600,y=350)

    captcha_text = generate_captcha()
    captcha_image = generate_image(captcha_text)

    photo = ImageTk.PhotoImage(captcha_image)
    image_label = Label(main, image=photo)
    image_label.image = photo  # Keep a reference to the image to prevent garbage collection
    image_label.place(x=450, y=400)

    # Input field for user entry
    entry = Entry(main, font=('Arial', 14), width=30)
    entry.place(x=600, y=400)
    # Submit button
    submit_button = Button(main, text="Submit", width=20, command=validate_and_submit)
    submit_button.place(x=600, y=450)
    # Refresh button
    refresh_button = Button(main, text="Refresh", command=refresh, width=20)
    refresh_button.place(x=780, y=450)
    Back_to_Main=Button(main,text="EXIT",command=start_page,width=30)
    Back_to_Main.place(x=600,y=500)

def validate_and_submit():
    username = name_entry.get()
    password = pass_entry.get()
    email = email_entry.get()
    fullname = fullname_entry.get()
    mobile = mobile_entry.get()
    user_captcha = entry.get()

    if not username:
        label=Label(main,text="username required!",font=('arial', 15), fg="red")
        label.place(x=600,y=550)
        return

    if not password:
        label = Label(main, text="password required!", font=('arial', 15), fg="red")
        label.place(x=600, y=550)
        return

    if not email:
        label = Label(main, text="email required!", font=('arial', 15), fg="red")
        label.place(x=600, y=550)
        return

    if not fullname:
        label = Label(main, text="name required!", font=('arial', 15), fg="red")
        label.place(x=600, y=550)
        return

    if not mobile:
        label = Label(main, text="mobile number required!", font=('arial', 15), fg="red")
        label.place(x=600, y=550)
        return

    if len(mobile) != 10 or not mobile.isdigit():
        label = Label(main, text="mobile number must be of 10 digits", font=('arial', 15), fg="red")
        label.place(x=600, y=550)
        return

    if user_captcha != captcha_text:
        label = Label(main, text="captcha does not match", font=('arial', 15), fg="red")
        label.place(x=600, y=550)
        return

    # All validations passed, submit the form
    submit(username, password, email, fullname, mobile)
def generate_captcha():
    global captcha_text
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return captcha_text

def generate_image(text):
    width, height = 120, 30
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 24)
    d.text((10, 0), text, font=font, fill=(0, 0, 0))
    return image

# Function to refresh CAPTCHA
def refresh():
    global captcha_text, image_label
    captcha_text = generate_captcha()
    image = generate_image(captcha_text)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

def submit(username,password,email,fullname,mobile):
    global captcha_text, entry,name_entry,pass_entry,fullname_entry,email_entry,mobile_entry
    if entry:
        user_input = entry.get()
        if user_input == captcha_text:
            messagebox.showinfo("Success", "CAPTCHA verified!")
            entry.delete(0, END)  # Clear the entry field
            name_entry.delete(0,END)
            pass_entry.delete(0,END)
            email_entry.delete(0,END)
            fullname_entry.delete(0,END)
            mobile_entry.delete(0,END)
            refresh()
            create_user(username,password,email,fullname,mobile)
        else:
            messagebox.showerror("Error", "Incorrect CAPTCHA, please try again.")
            refresh()
    else:
        messagebox.showerror("Error", "Entry field not initialized.")

def create_user(username, password, email, fullname, mobile):
    try:
        # Attempt to insert user data into the database
        cursor.execute("INSERT INTO users(username, password, email, fullname, mobile) VALUES (%s, %s, %s, %s, %s)", (username, password, email, fullname, mobile))
        db.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except mysql.connector.IntegrityError as e:
        # Handle integrity constraint violations (e.g., duplicate username or email)
        messagebox.showerror("Error", "This email or username has been used already! Please use another email or username.")
    except Exception as e:
        # Handle other unexpected errors
        messagebox.showerror("Error", f"Failed to create user: {e}")

def login_page(username, password):
    try:
        cursor.execute("SELECT username FROM users WHERE username=%s AND password=%s", (username, password))
        dbusername = cursor.fetchone()[0]
        cursor.execute("SELECT user_id FROM users WHERE username=%s AND password=%s", (username, password))
        user_id = cursor.fetchone()[0]
        main_page(user_id)
    except Exception as e:
        label=Label(main,text="please enter valid username and password",font=('arial', 15),fg="red")
        label.place(x=450,y=750)

def main_page(user_id):
    for widget in main.winfo_children():
        widget.destroy()
    logo_path = "C:\\Users\\gopin\\Downloads\\main page.2jpg.jpeg"
    image(logo_path)
    create_account = Button(main, text="CREATE ACCOUNT", width=30,font=('arial', 15), command=lambda: Create_Account(user_id))
    create_account.place(x=150,y=200)
    profile = Button(main, text="PROFILE & BALANCE", width=30,font=('arial', 15),command=lambda :Profile(user_id))
    profile.place(x=150,y=250)

    deposit_btn = Button(main, text="DEPOSIT", width=30,font=('arial', 15),command=lambda :deposit(user_id,))
    deposit_btn.place(x=150,y=300)
    withdraw_btn = Button(main, text="WITHDRAW",command=lambda :withdraw(user_id,), width=30,font=('arial', 15))
    withdraw_btn.place(x=150,y=350)
    transfer_btn = Button(main, text="TRANSFER",command=lambda :transfer(user_id,), width=30,font=('arial', 15))
    transfer_btn.place(x=150,y=400)
    transaction_history_btn = Button(main, text="TRANSACTION HISTORY",command=lambda :transaction_history(user_id,), width=30,font=('arial', 15))
    transaction_history_btn.place(x=150,y=450)
    delete_acc=Button(main,text="DELETE ACCOUNT",width=30,font=('arial', 15),command=lambda :delete_account(user_id,))
    delete_acc.place(x=150,y=500)
    delete_acc = Button(main, text="DELETE USER", width=30, font=('arial', 15),
                        command=lambda: delete_user(user_id, ))
    delete_acc.place(x=150, y=550)
    exit_button = Button(main, text="LOG OUT",command=start_page, width=30,font=('arial', 15))
    exit_button.place(x=150,y=600)

def Create_Account(user_id):
    for widget in main.winfo_children():
        widget.destroy()
    logo_path = "C:\\Users\\gopin\\Downloads\\main page.jpg"
    image(logo_path)
    user_id=user_id
    label=Label(main,text="CREATING NEW ACCOUNT",font=('Comfort', 35), fg="red")
    label.place(x=450,y=100)
    label1=Label(main,text="Name:",font=('arial', 15),width=20)
    label1.place(x=450,y=250)
    entry1=Entry(main,font=('arial', 15),width=30)
    entry1.place(x=700,y=250)
    label2=Label(main,text="Age:",font=('arial', 15),width=20)
    label2.place(x=450,y=300)
    entry2=Entry(main,font=('arial', 15),width=30)
    entry2.place(x=700,y=300)
    button = Button(main, text="LOGIN", font=('arial', 15), width=30,command=lambda :CreateAccount_db(user_id,entry1.get(),entry2.get(),))
    button.place(x=700,y=350)
    back_button = Button(main, text="EXIT", width=30, command=lambda :main_page(user_id,),font=('arial', 15))
    back_button.place(x=700, y=400)


def CreateAccount_db(user_id,name, age):
    try:
        cursor.execute("INSERT INTO accounts (user_id,name, age, balance) VALUES (%s, %s, %s,%s)", (user_id,name, age, 0.00))
        db.commit()
        account_id = cursor.lastrowid
        label=Label(main,text="account created successfully", font=('arial', 15))
        label.place(x=600,y=450)
        account_label=Label(main,text=f"user_id={user_id}\n\n Account_id={account_id}\n\nName={name}\n\n Age={age}\n\n Balance=0.00", font=('arial', 15))
        account_label.place(x=600,y=500)

    except Exception as e:
        label=Label(main,text=f"error in creating account:{e}")

def Profile(user_id):
    try:
        for widget in main.winfo_children():
            widget.destroy()
        logo_path = "C:\\Users\\gopin\\Downloads\\profile2.jpg"
        image(logo_path)
        cursor.execute("SELECT * FROM users where user_id=%s", (user_id,))
        data = cursor.fetchone()
        user=Label(main,text=f"user_id={data[0]}\n\nusername={data[1]}\n\npassword={data[2]}\n\nemail={data[3]}\n\nfull_name={data[4]}\n\nmobile_number={data[5]}",font=('arial', 15))
        user.place(x=450,y=100)

        cursor.execute("select account_id from accounts where user_id=%s",(user_id,))
        acc_ids = cursor.fetchall()  # fetchall() to get all results
        # Display account IDs
        if acc_ids:
            for i, acc_id in enumerate(acc_ids, start=1):
                cursor.execute("select balance from accounts where account_id=%s",(acc_id))
                balance=cursor.fetchone()[0]
                acc_label = Label(main, text=f"Account {i} ID: {acc_id[0]} -- Balance:{balance}", font=('arial', 15))
                acc_label.place(x=700, y=50 + i * 50)
        back_button = Button(main, text="EXIT", width=15, command=lambda :main_page(user_id,), font=('arial', 15))
        back_button.place(x=450,y=400)

    except Exception as e:
        print(e)

def deposit(user_id):
    for widget in main.winfo_children():
        widget.destroy()
    logo_path = "C:\\Users\\gopin\\Downloads\\deposit2.webp"
    image(logo_path)
    acc_label=Label(main,text="Account Number:",font=('arial', 15),width=20)
    acc_label.place(x=400,y=200)
    acc_entry=Entry(main, width=30,font=('arial', 15))
    acc_entry.place(x=700,y=200)
    bal_label = Label(main, text="Amount:", font=('arial', 15),width=20)
    bal_label.place(x=400, y=250)
    bal_entry = Entry(main, width=30, font=('arial', 15))
    bal_entry.place(x=700, y=250)
    deposit_button=Button(main,text="DEPOSIT",font=('arial', 15), width=30,command=lambda :deposit_db(acc_entry.get(),bal_entry.get()))
    deposit_button.place(x=700,y=300)
    exit_button = Button(main, text="EXIT", command=lambda :main_page(user_id,),font=('arial', 15), width=30)
    exit_button.place(x=700,y=350)
def deposit_db(account_id,bal):
    try:
        amount=int(bal)
        if (amount>=0):
            cursor.execute("UPDATE accounts SET balance=balance+%s WHERE account_id=%s",(amount,account_id,))
            db.commit()
            cursor.execute("INSERT INTO transactions (account_id,type,amount) VALUES (%s,%s,%s)",(account_id,'deposit',amount))
            db.commit()
            label = Label(main, text=f"the amount of {amount} has been desposited successfully!",font=('arial', 15))
            label.place(x=600, y=400)
            cursor.execute("SELECT balance FROM accounts WHERE account_id=%s",(account_id,))
            balance=cursor.fetchone()[0]
            label2 = Label(main, text=f"Total Balance after deposit={balance}",font=('arial', 15))
            label2.place(x=600, y=450)
        else:
            label = Label(main, text="enter valid amount!",font=('arial', 15),fg="red")
            label.place(x=600, y=400)
    except Exception as e:
        label = Label(main, text=f"enter valid account_id! {e}", font=('arial', 15), fg="red")
        label.place(x=600, y=400)

def withdraw(user_id):
    for widget in main.winfo_children():
        widget.destroy()
    logo_path = "C:\\Users\\gopin\\Downloads\\withdraw1.webp"
    image(logo_path)
    acc_label=Label(main,text="Account Number:",font=('arial', 15), width=20)
    acc_label.place(x=400,y=200)
    acc_entry=Entry(main, width=30,font=('arial', 15))
    acc_entry.place(x=700,y=200)
    bal_label = Label(main, text="Amount:", font=('arial', 15), width=20 )
    bal_label.place(x=400, y=250)
    bal_entry = Entry(main, width=30, font=('arial', 15))
    bal_entry.place(x=700, y=250)
    deposit_button=Button(main,text="WITHDRAW",font=('arial', 15), width=30,command=lambda :withdraw_db(acc_entry.get(),bal_entry.get()))
    deposit_button.place(x=700,y=300)
    exit_button = Button(main, text="EXIT", command=lambda :main_page(user_id,), font = ('arial', 15), width = 30)
    exit_button.place(x=700, y=350)
def withdraw_db(account_id,bal):
    try:
        amount=int(bal)
        if (amount>=0):
            cursor.execute("SELECT balance FROM accounts WHERE account_id=%s", (account_id,))
            b = cursor.fetchone()[0]
            if b>=amount:
                cursor.execute("UPDATE accounts SET balance=balance-%s WHERE account_id=%s",(amount,account_id,))
                db.commit()
                cursor.execute("INSERT INTO transactions (account_id,type,amount) VALUES (%s,%s,%s)",
                               (account_id, 'withdraw', amount))
                db.commit()
                label = Label(main, text=f"the amount of {amount} has been withdrawn successfully!",font=('arial', 15))
                label.place(x=600, y=400)
                cursor.execute("SELECT balance FROM accounts WHERE account_id=%s",(account_id,))
                balance=cursor.fetchone()[0]
                label2 = Label(main, text=f"Total Balance after withdraw={balance}",font=('arial', 15))
                label2.place(x=600, y=450)
            else:
                label = Label(main, text="Insufficient Funds!", font=('arial', 15), fg="red")
                label.place(x=600, y=400)
        else:
            label = Label(main, text="enter valid amount!",font=('arial', 15),fg="red")
            label.place(x=600, y=400)
    except Exception as e:
        label = Label(main, text=f"enter valid account_id! {e}", font=('arial', 15), fg="red")
        label.place(x=600, y=400)

def transfer(user_id):
    for widget in main.winfo_children():
        widget.destroy()
    logo_path = "C:\\Users\\gopin\\Downloads\\transfer.jpg"
    image(logo_path)
    from_acc_label = Label(main, text="From Account Number:", font=('arial', 15), width=20)
    from_acc_label.place(x=400, y=200)
    from_acc_entry = Entry(main, width=30, font=('arial', 15))
    from_acc_entry.place(x=700, y=200)
    to_acc_label = Label(main, text="To Account Number:", font=('arial', 15), width=20)
    to_acc_label.place(x=400, y=250)
    to_acc_entry = Entry(main, width=30, font=('arial', 15))
    to_acc_entry.place(x=700, y=250)
    bal_label = Label(main, text="Amount:", font=('arial', 15), width=20)
    bal_label.place(x=400, y=300)
    bal_entry = Entry(main, width=30, font=('arial', 15))
    bal_entry.place(x=700, y=300)
    deposit_button = Button(main, text="TRANSFER", font=('arial', 15), width=30,
                            command=lambda: transfer_db(from_acc_entry.get(),to_acc_entry.get(), bal_entry.get()))
    deposit_button.place(x=700, y=350)
    exit_button = Button(main, text="EXIT", command=lambda :main_page(user_id,), font=('arial', 15), width=30)
    exit_button.place(x=700, y=400)

def transfer_db(from_acc,to_acc,bal):
    try:
        amount = int(bal)
        if (amount >= 0):
            cursor.execute("SELECT balance FROM accounts WHERE account_id=%s",(from_acc,))
            b = cursor.fetchone()[0]
            if b >= amount:
                cursor.execute("UPDATE accounts SET balance=balance-%s WHERE account_id=%s", (amount, from_acc,))
                db.commit()
                cursor.execute("INSERT INTO transactions (account_id,type,amount) VALUES (%s,%s,%s)",
                               (from_acc, 'transfer', -amount))
                cursor.execute("UPDATE accounts SET balance=balance+%s WHERE account_id=%s", (amount, to_acc,))
                db.commit()
                cursor.execute("INSERT INTO transactions (account_id,type,amount) VALUES (%s,%s,%s)",
                               (to_acc, 'transfer', +amount))
                db.commit()
                label = Label(main, text=f"the amount of {amount} has been transfered successfully! from account:{from_acc} to account:{to_acc}", font=('arial', 15))
                label.place(x=600, y=450)
                cursor.execute("SELECT balance FROM accounts WHERE account_id=%s", (from_acc,))
                balance = cursor.fetchone()[0]
                label2 = Label(main, text=f"Total Balance after transfer={balance}", font=('arial', 15))
                label2.place(x=600, y=500)

            else:
                label = Label(main, text="Insufficient Funds!", font=('arial', 15), fg="red")
                label.place(x=600, y=450)
        else:
            label = Label(main, text="enter valid amount!", font=('arial', 15), fg="red")
            label.place(x=600, y=450)
    except Exception as e:
        label = Label(main, text=f"enter valid account_id! {e}", font=('arial', 15), fg="red")
        label.place(x=600, y=450)

def transaction_history(user_id):
    for widget in main.winfo_children():
        widget.destroy()
    logo_path = "C:\\Users\\gopin\\Downloads\\transactions.jpg"
    image(logo_path)
    label=Label(main,text="Account_ID:", font=('arial', 15),width=20)
    label.place(x=400,y=100)
    acc_entry=Entry(main, font=('arial', 15),width=30)
    acc_entry.place(x=700,y=100)
    btn=Button(main,text="SHOW HISTORY",command=lambda :transaction_history_db(acc_entry.get(),user_id,),width=30, font=('arial', 15))
    btn.place(x=600,y=150)
    exit_button = Button(main, text="EXIT", command=lambda: main_page(user_id, ), font=('arial', 15), width=30)
    exit_button.place(x=600, y=200)
def transaction_history_db(account_id,user_id):
    try:
        cursor.execute("SELECT account_id FROM accounts WHERE account_id=%s", (account_id,))
        result = cursor.fetchone()

        if result is None:
            label = Label(main, text="Account does not exist:", font=('arial', 15), width=30, fg="red")
            label.place(x=700, y=250)
        else:
            heading = Label(main, text="TRANSACTION HISTORY", font=('Comfort', 25), fg="red")
            heading.place(x=450, y=250)

            # Create Treeview to display transaction history
            tree = ttk.Treeview(main, columns=("Transaction ID","account_id", "Date", "Type", "Amount"), show="headings")
            tree.heading("Transaction ID", text="Transaction ID")
            tree.heading("account_id",text="account_id")
            tree.heading("Date", text="Date")
            tree.heading("Type", text="Type")
            tree.heading("Amount", text="Amount")

            # Fetch transaction history from the database
            cursor.execute("SELECT transaction_id,account_id, time_date, type, amount FROM transactions WHERE account_id = %s",
                           (account_id,))
            transactions = cursor.fetchall()

            for transaction in transactions:
                tree.insert("", "end", values=transaction)
            tree.pack(padx=20, pady=100)
            # Back button
            back_button = Button(main, text="BACK", font=('arial', 15), width=20, command=lambda :transaction_history(user_id,))
            back_button.pack(pady=20)
    except Exception as e:
        print(e)

def delete_account(user_id):
    for widget in main.winfo_children():
        widget.destroy()
    label=Label(main,text="Account_ID:",font=('arial', 15), width=20)
    label.place(x=450,y=300)
    acc_entry=Entry(main,font=('arial', 15), width=30)
    acc_entry.place(x=700,y=300)
    btn=Button(main,text="Delete Account",font=('arial', 15), width=30,command=lambda :delete_account_db(acc_entry.get()))
    btn.place(x=700,y=350)
    exit_button = Button(main, text="EXIT", command=lambda: main_page(user_id, ), font=('arial', 15), width=30)
    exit_button.place(x=700, y=400)

def delete_account_db(account_id):
    try:
        print(f"Trying to delete account with ID: {account_id}")
        cursor.execute("SELECT account_id FROM accounts WHERE account_id=%s", (account_id,))
        result = cursor.fetchone()
        if result is None:
            label = Label(main, text="Account does not exist:", font=('arial', 15), width=30, fg="red")
            label.place(x=700, y=450)
        else:
            # Delete related transactions first
            cursor.execute("DELETE FROM transactions WHERE account_id=%s", (account_id,))
            db.commit()

            # Delete the account
            cursor.execute("DELETE FROM accounts WHERE account_id=%s", (account_id,))
            db.commit()

            label = Label(main, text="Account Deleted Successfully!", font=('arial', 15), width=30)
            label.place(x=700, y=450)
            print("Account deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        label = Label(main, text="An error occurred:", font=('arial', 15), width=30, fg="red")
        label.place(x=700, y=450)

def delete_user(user_id):
    for widget in main.winfo_children():
        widget.destroy()
    label=Label(main,text="user_ID",font=('arial', 15), width=20)
    label.place(x=450,y=300)
    acc_entry=Entry(main,font=('arial', 15), width=30)
    acc_entry.place(x=700,y=300)
    btn=Button(main,text="Delete User",font=('arial', 15), width=30,command=lambda :delete_user_db(acc_entry.get()))
    btn.place(x=700,y=350)
    exit_button = Button(main, text="EXIT", command=lambda: start_page(), font=('arial', 15), width=30)
    exit_button.place(x=700, y=400)

def delete_user_db(user_id):
    try:
        cursor.execute("SELECT user_id FROM users WHERE user_id=%s", (user_id,))
        result = cursor.fetchone()

        if result is None:
            label = Label(main, text="User does not exist:", font=('arial', 15), width=30, fg="red")
            label.place(x=700, y=450)
        else:
            cursor.execute("SELECT account_id FROM accounts WHERE user_id=%s", (user_id,))
            res = cursor.fetchall()
            if res:
                for acc in res:
                    delete_account_db(acc[0])

            cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
            db.commit()

            label = Label(main, text="User Deleted Successfully!", font=('arial', 15), width=30)
            label.place(x=700, y=450)

    except Exception as e:
        print(f"Error: {e}")
        label = Label(main, text="An error occurred:", font=('arial', 15), width=30, fg="red")
        label.place(x=700, y=450)

start_page()
main.mainloop()