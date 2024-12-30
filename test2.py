from tkinter import *



BG_COLOR = "#ffffff"
TEXT_COLOR = "#000000"

FONT = "Arial 14"


# Send function
def send(event):
    send = "You: " + e.get()
    txt.config(state=NORMAL)
    txt.insert(END, send + "\n")
    txt.config(state=DISABLED)

    message = e.get().lower()

    txt.config(state=NORMAL)
    txt.insert(END, "Bot: Sorry! I didn't understand that" + "\n")
    txt.config(state=DISABLED)
    txt.see(END)

    e.delete(0, END)


if __name__ == '__main__':

    # GUI
    root = Tk()
    root.title("RPC chat")
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=50, state=DISABLED)
    txt.grid(row=0, column=0, sticky=N + E + S + W)

    scrollbar = Scrollbar(root, command=txt.yview)
    scrollbar.grid(row=0, column=1, sticky=N + S)
    txt.config(yscrollcommand=scrollbar.set)

    e = Entry(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=1)
    e.grid(row=1, column=0, columnspan=2, sticky=E + W)
    e.focus_set()

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.bind("<Return>", send)
    root.mainloop()