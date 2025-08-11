import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk
import dice # Import our dice logic from dice.py
import webbrowser # Import the webbrowser module for opening URLs
import os # Import os module for path manipulation
import sys # Import sys module to check for PyInstaller environment

class ChanceMusicDiceApp:
    """
    A Tkinter application for a chance music dice roller.
    """
    def __init__(self, master):
        """
        Initializes the main application window and its components.
        """
        self.master = master
        master.title("Chance Music Dice Roller")
        master.state('zoomed') # Set the window to start in a maximized (fullscreen windowed) state
        master.resizable(True, True) # Allow resizing
        master.config(bg="#E6EBF3") # Soft blue-gray background

        # --- Favicon Integration (PyInstaller-aware pathing) ---
        try:
            # Determine the base path for assets, considering PyInstaller
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                # Running as a PyInstaller bundle (e.g., .exe)
                base_path = sys._MEIPASS
            else:
                # Running from source (e.g., python main.py)
                base_path = os.path.abspath(os.path.dirname(__file__))
            
            # Construct the absolute path to the icon file
            # Assumes assets/images is relative to the directory of gui.py or _MEIPASS
            icon_path = os.path.join(base_path, "assets", "images", "app_icon.ico")
            
            # For debugging: print the resolved path
            print(f"Attempting to load icon from: {icon_path}")

            master.iconbitmap(icon_path)
            
        except tk.TclError as e:
            print(f"Warning: Could not load icon file from {icon_path}. Ensure it's a valid .ico file and path is correct. Error: {e}")
        except FileNotFoundError:
            print(f"Error: Icon file not found at {icon_path}. Check your --add-data path in PyInstaller.")
        except Exception as e:
            print(f"An unexpected error occurred while loading icon: {e}")
        # --------------------------------------------------------

        # --- Font Configuration ---
        self.title_font_size = 48
        self.button_font_size = 18
        self.instruction_font_size = 14
        self.die_label_font_size = 20 # Font for "Duration:", "Chord:", etc.
        self.die_value_font_size = 40 # Font for the rolled value

        self.title_font = tkFont.Font(family="Noto Sans", size=self.title_font_size, weight="bold")
        self.button_font = tkFont.Font(family="Noto Sans", size=self.button_font_size, weight="bold")
        self.instruction_font = tkFont.Font(family="Noto Sans", size=self.instruction_font_size)
        self.die_label_font = tkFont.Font(family="Noto Sans", size=self.die_label_font_size, weight="bold")
        self.die_value_font = tkFont.Font(family="Noto Sans", size=self.die_value_font_size, weight="bold")

        self.tifinagh_font = tkFont.Font(family="Noto Sans Tifinagh", size=self.die_value_font_size, weight="bold")
        self.math_font = tkFont.Font(family="Noto Sans Math", size=self.die_value_font_size, weight="bold")

        # Custom font paths (used for reference, Tkinter relies on system fonts)
        # These paths are for when running from source, not for bundled app
        self.noto_sans_font_path = f"{dice.FONTS_DIR}/NotoSans-VariableFont_wdth,wght.ttf"
        self.noto_tifinagh_font_path = f"{dice.FONTS_DIR}/NotoSansTifinagh-Regular.ttf"
        self.noto_math_font_path = f"{dice.FONTS_DIR}/NotoSansMath-Regular.ttf"

        try:
            # Attempt to configure default Tkinter fonts - more for general text
            tkFont.nametofont("TkDefaultFont").configure(family="Noto Sans", size=12)
            tkFont.nametofont("TkTextFont").configure(family="Noto Sans", size=12)
            tkFont.nametofont("TkFixedFont").configure(family="Noto Sans", size=12)
            tkFont.families() # Force Tkinter to scan for available fonts
        except Exception as e:
            print(f"Error configuring default fonts: {e}")
            messagebox.showerror("Font Error", "Could not configure default Noto Sans font. Please ensure it's installed.")

        # --- Image Cache ---
        self.duration_images_cache = {}

        # --- UI Layout ---
        # Main content frame for the title, dice, and buttons
        self.main_content_frame = tk.Frame(master, bg="#E6EBF3", padx=20, pady=20)
        self.main_content_frame.pack(expand=True, fill=tk.BOTH)

        # Title Label
        self.title_label = tk.Label(self.main_content_frame, text="Chance Music Dice Roller", font=self.title_font, bg="#E6EBF3", fg="#334B68") # Dark blue text
        self.title_label.pack(pady=20)

        # Canvas to draw all dice placeholders and results
        self.dice_canvas = tk.Canvas(self.main_content_frame, bg="#E6EBF3", highlightthickness=0)
        self.dice_canvas.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)

        # Frame for the Roll Dice button and instruction message
        self.bottom_controls_frame = tk.Frame(self.main_content_frame, bg="#E6EBF3")
        self.bottom_controls_frame.pack(pady=10)

        # Roll Dice Button
        self.roll_button = tk.Button(self.bottom_controls_frame, text="Roll Dice", command=self.roll_dice, font=self.button_font,
                                     relief=tk.RAISED, bd=3, bg="#5A9BD6", fg="white", activebackground="#4A8BC1", activeforeground="white",
                                     cursor="hand2", padx=25, pady=10)
        self.roll_button.pack(pady=10)

        # Instruction Message
        self.instruction_label = tk.Label(self.bottom_controls_frame, text="Click \"Roll Dice\" to generate some music!",
                                          font=self.instruction_font, bg="#F0F3F7", fg="#555555",
                                          relief=tk.FLAT, bd=1, padx=20, pady=10)
        self.instruction_label.pack(pady=5)

        # --- Internal State for Dice Results (for redraw on resize) ---
        self._last_rolled_duration = None
        self._last_rolled_augmentation = None
        self._last_rolled_chord = None
        self._last_rolled_pitch = "C" # Default pitch for initial draw

        # --- TET Choice (Radio Buttons) and Help Button - Reintegrated ---
        # Create a frame for these controls to be placed above the main content or elsewhere
        self.control_panel_frame = tk.Frame(master, bg="#E6EBF3", padx=15, pady=10, relief=tk.FLAT)

        self.tet_choice = tk.IntVar(value=12) # Default to 12-TET
        tet_label = tk.Label(self.control_panel_frame, text="TET:", font=self.instruction_font, bg="#E6EBF3", fg="#263238")
        tet_label.pack(side=tk.LEFT, padx=5)

        self.tet_12_radio = tk.Radiobutton(self.control_panel_frame, text="12-TET", variable=self.tet_choice, value=12, font=self.instruction_font, bg="#E6EBF3", fg="#424242", selectcolor="#B0BEC5")
        self.tet_12_radio.pack(side=tk.LEFT, padx=2)

        self.tet_24_radio = tk.Radiobutton(self.control_panel_frame, text="24-TET", variable=self.tet_choice, value=24, font=self.instruction_font, bg="#E6EBF3", fg="#424242", selectcolor="#B0BEC5")
        self.tet_24_radio.pack(side=tk.LEFT, padx=2)

        self.help_button = tk.Button(self.control_panel_frame, text="Help", command=self.show_help, font=self.instruction_font, relief=tk.RAISED, bd=2,
                                     bg="#8BC34A", fg="white", activebackground="#7CB342", activeforeground="white",
                                     cursor="question_arrow", padx=10, pady=5)
        self.help_button.pack(side=tk.RIGHT, padx=5)
        
        # Position the control panel frame absolutely for top-right corner placement
        self.control_panel_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-15, y=15)


        # Bind resize event to redraw all dice elements
        self.master.bind("<Configure>", self.on_resize)
        
        # Initial draw of dice placeholders and a first roll
        self.master.after(100, self.draw_dice_placeholders) # Draw after mainloop starts to get proper canvas size
        self.master.after(200, self.roll_dice) # Then perform an initial roll

    def draw_dice_placeholders(self):
        """
        Draws the four dice placeholders (rounded rectangles) on the canvas.
        All dice will now be the same size.
        """
        canvas = self.dice_canvas
        canvas.delete("all") # Clear canvas before redrawing

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0:
            print("Warning: Canvas has invalid dimensions for drawing placeholders.")
            return

        # Define sizes and spacing
        num_dice = 4
        padding_x = 50 # Horizontal padding from canvas edge
        padding_y = 50 # Vertical padding from canvas edge
        spacing_x = 40 # Space between dice

        # All dice will now be the same size
        # Calculate a single die dimension based on fitting all 4 equally
        die_width = (canvas_width - 2 * padding_x - (num_dice - 1) * spacing_x) / num_dice
        die_height = die_width * 1.2 # Maintain the slightly taller aspect ratio for text/image

        # Calculate total width required by the equally sized dice
        total_content_width = (die_width * num_dice) + ((num_dice - 1) * spacing_x)

        # Calculate starting X position to center the entire group of dice
        start_x = (canvas_width - total_content_width) / 2
        start_y = (canvas_height - die_height) / 2 # Vertically center them

        self.die_coords = [] # Store coordinates for each die to use for drawing results

        current_x = start_x
        # Draw 4 dice placeholders (all now square)
        for i in range(num_dice):
            x1 = current_x
            x2 = x1 + die_width
            y1 = start_y
            y2 = y1 + die_height
            
            # Draw a subtle shadow (offset rounded rectangle)
            self.create_rounded_rectangle(canvas, x1 + 5, y1 + 5, x2 + 5, y2 + 5,
                                          radius=15, fill="#D0D3DB", outline="")

            # Draw the main rounded rectangle placeholder
            self.create_rounded_rectangle(canvas, x1, y1, x2, y2,
                                          radius=15, fill="#FFFFFF", outline="#A0A8B4", width=2)
            self.die_coords.append({"type": "square", "bbox": (x1, y1, x2, y2)})
            
            current_x += die_width + spacing_x # Advance X for the next die
        
        self.redraw_dice_content()


    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """
        Draws a rounded rectangle on a Tkinter canvas.
        Based on a common Tkinter rounded rectangle drawing method.
        """
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2-radius,
                  x1, y1+radius]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def roll_dice(self):
        """
        Rolls all dice and updates the display with the new results.
        """
        tet_choice = self.tet_choice.get() # Now correctly uses the radio button selection
        results = dice.roll_all_dice(tet_choice)

        self._last_rolled_duration = results["duration"]
        self._last_rolled_pitch = results["pitch"] # Swapped
        self._last_rolled_chord = results["chord"]
        self._last_rolled_augmentation = results["augmentation"] # Swapped

        self.redraw_dice_content()

    def redraw_dice_content(self):
        """
        Redraws the content (image/text) inside the dice placeholders.
        Called after a roll or a resize.
        """
        canvas = self.dice_canvas
        canvas.delete("content_tag") 

        if not self.die_coords:
            return
        
        # Order of drawing content MUST match the order of die_coords: Duration, Pitch, Chord, Augmentation

        # Duration Die (Index 0)
        if self._last_rolled_duration:
            die_bbox = self.die_coords[0]["bbox"]
            die_center_x = (die_bbox[0] + die_bbox[2]) / 2
            die_center_y = (die_bbox[1] + die_bbox[3]) / 2

            image_target_width = (die_bbox[2] - die_bbox[0]) * 0.8
            image_target_height = (die_bbox[3] - die_bbox[1]) * 0.8 # Adjusted height to fill more space

            # Fix: Use os.path.join for image_path to handle bundled assets
            image_filename = dice.get_duration_image_path(self._last_rolled_duration).split('/')[-1] # Get just the filename
            image_path = self.get_asset_path(os.path.join("images", image_filename)) # Construct path for bundled app

            if image_path: # Check if image_path is not None or empty
                tk_image = self.load_and_resize_image(image_path, image_target_width, image_target_height)
                if tk_image:
                    # Position image slightly higher to be centered in the available space
                    canvas.create_image(die_center_x, die_center_y, image=tk_image, tags="content_tag")
                    self.duration_images_cache[("current_display", self._last_rolled_duration)] = tk_image

            canvas.create_text(die_center_x, die_bbox[1] + 20, # Vertically offset from top
                               text="Duration:",
                               font=self.die_label_font, fill="#555555", tags="content_tag")


        # Pitch Die (Index 1) - Now a square
        if self._last_rolled_pitch:
            self.update_pitch_display_on_canvas(self._last_rolled_pitch, self.die_coords[1])


        # Chord Die (Index 2)
        if self._last_rolled_chord:
            die_bbox = self.die_coords[2]["bbox"]
            die_center_x = (die_bbox[0] + die_bbox[2]) / 2
            die_center_y = (die_bbox[1] + die_bbox[3]) / 2
            canvas.create_text(die_center_x, die_center_y + 10, # Vertically centered value
                               text=self._last_rolled_chord,
                               font=self.die_value_font, fill="#333333", tags="content_tag")
            canvas.create_text(die_center_x, die_bbox[1] + 20, # Vertically offset from top
                               text="Chord:",
                               font=self.die_label_font, fill="#555555", tags="content_tag")

        # Augmentation Die (Index 3) - Now a square
        if self._last_rolled_augmentation:
            die_bbox = self.die_coords[3]["bbox"]
            die_center_x = (die_bbox[0] + die_bbox[2]) / 2
            die_center_y = (die_bbox[1] + die_bbox[3]) / 2
            canvas.create_text(die_center_x, die_center_y + 10, # Vertically centered value
                               text=self._last_rolled_augmentation,
                               font=self.die_value_font, fill="#333333", tags="content_tag")
            canvas.create_text(die_center_x, die_bbox[1] + 20, # Vertically offset from top
                               text="Augmentation:",
                               font=self.die_label_font, fill="#555555", tags="content_tag")


    def update_pitch_display_on_canvas(self, pitch_result, die_coords):
        """
        Updates the pitch display on the main canvas within its specific die area.
        Handles special characters without rotation, and centers text.
        """
        canvas = self.dice_canvas
        canvas.delete("pitch_content_tag") 

        die_bbox = die_coords["bbox"]
        die_center_x = (die_bbox[0] + die_bbox[2]) / 2
        die_center_y = (die_bbox[1] + die_bbox[3]) / 2

        # Draw "Pitch:" label
        canvas.create_text(die_center_x, die_bbox[1] + 20, # Position "Pitch:" label at the top center of the die
                           text="Pitch:",
                           font=self.die_label_font, fill="#555555", tags="pitch_content_tag")

        # Calculate the total width of the pitch_result to center it
        total_text_width = 0
        temp_segments = []
        
        # Prepare segments for measurement
        segment_start_index = 0
        for i, char in enumerate(pitch_result):
            # Check if the character is one of our special symbols or a separator
            if char in ["ⵐ", "ȸ", "⩨", "𝄫", "#", "b", "/"]:
                # If there's accumulated text before this special character, add it as a segment
                if segment_start_index < i:
                    temp_segments.append((pitch_result[segment_start_index:i], self.die_value_font))
                # Add the special character as its own segment with its specific font
                temp_segments.append((char, self.get_font_for_char(char)))
                # Update the start index for the next segment
                segment_start_index = i + 1
        
        # Add any remaining text as the last segment
        if segment_start_index < len(pitch_result):
            temp_segments.append((pitch_result[segment_start_index:], self.die_value_font))

        # Calculate total width by measuring each segment with its correct font
        for text, font_obj in temp_segments:
            total_text_width += font_obj.measure(text)

        # Calculate starting x for horizontally centered text
        current_x = die_center_x - (total_text_width / 2)
        text_y = die_center_y + 10 # Vertically centered for value, adjusted slightly down from true center

        # Now draw the text segment by segment
        for text, font_obj in temp_segments:
            canvas.create_text(current_x, text_y, text=text, anchor="w", font=font_obj, fill="#333333", tags="pitch_content_tag")
            current_x += font_obj.measure(text)

    def get_font_for_char(self, char):
        """Helper to get the correct font for a specific character."""
        if char == "ⵐ": return self.tifinagh_font
        if char == "⩨": return self.math_font
        # Default for others like #, b, /, ȸ, 𝄫
        return self.die_value_font 

    def show_help(self):
        """
        Opens a web browser to the project's documentation.
        """
        documentation_url = "https://github.com/Ravis-World/Chance-Music-Dice/Chance%20Music%20Dice%20Documentation/index.html"
        webbrowser.open_new(documentation_url)

    def on_resize(self, event):
        """
        Handles window resize events to redraw placeholders and content.
        """
        _ = event # Acknowledge the 'event' argument to suppress Pylance warning
        self.master.update_idletasks() # Ensure dimensions are updated
        self.draw_dice_placeholders() # Redraw shapes based on new canvas size
        # redraw_dice_content() is called by draw_dice_placeholders()


    def load_and_resize_image(self, image_path, target_width, target_height):
        """
        Loads an image, resizes it to fit within target_width/height while maintaining aspect ratio,
        and returns a Tkinter PhotoImage object.
        Caches the image to prevent garbage collection.
        """
        if target_width <= 0 or target_height <= 0:
            return None

        # Create a more robust cache key that includes size
        cache_key = (image_path, target_width, target_height)
        if cache_key in self.duration_images_cache:
            return self.duration_images_cache[cache_key]

        try:
            pil_image = Image.open(image_path)
            original_width, original_height = pil_image.size

            # Calculate new dimensions to fit within target while maintaining aspect ratio
            ratio = min(target_width / max(1, original_width), target_height / max(1, original_height))
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            min_dim = 60
            if new_width < min_dim or new_height < min_dim:
                scale_up_ratio = max(min_dim / max(1, new_width), min_dim / max(1, new_height))
                new_width = int(new_width * scale_up_ratio)
                new_height = int(new_height * scale_up_ratio)

            new_width = min(new_width, target_width)
            new_height = min(new_height, target_height)
            
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.duration_images_cache[cache_key] = tk_image
            return tk_image
        except FileNotFoundError:
            print(f"Error: Image not found at {image_path}. Check your --add-data path in PyInstaller for assets.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while loading image {image_path}: {e}")
            return None

    def get_asset_path(self, relative_path):
        """
        Resolves the absolute path to an asset, handling both
        development environment and PyInstaller bundled environment.
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running as a PyInstaller bundle
            return os.path.join(sys._MEIPASS, "assets", relative_path)
        else:
            # Running from source (assuming assets is sibling to src)
            # Or if assets is directly in src, adjust '..' accordingly
            current_dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(os.path.dirname(current_dir), "assets", relative_path)