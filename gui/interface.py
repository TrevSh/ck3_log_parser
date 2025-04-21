import sys
from core import log_parser
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QPushButton, QHeaderView
)

class LogViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CK3 Log Viewer")

        self.layout = QVBoxLayout()

        # Filter controls
        controls = QHBoxLayout()
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Error", "Warning", "Info"])
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search log messages...")
        self.refresh_button = QPushButton("Refresh Logs")

        controls.addWidget(self.type_filter)
        controls.addWidget(self.search_bar)
        controls.addWidget(self.refresh_button)

        # Log table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Level", "Location", "Message"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)


        self.layout.addLayout(controls)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        # Bind events
        self.refresh_button.clicked.connect(self.load_logs)
    
    def populate_table(self):
        self.table.setRowCount(0)
        for log_entry in log_parser.parsed_errors:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(log_entry.timestamp))
            self.table.setItem(row_position, 1, QTableWidgetItem(log_entry.log_type))
            self.table.setItem(row_position, 2, QTableWidgetItem(log_entry.file))
            self.table.setItem(row_position, 3, QTableWidgetItem(log_entry.message))
            

    def load_logs(self):
        log_parser.clear_parsed_logs()
        log_files = log_parser.get_log_files()
        for log_type, path in log_files.items():
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    log_parser.parse_and_append_line(line, log_type)

        self.populate_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = LogViewer()
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec_())