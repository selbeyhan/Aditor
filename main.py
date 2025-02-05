import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def safe_exit(window):
    window.destroy()

def openfile(window, text_edit):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    
    text_edit.delete(1.0, tk.END)
    with open(filepath, "r") as f:
        content = f.read()
        text_edit.insert(tk.END, content)

    window.title(f"File Open: {filepath}")

def savefile(window, text_edit):
    filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    
    with open(filepath, "w") as f:
        content = text_edit.get(1.0, tk.END)
        f.write(content)

    window.title(f"File Save: {filepath}")

def select_dropdown(navbar_option, sub_option, dropdown_var):
    dropdown_var.set(navbar_option)
    if sub_option == "Open":
        openfile(window, text_edit)
    elif sub_option == "Save":
        savefile(window, text_edit)
    # You can add more logic for other options if needed.

def settings():
    pass

def main():
    global window, text_edit
    window = tk.Tk()
    window.title("Aditor")
    window.rowconfigure(1, minsize=400)
    window.columnconfigure(0, minsize=400)

    text_edit = tk.Text(window, font="Helvetica 18")
    text_edit.grid(row=1, column=0)

    navbar = tk.Frame(window, bd=2)

    # Define the active foreground color you want for all navbar elements:
    active_fg_color = "red"

    # ===== File Drop-down =====
    file_dropdown_var = tk.StringVar(navbar)
    file_options = ("New", "Open", "Save", "Save and Close", "Rename", "Properties")
    file_dropdown_var.set("File")  # Default text
    file_dropdown = tk.OptionMenu(navbar, file_dropdown_var, *file_options, 
                                 command=lambda option: select_dropdown("File", option, file_dropdown_var))
    file_dropdown.grid(row=0, column=0, padx=5, sticky="ew")
    # Change active foreground color for the OptionMenu button and its menu:
    file_dropdown.config(activeforeground=active_fg_color)
    file_dropdown["menu"].config(activeforeground=active_fg_color)

    # ===== Edit Drop-down =====
    edit_dropdown_var = tk.StringVar(navbar)
    edit_options = ("Paste", "Paste and match style", "Find", "Find and Replace")
    edit_dropdown_var.set("Edit")
    edit_dropdown = tk.OptionMenu(navbar, edit_dropdown_var, *edit_options, 
                                 command=lambda option: select_dropdown("Edit", option, edit_dropdown_var))
    edit_dropdown.grid(row=0, column=1, padx=5, sticky="ew")
    edit_dropdown.config(activeforeground=active_fg_color)
    edit_dropdown["menu"].config(activeforeground=active_fg_color)

    # ===== Format Drop-down =====
    format_dropdown_var = tk.StringVar(navbar)
    format_options = ("Font", "Text")
    format_dropdown_var.set("Format")
    format_dropdown = tk.OptionMenu(navbar, format_dropdown_var, *format_options, 
                                   command=lambda option: select_dropdown("Format", option, format_dropdown_var))
    format_dropdown.grid(row=0, column=2, padx=5, sticky="ew")
    format_dropdown.config(activeforeground=active_fg_color)
    format_dropdown["menu"].config(activeforeground=active_fg_color)

    # ===== View Drop-down =====
    view_dropdown_var = tk.StringVar(navbar)
    view_options = ("Nothing In Here For Now",)  # Single option as a tuple
    view_dropdown_var.set("View")
    view_dropdown = tk.OptionMenu(navbar, view_dropdown_var, *view_options, 
                                 command=lambda option: select_dropdown("View", option, view_dropdown_var))
    view_dropdown.grid(row=0, column=3, padx=5, sticky="ew")
    view_dropdown.config(activeforeground=active_fg_color)
    view_dropdown["menu"].config(activeforeground=active_fg_color)

    # ===== Window Drop-down =====
    window_dropdown_var = tk.StringVar(navbar)
    window_options = ("Zoom",)
    window_dropdown_var.set("Window")
    window_dropdown = tk.OptionMenu(navbar, window_dropdown_var, *window_options, 
                                   command=lambda option: select_dropdown("Window", option, window_dropdown_var))
    window_dropdown.grid(row=0, column=4, padx=5, sticky="ew")
    window_dropdown.config(activeforeground=active_fg_color)
    window_dropdown["menu"].config(activeforeground=active_fg_color)

    # ===== Settings Button =====
    settings_button = tk.Button(navbar, text="Settings", command=settings)
    settings_button.grid(row=0, column=6, padx=5, sticky="ew")
    settings_button.config(activeforeground=active_fg_color)

    navbar.grid(row=0, column=0, columnspan=2, sticky="ew")

    # Keyboard bindings
    window.bind("<Control-s>", lambda x: savefile(window, text_edit))
    window.bind("<Control-o>", lambda x: openfile(window, text_edit))
    window.bind("<Control-w>", lambda x: safe_exit(window))

    window.mainloop()

if __name__ == "__main__":
    main()
