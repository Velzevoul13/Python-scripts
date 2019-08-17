from tkinter import *
from backEnd import Database

database = Database("books.db")

"""
"""
class Window(object):
    def __init__(self, window):
        self.window = window
        self.window.wm_title("Bookstore")

        line1 = Label(window, text="Title")
        line1.grid(row=0, column=0)

        line2 = Label(window, text="Author")
        line2.grid(row=0, column=2)

        line3 = Label(window, text="Year")
        line3.grid(row=1, column=0)

        line4 = Label(window, text="ISBN")
        line4.grid(row=1, column=2)

        """
        """

        self.title_text = StringVar()
        self.entry1 = Entry(window, textvariable=self.title_text, width=30)
        self.entry1.grid(row=0, column=1)

        self.author_text = StringVar()
        self.entry2 = Entry(window, textvariable=self.author_text, width=30)
        self.entry2.grid(row=0, column=3)

        self.year_text = StringVar()
        self.entry3 = Entry(window, textvariable=self.year_text, width=30)
        self.entry3.grid(row=1, column=1)

        self.isbn_text = StringVar()
        self.entry4 = Entry(window, textvariable=self.isbn_text, width=30)
        self.entry4.grid(row=1, column=3)

        """
        """

        self.main_list = Listbox(window, height=25, width=35)
        self.main_list.grid(row=2, column=0, rowspan=6, columnspan=2)

        """
        """

        scrollbar1 = Scrollbar(window)
        scrollbar1.grid(row=2, column=2, rowspan=6)

        self.main_list.configure(yscrollcommand=scrollbar1.set)
        scrollbar1.configure(command=self.main_list.yview)

        self.main_list.bind('<<ListboxSelect>>', self.get_selected_row)

        """
        """

        button1 = Button(window, text="View All", width=15, command=self.view_command)
        button1.grid(row=2, column=3)

        button2 = Button(window, text="Search Entry", width=15, command=self.search_command)
        button2.grid(row=3, column=3)

        button3 = Button(window, text="Add Entry", width=15, command=self.insert_command)
        button3.grid(row=4, column=3)

        button4 = Button(window, text="Update Entry", width=15, command=self.update_command)
        button4.grid(row=5, column=3)

        button5 = Button(window, text="Delete Entry", width=15, command=self.delete_command)
        button5.grid(row=6, column=3)

        button6 = Button(window, text="Close", width=15, command=window.destroy)
        button6.grid(row=7, column=3)

    def get_selected_row(self, event):
        try:
            global selected_tuple
            index = self.main_list.curselection()[0]
            selected_tuple = self.main_list.get(index)
            self.entry1.delete(0, END)
            self.entry1.insert(END, self.selected_tuple[1])
            self.entry2.delete(0, END)
            self.entry2.insert(END, self.selected_tuple[2])
            self.entry3.delete(0, END)
            self.entry3.insert(END, self.selected_tuple[3])
            self.entry4.delete(0, END)
            self.entry4.insert(END, self.selected_tuple[4])
        except IndexError:
            pass


    def view_command(self):
        self.main_list.delete(0, END)
        for row in database.view():
            self.main_list.insert(END, row)


    def search_command(self):
        self.main_list.delete(0, END)
        for row in database.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.main_list.insert(END, row)


    def insert_command(self):
        database.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.main_list.delete(0, END)
        self.main_list.insert(END, (self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()))


    def delete_command(self):
        database.delete(self.selected_tuple[0])


    def update_command(self):
        database.update(self.selected_tuple[0], self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())


"""
"""

window = Tk()
Window(window)
window.wm_title("Book Store")
window.geometry("450x450")
window.resizable(0, 0)

"""
"""
window.mainloop()
