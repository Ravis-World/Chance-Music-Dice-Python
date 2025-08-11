import random

# Base directory for our assets
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
FONTS_DIR = f"{ASSETS_DIR}/fonts"

# --- Dice Definitions ---

# Duration Die: Maps musical duration names to their image file paths
# You'll need to make sure these image files exist in your assets/images directory.
duration_die = {
    "breve": f"{IMAGES_DIR}/breve.png",
    "semibreve": f"{IMAGES_DIR}/semibreve.png",
    "minim": f"{IMAGES_DIR}/minim.png",
    "crotchet": f"{IMAGES_DIR}/crotchet.png",
    "quaver": f"{IMAGES_DIR}/quaver.png",
    "semiquaver": f"{IMAGES_DIR}/semiquaver.png",
    "demisemiquaver": f"{IMAGES_DIR}/demisemiquaver.png",
    "hemidemisemiquaver": f"{IMAGES_DIR}/hemidemisemiquaver.png",
}

# Augmentation Die: "Dot" or "No Dot"
augmentation_die = ["Dot", "No Dot"]

# Pitch Die: 12-TET or 24-TET
# For 24-TET, we now include both enharmonic spellings in the string,
# and use specific Unicode characters for half-sharps, half-flats,
# and the sesquisharp (⩨ from Noto Math).
pitch_die_12tet = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]

pitch_die_24tet = [
    "C",
    "Cⵐ/Dȸ",
    "C#/Db",
    "C⩨/Dd",
    "D",
    "Dⵐ/Eȸ",
    "D#/Eb",
    "D⩨/Ed",
    "E",
    "Eⵐ/Fd",
    "F",
    "Fⵐ/Gȸ",
    "F#/Gb",
    "F⩨/Gd",
    "G",
    "Gⵐ/Aȸ",
    "G#/Ab",
    "G⩨/Ad",
    "A",
    "Aⵐ/Bȸ",
    "A#/Bb",
    "A⩨/Bd",
    "B",
    "Bⵐ/Cd"
]

# Chord Die: This is a placeholder for now.
# We'll need to define the values based on your specific rules.
# For example, it could contain chord types like "Major", "Minor", "Diminished", etc.
chord_die = [
    'maj',
    'min',
    'dim',
    'aug',
    'sus2',
    'sus4',
    'maj7',
    'min7',
    '7',
    'dim7',
    'aug7',
    'power',
    'none',
    'none',
    'none',
    'none',
    'none',
    'none',
    'none',
    'none',
    'none',
    'none',
    'none',
    'none'
]

# --- Rolling Functions ---

def roll_die(die_options):
    """
    Takes a dictionary or list and returns a random key or item.
    """
    if isinstance(die_options, dict):
        # If it's a dictionary, we get its keys as a list and pick one.
        return random.choice(list(die_options.keys()))
    else:
        # If it's not a dictionary (it should be a list in our current design),
        # we pick directly from it.
        return random.choice(die_options)

def roll_all_dice(tet_choice):
    """
    Rolls all the dice and returns a dictionary of the results.
    `tet_choice` should be either 12 or 24.
    """
    results = {
        "duration": roll_die(duration_die),
        "augmentation": roll_die(augmentation_die),
        "chord": roll_die(chord_die)
    }

    if tet_choice == 24:
        results["pitch"] = roll_die(pitch_die_24tet)
    else:
        results["pitch"] = roll_die(pitch_die_12tet)

    return results

def get_duration_image_path(duration_name):
    """
    Returns the image path for a given duration name.
    """
    return duration_die.get(duration_name)
