import tkinter as tk
from gui import ChanceMusicDiceApp

if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()

    # Instantiate the ChanceMusicDiceApp
    # This initializes the GUI elements and sets up the window
    app = ChanceMusicDiceApp(root)

    # Start the Tkinter event loop
    # This makes the window appear and handles all user interactions
    root.mainloop()
