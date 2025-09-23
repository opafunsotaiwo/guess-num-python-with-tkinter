import tkinter as tk
from tkinter import messagebox

def validate_name(new_value):
    """Allow only letters and spaces in the Name field"""
    return all(ch.isalpha() or ch.isspace() for ch in new_value)

def submit_form():
    name = entry_name.get()
    age = entry_age.get()
    subscribe = var_subscribe.get()
    hobbies = entry_hobbies.get()

    # Validate Name
    if not name.strip():
        messagebox.showerror("Invalid Input", "Name cannot be empty!")
        return

    if not all(ch.isalpha() or ch.isspace() for ch in name):
        messagebox.showerror("Invalid Input", "Name must contain only letters and spaces!")
        return

    # Validate Age
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Invalid Input", "Age must be an integer!")
        return

    details = f"""
    Name: {name}
    Age: {age}
    Subscribed: {"Yes" if subscribe else "No"}
    Hobbies: {hobbies}
    """

    messagebox.showinfo("User Details", details)


# Main Window
root = tk.Tk()
root.title("User Form")
root.geometry("400x300")

# Validation for Name
vcmd = (root.register(validate_name), "%P")

# Name
tk.Label(root, text="Name:").pack(pady=5)
entry_name = tk.Entry(root, width=40, validate="key", validatecommand=vcmd)
entry_name.pack(pady=5)

# Age
tk.Label(root, text="Age:").pack(pady=5)
entry_age = tk.Entry(root, width=40)
entry_age.pack(pady=5)

# Subscribe Checkbox
var_subscribe = tk.BooleanVar()
chk_subscribe = tk.Checkbutton(root, text="Subscribe to newsletter", variable=var_subscribe)
chk_subscribe.pack(pady=5)

# Hobbies
tk.Label(root, text="Hobbies (comma-separated):").pack(pady=5)
entry_hobbies = tk.Entry(root, width=40)
entry_hobbies.pack(pady=5)

# Submit Button
btn_submit = tk.Button(root, text="Submit", command=submit_form)
btn_submit.pack(pady=15)

root.mainloop()
