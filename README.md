Chance Music Dice Roller 🎶🎲
=============================

The Chance Music Dice Roller is a simple desktop application built with Python's Tkinter that generates musical parameters (duration, pitch, chord, and augmentation) by simulating the roll of various "dice." This tool is inspired by **aleatoric music**, a compositional approach where some elements of music are left to chance or determined by unpredictable procedures. It serves as a creative prompt generator for composers, musicians, or anyone exploring experimental music.

Features ✨
----------

*   **Randomized Musical Parameters:** Get instant suggestions for core musical elements:
    
    *   **Note Durations:** Rolls various standard musical note values (e.g., breve, semibreve, crotchet, quaver).
        
    *   **Pitches (12-TET or 24-TET):** Generates pitches within 12-Tone Equal Temperament (standard chromatic scale) or 24-Tone Equal Temperament, which includes microtonal pitches represented with special Unicode symbols (half-sharps ⵐ, sesquisharps ⩨, etc.).
        
    *   **Chord Qualities:** Rolls a variety of chord types (e.g., Major, Minor, Diminished, Augmented, sus2, sus4, various 7ths, power chord, or "none").
        
    *   **Augmentation:** Determines if the chosen note duration is "Dotted" or "No Dot."
        
*   **Visual Dice Interface:** A clean and intuitive graphical user interface (GUI) with distinct "dice" for each musical parameter, designed for clarity and ease of use.
    
*   **Microtonal Support:** Leverages specific Unicode fonts to accurately display 24-TET pitches, allowing for exploration beyond standard Western tuning systems.
    
*   **Help & Documentation:** A dedicated "Help" button that opens the project's GitHub repository in your web browser for detailed documentation and background information.
    
*   **Custom Application Icon:** A custom favicon appears in the window title and taskbar/dock when the application is running, providing a unique identity.
    
*   **Fullscreen Windowed Mode:** The application launches maximized to fill your screen, providing an immersive experience without hiding the taskbar.
    

Installation 🚀
---------------


### Downloading a Standalone Executable (for Windows Users) 📦

For Windows users, there is standalone executable for download.

1.  Navigate to the repository's [Releases](https://github.com/ravis-world/Chance-Music-Dice-Python/releases) page.
    
2.  You should see a file ready for download. Go ahead and download the file.
    
3.  You are done.

### Steps for Running from Source (Recommended for Development and Cross-Platform Users)

To run this application, you'll need Python 3 and the Pillow library.

#### Prerequisites

*   **Python 3.x:** Download and install from [python.org](https://www.python.org/downloads/).
    
*   **Pillow Library:** Used for image handling.

1.  ```bash
    git clone https://github.com/Ravis-World/Chance-Music-Dice.git
    cd Chance-Music-Dice
    ```
    
2.  ```bash
    cd src
    ```
    
3.  Activate the virtual environment; use the command that works with your operating system:
    ```bash
    source venv/bin/activate
    .\venv\Scripts\activate
    ```
        
4.  ```bash
    pip install pillow
    ```
    
5.  **Ensure Fonts and Assets are Present:** The application relies on specific font files (Noto Sans, Noto Sans Tifinagh, Noto Sans Math) and image assets for musical durations. Ensure the assets/fonts/ and assets/images/ directories within your project contain the necessary files.
    
    *   **Fonts:** While the app points to paths, Tkinter primarily relies on these fonts being installed on your **operating system**. It's recommended to install the Noto Sans font family system-wide for the best visual experience, especially for the special characters in 24-TET.
        
    *   **Favicon:** Make sure your app_icon.ico file is in assets/images/ for the application icon to display correctly.
    

How to Use 🎮
--------

1.  **Roll the Dice:**Click the "Roll Dice" button to generate new musical parameters. The results will be displayed on the four dice.
    
2.  **Select TET:**Use the "TET:" radio buttons in the top-right corner to switch between 12-TET (standard chromatic scale) and 24-TET (microtonal pitches).
    
3.  **Get Help:**Click the "Help" button in the top-right corner to open the project's GitHub documentation in your web browser.
    

Contributing 🤝
---------------

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/ravis-world/Chance-Music-Dice-Python).

Credits
-------

### Images

**Semibreve, Minim, Crotchet, Quaver, Semiquaver, Demisemiquaver:** By Christophe Dang Ngoc Chan ( [cdang](//commons.wikimedia.org/wiki/User:Cdang "User:Cdang") ) - self-made, with Inkscape, from LilyPond model, [CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/ "Creative Commons Attribution-Share Alike 3.0") .  
Semibreve: [Link](https://commons.wikimedia.org/w/index.php?curid=1334978)  
Minim: [Link](https://commons.wikimedia.org/w/index.php?curid=1334961)  
Crotchet: [Link](https://commons.wikimedia.org/w/index.php?curid=1334974)  
Quaver: [Link](https://commons.wikimedia.org/w/index.php?curid=1334967)  
Semiquaver: [Link](https://commons.wikimedia.org/w/index.php?curid=1334970)  
Demisemiquaver: [Link](https://commons.wikimedia.org/w/index.php?curid=1334983)

  

**Breve and Hemidemisemiquaver**: From Copyleft Website Liam Pitcher [Link](https://www.liampitcher.com/classical-music-blog/note-values)