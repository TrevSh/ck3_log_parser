from core import log_parser
from gui.interface import LogViewer
from PySide6.QtWidgets import QApplication
import sys

log_parser.clear_parsed_logs()
# parse logs here if needed

app = QApplication(sys.argv)
viewer = LogViewer()
viewer.resize(800, 600)
viewer.show()
sys.exit(app.exec())
