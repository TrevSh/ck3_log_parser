from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    timestamp: datetime
    log_type: str  # 'error', 'warning', 'info'
    message: str
    file: str  # source log file
