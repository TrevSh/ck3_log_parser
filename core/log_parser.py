import os
from pathlib import Path

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

def parse_line(line, log_type):
    if log_type == "error":
        if "Error" or "Script Location" in line:
            print(f"Error found: {line.strip()}")
    # elif log_type == "debug":
    #     # Example parsing for debug logs
    #     if "DEBUG" in line:
    #         print(f"Debug info: {line.strip()}")
    # elif log_type == "game":
    #     # Example parsing for game logs
    #     if "GAME" in line:
    #         print(f"Game event: {line.strip()}")

log_files = get_log_files()
for log_type, path in log_files.items():
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            parse_line(line, log_type)
