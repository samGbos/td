import os
import re
from pathlib import Path

LEVELS_DIRECTORY = 'levels/'


def get_next_uncreated_level_filepath():
    # Generate the next file name
    _, latest_level_number = get_latest_level_filepath_and_number()
    next_level_number = latest_level_number + 1
    next_file_name = f"level{next_level_number:02d}.json"
    return Path(LEVELS_DIRECTORY) / next_file_name


def get_latest_level_filepath_and_number():
    # List all files in the directory
    filenames = os.listdir(LEVELS_DIRECTORY)

    # Find all matching files and extract their level numbers
    levels = []
    max_level = None
    max_level_filename = None
    for filename in filenames:
        match = re.match(r"level(\d+)(_.*)?\.json", filename)
        print(filename, match)
        if match:
            level = int(match.group(1))
            if max_level is None or level > max_level:
                max_level = level
                max_level_filename = filename

    if max_level is None:
        return None, None
    return Path(LEVELS_DIRECTORY) / max_level_filename, max_level
