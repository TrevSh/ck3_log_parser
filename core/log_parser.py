import os, re
from . import log_models
from pathlib import Path

parsed_errors = {}
parsed_debug = {}
parsed_game = {}

class LogParser:
    def __init__(self, log_dir: Path = None):
        self.log_dir = log_dir
        self.parsed_errors = {}
        self.parsed_debug = {}
        self.parsed_game = {}
        

    def get_log_files(self):
        if not self.log_dir:
            return
        self.log_dir = Path(self.log_dir)
        return {
            "error": self.log_dir / "error.log",
            "debug": self.log_dir / "debug.log",
            "game": self.log_dir / "game.log",
        }
    
    def change_log_dir(self, new_dir: Path):
        if new_dir != self.log_dir:
            self.log_dir = new_dir
            self.clear_parsed_logs()

    def clear_parsed_logs(self):
        self.parsed_errors.clear()
        self.parsed_debug.clear()
        self.parsed_game.clear()

    def parse(self):
        if self.log_dir:
            self.clear_parsed_logs()
            for log_type, path in self.get_log_files().items():
                if path.exists():
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            self.parse_line(line, log_type)

    def parse_line(self, line, log_type):
        if not line.strip():
            return

        # Match [timestamp][level][location]
        matches = re.findall(r'\[(.*?)\]', line)
        # Message = everything outside brackets after the last ]
        outside = re.sub(r'\[.*?\]:', '', line).strip()
        # Optional file match for mods/scripts
        file_match = re.search(r'([a-zA-Z0-9_/\\.-]+\.(?:txt|mod))', line)

        # If log has at least timestamp-level-location
        if len(matches) >= 3:
            timestamp = matches[0]
            level = matches[1]
            location = matches[2]

            entry = log_models.LogEntry(
                timestamp=timestamp,
                log_type=log_type,
                message=outside,
                file=file_match.group(0) if file_match else location  # fallback to [location]
            )
            
            self.append_entry(entry, log_type)
    
    def append_entry(self, entry, log_type):
        key = (entry.timestamp, entry.message)

        if log_type == "error":
                self.parsed_errors.setdefault(key, entry)
        elif log_type == "debug":
                self.parsed_debug.setdefault(key, entry)
        elif log_type == "game":
                self.parsed_game.setdefault(key, entry)
        
    def get_all_entries(self, deduped=False):
        combined = (
            list(self.parsed_errors.values()) +
            list(self.parsed_debug.values()) +
            list(self.parsed_game.values())
        )

        if deduped:
            combined = {
                (e.timestamp, e.message): e
                for e in combined
            }.values()

        return sorted(combined, key=lambda e: e.timestamp)     