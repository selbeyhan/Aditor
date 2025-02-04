import tkinter as tk

def main():
    window = tk.Tk()
    window.title("Text Editor")
    window.rowconfigure(0, minsize=400)
    window.columnconfigure(1, minsize=400)


    text_edit = tk.Text(window, font="Helvetica 18")
    text_edit.grid(row=0, column=1)

    frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    save_button = tk.Button(frame, text="Save")
    open_button = tk.Button(frame, text="Open")


    save_button.grid(row=0, column=0, padx=5, pady=5)
    open_button.grid(row=1,column=0, padx=5)
    frame.grid(row=0,column=0, stick="ns")

    window.mainloop()

main()
