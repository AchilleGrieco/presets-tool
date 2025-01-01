import json
import tkinter as tk
from tkinter import messagebox
import pyperclip
import keyboard
import pygetwindow as gw
import os
import win32gui

TEMPLATE_FOLDER = "templates"

SEARCH_HOTKEY = "ctrl+alt+i"
ADD_ENTRY_HOTKEY = "ctrl+i"

COLORS = {
    "bg": "#2b2b2b",
    "fg": "#ffffff",
    "entry_bg": "#3b3b3b",
    "button_bg": "#404040",
    "button_active": "#4a4a4a",
    "accent": "#6272a4",
    "error": "#ff5555",
    "success": "#50fa7b"
}

def configure_styles(root):
    """Configure dark theme styles for the GUI"""
    root.configure(bg=COLORS["bg"])
    
    frame_style = {
        "bg": COLORS["bg"]
    }
    
    label_style = {
        "bg": COLORS["bg"],
        "fg": COLORS["fg"]
    }
    
    button_style = {
        "bg": COLORS["button_bg"],
        "fg": COLORS["fg"],
        "font": ("Segoe UI", 10),
        "padx": 15,
        "pady": 5,
        "bd": 0,
        "relief": tk.FLAT,
        "activebackground": COLORS["button_active"],
        "activeforeground": COLORS["fg"]
    }
    
    entry_style = {
        "bg": COLORS["entry_bg"],
        "fg": COLORS["fg"],
        "font": ("Consolas", 10),
        "bd": 0,
        "relief": tk.FLAT,
        "insertbackground": COLORS["fg"]
    }
    
    return frame_style, label_style, button_style, entry_style

if not os.path.exists(TEMPLATE_FOLDER):
    os.makedirs(TEMPLATE_FOLDER)

def normalize_title(title):
    return title.lower().strip()

