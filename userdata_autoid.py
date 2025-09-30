import os

# Suppress gRPC warnings from Firebase
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""

import tkinter as tk
from tkinter import messagebox, ttk
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------- FIREBASE SETUP ----------------
cred = credentials.Certificate("serviceAccountkey.json")  # your Firebase service account key
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------- CRUD FUNCTIONS ----------------
def submit_form():
    name = entry_name.get()
    age = entry_age.get()
    subscribed = var_subscribe.get()
    hobbies = entry_hobbies.get()

    # Validation
    # Name validation: not empty, must contain letters
    if not name.strip():
        messagebox.showerror("Error", "Name cannot be empty!")
        return
    if not any(char.isalpha() for char in name):
        messagebox.showerror("Error", "Name must contain letters (not just numbers).")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number!")
        return

    # Transaction for auto-increment ID
    counter_ref = db.collection("counters").document("userCounter")

    @firestore.transactional
    def get_new_id(transaction):
        snapshot = counter_ref.get(transaction=transaction)
        if snapshot.exists:
            new_id = snapshot.to_dict()["value"] + 1
        else:
            new_id = 1
        transaction.set(counter_ref, {"value": new_id})
        return new_id

    # Run inside transaction
    transaction = db.transaction()
    new_id = get_new_id(transaction)

    # Save user under users/{id}
    db.collection("users").document(str(new_id)).set({
        "id": new_id,
        "name": name,
        "age": age,
        "subscribed": subscribed,
        "hobbies": hobbies
    })

    messagebox.showinfo("Success", f"User '{name}' saved to cloud with ID {new_id}!")
    load_users()


def load_users():
    """Load all users from Firestore into the Treeview"""
    for row in tree.get_children():
        tree.delete(row)

    docs = db.collection("users").stream()
    for doc in docs:
        data = doc.to_dict()
        tree.insert("", tk.END, values=(
            data.get("id", "N/A"),
            data.get("name", "unkown"),
            data.get("age", "N/A"),
            data.get("subscribed", "N/A"),
            data.get("hobbies", "")))


def update_user():
    user_id = entry_id.get()
    if not user_id.strip():
        messagebox.showerror("Error", "Enter User ID to update.")
        return

    doc_ref = db.collection("users").document(user_id)
    if not doc_ref.get().exists:
        messagebox.showerror("Error", f"No user found with ID {user_id}.")
        return

    doc_ref.update({
        "name": entry_name.get(),
        "age": int(entry_age.get()),
        "subscribed": var_subscribe.get(),
        "hobbies": entry_hobbies.get()
    })

    messagebox.showinfo("Success", f"User ID {user_id} updated successfully.")
    load_users()


def delete_user():
    user_id = entry_id.get()
    if not user_id.strip():
        messagebox.showerror("Error", "Enter User ID to delete.")
        return

    doc_ref = db.collection("users").document(user_id)
    if not doc_ref.get().exists:
        messagebox.showerror("Error", f"No user found with ID {user_id}.")
        return

    doc_ref.delete()
    messagebox.showinfo("Success", f"User ID {user_id} deleted successfully.")
    load_users()


# ---------------- TKINTER UI ----------------
root = tk.Tk()
root.title("User Form with Firebase Firestore")
root.geometry("750x600")

# ID (for update/delete)
tk.Label(root, text="User ID (for Update/Delete):").pack(pady=2)
entry_id = tk.Entry(root, width=40)
entry_id.pack(pady=2)

# Name
tk.Label(root, text="Name:").pack(pady=2)
entry_name = tk.Entry(root, width=40)
entry_name.pack(pady=2)

# Age
tk.Label(root, text="Age:").pack(pady=2)
entry_age = tk.Entry(root, width=40)
entry_age.pack(pady=2)

# Subscribe Checkbox
var_subscribe = tk.BooleanVar()
chk_subscribe = tk.Checkbutton(root, text="Subscribe to newsletter", variable=var_subscribe)
chk_subscribe.pack(pady=2)

# Hobbies
tk.Label(root, text="Hobbies (comma-separated):").pack(pady=2)
entry_hobbies = tk.Entry(root, width=40)
entry_hobbies.pack(pady=2)

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)
tk.Button(frame_buttons, text="Create User", command=submit_form, width=15, bg="green", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Update User", command=update_user, width=15, bg="orange", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete User", command=delete_user, width=15, bg="red", fg="white").grid(row=0, column=2, padx=5)

# Treeview Table
columns = ("ID", "Name", "Age", "Subscribed", "Hobbies")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(pady=20, fill="x")

# Load data initially
load_users()

root.mainloop()
