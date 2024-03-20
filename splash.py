# import tkinter as tk
# from tkinter import ttk
# import time

# def close_splash_screen():
#     splash_screen.destroy()
#     root.deiconify()

# def show_main_window():
#     global root
#     root = tk.Tk()
#     root.title("Main Window")
#     # Add your main window widgets here
#     label = ttk.Label(root, text="Welcome to the Main Window!")
#     label.pack(padx=20, pady=20)
#     root.mainloop()

# # Create splash screen
# splash_screen = tk.Toplevel()
# splash_screen.overrideredirect(True)  # Remove window decorations
# splash_screen.geometry("600x400")  # Set window size
# # Add your splash screen content here, e.g., an image
# splash_label = ttk.Label(splash_screen, text="Splash Screen")
# splash_label.pack(expand=True)

# # Close splash screen after 2 seconds (2000 milliseconds)
# splash_screen.after(2000, close_splash_screen)

# # Hide the root window until splash screen is closed
# root = None
# show_main_window()

import tkinter as tk#
import time#
#{
class SplashScreen(tk.Toplevel):
  def __init__(self, app, delay=3, image_path="splash_bg.png"):    #path
    super().__init__(app)
    # Optional: Set window size and position
    self.geometry("300x200+500+200")
    self.overrideredirect(True)

    # Add your splash screen content here (label, image, etc.)
    label = tk.Label(self, text="Your App Name", font=("Arial", 24))
    label.pack()

    # Schedule the main window to be shown after a delay
    self.after(delay * 1000, self.destroy_splash)
  
  def destroy_splash(self):
    self.destroy()
    # app.deiconify() 
#}
class MainApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Main Window")
    self.withdraw()  # Hide the main window initially

    # Create the splash screen and pass the main window as an argument
    splash = SplashScreen(self)
    
    # Your main window content goes here (buttons, labels, etc.)
    label = tk.Label(self, text="Welcome to the Home Page!")
    label.pack()

if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
