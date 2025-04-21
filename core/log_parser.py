import os, re
from . import log_models
from . import utils
from pathlib import Path

parsed_errors = []
parsed_debug = []
parsed_game = []


class LogParser:
    def __init__(self, log_dir: Path = None):
        self.log_dir = log_dir or self.get_default_log_dir()
        self.parsed_errors = []
        self.parsed_debug = []
        self.parsed_game = []

    def get_default_log_dir(self):
        import os
        user = os.environ['USERPROFILE']
        return Path(user) / 'Documents' / 'Paradox Interactive' / 'Crusader Kings III' / 'logs'

    def get_log_files(self):
        return {
            "error": self.log_dir / "error.log",
            "debug": self.log_dir / "debug.log",
            "game": self.log_dir / "game.log",
        }

    def clear_parsed_logs(self):
        self.parsed_errors.clear()
        self.parsed_debug.clear()
        self.parsed_game.clear()

    def parse(self):
        self.clear_parsed_logs()
        for log_type, path in self.get_log_files().items():
            if path.exists():
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        self.parse_and_append_line(line, log_type)

    def parse_and_append_line(self, line, log_type):
        if not line.strip():
            return

        if log_type == "error":
            matches = re.findall(r'\[(.*?)\]', line)
            file_match = re.search(r'([a-zA-Z0-9_/\\.-]+\.(?:txt|mod))', line)
            if len(matches) >= 3:
                timestamp = matches[0]
                new_entry = log_models.LogEntry(
                    timestamp=timestamp,
                    log_type="error",
                    message=line.strip(),
                    file=file_match.group(0) if file_match else "Unknown"
                )
                self.parsed_errors.append(new_entry)
        elif log_type == "debug" and "DEBUG" in line:
            self.parsed_debug.append(line.strip())
        elif log_type == "game" and "GAME" in line:
            self.parsed_game.append(line.strip())