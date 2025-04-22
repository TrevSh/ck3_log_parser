import sys
from core import log_parser
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QPushButton, QHeaderView,
    QFileDialog, 
)

class LogViewer(QWidget):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser
        self.setWindowTitle("CK3 Log Viewer")

        self.layout = QVBoxLayout()

        # Filter controls
        controls = QHBoxLayout()
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Error", "Warning", "Debug"])
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search log messages...")
        self.refresh_button = QPushButton("Refresh Logs")

        controls.addWidget(self.type_filter)
        controls.addWidget(self.search_bar)
        controls.addWidget(self.refresh_button)
        
        #Add Folder
        self.folder_button = QPushButton("Select Log Folder")
        self.folder_button.clicked.connect(self.browse_log_folder)
        controls.addWidget(self.folder_button)


        # Log table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Level", "Location", "Message"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)


        self.layout.addLayout(controls)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        # Bind events
        self.refresh_button.clicked.connect(self.load_logs)
        self.type_filter.currentIndexChanged.connect(self.apply_filters)
        self.search_bar.textChanged.connect(self.apply_filters)

    
    def create_rows(self, log_entries):
        for log_entry in log_entries:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(log_entry.timestamp or ""))
            self.table.setItem(row_position, 1, QTableWidgetItem(log_entry.log_type or ""))
            self.table.setItem(row_position, 2, QTableWidgetItem(log_entry.file or ""))

            message_item = QTableWidgetItem(log_entry.message or "")
            message_item.setToolTip(log_entry.message or "")
            message_item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.table.setItem(row_position, 3, message_item)

    def populate_table(self):
        self.table.setRowCount(0)
        self.create_rows(self.parser.get_all_entries())
        
    def browse_log_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select CK3 Logs Folder")
        if folder:
            print("User selected folder:", folder)
            self.load_logs_from_folder(folder)
            
    def load_logs_from_folder(self, folder_path):
        self.parser.clear_parsed_logs()
        log_files = self.parser.get_log_files()

        for log_type, path in log_files.items():
            if path.exists():
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    for line in file:
                        self.parser.parse_and_append_line(line, log_type)

        self.populate_table()  # Your own table update function
                

    def load_logs(self):
        self.parser.clear_parsed_logs()
        log_files = self.parser.get_log_files()
        for log_type, path in log_files.items():
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    self.parser.parse_line(line, log_type)

        self.populate_table()
        
    def apply_filters(self):
        selected_type = self.type_filter.currentText().lower()
        search_text = self.search_bar.text().lower()

        # Get all logs from the parser
        all_logs = self.parser.get_all_entries()

        # Apply filters
        filtered = []

        for entry in all_logs:
            # Match log type (if not "All")
            if selected_type != "all" and selected_type not in entry.log_type.lower():
                continue

            # Match search text in message (optional)
            if search_text and search_text not in entry.message.lower():
                continue

            filtered.append(entry)

        # Now show filtered results
        self.table.setRowCount(0)
        self.create_rows(filtered)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = LogViewer()
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec_())