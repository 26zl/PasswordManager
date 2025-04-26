"""
Password Manager
---------------

Owner: Laurent Zogaj
Date delivered: April 11, 2025
Updated: April 26, 2025 

Description:
This project is a password manager that allows users to store, retrieve, and manage passwords
securely on their computer. Passwords are encrypted using the cryptography library with
symmetric encryption (Fernet). The program also provides functionality to generate random
and secure passwords.

Dependencies:
- tkinter (for GUI)
- cryptography (for encryption/decryption)
- secrets (for secure password generation)
- string (for character sets)
- csv (for storing passwords in CSV format)
- datetime (for password timestamps)
- os (for file handling)
- sys (for system functions)

File structure:
These will be created when you start the application and save passwords
- passwords.csv: stored password data
- secret.key: encryption key

Important:
This is only a prototype application.
"""

# Imports
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import secrets
import string
import os
import sys
import csv
import datetime
from cryptography.fernet import Fernet

# --- Constants ---
SAVE_FILE = "passwords.csv"  # File storing the passwords
KEY_FILE = "secret.key"      # File containing the encryption key

# --- Global variables ---
saved_passwords = {}  # Empty dictionary to store passwords
key = None           # Holds the encryption key


# --- Encryption ---
# Get or create the encryption key
def get_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    new_key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(new_key)
    return new_key

# Encrypt the password
def encrypt_password(password):
    try:
        f = Fernet(key)
        if not isinstance(password, str):
            password = str(password)
        return f.encrypt(password.encode("utf-8"))
    except Exception as error:
        messagebox.showerror("Error", f"Could not encrypt password: {error}")
        return None
    
# Decrypt the password
def decrypt_password(encrypted):
    try:
        f = Fernet(key)
        if isinstance(encrypted, str):
            encrypted = encrypted.encode("utf-8")
        return f.decrypt(encrypted).decode("utf-8")
    except Exception as error:
        messagebox.showerror("Error", f"Could not decrypt password: {error}")
        return None


