import tkinter as tk
from tkinter import ttk
import sqlite3 
import subprocess
from tkinter import *
from datetime import datetime
from tkcalendar import Calendar
import time
import pandas as pd
import pyarrow
import firebase_admin
from firebase_admin import credentials, db

splash = tk.Tk()
splash.geometry("644x420+450+200")
splash.overrideredirect(True)
bg_image = tk.PhotoImage(file="splash_bg.png")
background_label = tk.Label(splash, image=bg_image)
background_label.place(relwidth=1, relheight=1)

process = None  # global variable to hold the running process

def main_func():
    splash.destroy()
    # create the main window
    root = tk.Tk()
    root.title("Attendance System")
    root.geometry("1280x720")

    def start_stop():
        global process  # use the global variable

        if process is None:  # if the process is not running, start it
            process = subprocess.Popen(['python', 'getmac.py'])  # start the file
            button1.config(text='Stop')  # change the button text to "Stop"
        else:  # if the process is running, stop it
            process.terminate()  # terminate the process
            process = None  # set the process variable to None
            button1.config(text='Start')  # change the button text to "Start"

    def on_close():
        global process  # use the global variable
        update_exit_time()
        if process is not None:  # if the process is running, stop it
            process.terminate()  # terminate the process
        root.destroy()  # destroy the main window

    def net_address():
        subprocess.Popen(['python', 'n_address.py'])

    # create two tabs
    tab_control = ttk.Notebook(root)
    tab3 = ttk.Frame(tab_control)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab3, text='Start System')
    tab_control.add(tab1, text='Attendee Data')
    tab_control.add(tab2, text='Attendance Database')
    # Not working
    # bg_image = tk.PhotoImage(file="bg.png")
    # background_label1 = tk.Label(tab3, image=bg_image)
    # background_label2 = tk.Label(tab1, image=bg_image)
    # background_label3 = tk.Label(tab2, image=bg_image)
    # background_label1.place(relwidth=1, relheight=1)
    # background_label2.place(relwidth=1, relheight=1)
    # background_label3.place(relwidth=1, relheight=1)

    root.protocol("WM_DELETE_WINDOW", on_close)  # bind the WM_DELETE_WINDOW event to the on_close function
    button1 = tk.Button(tab3, text='Start the attendance system', command=start_stop, width=30, height= 2)
    button1.pack(pady=50)
    button2 = tk.Button(tab3, text='Change Network Address', command=net_address, width=30, height= 2)
    button2.place(relx=1, rely=1, anchor=tk.SE, x=-10, y=-10)
    # image = PhotoImage(file="download.png")

    # Add the image to a label and display it in both tabs
    # label = Label(tab3, image=image)
    label = Label(tab3)
    label.pack(pady=40)






    
    # Create a Treeview widget
    tree = ttk.Treeview(tab1)

    def add_data():
        # Get data from textboxes
        username = username_entry.get()
        mac_address = mac_entry.get()

        # Insert data into database
        conn = sqlite3.connect("attendance.db")
        c = conn.cursor()
        c.execute("INSERT INTO userdata (username, mac_address) VALUES (?, ?)", (username, mac_address))
        conn.commit()
        conn.close()

        # Clear textboxes
        username_entry.delete(0, tk.END)
        mac_entry.delete(0, tk.END)

        # Reload the database and update the Treeview widget
        reload_gui()

    def reload_gui():
        # Clear the current data in the Treeview widget
        tree.delete(*tree.get_children())

        # Reload the database
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute("SELECT * FROM userdata")
        data = c.fetchall()
        conn.close()

        # Add the updated data to the Treeview widget
        for row in data:
            tree.insert('', tk.END, values=row)

    def delete_record():
        # Get the ID from the user
        id = id_entry.get()

        # Connect to the database
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        # Delete the record with the given ID
        cursor.execute("DELETE FROM userdata WHERE id=?", (id,))
        conn.commit()

        # Close the database connection
        conn.close()

        # Clear the ID entry field
        id_entry.delete(0, tk.END)

        # Update the status label
        status_label.config(text="")

        # Reload the database and update the Treeview widget
        reload_gui()

    def update_exit_time():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE Attend SET exit_time = ? WHERE exit_time IS NULL", (current_time,))
        conn.commit()

        # Close the database connection
        conn.close()
    
    def on_button_click():
        # Connect to the SQLite database
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        # Create a Tkinter window
        window = tk.Toplevel(root)
        window.title("Select Date")

        # Create a Calendar widget
        cal = Calendar(window, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(padx=20, pady=20)

        # Function to extract attendance table to Excel
        def extract_to_excel():
            selected_date = cal.get_date()
            print("Selected Date:", selected_date)

            # Query the database to fetch attendance data for the selected date
            query = "SELECT user_id, entry_time, exit_time FROM Attend WHERE today_date = ?"
            cursor.execute(query, (selected_date,))
            data = cursor.fetchall()
            
            # Create a DataFrame from the fetched data
            df = pd.DataFrame(data, columns=['user_id', 'entry_time', 'exit_time'])
            
            # Export DataFrame to Excel
            filename = f"attendance_{selected_date}.xlsx"
            df.to_excel(filename, index=False)
            print("Attendance data exported to:", filename)

        # Create a button to extract attendance to Excel
        export_button = tk.Button(window, text="Export Attendance to Excel", command=extract_to_excel)
        export_button.pack(pady=10)


    # Create username label and entry box
    username_label = tk.Label(tab1, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(tab1)
    username_entry.pack()

    # Create MAC address label and entry box
    mac_label = tk.Label(tab1, text="MAC Address:")
    mac_label.pack()
    mac_entry = tk.Entry(tab1)
    mac_entry.pack()

    # Create add button
    add_button = tk.Button(tab1, text="Add", command=add_data)
    add_button.pack()

    # Create widgets for deleting records
    id_label = tk.Label(tab1, text="ID:")
    id_entry = tk.Entry(tab1)
    delete_button = tk.Button(tab1, text="Delete", command=delete_record)
    status_label = tk.Label(tab1, text="")
    id_label.pack()
    id_entry.pack()
    delete_button.pack()
    status_label.pack()

    # Define columns for the Treeview widget
    tree['columns'] = ('ID', 'Name', 'Mac')

    # Format column headers
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID', anchor=tk.CENTER, width=100)
    tree.column('Name', anchor=tk.CENTER, width=150)
    tree.column('Mac', anchor=tk.CENTER, width=100)

    # Add column headers to Treeview widget
    tree.heading('#0', text='', anchor=tk.CENTER)
    tree.heading('ID', text='ID', anchor=tk.CENTER)
    tree.heading('Name', text='Name', anchor=tk.CENTER)
    tree.heading('Mac', text= 'Mac', anchor=tk.CENTER)

    # Fetch data from the database and insert it into the Treeview widget
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM userdata'):

        tree.insert('', tk.END, text='', values=row)

    # Pack the Treeview widget
    tree.pack(expand=tk.YES, fill=tk.BOTH)

    # display the tabs
    tab_control.pack(expand=1, fill='both')

    def print_date():
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        selected_date = datetime.strptime(cal.get_date(), '%m/%d/%y')
        formatted_date = selected_date.strftime('%Y-%m-%d')
        print(formatted_date)
        user_id = combo.get()
        print(user_id)
        if user_id != "":
            from logtime import logtimecalc
            a= logtimecalc(formatted_date, user_id)
            result_label.config(text=f"Total Log time : {a}",font=("Arial", 16))
            c.execute("select * from Attend where today_date  = ? AND user_id = ?", (formatted_date, user_id))
            print_date = c.fetchall()
            print(print_date)
        else:
            result_label.config(text="")
            c.execute("select * from Attend where today_date  = ?", (formatted_date,))
            print_date = c.fetchall()
            print(print_date)
        
        # Clear the current Treeview data
        for row in treeview.get_children():
            treeview.delete(row)
        
        # Add the updated data to the Treeview widget
        for row in print_date:
            treeview.insert("", tk.END, values=row)

    def on_firebase_button_click():
        # Connect to the SQLite database
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        # Create a Tkinter window
        window = tk.Toplevel(root)
        window.title("Select Date")

        # Create a Calendar widget
        cal = Calendar(window, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(padx=20, pady=20)
        def export_to_firebase():
            cred = credentials.Certificate("wifi-based-attendance-systempc-firebase-adminsdk-zxfc9-ef14c8a7a2.json")
            firebase_admin.initialize_app(cred, {"databaseURL": "https://wifi-based-attendance-systempc-default-rtdb.firebaseio.com/"})
            ref = db.reference('/Attendance Data/')

            conn = sqlite3.connect("attendance.db")
            cursor = conn.cursor()
            selected_date = cal.get_date()

            # query = "SELECT user_id, entry_time, exit_time FROM Attend WHERE today_date = ?"
            cursor.execute("SELECT * FROM Attend WHERE today_date = ?", (selected_date,))
            data1 = cursor.fetchall()

            # Push records to Firebase
            for row in data1:
                srno, user_id, entry_time, exit_time, today_date = row

                # Pushing data to Firebase
                ref.push({
                    'srno': srno,
                    'user_id': user_id,
                    'entry_time': entry_time,
                    'exit_time': exit_time,
                    'today_date': today_date
                })

            print("Data exported to Firebase.")

        export_button = tk.Button(window, text="Export Attendance to Firebase", command=export_to_firebase)
        export_button.pack(pady=10)

    label = tk.Label(tab2, text="Select a employee by ID")
    label.pack()

    # Create a dropdown widget
    combo = ttk.Combobox(tab2, state="readonly")
    combo.pack()

    cal = Calendar(tab2, selectmode='day', year=2024, month=3, day=21)
    cal.pack(pady=20)

    combo['values'] = [""] 
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT id FROM userdata")
    user_ids = [row[0] for row in c.fetchall()]
    combo['values'] += tuple(user_ids)
    treeview = ttk.Treeview(tab2, show='headings')
    treeview['columns'] = ('ID', 'UID', 'Entry_time', 'Exit_time','today_date')
    # Set column headings
    treeview.heading('ID', text='ID')
    treeview.heading('UID', text='UID')
    treeview.heading('Entry_time', text='Entry time')
    treeview.heading('Exit_time', text='Exit time')
    treeview.heading('today_date', text='Entry Date')

    # Set column widths
    font = ("Arial", 16)

    treeview.column('ID', width=50,)
    treeview.column('UID', width=100)
    treeview.column('Entry_time', width=150)
    treeview.column('Exit_time', width=150)
    treeview.column('today_date', width=100)
    button = ttk.Button(tab2, text="Get Data", command=print_date)
    button3 = ttk.Button(tab2, text="Export to Excel", command=on_button_click)
    button.pack(pady=20)
    button3.place(relx=1, rely=1, anchor=tk.SE, x=-10, y=-40)
    export_button = ttk.Button(tab2, text="Export to Firebase", command=on_firebase_button_click)
    export_button.place(relx=1, rely=1, anchor=tk.SE, x=-10, y=-10)
    treeview.pack()
    result_label = tk.Label(tab2, text="",width=30,height=2)
    result_label.pack()

splash.after(2000, main_func)
# start the main event loop
mainloop()