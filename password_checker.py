import hashlib
import requests
import string
import tkinter as tk
from tkinter import messagebox

def password_strength(password):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = sum([has_lower, has_upper, has_digit, has_symbol])
    if length >= 12:
        score += 1
    return score

def strength_label(score):
    labels = {
        1: "Very Weak",
        2: "Weak",
        3: "Moderate",
        4: "Strong",
        5: "Very Strong"
    }
    return labels.get(score, "Very Weak")

def check_password_breach(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "Error contacting the breach database."
        hashes = response.text.splitlines()
        for line in hashes:
            h, count = line.split(":")
            if h == suffix:
                return f"⚠️ Found in {count} breaches!"
        return "✅ Not found in known breaches."
    except:
        return "⚠️ Error: No internet or API unavailable."

def check_password():
    password = entry.get()
    if not password:
        messagebox.showwarning("Warning", "Please enter a password.")
        return

    score = password_strength(password)
    label = strength_label(score)
    breach_result = check_password_breach(password)

    result_text = f"Strength: {label} ({score}/5)\n\nBreach Check:\n{breach_result}"
    result_label.config(text=result_text)

def toggle_password():
    if entry.cget('show') == '*':
        entry.config(show='')
        toggle_btn.config(text="Hide")
    else:
        entry.config(show='*')
        toggle_btn.config(text="Show")

# GUI setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x280")

tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=10)

entry_frame = tk.Frame(root)
entry_frame.pack()

entry = tk.Entry(entry_frame, show="*", width=25, font=("Arial", 12))
entry.pack(side="left")

toggle_btn = tk.Button(entry_frame, text="Show", command=toggle_password, font=("Arial", 10))
toggle_btn.pack(side="left", padx=5)

tk.Button(root, text="Check Password", command=check_password, font=("Arial", 12), bg="lightblue").pack(pady=15)

result_label = tk.Label(root, text="", font=("Arial", 11), wraplength=350, justify="left")
result_label.pack(pady=10)

root.mainloop()
