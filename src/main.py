import tkinter as tk
from gui import ChanceMusicDiceApp

# Define the current version of your application
__version__ = "1.0.01" # <--- Set your current app version here

def main():
    root = tk.Tk()
    # Pass the version number to the GUI app
    app = ChanceMusicDiceApp(root, __version__) 
    root.mainloop()

if __name__ == "__main__":
    main()