import sys, datetime
from core import log_parser
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QBrush, QColor
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QPushButton, QHeaderView,
    QFileDialog, QLabel
)

class LogViewer(QWidget):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser
        self.setWindowTitle("CK3 Log Viewer")

        self.layout = QVBoxLayout()

        #Customization
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QTableWidget {
                background-color: #2e2e2e;
                color: white;
                gridline-color: #555;
            }
            QHeaderView::section {
                background-color: #444;
                color: white;
                padding: 4px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #5e5e5e;
                border-radius: 5px;
                padding: 6px 12px;
                color: white;
            }
        """)

        self.setWindowTitle("CK3 Log Viewer!(Beta)")

        # Filter controls
        controls = QHBoxLayout()
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Error", "Game", "Debug"])
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
        
        github_label = QLabel()
        github_label.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 10pt;
                padding: 4px;
            }
            QLabel:hover {
                color: #fff;
            }
        """ )
        github_label.setText('<a href="https://github.com/TrevSh/ck3_log_parser">Contribute Here</a>')
        github_label.setOpenExternalLinks(True)
        github_label.setAlignment(Qt.AlignRight)  # Align to the right if placed in HBox
       
        # Footer row
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()                 # push the label to the right
        footer_layout.addWidget(github_label)
        self.layout.addLayout(footer_layout)
        
        self.timestamp_label = QLabel() 
        self.timestamp_label.setAlignment(Qt.AlignLeft)

        # Bind events
        self.refresh_button.clicked.connect(self.load_logs)
        self.type_filter.currentIndexChanged.connect(self.apply_filters)
        self.search_bar.textChanged.connect(self.apply_filters)
        
        # Settings
    
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
            self.parser.change_log_dir(folder)
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