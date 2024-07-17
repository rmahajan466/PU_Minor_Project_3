import tkinter as tk
from tkinter import messagebox
import json
import os

# Constants
USER_DATA_FILE = "users.json"

# Function to load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save user data
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file)

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
    users = load_user_data()
    
    if username in users and users[username] == password:
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Invalid username or password")

# Function to handle registration
def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_password_entry.get()
    users = load_user_data()
    
    if username in users:
        messagebox.showerror("Registration", "Username already exists")
    elif password != confirm_password:
        messagebox.showerror("Registration", "Passwords do not match")
    else:
        users[username] = password
        save_user_data(users)
        messagebox.showinfo("Registration", "Registration successful!")
        show_login()

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
