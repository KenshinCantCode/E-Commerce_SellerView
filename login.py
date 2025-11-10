import tkinter as tk
from tkinter import messagebox
import json, os, subprocess
import sys

USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f, indent=4)

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Login")
        self.root.geometry("400x500")
        self.root.config(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.mode = "login" 

        self.build_ui()

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = "🛍️ Register Account" if self.mode == "register" else "🛒 Seller Login"
        tk.Label(self.root, text=title, font=("Poppins", 22, "bold"), fg="#273c75", bg="#f5f6fa").pack(pady=(40, 10))
        tk.Label(self.root, text="E-Commerce Seller Portal", font=("Poppins", 11), fg="#718093", bg="#f5f6fa").pack(pady=(0, 20))

        tk.Label(self.root, text="Username", font=("Poppins", 11, "bold"), bg="#f5f6fa", fg="#2f3640").pack(anchor="w", padx=60)
        username_entry = tk.Entry(self.root, textvariable=self.username_var, font=("Poppins", 11), bd=1, relief="solid")
        username_entry.pack(padx=60, fill="x", pady=5, ipady=5)
        
        tk.Label(self.root, text="Password", font=("Poppins", 11, "bold"), bg="#f5f6fa", fg="#2f3640").pack(anchor="w", padx=60)
        password_entry = tk.Entry(self.root, textvariable=self.password_var, show="•", font=("Poppins", 11), bd=1, relief="solid")
        password_entry.pack(padx=60, fill="x", pady=5, ipady=5)

        
        username_entry.bind("<Return>", lambda e: self.handle_enter_key())
        password_entry.bind("<Return>", lambda e: self.handle_enter_key())

        
        if self.mode == "login":
            login_btn = tk.Button(self.root, text="Login", bg="#44bd32", fg="white", font=("Poppins", 12, "bold"),
                      relief="flat", bd=0, command=self.login)
            login_btn.pack(pady=(25, 5), ipadx=10, ipady=5)
            
            tk.Button(self.root, text="Create an account", bg="#00a8ff", fg="white",
                      font=("Poppins", 11, "bold"), relief="flat", bd=0, command=self.switch_to_register).pack(pady=(10, 5), ipadx=10, ipady=5)
        else:
            register_btn = tk.Button(self.root, text="Register", bg="#9c88ff", fg="white", font=("Poppins", 12, "bold"),
                      relief="flat", bd=0, command=self.register)
            register_btn.pack(pady=(25, 5), ipadx=10, ipady=5)
            
            tk.Button(self.root, text="Back to Login", bg="#e84118", fg="white",
                      font=("Poppins", 11, "bold"), relief="flat", bd=0, command=self.switch_to_login).pack(pady=(10, 5), ipadx=10, ipady=5)

        tk.Label(self.root, text="© 2025 PHARK Project", font=("Poppins", 9), fg="#718093", bg="#f5f6fa").pack(side="bottom", pady=10)

    def handle_enter_key(self):
        """Handle Enter key press for login or register"""
        if self.mode == "login":
            self.login()
        else:
            self.register()

    def switch_to_register(self):
        self.mode = "register"
        self.username_var.set("")
        self.password_var.set("")
        self.build_ui()

    def switch_to_login(self):
        self.mode = "login"
        self.username_var.set("")
        self.password_var.set("")
        self.build_ui()

    def register(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        with open(USER_FILE, "r") as f:
            users = json.load(f)

        if username in users:
            messagebox.showerror("Error", "Username already exists!")
            return

        users[username] = password
        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)

        messagebox.showinfo("Success", "Account created successfully!")
        self.switch_to_login()

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        with open(USER_FILE, "r") as f:
            users = json.load(f)

        if username in users and users[username] == password:
            messagebox.showinfo("Welcome", f"Welcome back, {username}!")
            
            with open("current_user.txt", "w") as f:
                f.write(username)
            
            
            self.root.destroy()
            
           
            python = sys.executable
            subprocess.Popen([python, "dashboard.py"])
            
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()