def load_templates(window_title):
    normalized_title = normalize_title(window_title)

    for file in os.listdir(TEMPLATE_FOLDER):
        if file.endswith(".json"):
            try:
                with open(os.path.join(TEMPLATE_FOLDER, file), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "template_names" in data:
                        template_names = [name.lower().strip() for name in data["template_names"]]
                        templates = data["templates"]
                    else:
                        template_names = [file[:-5].lower()]
                        templates = data

                    if any(name in normalized_title for name in template_names):
                        return templates, template_names
            except json.JSONDecodeError:
                print(f"Error loading the file {file}")
                continue
    
    print("No related dictionary found")
    return {}, []

def on_hotkey():
    active_window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(active_window).lower()
    
    template_names = []
    template_dict = None
    
    for template_file in os.listdir(TEMPLATE_FOLDER):
        if template_file.endswith('.json'):
            with open(os.path.join(TEMPLATE_FOLDER, template_file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                if any(name.lower() in window_title for name in data.get("template_names", [])):
                    template_names = data.get("template_names", [])
                    template_dict = data.get("templates", {})
                    break
    
    if not template_dict:
        messagebox.showerror("Error", "No template find for this window")
        return
    
    root = tk.Tk()
    root.title("Add template")
    
    root.attributes("-topmost", True)

    frame_style, label_style, button_style, entry_style = configure_styles(root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - 350) // 2
    y_position = (screen_height - 250) // 2
    root.geometry(f"350x250+{x_position}+{y_position}")

    main_frame = tk.Frame(root, **frame_style)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    template_names_str = ", ".join(template_names)
    template_label = tk.Label(main_frame, text=f"Active template for: {template_names_str}", 
                            **label_style, font=("Segoe UI", 10, "bold"))
    template_label.pack(pady=5)

    label = tk.Label(main_frame, text="Insert keyword:", **label_style, font=("Segoe UI", 10))
    label.pack(pady=5)

    entry = tk.Entry(main_frame, width=30, **entry_style)
    entry.pack(pady=5, ipady=5)

    preview_frame = tk.Frame(main_frame, bg=COLORS["entry_bg"], bd=0)
    preview_frame.pack(fill=tk.X, pady=10)
    
    preview_label = tk.Label(preview_frame, text="Preview:", anchor='w', **label_style)
    preview_label.pack(anchor='w', padx=5)
    
    preview_text = tk.Text(preview_frame, height=3, width=30, wrap=tk.WORD, **entry_style)
    preview_text.pack(padx=5, pady=5, fill=tk.X)
    preview_text.config(state=tk.DISABLED)

    error_label = tk.Label(main_frame, text="", fg=COLORS["error"], **frame_style)
    error_label.pack()

    def update_preview(*args):
        current_text = entry.get().lower()
        preview_text.config(state=tk.NORMAL)
        preview_text.delete(1.0, tk.END)
        
        if current_text:
            exact_match = None
            for key in template_dict:
                if key.lower() == current_text:
                    exact_match = key
                    break
            
            if exact_match:
                preview_text.insert(tk.END, template_dict[exact_match])
                error_label.config(text="")
            else:
                matches = [key for key in template_dict.keys() if key.lower().startswith(current_text)]
                
                if len(matches) == 1:
                    preview_text.insert(tk.END, template_dict[matches[0]])
                    error_label.config(text="")
                elif len(matches) > 1:
                    preview_text.insert(tk.END, "Multiple matches...")
                    error_label.config(text="")
                else:
                    preview_text.insert(tk.END, "No match found")
                    error_label.config(text="")
        
        preview_text.config(state=tk.DISABLED)

    def insert_template(*args):
        current_text = entry.get().lower()
        if current_text:
            exact_match = None
            for key in template_dict:
                if key.lower() == current_text:
                    exact_match = key
                    break
            
            if exact_match:
                pyperclip.copy(template_dict[exact_match])
                keyboard.press_and_release('ctrl+v')
                root.destroy()
            else:
                matches = [key for key in template_dict.keys() if key.lower().startswith(current_text)]
                
                if len(matches) == 1:
                    pyperclip.copy(template_dict[matches[0]])
                    keyboard.press_and_release('ctrl+v')
                    root.destroy()
                elif len(matches) > 1:
                    error_label.config(text="Multiple matches found")
                else:
                    error_label.config(text="No match found")
        else:
            error_label.config(text="Enter a keyword")

    entry.bind('<KeyRelease>', update_preview)

    entry.bind('<Return>', insert_template)

    def on_escape(*args):
        root.destroy()

    root.bind('<Escape>', on_escape)

    def set_focus():
        root.focus_force()
        entry.focus_set()
        
    root.after(100, set_focus)
    
    root.mainloop()

def add_template_entry():
    active_window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(active_window).lower()
    
    template_names = []
    template_file_path = None
    
    for template_file in os.listdir(TEMPLATE_FOLDER):
        if template_file.endswith('.json'):
            with open(os.path.join(TEMPLATE_FOLDER, template_file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                if any(name.lower() in window_title for name in data.get("template_names", [])):
                    template_names = data.get("template_names", [])
                    template_file_path = os.path.join(TEMPLATE_FOLDER, template_file)
                    break
    
    if not template_file_path:
        messagebox.showerror("Error", "No template found for this window")
        return
    
    root = tk.Tk()
    root.title("Add template")
    
    root.attributes("-topmost", True)

    frame_style, label_style, button_style, entry_style = configure_styles(root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - 450) // 2
    y_position = (screen_height - 350) // 2
    root.geometry(f"450x350+{x_position}+{y_position}")

    main_frame = tk.Frame(root, **frame_style)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    template_names_str = ", ".join(template_names)
    template_label = tk.Label(main_frame, text=f"Add entry to the template: {template_names_str}", 
                            **label_style, font=("Segoe UI", 10, "bold"))
    template_label.pack(pady=10)

    key_frame = tk.Frame(main_frame, **frame_style)
    key_frame.pack(fill=tk.X, pady=5)
    
    key_label = tk.Label(key_frame, text="Keyword:", **label_style, font=("Segoe UI", 10))
    key_label.pack(anchor='w')
    
    key_entry = tk.Entry(key_frame, width=40, **entry_style)
    key_entry.pack(fill=tk.X, ipady=5)

    value_frame = tk.Frame(main_frame, **frame_style)
    value_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    value_label = tk.Label(value_frame, text="Template text:", **label_style, font=("Segoe UI", 10))
    value_label.pack(anchor='w')
    
    value_text = tk.Text(value_frame, height=8, **entry_style)
    value_text.pack(fill=tk.BOTH, expand=True, pady=5)

    def save_entry():
        key = key_entry.get().strip()
        value = value_text.get("1.0", tk.END).strip()
        
        if not key or not value:
            messagebox.showerror("Error", "Insert both key and template value")
            return
        
        try:
            with open(template_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if any(key.lower() == existing_key.lower() for existing_key in data.get("templates", {})):
                messagebox.showerror("Error", "Key already present in the template")
                return
            
            data.setdefault("templates", {})[key] = value
            
            with open(template_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            key_entry.delete(0, tk.END)
            value_text.delete("1.0", tk.END)
            key_entry.focus_set()
            
        except Exception as e:
            messagebox.showerror("Error", "Impossible to find the template file")

    button_frame = tk.Frame(main_frame, **frame_style)
    button_frame.pack(pady=10)
    
    save_button = tk.Button(button_frame, text="Save and continue", command=save_entry, **button_style)
    save_button.pack(side=tk.LEFT, padx=5)
    
    def save_and_close():
        save_entry()
        root.destroy()
    
    save_close_button = tk.Button(button_frame, text="Save and exit", command=save_and_close, **button_style)
    save_close_button.pack(side=tk.LEFT, padx=5)

    def on_escape(*args):
        root.destroy()

    root.bind('<Escape>', on_escape)

    def set_focus():
        root.focus_force()
        key_entry.focus_set()
        
    root.after(100, set_focus)
    
    root.mainloop()

def main():
    keyboard.add_hotkey(SEARCH_HOTKEY, on_hotkey)
    keyboard.add_hotkey(ADD_ENTRY_HOTKEY, add_template_entry)
    keyboard.wait()

if __name__ == "__main__":
    main()
