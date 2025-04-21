from core.log_parser import LogParser
from PySide6.QtWidgets import QApplication
from gui.interface import LogViewer
from core.utils import get_windows_default_log_dir
import sys
from pathlib import Path

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the parser. Change later to find the log dir automatically depending on the OS
    parser = LogParser(get_windows_default_log_dir())

    # Clear logs
    parser.clear_parsed_logs()

    # Parse logs
    parser.parse()

    # Pass it to your GUI (if applicable)
    viewer = LogViewer(parser)
    viewer.resize(1000, 600)
    viewer.show()

    sys.exit(app.exec())
