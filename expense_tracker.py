from tkinter import *
from tkinter import ttk
import sqlite3 as db
from tkcalendar import DateEntry


def init():
    global connectionObjn
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS expenses (
        date TEXT,
        name TEXT,
        title TEXT,
        expense REAL
    )
    '''
    curr.execute(query)
    connectionObjn.commit()


def submitexpense():
    try:
        
        date_val = dateEntry.get()
        name_val = Name.get()
        title_val = Title.get()
        expense_val = Expense.get()
        
   
        if not all([date_val, name_val, title_val]):
            raise ValueError("All fields are required")
        if not isinstance(expense_val, (int, float)):
            raise ValueError("Expense must be a number")
        
       
        values = [date_val, name_val, title_val, float(expense_val)]
        
       
        Etable.insert('', 'end', values=values)
        
        
        curr = connectionObjn.cursor()
        query = "INSERT INTO expenses VALUES (?, ?, ?, ?)"
        curr.execute(query, values)
        connectionObjn.commit()
        
        Name.set('')
        Title.set('')
        Expense.set(0)
        
        
        status_label.config(text="Expense added successfully!", fg="green")
        
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")


def viewexpense():
    try:
        # Clear existing data 
        for item in Etable.get_children():
            Etable.delete(item)
        
        # Geting all expenses
        curr = connectionObjn.cursor()
        curr.execute("SELECT * FROM expenses")
        rows = curr.fetchall()
        
        # total
        curr.execute("SELECT SUM(expense) FROM expenses")
        total = curr.fetchone()[0] or 0
        
       
        for row in rows:
            Etable.insert('', 'end', values=row)
        
      
        total_label.config(text=f"Total Expenses: ${total:.2f}")
        status_label.config(text="Expenses loaded successfully!", fg="green")
        
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")


def clear_form():
    Name.set('')
    Title.set('')
    Expense.set(0)
    status_label.config(text="Form cleared", fg="blue")


def on_closing():
    connectionObjn.close()
    root.destroy()


init()


root = Tk()
root.title("ProjectGurukul Expense Tracker")
root.geometry('900x700')


dateLabel = Label(root, text="Date", font=('arial', 15, 'bold'), 
                 bg="DodgerBlue2", fg="white", width=12)
dateLabel.grid(row=0, column=0, padx=7, pady=7)

dateEntry = DateEntry(root, width=12, font=('arial', 15, 'bold'))
dateEntry.grid(row=0, column=1, padx=7, pady=7)


Name = StringVar()
nameLabel = Label(root, text="Name", font=('arial', 15, 'bold'), 
                 bg="DodgerBlue2", fg="white", width=12)
nameLabel.grid(row=1, column=0, padx=7, pady=7)

NameEntry = Entry(root, textvariable=Name, font=('arial', 15, 'bold'))
NameEntry.grid(row=1, column=1, padx=7, pady=7)


Title = StringVar()
titleLabel = Label(root, text="Title", font=('arial', 15, 'bold'), 
                  bg="DodgerBlue2", fg="white", width=12)
titleLabel.grid(row=2, column=0, padx=7, pady=7)

titleEntry = Entry(root, textvariable=Title, font=('arial', 15, 'bold'))
titleEntry.grid(row=2, column=1, padx=7, pady=7)


Expense = DoubleVar()
expenseLabel = Label(root, text="Expense", font=('arial', 15, 'bold'), 
                    bg="DodgerBlue2", fg="white", width=12)
expenseLabel.grid(row=3, column=0, padx=7, pady=7)

expenseEntry = Entry(root, textvariable=Expense, font=('arial', 15, 'bold'))
expenseEntry.grid(row=3, column=1, padx=7, pady=7)


submitbtn = Button(root, command=submitexpense, text="Submit",
                  font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
submitbtn.grid(row=4, column=0, padx=13, pady=13)

viewbtn = Button(root, command=viewexpense, text="View Expenses",
                font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
viewbtn.grid(row=4, column=1, padx=13, pady=13)

clearbtn = Button(root, command=clear_form, text="Clear Form",
                 font=('arial', 15, 'bold'), bg="red", fg="white", width=12)
clearbtn.grid(row=4, column=2, padx=13, pady=13)


Elist = ['Date', 'Name', 'Title', 'Expense']
Etable = ttk.Treeview(root, columns=Elist, show='headings', height=15)


vsb = ttk.Scrollbar(root, orient="vertical", command=Etable.yview)
vsb.grid(row=5, column=3, sticky='ns')
hsb = ttk.Scrollbar(root, orient="horizontal", command=Etable.xview)
hsb.grid(row=6, column=0, columnspan=3, sticky='ew')
Etable.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)


for col in Elist:
    Etable.heading(col, text=col)
    Etable.column(col, width=150, anchor='center')

Etable.grid(row=5, column=0, padx=7, pady=7, columnspan=3)


total_label = Label(root, text="Total Expenses: $0.00", 
                   font=('arial', 15, 'bold'), bg="green", fg="white")
total_label.grid(row=7, column=0, columnspan=3, padx=7, pady=7, sticky='ew')


status_label = Label(root, text="Ready", font=('arial', 12))
status_label.grid(row=8, column=0, columnspan=3, padx=7, pady=7)


root.protocol("WM_DELETE_WINDOW", on_closing)


mainloop()