import os
from pathlib import Path

parsed_errors = []
parsed_debug = []
parsed_game = []

def get_ck3_logs_dir():
    user = os.environ['USERPROFILE']
    log_path = Path(user) / 'Documents' / 'Paradox Interactive' / 'Crusader Kings III' / 'logs'
    return log_path

def get_log_files():
    logs_dir = get_ck3_logs_dir()
    log_files = {
        "error": logs_dir / "error.log",
        "debug": logs_dir / "debug.log",
        "game": logs_dir / "game.log",
    }
    return log_files

def clear_parsed_logs():
    global parsed_errors, parsed_debug, parsed_game
    parsed_errors = []
    parsed_debug = []
    parsed_game = []

def parse_and_append_line(line, log_type):
    clear_parsed_logs()
    if not line.strip():
        return  # Skip empty lines
    if log_type == "error":
        if "Error" or "Script Location" in line:
            parsed_errors.append(line.strip())
    elif log_type == "debug":
        if "DEBUG" in line:
            parsed_debug.append(line.strip())
    elif log_type == "game":
        if "GAME" in line:
            parsed_game.append(line.strip())

log_files = get_log_files()
for log_type, path in log_files.items():
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            parse_and_append_line(line, log_type)
print(parsed_errors)