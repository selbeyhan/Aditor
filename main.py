import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import json
import os

config_file_path = "config.json"
default_config = {
    "config_file_path" : "config.json", "theme": "light",
    "font" : "Helvetica",
    "font_size" : 18,
    "line_numbers": True,
    "wrap": False
}

def load_config():
    if os.path.exists(default_config["config_file_path"]):
        try:
            with open(default_config["config_file_path"], "r") as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError:
            return default_config
    else:
        return default_config.copy()

def save_config(config):
    if(config["config_file_path"]):
        with open(config["config_file_path"], "w") as f:
            json.dump(config, f, indent=4)
    else:
        with open(default_config["config_file_path"], "w") as f:
            json.dump(config, f, indent=4)

def safe_exit(local, config):
    save_config(config)
    local.destroy()

def openfile(window, text_edit):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    text_edit.delete("1.0", tk.END)
    with open(filepath, "r") as f:
        content = f.read()
    text_edit.insert(tk.END, content)
    window.title(f"File Open: {filepath}")

def savefile(window, text_edit):
    filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    with open(filepath, "w") as f:
        content = text_edit.get("1.0", tk.END)
        f.write(content)
    window.title(f"File Save: {filepath}")

def select_dropdown(navbar_option, sub_option, dropdown_var):
    dropdown_var.set(navbar_option)
    if navbar_option == "File":
        if sub_option == "Open":
            openfile(window, text_edit)
        elif sub_option == "Save":
            savefile(window, text_edit)
    # You can add logic for other menus as needed.

def update_line_numbers(event=None):
    """Updates the line numbers shown on the left side."""
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", tk.END)
    # Get the total number of lines in the text editor.
    total_lines = int(text_edit.index("end-1c").split('.')[0])
    # Create a string with line numbers.
    numbers = "\n".join(str(i) for i in range(1, total_lines + 1))
    line_numbers.insert("1.0", numbers)
    line_numbers.config(state="disabled")

def settings():
    settingsmenu = tk.Frame(window, bd=10)
    settingsmenu.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nesw")

    close_button = tk.Button(settingsmenu, text="Close", command=lambda: safe_exit(settingsmenu)) 
    close_button.pack()


def main():
    global window, text_edit, line_numbers, font_type, font_size, font 
    config = load_config()

    window = tk.Tk()
    window.title("Aditor")
    font_type = config["font"] 
    font_size = config["font_size"] 
    font = f"{font_type} {font_size}" 

    # Configure the grid:
    # Row 0 will be the navbar.
    # Row 1 will hold the main content in two columns.
    window.rowconfigure(1, weight=1)
    window.columnconfigure(0, weight=0)  # Left column for line numbers (fixed width)
    window.columnconfigure(1, weight=1)  # Right column for text editor (expands)

    # ===== Navbar (Row 0, spanning both columns) =====
    navbar = tk.Frame(window, bd=2)
    navbar.grid(row=0, column=0, columnspan=2, sticky="ew")

    # ----- File Drop-down -----
    file_dropdown_var = tk.StringVar(navbar)
    file_options = ("New", "Open", "Save", "Save and Close", "Rename", "Properties")
    file_dropdown_var.set("File")  # Default text
    file_dropdown = tk.OptionMenu(navbar, file_dropdown_var, *file_options, command=lambda option: select_dropdown("File", option, file_dropdown_var))
    file_dropdown.grid(row=0, column=0, padx=5, sticky="ew")

    # ----- Edit Drop-down -----
    edit_dropdown_var = tk.StringVar(navbar)
    edit_options = ("Paste", "Paste and match style", "Find", "Find and Replace")
    edit_dropdown_var.set("Edit")
    edit_dropdown = tk.OptionMenu(navbar, edit_dropdown_var, *edit_options, command=lambda option: select_dropdown("Edit", option, edit_dropdown_var))
    edit_dropdown.grid(row=0, column=1, padx=5, sticky="ew")

    # ----- Format Drop-down -----
    format_dropdown_var = tk.StringVar(navbar)
    format_options = ("Font", "Text")
    format_dropdown_var.set("Format")
    format_dropdown = tk.OptionMenu(navbar, format_dropdown_var, *format_options, command=lambda option: select_dropdown("Format", option, format_dropdown_var))
    format_dropdown.grid(row=0, column=2, padx=5, sticky="ew")

    # ----- View Drop-down -----
    view_dropdown_var = tk.StringVar(navbar)
    view_options = ("Nothing In Here For Now",)
    view_dropdown_var.set("View")
    view_dropdown = tk.OptionMenu(navbar, view_dropdown_var, *view_options, command=lambda option: select_dropdown("View", option, view_dropdown_var))
    view_dropdown.grid(row=0, column=3, padx=5, sticky="ew")

    # ----- Window Drop-down -----
    window_dropdown_var = tk.StringVar(navbar)
    window_options = ("Zoom",)
    window_dropdown_var.set("Window")
    window_dropdown = tk.OptionMenu(navbar, window_dropdown_var, *window_options, command=lambda option: select_dropdown("Window", option, window_dropdown_var))
    window_dropdown.grid(row=0, column=4, padx=5, sticky="ew")

    # ----- Settings Button -----
    settings_button = tk.Button(navbar, text="Settings", command=settings)
    settings_button.grid(row=0, column=5, padx=5, sticky="ew")


    # ===== Main Content Area (Row 1) =====
    # Create the Line Numbers widget (Left Column)
    line_numbers = tk.Text(window, font=font, width=4, padx=3, takefocus=0, border=0, background='lightgrey', state='disabled', wrap="none")
    line_numbers.grid(row=1, column=0, sticky="ne")

    # Create the Text Editor widget (Right Column)
    text_edit = tk.Text(window, font=font, wrap="none")
    text_edit.grid(row=1, column=1, sticky="nsew")

    # Bind key release events to update the line numbers.
    text_edit.bind("<KeyRelease>", update_line_numbers)

    # Update line numbers once at startup.
    update_line_numbers()

    # Auto focus on the text area at startup.
    text_edit.focus_set()

    # Keyboard shortcuts
    window.bind("<Control-s>", lambda event: savefile(window, text_edit))
    window.bind("<Control-o>", lambda event: openfile(window, text_edit))
    window.bind("<Control-w>", lambda event: safe_exit(window, config))

    window.protocol("WM_DELETE_WINDOW", lambda:  safe_exit(window, config))
    window.mainloop()

if __name__ == "__main__":
    main()
