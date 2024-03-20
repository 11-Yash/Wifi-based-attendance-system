import tkinter as tk
from tkinter import messagebox
def save_network_address():
    network_address = entry.get()
    try:
        with open('network_address.txt', 'w') as f:
            f.write(network_address)
        messagebox.showinfo("Success", "Network address saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save network address: {e}")

def load_network_address():
    try:
        with open('network_address.txt', 'r') as f:
            network_address = f.read()
            entry.insert(0, network_address)
    except FileNotFoundError:
        pass

root = tk.Tk()
root.title("Change Network Address")

root.geometry("400x300")

label = tk.Label(root, text="Enter Network Address:")
label.pack()

entry = tk.Entry(root, width=30)
entry.pack()

load_network_address()

button = tk.Button(root, text="Save", command=save_network_address)
button.pack()

root.mainloop()