import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk
import dice # Import our dice logic from dice.py
import webbrowser # Import the webbrowser module for opening URLs
import os # Import os module for path manipulation
import sys # Import sys module to check for PyInstaller environment

# Removed: import requests
# Removed: from packaging.version import parse as parse_version

class ChanceMusicDiceApp:
    """
    A Tkinter application for a chance music dice roller.
    """
    def __init__(self, master, app_version): # app_version is now just for display
        """
        Initializes the main application window and its components.
        """
        self.master = master
        self.local_app_version = app_version # Store the local version for display
        self.GITHUB_RELEASES_URL = "https://github.com/Ravis-World/Chance-Music-Dice-Python/releases" # User-friendly releases page URL

        master.title("Chance Music Dice Roller")
        master.state('zoomed')
        master.resizable(False, False)
        master.config(bg="#E6EBF3")

        # --- Favicon Integration (PyInstaller-aware pathing) ---
        try:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(os.path.dirname(__file__))
            
            icon_path = os.path.join(base_path, "assets", "images", "app_icon.ico")
            
            master.iconbitmap(icon_path)
            
        except tk.TclError as e:
            print(f"Warning: Could not load icon file from {icon_path}. Error: {e}")
        except FileNotFoundError:
            print(f"Error: Icon file not found at {icon_path}. Check your --add-data path in PyInstaller.")
        except Exception as e:
            print(f"An unexpected error occurred while loading icon: {e}")
        # --------------------------------------------------------

        # --- Font Configuration ---
        self.title_font_size = 48
        self.button_font_size = 18
        self.instruction_font_size = 14
        self.die_label_font_size = 20
        self.die_value_font_size = 40

        self.title_font = tkFont.Font(family="Noto Sans", size=self.title_font_size, weight="bold")
        self.button_font = tkFont.Font(family="Noto Sans", size=self.button_font_size, weight="bold")
        self.instruction_font = tkFont.Font(family="Noto Sans", size=self.instruction_font_size)
        self.die_label_font = tkFont.Font(family="Noto Sans", size=self.die_label_font_size, weight="bold")
        self.die_value_font = tkFont.Font(family="Noto Sans", size=self.die_value_font_size, weight="bold")

        self.tifinagh_font = tkFont.Font(family="Noto Sans Tifinagh", size=self.die_value_font_size, weight="bold")
        self.math_font = tkFont.Font(family="Noto Sans Math", size=self.die_value_font_size, weight="bold")

        self.noto_sans_font_path = f"{dice.FONTS_DIR}/NotoSans-VariableFont_wdth,wght.ttf"
        self.noto_tifinagh_font_path = f"{dice.FONTS_DIR}/NotoSansTifinagh-Regular.ttf"
        self.noto_math_font_path = f"{dice.FONTS_DIR}/NotoSansMath-Regular.ttf"

        try:
            tkFont.nametofont("TkDefaultFont").configure(family="Noto Sans", size=12)
            tkFont.nametofont("TkTextFont").configure(family="Noto Sans", size=12)
            tkFont.nametofont("TkFixedFont").configure(family="Noto Sans", size=12)
            tkFont.families()
        except Exception as e:
            print(f"Error configuring default fonts: {e}")
            messagebox.showerror("Font Error", "Could not configure default Noto Sans font. Please ensure it's installed.")

        # --- Image Cache ---
        self.duration_images_cache = {}

        # --- UI Layout ---
        # 1. Top Bar Frame: Holds title and control buttons
        self.top_bar_frame = tk.Frame(master, bg="#E6EBF3", padx=20, pady=25) 
        self.top_bar_frame.pack(side=tk.TOP, fill=tk.X)

        # Title Label (now inside top_bar_frame)
        self.title_label = tk.Label(self.top_bar_frame, text="Chance Music Dice Roller", font=self.title_font, bg="#E6EBF3", fg="#334B68")
        self.title_label.pack(side=tk.LEFT, padx=0, pady=0)

        # Control Panel Frame (now inside top_bar_frame)
        self.control_panel_frame = tk.Frame(self.top_bar_frame, bg="#E6EBF3", padx=15, pady=0, relief=tk.FLAT)
        self.control_panel_frame.pack(side=tk.RIGHT)

        # Display current version
        self.version_label = tk.Label(self.control_panel_frame, text=f"Version: {self.local_app_version}", font=self.instruction_font, bg="#E6EBF3", fg="#555555")
        self.version_label.pack(side=tk.LEFT, padx=5)

        self.tet_choice = tk.IntVar(value=12)
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
        
        # Removed: Check for Updates button
        # self.update_button = tk.Button(self.control_panel_frame, text="Check for Updates", command=self.check_for_updates, font=self.instruction_font, relief=tk.RAISED, bd=2,
        #                                bg="#607D8B", fg="white", activebackground="#455A64", activeforeground="white",
        #                                cursor="hand2", padx=10, pady=5)
        # self.update_button.pack(side=tk.RIGHT, padx=10)

        # "Go to Releases" button (now serves the purpose of directing to updates)
        self.go_to_releases_button = tk.Button(self.control_panel_frame, text="Go to Releases", command=self.go_to_releases, font=self.instruction_font, relief=tk.RAISED, bd=2,
                                               bg="#4CAF50", fg="white", activebackground="#388E3C", activeforeground="white",
                                               cursor="hand2", padx=10, pady=5)
        self.go_to_releases_button.pack(side=tk.RIGHT, padx=5)


        # 2. Main Content Frame: Holds the dice canvas
        self.main_content_frame = tk.Frame(master, bg="#E6EBF3", padx=20, pady=20)
        self.main_content_frame.pack(expand=True, fill=tk.BOTH) # Expands to fill remaining space

        # Canvas to draw all dice placeholders and results
        self.dice_canvas = tk.Canvas(self.main_content_frame, bg="#E6EBF3", highlightthickness=0)
        self.dice_canvas.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)

        # 3. Bottom Controls Frame: Holds the Roll Dice button and instruction message
        self.bottom_controls_frame = tk.Frame(master, bg="#E6EBF3", pady=10)
        self.bottom_controls_frame.pack(side=tk.BOTTOM, fill=tk.X) # Pack to the bottom

        self.roll_button = tk.Button(self.bottom_controls_frame, text="Roll Dice", command=self.roll_dice, font=self.button_font,
                                     relief=tk.RAISED, bd=3, bg="#5A9BD6", fg="white", activebackground="#4A8BC1", activeforeground="white",
                                     cursor="hand2", padx=25, pady=10)
        self.roll_button.pack(pady=10)

        self.instruction_label = tk.Label(self.bottom_controls_frame, text="Click \"Roll Dice\" to generate some music!",
                                          font=self.instruction_font, bg="#F0F3F7", fg="#555555",
                                          relief=tk.FLAT, bd=1, padx=20, pady=10)
        self.instruction_label.pack(pady=5)

        # --- Internal State for Dice Results (for redraw on resize) ---
        self._last_rolled_duration = None
        self._last_rolled_augmentation = None
        self._last_rolled_chord = None
        self._last_rolled_pitch = "C"

        self.master.bind("<Configure>", self.on_resize)
        
        self.master.after(100, self.draw_dice_placeholders)
        self.master.after(200, self.roll_dice)

    def draw_dice_placeholders(self):
        canvas = self.dice_canvas
        canvas.delete("all")

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0:
            print("Warning: Canvas has invalid dimensions for drawing placeholders.")
            return

        num_dice = 4
        padding_x = 50
        padding_y = 50
        spacing_x = 40

        die_width = (canvas_width - 2 * padding_x - (num_dice - 1) * spacing_x) / num_dice
        die_height = die_width * 1.2

        total_content_width = (die_width * num_dice) + ((num_dice - 1) * spacing_x)

        start_x = (canvas_width - total_content_width) / 2
        start_y = (canvas_height - die_height) / 2

        self.die_coords = []

        current_x = start_x
        for i in range(num_dice):
            x1 = current_x
            x2 = x1 + die_width
            y1 = start_y
            y2 = y1 + die_height
            
            self.create_rounded_rectangle(canvas, x1 + 5, y1 + 5, x2 + 5, y2 + 5,
                                          radius=15, fill="#D0D3DB", outline="")

            self.create_rounded_rectangle(canvas, x1, y1, x2, y2,
                                          radius=15, fill="#FFFFFF", outline="#A0A8B4", width=2)
            self.die_coords.append({"type": "square", "bbox": (x1, y1, x2, y2)})
            
            current_x += die_width + spacing_x # die_w should be die_width here

        self.redraw_dice_content()


    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
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
        tet_choice = self.tet_choice.get()
        results = dice.roll_all_dice(tet_choice)

        self._last_rolled_duration = results["duration"]
        self._last_rolled_pitch = results["pitch"]
        self._last_rolled_chord = results["chord"]
        self._last_rolled_augmentation = results["augmentation"]

        self.redraw_dice_content()

    def redraw_dice_content(self):
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
            image_target_height = (die_bbox[3] - die_bbox[1]) * 0.8 # Corrected to 0.8

            image_filename = dice.get_duration_image_path(self._last_rolled_duration).split('/')[-1]
            image_path = self.get_asset_path(os.path.join("images", image_filename))

            if image_path:
                tk_image = self.load_and_resize_image(image_path, image_target_width, image_target_height)
                if tk_image:
                    canvas.create_image(die_center_x, die_center_y, image=tk_image, tags="content_tag") # Centered
                    self.duration_images_cache[("current_display", self._last_rolled_duration)] = tk_image

            canvas.create_text(die_center_x, die_bbox[1] + 20,
                               text="Duration:",
                               font=self.die_label_font, fill="#555555", tags="content_tag")


        # Pitch Die (Index 1)
        if self._last_rolled_pitch:
            self.update_pitch_display_on_canvas(self._last_rolled_pitch, self.die_coords[1])


        # Chord Die (Index 2)
        if self._last_rolled_chord:
            die_bbox = self.die_coords[2]["bbox"]
            die_center_x = (die_bbox[0] + die_bbox[2]) / 2
            die_center_y = (die_bbox[1] + die_bbox[3]) / 2
            canvas.create_text(die_center_x, die_center_y + 10,
                               text=self._last_rolled_chord,
                               font=self.die_value_font, fill="#333333", tags="content_tag")
            canvas.create_text(die_center_x, die_bbox[1] + 20,
                               text="Chord:",
                               font=self.die_label_font, fill="#555555", tags="content_tag")

        # Augmentation Die (Index 3)
        if self._last_rolled_augmentation:
            die_bbox = self.die_coords[3]["bbox"]
            die_center_x = (die_bbox[0] + die_bbox[2]) / 2
            die_center_y = (die_bbox[1] + die_bbox[3]) / 2
            canvas.create_text(die_center_x, die_center_y + 10,
                               text=self._last_rolled_augmentation,
                               font=self.die_value_font, fill="#333333", tags="content_tag")
            canvas.create_text(die_center_x, die_bbox[1] + 20,
                               text="Augmentation:",
                               font=self.die_label_font, fill="#555555", tags="content_tag")


    def update_pitch_display_on_canvas(self, pitch_result, die_coords):
        canvas = self.dice_canvas
        canvas.delete("pitch_content_tag") 

        die_bbox = die_coords["bbox"]
        die_center_x = (die_bbox[0] + die_bbox[2]) / 2
        die_center_y = (die_bbox[1] + die_bbox[3]) / 2

        canvas.create_text(die_center_x, die_bbox[1] + 20,
                           text="Pitch:",
                           font=self.die_label_font, fill="#555555", tags="pitch_content_tag")

        total_text_width = 0
        temp_segments = []
        
        segment_start_index = 0
        for i, char in enumerate(pitch_result):
            if char in ["ⵐ", "ȸ", "⩨", "𝄫", "#", "b", "/"]:
                if segment_start_index < i:
                    temp_segments.append((pitch_result[segment_start_index:i], self.die_value_font))
                temp_segments.append((char, self.get_font_for_char(char)))
                segment_start_index = i + 1
        
        if segment_start_index < len(pitch_result):
            temp_segments.append((pitch_result[segment_start_index:], self.die_value_font))

        for text, font_obj in temp_segments:
            total_text_width += font_obj.measure(text)

        current_x = die_center_x - (total_text_width / 2)
        text_y = die_center_y + 10

        for text, font_obj in temp_segments:
            canvas.create_text(current_x, text_y, text=text, anchor="w", font=font_obj, fill="#333333", tags="pitch_content_tag")
            current_x += font_obj.measure(text)

    def get_font_for_char(self, char):
        if char == "ⵐ": return self.tifinagh_font
        if char == "⩨": return self.math_font
        return self.die_value_font 

    def show_help(self):
        documentation_url = "https://github.com/Ravis-World/Chance-Music-Dice-Python/blob/master/README.md"
        webbrowser.open_new(documentation_url)

    def on_resize(self, event):
        _ = event
        self.master.update_idletasks()
        self.draw_dice_placeholders()

    def load_and_resize_image(self, image_path, target_width, target_height):
        if target_width <= 0 or target_height <= 0:
            return None

        cache_key = (image_path, target_width, target_height)
        if cache_key in self.duration_images_cache:
            return self.duration_images_cache[cache_key]

        try:
            pil_image = Image.open(image_path)
            original_width, original_height = pil_image.size

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
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root_dir = os.path.dirname(current_script_dir) # Go up from src to project root
            return os.path.join(project_root_dir, "assets", relative_path)

    def go_to_releases(self):
        """
        Opens the GitHub releases page in the user's web browser.
        """
        webbrowser.open_new(self.GITHUB_RELEASES_URL)

    # Removed: check_for_updates method
    # def check_for_updates(self):
    #     """
    #     Checks for a newer version of the application on GitHub Releases.
    #     Notifies the user if an update is available and offers to go to releases page.
    #     """
    #     try:
    #         response = requests.get(self.GITHUB_REPO_API, timeout=5)
    #         response.raise_for_status()
            
    #         latest_release = response.json()
    #         latest_version_str = latest_release['tag_name']

    #         if latest_version_str.startswith('v'):
    #             latest_version_str = latest_version_str[1:]

    #         current_version = parse_version(self.local_app_version)
    #         remote_version = parse_version(latest_version_str)

    #         if remote_version > current_version:
    #             messagebox.showinfo(
    #                 "Update Available!",
    #                 f"A new version ({latest_version_str}) is available!\n"
    #                 f"You are currently running version {self.local_app_version}.\n\n"
    #                 f"Please visit the releases page to download the latest version:\n"
    #                 f"{self.GITHUB_RELEASES_URL}"
    #             )
    #         else:
    #             messagebox.showinfo(
    #                 "No Updates",
    #                 f"You are running the latest version ({self.local_app_version})."
    #             )

    #     except requests.exceptions.Timeout:
    #         messagebox.showerror("Network Error", "Could not check for updates: Request timed out. Check your internet connection.")
    #     except requests.exceptions.RequestException as e:
    #         messagebox.showerror("Network Error", f"Could not check for updates: {e}\nCheck your internet connection or GitHub API access.")
    #     except KeyError:
    #         messagebox.showerror("Update Error", "Could not parse GitHub release data. The API response format might have changed.")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"An unexpected error occurred during update check: {e}")