# --- Password Generation ---
# Generate password using secrets instead of random for better security
def generate_password():
    length = secrets.randbelow(8) + 12  # Between 12-20 characters
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# --- Storage and Retrieval ---
# Save passwords to a CSV file
def save_passwords(data):
    try:
        if not os.path.exists(KEY_FILE):
            messagebox.showerror("Error", "Key file is missing.")
            return False
        
        with open(SAVE_FILE, "w", newline='', encoding='utf-8') as f:
            fields = ["platform", "username", "encrypted_password", "date"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            for platform, info in data.items(): 
                if not isinstance(info, dict):
                    continue
                
                password_data = info.get("password", b"")
                if isinstance(password_data, bytes):
                    encrypted_password = password_data.decode("utf-8", errors="replace")
                else:
                    encrypted_password = str(password_data)
                
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(info, dict) and "date" in info:
                    date = info["date"]
                
                row = {
                    "platform": platform,
                    "username": info.get("username", ""),
                    "encrypted_password": encrypted_password,
                    "date": date
                }
                writer.writerow(row)
        return True
    except Exception as error:
        messagebox.showerror("Save Error", f"Could not save: {error}")
        return False
    
# Load passwords from the CSV file
def load_passwords():
    password_data = {}
    if not os.path.exists(SAVE_FILE):
        return password_data
    try:
        with open(SAVE_FILE, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "platform" not in row or "encrypted_password" not in row:
                    continue
                    
                encrypted = row["encrypted_password"]
                if not isinstance(encrypted, bytes):
                    try:
                        encrypted = encrypted.encode("utf-8")
                    except:
                        continue
                        
                password_data[row["platform"]] = {
                    "username": row.get("username", ""),
                    "password": encrypted,
                    "date": row.get("date", "")
                }
        return password_data
    except Exception as error:
        messagebox.showerror("Error", f"Could not read file: {error}")
        return {}

# --- GUI Functions ---
# Add password to dictionary and save to CSV file
def add_entry():
    platform = platform_entry.get().strip()
    user = username_entry.get().strip()
    password = password_entry.get().strip()

    if not all([platform, user, password]):
        messagebox.showwarning("Error", "All fields must be filled in.")
        return
    if len(password) < 8 or len(password) > 25:
        messagebox.showerror("Error", "Password must be between 8 and 25 characters long.")
        return
        
    encrypted = encrypt_password(password)
    if not encrypted:
        return
        
    saved_passwords[platform] = {
        "username": user,
        "password": encrypted,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if save_passwords(saved_passwords):
        messagebox.showinfo("Saved", "Password saved successfully.")
        clear_fields()
    else:
        messagebox.showerror("Error", "Could not save password.")

# Retrieve password from dictionary and decrypt it
def retrieve_entry():
    platform = platform_entry.get().strip()
    data = None
    
    if platform in saved_passwords:
        data = saved_passwords[platform]
    else:
        # Try case-insensitive search
        for name, info in saved_passwords.items():
            if isinstance(name, str) and isinstance(platform, str):
                if name.lower() == platform.lower():
                    platform = name
                    data = info
                    break
    
    if not data:
        messagebox.showwarning("Error", "No data found.")
        return
    
    password = decrypt_password(data["password"])
    if password:
        messagebox.showinfo("Password", f"Platform: {platform}\nUsername: {data['username']}\nPassword: {password}")
        platform_entry.delete(0, tk.END)
        platform_entry.insert(0, platform)

# Generate a random password and fill it in the password field
def generate_and_fill():
    password_entry.delete(0, tk.END)
    password_entry.insert(0, generate_password())

# Clear the input fields
def clear_fields():
    platform_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Emergency function to delete all data
def delete_all():
    if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all data?"):
        if not os.path.exists(SAVE_FILE) and not os.path.exists(KEY_FILE):
            messagebox.showerror("Error", "No data found to delete.")
            return
            
        saved_passwords.clear()
        
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        if os.path.exists(KEY_FILE):
            os.remove(KEY_FILE)
            
        messagebox.showinfo("Deleted", "All data has been removed.")
        sys.exit(0) 

# Show information about the password manager and how to use it
def show_info():
    info_window = tk.Toplevel(window)
    info_window.title("Password Manager Information")
    info_window.geometry("500x400")
    
    # Scrollbar
    text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD)
    text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Center the text 
    text.tag_configure("center", justify='center')

    # Information text
    information_text = """
    PASSWORD MANAGER - USER GUIDE
    =============================
    
    This password manager helps you store and manage your passwords securely.
    
    FEATURES:
    ---------
    
    1. STORE PASSWORDS
       Fill in platform (e.g., Facebook, Gmail), username and password,
       and click "Save" to store the information securely.
    
    2. RETRIEVE PASSWORDS
       Enter the platform name and click "Retrieve" to view username and password.
    
    3. GENERATE PASSWORDS
       Click "Generate" to create a random, strong password.
    
    4. "EMERGENCY BUTTON!!" DELETE ALL DATA
       Click "Delete All" to remove all stored passwords.
    
    SECURITY:
    ---------
    
    - All passwords are stored encrypted on your computer
    - Use a strong, unique password for each platform
    - Regularly update important passwords for increased security

    NOTE: This password manager is by no means complete and lacks important functionality.
    This is just a basic version for demonstration purposes.
    Please be careful about using this in production as it is a demo and not intended for real use.
    """
    
    # Insert the text
    text.insert(tk.END, information_text, "center")
    text.config(state=tk.DISABLED)
    
    ttk.Button(info_window, text="Close", command=info_window.destroy).pack(pady=10)

# --- Main Program / GUI ---
key = get_create_key()           # Initialize key
saved_passwords = load_passwords()  # Load existing passwords

window = tk.Tk()
window.title("Password Manager")

style = ttk.Style()
style.theme_use("clam")

# Frame
main_frame = ttk.Frame(window, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Info button on top
ttk.Button(main_frame, text="Information", command=show_info).pack(pady=(0, 10))

# Input field frame
input_frame = ttk.LabelFrame(main_frame, padding=10)
input_frame.pack(fill=tk.X)

# Fields for input
field_frame = ttk.Frame(input_frame)
field_frame.pack(fill=tk.X)

ttk.Label(field_frame, text="Platform:").grid(row=0, column=0, sticky="E", padx=5, pady=5)
platform_entry = ttk.Entry(field_frame, width=30)
platform_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(field_frame, text="Username:").grid(row=1, column=0, sticky="E", padx=5, pady=5)
username_entry = ttk.Entry(field_frame, width=30)
username_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(field_frame, text="Password:").grid(row=2, column=0, sticky="E", padx=5, pady=5)
password_entry = ttk.Entry(field_frame, width=30, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)
ttk.Button(field_frame, text="Generate", command=generate_and_fill).grid(row=2, column=2, padx=5)

# Button row
button_frame = ttk.Frame(input_frame)
button_frame.pack(fill=tk.X, pady=10)

# Various buttons
ttk.Button(button_frame, text="Retrieve", command=retrieve_entry).pack(side=tk.LEFT, expand=True, padx=5)
ttk.Button(button_frame, text="Save", command=add_entry).pack(side=tk.LEFT, expand=True, padx=5)
ttk.Button(button_frame, text="Clear", command=clear_fields).pack(side=tk.LEFT, expand=True, padx=5)

# Bottom buttons
bottom_frame = ttk.Frame(main_frame)
bottom_frame.pack(fill=tk.X, pady=10)
ttk.Button(bottom_frame, text="Delete All", command=delete_all).pack()

window.mainloop()