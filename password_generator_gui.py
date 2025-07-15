import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random
import string

# Helper function to generate a single password with security rules
def generate_password(length, use_letters, use_numbers, use_symbols, exclude_chars):
    char_types = []
    if use_letters:
        char_types.append(string.ascii_letters)
    if use_numbers:
        char_types.append(string.digits)
    if use_symbols:
        char_types.append(string.punctuation)
    if not char_types:
        raise ValueError("At least one character type must be selected.")
    
    # Build the full character set, minus excluded characters
    char_set = ''.join(char_types)
    char_set = ''.join([c for c in char_set if c not in exclude_chars])
    if not char_set:
        raise ValueError("Character set is empty after exclusions.")

    # Ensure at least one from each selected type
    password = [random.choice([c for c in t if c not in exclude_chars]) for t in char_types]
    if length < len(password):
        raise ValueError(f"Length must be at least {len(password)} to include all selected types.")
    password += [random.choice(char_set) for _ in range(length - len(password))]
    random.shuffle(password)
    return ''.join(password)

# GUI Application
class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        root.title("Advanced Password Generator")
        self.set_theme()
        self.center_window(500, 440)

        # Outer frame for centering the box
        outer_frame = tk.Frame(root, bg=self.bg_color)
        outer_frame.pack(expand=True, fill='both')

        # Box frame (simulated rounded corners with padding and color)
        box_frame = tk.Frame(outer_frame, bg=self.box_bg, bd=2, relief='ridge', highlightthickness=2, highlightbackground=self.select_color)
        box_frame.place(relx=0.5, rely=0.5, anchor='center', width=380, height=390)

        # Password length
        tk.Label(box_frame, text="Password Length:", bg=self.box_bg, fg=self.fg_color).grid(row=0, column=0, sticky='e', pady=8, padx=8)
        self.length_var = tk.IntVar(value=12)
        tk.Entry(box_frame, textvariable=self.length_var, width=5, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color).grid(row=0, column=1, sticky='w', pady=8, padx=8)

        # Number of suggestions
        tk.Label(box_frame, text="Number of Suggestions:", bg=self.box_bg, fg=self.fg_color).grid(row=1, column=0, sticky='e', pady=8, padx=8)
        self.suggestions_var = tk.IntVar(value=5)
        tk.Entry(box_frame, textvariable=self.suggestions_var, width=5, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color).grid(row=1, column=1, sticky='w', pady=8, padx=8)

        # Character types
        self.letters_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        tk.Checkbutton(box_frame, text="Letters", variable=self.letters_var, bg=self.box_bg, fg=self.fg_color, selectcolor=self.select_color, activebackground=self.box_bg).grid(row=2, column=0, sticky='w', pady=8, padx=8)
        tk.Checkbutton(box_frame, text="Numbers", variable=self.numbers_var, bg=self.box_bg, fg=self.fg_color, selectcolor=self.select_color, activebackground=self.box_bg).grid(row=2, column=1, sticky='w', pady=8, padx=8)
        tk.Checkbutton(box_frame, text="Symbols", variable=self.symbols_var, bg=self.box_bg, fg=self.fg_color, selectcolor=self.select_color, activebackground=self.box_bg).grid(row=2, column=2, sticky='w', pady=8, padx=8)

        # Exclude characters
        tk.Label(box_frame, text="Exclude Characters:", bg=self.box_bg, fg=self.fg_color).grid(row=3, column=0, sticky='e', pady=8, padx=8)
        self.exclude_var = tk.StringVar()
        tk.Entry(box_frame, textvariable=self.exclude_var, width=15, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color).grid(row=3, column=1, columnspan=2, sticky='w', pady=8, padx=8)

        # Highlighted Generate button
        self.bold_font = ("Segoe UI", 11, "bold")
        self.big_bold_font = ("Segoe UI", 12, "bold")
        tk.Button(box_frame, text="Generate Passwords", command=self.generate_passwords, bg=self.button_highlight_bg, fg=self.button_fg, activebackground=self.button_active_bg, font=self.big_bold_font, relief='raised', bd=3).grid(row=4, column=0, columnspan=3, pady=12, padx=8, sticky='ew')

        # Password suggestions listbox
        self.suggestions_listbox = tk.Listbox(box_frame, width=40, height=6, bg=self.listbox_bg, fg=self.fg_color, selectbackground=self.select_color, selectforeground=self.bg_color, font=self.bold_font)
        self.suggestions_listbox.grid(row=5, column=0, columnspan=3, pady=8, padx=8, sticky='ew')

        # Highlighted Copy button
        tk.Button(box_frame, text="Copy Selected", command=self.copy_selected, bg=self.button_highlight_bg, fg=self.button_fg, activebackground=self.button_active_bg, font=self.big_bold_font, relief='raised', bd=3).grid(row=6, column=0, columnspan=3, pady=10, padx=8, sticky='ew')

        # Configure grid to center widgets
        for i in range(7):
            box_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            box_frame.grid_columnconfigure(j, weight=1)

    def set_theme(self):
        # Simple dark theme with highlight
        self.bg_color = '#23272e'
        self.box_bg = '#282a36'
        self.fg_color = '#f8f8f2'
        self.button_bg = '#44475a'
        self.button_fg = '#f8f8f2'
        self.button_active_bg = '#6272a4'
        self.button_highlight_bg = '#bd93f9'
        self.entry_bg = '#282a36'
        self.listbox_bg = '#23272e'
        self.select_color = '#bd93f9'
        self.root.configure(bg=self.bg_color)

    def center_window(self, width, height):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def generate_passwords(self):
        self.suggestions_listbox.delete(0, tk.END)
        length = self.length_var.get()
        num_suggestions = self.suggestions_var.get()
        use_letters = self.letters_var.get()
        use_numbers = self.numbers_var.get()
        use_symbols = self.symbols_var.get()
        exclude_chars = self.exclude_var.get()
        if not (use_letters or use_numbers or use_symbols):
            messagebox.showerror("Error", "Select at least one character type.")
            return
        try:
            passwords = set()
            while len(passwords) < num_suggestions:
                pw = generate_password(length, use_letters, use_numbers, use_symbols, exclude_chars)
                passwords.add(pw)
            for pw in passwords:
                self.suggestions_listbox.insert(tk.END, pw)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_selected(self):
        selected = self.suggestions_listbox.curselection()
        if not selected:
            messagebox.showinfo("Copy Password", "Please select a password to copy.")
            return
        password = self.suggestions_listbox.get(selected[0])
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copy Password", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop() 