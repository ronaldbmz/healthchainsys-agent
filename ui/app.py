import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox
from core.validator import validate_file  # we’ll define this shortly

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        status_label.config(text=f"Selected file:\n{file_path}")
        run_button.config(state=tk.NORMAL)
        run_button.file_path = file_path

def run_validation():
    file_path = run_button.file_path
    result = validate_file(file_path)
    messagebox.showinfo("Validation Complete", result)
    status_label.config(text="✅ Validation complete.")

# UI Setup
window = tk.Tk()
window.title("HealthChainBot Validator")
window.geometry("400x200")

browse_button = tk.Button(window, text="📂 Choose CSV File", command=browse_file)
browse_button.pack(pady=10)

run_button = tk.Button(window, text="🤖 Run Validation", state=tk.DISABLED, command=run_validation)
run_button.pack(pady=10)

status_label = tk.Label(window, text="Please select a CSV file to validate.")
status_label.pack(pady=20)

window.mainloop()
