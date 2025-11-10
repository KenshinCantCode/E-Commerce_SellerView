import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, ttk
from PIL import Image, ImageTk
import sqlite3
import os

BG_COLOR = "#f5f6fa"
CARD_BG = "#ffffff"
ACCENT = "#00a8ff"
SUCCESS = "#4cd137"
DANGER = "#e84118"
TEXT_COLOR = "#2f3640"

class SellerDashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        
        self.root.title(f"Seller Dashboard - {self.username}")
        self.root.geometry("1100x650")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)

        
        self.conn = sqlite3.connect("products.db")
        self.c = self.conn.cursor()
        
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT,
                            name TEXT,
                            price REAL,
                            qty INTEGER,
                            category TEXT,
                            image_path TEXT)''')
        self.conn.commit()

        
        self.name_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.cat_var = tk.StringVar()
        self.image_path = None
        
        
        self.categories = ["Electronics", "Clothing", "Books", "Home & Garden", 
                          "Sports", "Beauty", "Toys", "Food", "Other"]

        self.product_cards = []
        self.product_images = []

        self.create_ui()
        self.load_products()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            
            try:
                self.conn.close()
            except Exception:
                pass
            
            self.root.destroy()
            
            import login
            root = tk.Tk()
            app = login.LoginApp(root)
            root.mainloop()

    def create_ui(self):
        
        header_frame = tk.Frame(self.root, bg=ACCENT)
        header_frame.pack(fill=tk.X, padx=0, pady=0)

        
        header = tk.Label(header_frame, text=f"🛒 Seller Dashboard - {self.username}",
                          font=("Poppins", 22, "bold"), bg=ACCENT, fg="white", pady=15)
        header.pack(side="left", padx=20)

        
        logout_btn = tk.Button(header_frame, text="Logout", bg=DANGER, fg="white",
                             font=("Poppins", 11, "bold"), bd=0, relief="flat",
                             command=self.logout)
        logout_btn.pack(side="right", padx=20, pady=15)

       
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        
        left_frame = tk.Frame(main_frame, bg=CARD_BG, width=350, height=500, bd=1, relief="solid")
        left_frame.pack(side="left", fill="y", padx=(0, 20))
        left_frame.pack_propagate(False)

        
        right_frame = tk.Frame(main_frame, bg=BG_COLOR)
        right_frame.pack(side="right", fill="both", expand=True)

        
        self.build_form(left_frame)
        
        
        self.build_products_area(right_frame)

    def build_form(self, parent):
        tk.Label(parent, text="Add Product", font=("Poppins", 16, "bold"),
                 bg=CARD_BG, fg=TEXT_COLOR).pack(pady=(20, 15))

        
        tk.Label(parent, text="Product Name", font=("Poppins", 11, "bold"),
                 bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=(5, 0))
        tk.Entry(parent, textvariable=self.name_var, font=("Poppins", 11), 
                bd=1, relief="solid").pack(padx=20, fill="x", pady=5, ipady=3)

        
        tk.Label(parent, text="Price (₱)", font=("Poppins", 11, "bold"),
                 bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=(5, 0))
        tk.Entry(parent, textvariable=self.price_var, font=("Poppins", 11), 
                bd=1, relief="solid").pack(padx=20, fill="x", pady=5, ipady=3)

       
        tk.Label(parent, text="Quantity", font=("Poppins", 11, "bold"),
                 bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=(5, 0))
        tk.Entry(parent, textvariable=self.qty_var, font=("Poppins", 11), 
                bd=1, relief="solid").pack(padx=20, fill="x", pady=5, ipady=3)

        
        tk.Label(parent, text="Category", font=("Poppins", 11, "bold"),
                 bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=(5, 0))
        
        self.cat_combobox = ttk.Combobox(parent, textvariable=self.cat_var, 
                                       values=self.categories, state="readonly",
                                       font=("Poppins", 11))
        self.cat_combobox.pack(padx=20, fill="x", pady=5, ipady=3)
        self.cat_combobox.set("Select Category")

        
        select_img_btn = tk.Button(parent, text="Select Image", bg="#9c88ff", fg="white",
                                  font=("Poppins", 10, "bold"), bd=0, relief="flat",
                                  command=self.select_image)
        select_img_btn.pack(pady=15, ipadx=10, ipady=5)

        
        add_product_btn = tk.Button(parent, text="Add Product", bg=SUCCESS, fg="white",
                                   font=("Poppins", 12, "bold"), bd=0, relief="flat",
                                   command=self.add_product)
        add_product_btn.pack(pady=10, ipadx=10, ipady=5)

    def build_products_area(self, parent):
        tk.Label(parent, text="Your Products", font=("Poppins", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 15))

        
        self.canvas = tk.Canvas(parent, bg=BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Selected", "Product image selected successfully!")

    def add_product(self):
        name = self.name_var.get().strip()
        price = self.price_var.get().strip()
        qty = self.qty_var.get().strip()
        cat = self.cat_var.get().strip()

        if not name or not price or not qty or not cat or cat == "Select Category":
            messagebox.showwarning("Missing Info", "Please fill out all fields and select a category.")
            return

        try:
            self.c.execute("INSERT INTO products (user_id, name, price, qty, category, image_path) VALUES (?, ?, ?, ?, ?, ?)",
                           (self.username, name, float(price), int(qty), cat, self.image_path))
            self.conn.commit()
            self.clear_form()
            self.load_products()
            messagebox.showinfo("Success", "Product added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product:\n{e}")

    def clear_form(self):
        self.name_var.set("")
        self.price_var.set("")
        self.qty_var.set("")
        self.cat_combobox.set("Select Category")
        self.image_path = None

    def load_products(self):
        self.product_cards.clear()
        self.product_images.clear()
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.c.execute("SELECT * FROM products WHERE user_id = ?", (self.username,))
        products = self.c.fetchall()

        if not products:
            tk.Label(self.scrollable_frame, text="No products added yet.",
                     font=("Poppins", 14), bg=BG_COLOR, fg="#7f8c8d").pack(expand=True, pady=100)
            return

        row, col = 0, 0
        for product in products:
            self.create_product_card(product, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def create_product_card(self, product, row, col):
        card_frame = tk.Frame(self.scrollable_frame, bg=BG_COLOR)
        card_frame.grid(row=row, column=col, padx=15, pady=15)

        card = tk.Frame(card_frame, bg=CARD_BG, bd=1, relief="solid", width=200, height=230, cursor="hand2")
        card.pack()
        card.pack_propagate(False)

        
        card.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))
        card.bind("<Enter>", lambda e: e.widget.config(bg="#f0f0f0"))
        card.bind("<Leave>", lambda e: e.widget.config(bg=CARD_BG))

        
        img_path = product[6]
        img_frame = tk.Frame(card, bg=CARD_BG, height=120, cursor="hand2")
        img_frame.pack(fill="x", pady=5)
        img_frame.pack_propagate(False)
        img_frame.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))

        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                img = img.resize((180, 120))
                photo_img = ImageTk.PhotoImage(img)
                
                img_label = tk.Label(img_frame, image=photo_img, bg=CARD_BG, cursor="hand2")
                img_label.image = photo_img
                img_label.pack(expand=True)
                img_label.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))
                self.product_images.append(photo_img)
            except:
                no_img_label = tk.Label(img_frame, text="[Image Error]", bg=CARD_BG, fg=DANGER, cursor="hand2")
                no_img_label.pack(expand=True)
                no_img_label.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))
        else:
            no_img_label = tk.Label(img_frame, text="[No Image]", bg=CARD_BG, fg="#888", cursor="hand2")
            no_img_label.pack(expand=True)
            no_img_label.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))

        
        info_frame = tk.Frame(card, bg=CARD_BG, cursor="hand2")
        info_frame.pack(fill="x", padx=10, pady=5)
        info_frame.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))

        name_label = tk.Label(info_frame, text=product[2], font=("Poppins", 12, "bold"), 
                bg=CARD_BG, fg=TEXT_COLOR, cursor="hand2")
        name_label.pack(anchor="w")
        name_label.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))

        price_label = tk.Label(info_frame, text=f"₱{product[3]:.2f} | {product[4]} pcs", font=("Poppins", 10),
                bg=CARD_BG, fg="#636e72", cursor="hand2")
        price_label.pack(anchor="w")
        price_label.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))

        cat_label = tk.Label(info_frame, text=product[5], font=("Poppins", 9, "italic"), 
                bg=CARD_BG, fg="#718093", cursor="hand2")
        cat_label.pack(anchor="w")
        cat_label.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))

        
        button_frame = tk.Frame(card, bg=CARD_BG)
        button_frame.pack(side="bottom", fill="x", pady=5)

        
        def stop_propagation(e):
            return "break"

        edit_btn = tk.Button(button_frame, text="Edit", bg=ACCENT, fg="white", bd=0,
                 font=("Poppins", 10, "bold"), 
                 command=lambda p=product: self.edit_product_popup(p))
        edit_btn.pack(side="left", padx=10, pady=5, ipadx=8)
        edit_btn.bind("<Button-1>", stop_propagation)

        delete_btn = tk.Button(button_frame, text="Delete", bg=DANGER, fg="white", bd=0,
                 font=("Poppins", 10, "bold"), 
                 command=lambda: self.delete_product(product[0]))
        delete_btn.pack(side="right", padx=10, pady=5, ipadx=8)
        delete_btn.bind("<Button-1>", stop_propagation)

        button_frame.bind("<Button-1>", stop_propagation)

    def show_product_details(self, product):
        """Show detailed product information when product is clicked"""
        details = Toplevel(self.root)
        details.title("Product Details")
        details.geometry("550x700")
        details.config(bg="white")
        details.resizable(False, False)
        
        
        details.transient(self.root)
        details.grab_set()

        tk.Label(details, text="📦 Product Details", font=("Poppins", 20, "bold"), 
                 bg="white", fg=ACCENT).pack(pady=20)

        
        img_frame = tk.Frame(details, bg="white")
        img_frame.pack(pady=10)
        
        img_path = product[6]
        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                img = img.resize((250, 180))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(img_frame, image=img_tk, bg="white")
                img_label.image = img_tk
                img_label.pack()
            except:
                tk.Label(img_frame, text="[Image Not Available]", bg="white", fg=DANGER, 
                        font=("Poppins", 10)).pack()
        else:
            tk.Label(img_frame, text="[No Image Available]", bg="white", fg="#888", 
                    font=("Poppins", 10)).pack()

        
        info_frame = tk.Frame(details, bg="white")
        info_frame.pack(pady=20, padx=30, fill="x")

        details_data = [
            ("Product Name:", product[2]),
            ("Price:", f"₱{float(product[3]):.2f}"),
            ("Quantity:", f"{product[4]} pieces"),
            ("Category:", product[5]),
            ("Product ID:", f"#{product[0]}"),
            ("Added by:", product[1])
        ]

        for label, value in details_data:
            row_frame = tk.Frame(info_frame, bg="white")
            row_frame.pack(fill="x", pady=8)
            
            tk.Label(row_frame, text=label, font=("Poppins", 11, "bold"), 
                    bg="white", fg=TEXT_COLOR, width=15, anchor="w").pack(side=tk.LEFT)
            tk.Label(row_frame, text=value, font=("Poppins", 11), 
                    bg="white", fg="#636e72", anchor="w").pack(side=tk.LEFT, fill="x", expand=True)

        
        action_frame = tk.Frame(details, bg="white")
        action_frame.pack(pady=20)

        tk.Button(action_frame, text="✏️ Edit Product", bg=ACCENT, fg="white",
                 font=("Poppins", 11, "bold"), bd=0, relief="flat",
                 command=lambda p=product: [details.destroy(), self.edit_product_popup(p)]).pack(side="left", padx=10, ipadx=15, ipady=5)

        tk.Button(action_frame, text="❌ Delete Product", bg=DANGER, fg="white",
                 font=("Poppins", 11, "bold"), bd=0, relief="flat",
                 command=lambda: [details.destroy(), self.delete_product(product[0])]).pack(side="left", padx=10, ipadx=15, ipady=5)

        tk.Button(action_frame, text="Close", bg="#95a5a6", fg="white",
                 font=("Poppins", 11, "bold"), bd=0, relief="flat",
                 command=details.destroy).pack(side="left", padx=10, ipadx=15, ipady=5)

    def edit_product_popup(self, product):
        """Enhanced edit product popup with full functionality"""
        edit = Toplevel(self.root)
        edit.title("Edit Product")
        edit.geometry("450x750")
        edit.config(bg="white")
        edit.resizable(False, False)
        
        
        edit.transient(self.root)
        edit.grab_set()

        tk.Label(edit, text="✏️ Edit Product", font=("Poppins", 20, "bold"), 
                 bg="white", fg=ACCENT).pack(pady=20)

        
        name_var = tk.StringVar(value=product[2])
        price_var = tk.StringVar(value=str(product[3]))
        qty_var = tk.StringVar(value=str(product[4]))
        cat_var = tk.StringVar(value=product[5])
        new_image_path = [product[6]]  

        
        form_frame = tk.Frame(edit, bg="white")
        form_frame.pack(fill="x", padx=30, pady=10)

        
        tk.Label(form_frame, text="Product Name", font=("Poppins", 11, "bold"), 
                bg="white", fg=TEXT_COLOR, anchor="w").pack(fill="x", pady=(5, 0))
        name_entry = tk.Entry(form_frame, textvariable=name_var, font=("Poppins", 11), 
                             bd=1, relief="solid")
        name_entry.pack(fill="x", pady=5, ipady=3)

        
        tk.Label(form_frame, text="Price (₱)", font=("Poppins", 11, "bold"), 
                bg="white", fg=TEXT_COLOR, anchor="w").pack(fill="x", pady=(5, 0))
        price_entry = tk.Entry(form_frame, textvariable=price_var, font=("Poppins", 11), 
                              bd=1, relief="solid")
        price_entry.pack(fill="x", pady=5, ipady=3)

        
        tk.Label(form_frame, text="Quantity", font=("Poppins", 11, "bold"), 
                bg="white", fg=TEXT_COLOR, anchor="w").pack(fill="x", pady=(5, 0))
        qty_entry = tk.Entry(form_frame, textvariable=qty_var, font=("Poppins", 11), 
                            bd=1, relief="solid")
        qty_entry.pack(fill="x", pady=5, ipady=3)

        
        tk.Label(form_frame, text="Category", font=("Poppins", 11, "bold"), 
                bg="white", fg=TEXT_COLOR, anchor="w").pack(fill="x", pady=(5, 0))
        cat_combobox = ttk.Combobox(form_frame, textvariable=cat_var, 
                                   values=self.categories, state="readonly",
                                   font=("Poppins", 11))
        cat_combobox.pack(fill="x", pady=5, ipady=3)

        
        tk.Label(edit, text="Current Image", font=("Poppins", 12, "bold"), 
                bg="white", fg=TEXT_COLOR).pack(pady=(20, 10))

        img_display_frame = tk.Frame(edit, bg="white")
        img_display_frame.pack(pady=10)

        if product[6] and os.path.exists(product[6]):
            try:
                img = Image.open(product[6])
                img = img.resize((200, 150))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(img_display_frame, image=img_tk, bg="white")
                img_label.image = img_tk
                img_label.pack()
            except:
                tk.Label(img_display_frame, text="[Current Image Error]", 
                        bg="white", fg=DANGER, font=("Poppins", 10)).pack()
        else:
            tk.Label(img_display_frame, text="[No Current Image]", 
                    bg="white", fg="#888", font=("Poppins", 10)).pack()

        
        def change_image():
            file_path = filedialog.askopenfilename(
                title="Select Product Image",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")]
            )
            if file_path:
                new_image_path[0] = file_path
                messagebox.showinfo("Success", "New image selected! Click 'Save Changes' to update.")

        tk.Button(edit, text="🖼️ Change Image", bg="#9c88ff", fg="white",
                  font=("Poppins", 11, "bold"), bd=0, relief="flat",
                  command=change_image).pack(pady=10, ipadx=10, ipady=5)

    
        def save_changes():
            name = name_var.get().strip()
            price = price_var.get().strip()
            qty = qty_var.get().strip()
            cat = cat_var.get().strip()

            if not name or not price or not qty or not cat:
                messagebox.showwarning("Missing Info", "Please fill out all fields.")
                return

            try:
                
                price_val = float(price)
                qty_val = int(qty)

                if price_val < 0 or qty_val < 0:
                    messagebox.showwarning("Invalid Input", "Price and quantity must be positive numbers.")
                    return

            
                self.c.execute('''UPDATE products 
                                SET name=?, price=?, qty=?, category=?, image_path=?
                                WHERE id=? AND user_id=?''',
                            (name, price_val, qty_val, cat, new_image_path[0], product[0], self.username))
                self.conn.commit()

                
                self.load_products()
                
                
                edit.destroy()
                
                messagebox.showinfo("Success", "Product updated successfully!")
                
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for price and quantity.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update product:\n{str(e)}")

        
        button_frame = tk.Frame(edit, bg="white")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="💾 Save Changes", bg=SUCCESS, fg="white",
                  font=("Poppins", 12, "bold"), bd=0, relief="flat",
                  command=save_changes).pack(side="left", padx=10, ipadx=15, ipady=5)

        tk.Button(button_frame, text="❌ Cancel", bg=DANGER, fg="white",
                  font=("Poppins", 12, "bold"), bd=0, relief="flat",
                  command=edit.destroy).pack(side="left", padx=10, ipadx=15, ipady=5)

    def delete_product(self, product_id):
        if messagebox.askyesno("Confirm Delete", 
                              "Are you sure you want to delete this product?\nThis action cannot be undone."):
            self.c.execute("DELETE FROM products WHERE id=? AND user_id=?", (product_id, self.username))
            self.conn.commit()
            self.load_products()
            messagebox.showinfo("Deleted", "Product deleted successfully!")
    

if __name__ == "__main__":
    
    try:
        with open("current_user.txt", "r") as f:
            username = f.read().strip()
        
        if os.path.exists("current_user.txt"):
            os.remove("current_user.txt")
    except:
        username = "Unknown User"
    
    
    root = tk.Tk()
    app = SellerDashboard(root, username)
    root.mainloop()