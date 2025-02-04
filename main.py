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

def selected_option(navbar_option, sub_option, file_dropdown):
    if option == "Open":
        file_dropdown.set("File")
        openfile(window, text_edit)
    elif option == "Save":
        file_dropdown.set("File")
        savefile(window, text_edit)


def main():
    global window, text_edit
    window = tk.Tk()
    window.title("Aditor")
    window.rowconfigure(1, minsize=400)
    window.columnconfigure(0, minsize=400)

    text_edit = tk.Text(window, font="Helvetica 18")
    text_edit.grid(row=1, column=0)

    navbar = tk.Frame(window, bd=2)

    # Drop-down menu
    file_dropdown = tk.StringVar(navbar)
    file_dropdown_options = ("New", "Open", "Save", "Save and Close", "Rename", "Properties")
    file_dropdown.set("File")  # Default text
    file_dropdown_options = tk.OptionMenu(navbar, file_dropdown, *file_dropdown_options, command=lambda option: selected_option("File", option, file_dropdown))
    
    edit_dropdown = tk.StringVar(navbar)
    edit_dropdown_option = ("Paste", "Paste and match style", "Find", "Find and Replace")

    format_dropdown_option = ("Font", "Text")

    view_dropdown_option = ("Nothing In Here For Now")

    window_dropdown_option = ("Zoom")
    
    # Make settings a button 

    save_button = tk.Button(navbar, text="Save", command=lambda: savefile(window, text_edit))
    open_button = tk.Button(navbar, text="Open", command=lambda: openfile(window, text_edit))

    save_button.grid(row=0, column=0, padx=5, sticky="ew")
    open_button.grid(row=0, column=1, padx=5, sticky="ew")
    file_dropdown_options.grid(row=0, column=2, padx=5, sticky="ew")
    navbar.grid(row=0, column=0, columnspan=2, sticky="ew")

    window.bind("<Control-s>", lambda x: savefile(window, text_edit))
    window.bind("<Control-o>", lambda x: openfile(window, text_edit))
    window.bind("<Control-w>", lambda x: safe_exit(window))

    window.mainloop()

main()
