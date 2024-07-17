import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

# Constants
DB_FILE = "users.db"

# Function to initialize the database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new user to the database
def add_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Function to verify user credentials
def verify_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    return result[0] == password

# Function to check if a user already exists
def user_exists(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to switch to login page
def show_login():
    registration_frame.pack_forget()
    login_frame.pack()

# Function to switch to registration page
def show_registration():
    login_frame.pack_forget()
    registration_frame.pack()

# Function to handle login
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    
    if verify_user(username, password):
        messagebox.showinfo("Login", "Login successful!")
        root.destroy()  # Close the login window
        subprocess.run(["python", "main.py"])  # Run the main.py script
    else:
        messagebox.showerror("Login", "Invalid username or password")

# Function to handle registration
def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_password_entry.get()
    
    if user_exists(username):
        messagebox.showerror("Registration", "Username already exists")
    elif password != confirm_password:
        messagebox.showerror("Registration", "Passwords do not match")
    else:
        add_user(username, password)
        messagebox.showinfo("Registration", "Registration successful!")
        show_login()

# Initialize database
init_db()

# Main window
root = tk.Tk()
root.title("Login and Registration System")
root.geometry("400x300")  # Increased size of the main window

# Login frame
login_frame = tk.Frame(root, width=400, height=300)  # Set frame size
login_frame.pack_propagate(False)  # Prevent frame from resizing to fit widgets
tk.Label(login_frame, text="Username").pack(pady=5)
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack(pady=5)
tk.Label(login_frame, text="Password").pack(pady=5)
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack(pady=5)
tk.Button(login_frame, text="Login", command=login).pack(pady=5)
tk.Button(login_frame, text="Register", command=show_registration).pack(pady=5)

# Registration frame
registration_frame = tk.Frame(root, width=400, height=300)  # Set frame size
registration_frame.pack_propagate(False)  # Prevent frame from resizing to fit widgets
tk.Label(registration_frame, text="Username").pack(pady=5)
reg_username_entry = tk.Entry(registration_frame)
reg_username_entry.pack(pady=5)
tk.Label(registration_frame, text="Password").pack(pady=5)
reg_password_entry = tk.Entry(registration_frame, show="*")
reg_password_entry.pack(pady=5)
tk.Label(registration_frame, text="Confirm Password").pack(pady=5)
reg_confirm_password_entry = tk.Entry(registration_frame, show="*")
reg_confirm_password_entry.pack(pady=5)
tk.Button(registration_frame, text="Register", command=register).pack(pady=5)
tk.Button(registration_frame, text="Back to Login", command=show_login).pack(pady=5)

# Start with the login page
login_frame.pack()

root.mainloop()
