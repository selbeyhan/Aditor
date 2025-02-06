import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import json
import os

config_file_path = "config.json"
default_config = {
    "config_file_path" : "config.json",
    "theme": "Light",
    "font" : "Helvetica",
    "font_size" : 18,
    "line_numbers": True,
    "wrap": False,
    "nav_font_size" : 13,
    "nav_active_bg" : "#FFFF00",
    "nav_options_active_bg" : "#40E0D0"
}

def load_config():
    if os.path.exists(default_config["config_file_path"]):
        try:
            with open(default_config["config_file_path"], "r") as f:
                config = json.load(f)
            config = check_config_integrity(config) 
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

def check_config_integrity(config):
    for option in default_config:
        try:
            config[option]
            config[option] = default_config[option]
        except:
            raise Exception("Config File Error") 
    return config

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

def navbar_selection(option):
    if option == "File":
        if option == "Open":
            openfile(window, text_edit)
        elif option == "Save":
            savefile(window, text_edit)

def update_line_numbers(event=None, line_numbers=None, text_edit=None):
    if line_numbers is None or text_edit is None:
        return  # Prevent crashes if called incorrectly

    line_numbers.config(state="normal")
    line_numbers.delete("1.0", tk.END)
    total_lines = int(text_edit.index("end-1c").split('.')[0])
    numbers = "\n".join(str(i) for i in range(1, total_lines + 1))
    line_numbers.insert("1.0", numbers)
    line_numbers.config(state="disabled")

def highlight_current_line(event=None, text_edit=None):
    """Highlights the background of the current line."""
    text_edit.tag_remove("highlight", "1.0", tk.END)  # Remove previous highlight

    # Get the current cursor position
    current_line = text_edit.index(tk.INSERT).split(".")[0]  # Extract line number
    text_edit.tag_add("highlight", f"{current_line}.0", f"{current_line}.end+1c")

    # Style the tag
    text_edit.tag_configure("highlight", background="lightyellow")  # Change color as needed


def settings(window, config):
    settingsmenu = tk.Frame(window, bd=1)
    settingsmenu.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nesw")
    save_button = tk.Button(settingsmenu, text="Save", command=lambda: safe_exit(settingsmenu, config)) 
    close_button = tk.Button(settingsmenu, text="Close", command= lambda: settingsmenu.destroy()) 

    save_button.grid(row=2, column=1, sticky="ns")
    close_button.grid(row=3, column=2, sticky="ns")
    
    theme_options = ("Light", "Dark")
    theme_dropdown = make_dropdown(settingsmenu, config["theme"], theme_options, 1, 1, "ew")

def make_menu(window, config, default_var, options, row, column, sticky):
    menu_button = tk.Menubutton(window, text=default_var)
    menu = tk.Menu(menu_button, tearoff=False, font=(config["font"], config["nav_font_size"]), bg=config["nav_options_active_bg"])  # Apply bg to full menu
    menu_button["menu"] = menu

    for option in options:
        menu.add_command(label=option, command=lambda opt=option: navbar_selection(opt))

    menu_button.config(width=8, padx=5, font=(config["font"], config["nav_font_size"]), activebackground=config["nav_active_bg"])
    menu_button.pack(side=tk.LEFT)

def make_dropdown(window, default_var, options, row, column, sticky):
    dropdown_var = tk.StringVar(window)
    dropdown_var.set(default_var)
    dropdown = tk.OptionMenu(window, dropdown_var, *options)
    dropdown.config(width=10)
    dropdown.grid(row=row, column=column, padx=5, pady=5, sticky=sticky)
    return dropdown

def main():
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
    file_options = ("New", "Open", "Save", "Save and Close", "Rename", "Properties")
    file_dropdown = make_menu(navbar, config, "File", file_options, 0, 0, "ew")
     
    # ----- Edit Drop-down -----
    edit_options = ("Paste", "Paste and match style", "Find", "Find and Replace")
    edit_dropdown = make_menu(navbar, config, "Edit", edit_options, 0, 1, "ew")

    # ----- Format Drop-down -----
    format_options = ("Font", "Text")
    format_dropdown = make_menu(navbar, config, "Format", format_options, 0, 2, "ew")

    # ----- View Drop-down -----
    view_options = ("Nothing In Here For Now",)
    view_dropdown = make_menu(navbar, config, "View", view_options, 0, 3, "ew")
    
    # ----- Window Drop-down -----
    window_options = ("Zoom",)
    window_dropdown = make_menu(navbar, config, "Window", window_options, 0, 4, "ew")

    # ----- Settings Button -----
    settings_button = tk.Button(navbar, text="Settings", bd=0, command=lambda: settings(window, config))
    # settings_button.grid(row=0, column=5, padx=5, sticky="ew")


    # ===== Main Content Area (Row 1) =====
    # Create the Line Numbers widget (Left Column)
    line_numbers = tk.Text(window, font=font, width=4, padx=3, takefocus=0, border=0, background='lightgrey', state='disabled', wrap="none")
    line_numbers.grid(row=1, column=0, sticky="ne")

    # Create the Text Editor widget (Right Column)
    text_edit = tk.Text(window, font=font, wrap="none")
    text_edit.grid(row=1, column=1, sticky="nsew")

    # Bind key release events to update the line numbers.
    text_edit.bind("<KeyRelease>", lambda event: update_line_numbers(event, line_numbers, text_edit))
    text_edit.bind("<KeyRelease>", lambda event: [update_line_numbers(event, line_numbers, text_edit), highlight_current_line(event, text_edit)])
    text_edit.bind("<ButtonRelease>", lambda event: highlight_current_line(event, text_edit))  # Detects mouse clicks

    # Update line numbers once at startup.
    update_line_numbers(line_numbers)

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
