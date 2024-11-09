import tkinter as tk
from tkinter import messagebox
import secrets
import string
import hashlib
import sqlite3

# Function to generate a secure password
def generate_password(length=32):
    charset = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(charset) for _ in range(length))
    return password

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to save the password into the database
def save_password(topic, password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords (topic TEXT, password TEXT)''')
    c.execute('''INSERT INTO passwords (topic, password) VALUES (?, ?)''', (topic, password))
    conn.commit()
    conn.close()

# Function to retrieve the password based on the topic
def recover_password(topic):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''SELECT password FROM passwords WHERE topic=?''', (topic,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

# Function to handle password generation
def on_generate():
    topic = entry_topic.get()
    if topic:
        password = generate_password()
        save_password(topic, password)
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)
        messagebox.showinfo("Success", "Password generated and saved successfully!")
    else:
        messagebox.showwarning("Warning", "Please enter a topic!")

# Function to handle password recovery
def on_recover():
    topic = entry_topic.get()
    password = recover_password(topic)
    if password:
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)
        messagebox.showinfo("Recovered", "Password recovered successfully!")
    else:
        messagebox.showinfo("Not Found", "No password found for the given topic.")

# Function to copy the password to clipboard
def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(entry_password.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Function to handle window closing
def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Setting up the UI
root = tk.Tk()
root.title("Advanced Secure Password Generator")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg='#1c1c1c')

# Adding icons to buttons
try:
    generate_icon = tk.PhotoImage(file='path/to/generate_icon.png')  # Replace with the actual path to your icon file
    recover_icon = tk.PhotoImage(file='path/to/recover_icon.png')    # Replace with the actual path to your icon file
    copy_icon = tk.PhotoImage(file='path/to/copy_icon.png')          # Replace with the actual path to your icon file
except tk.TclError:
    generate_icon = None
    recover_icon = None
    copy_icon = None

# UI Elements
label_title = tk.Label(root, text="Advanced Secure Password Generator", font=("Helvetica", 22, 'bold'), fg='#f2a365', bg='#1c1c1c')
label_title.pack(pady=20)

frame_topic = tk.Frame(root, bg='#1c1c1c')
frame_topic.pack(pady=10)

label_topic = tk.Label(frame_topic, text="Topic:", font=("Helvetica", 14), fg='#ffffff', bg='#1c1c1c')
label_topic.pack(side=tk.LEFT, padx=5)

entry_topic = tk.Entry(frame_topic, width=30, font=("Helvetica", 14), bg='#333333', fg='#ffffff')
entry_topic.pack(side=tk.LEFT, padx=5)

frame_password = tk.Frame(root, bg='#1c1c1c')
frame_password.pack(pady=10)

label_password = tk.Label(frame_password, text="Password:", font=("Helvetica", 14), fg='#ffffff', bg='#1c1c1c')
label_password.pack(side=tk.LEFT, padx=5)

entry_password = tk.Entry(frame_password, width=30, font=("Helvetica", 14), bg='#333333', fg='#ffffff')
entry_password.pack(side=tk.LEFT, padx=5)

button_generate = tk.Button(root, text="Generate Password", image=generate_icon, compound=tk.LEFT if generate_icon else tk.NONE, font=("Helvetica", 14), bg='#006400', fg='#ffffff', command=on_generate)
button_generate.pack(pady=10)

button_recover = tk.Button(root, text="Recover Password", image=recover_icon, compound=tk.LEFT if recover_icon else tk.NONE, font=("Helvetica", 14), bg='#1e90ff', fg='#ffffff', command=on_recover)
button_recover.pack(pady=10)

button_copy = tk.Button(root, text="Copy to Clipboard", image=copy_icon, compound=tk.LEFT if copy_icon else tk.NONE, font=("Helvetica", 14), bg='#ffa500', fg='#ffffff', command=copy_to_clipboard)
button_copy.pack(pady=10)

# Developer Credit
label_credit = tk.Label(root, text="Developed by: Md Shifat Miah", font=("Helvetica", 10), fg='#888888', bg='#1c1c1c')
label_credit.pack(side=tk.BOTTOM, pady=10)

# Handling window close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the application
root.mainloop()
