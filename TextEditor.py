# Text Editor Application using PyQt6
# This application provides a simple text editor with customizable themes, fonts, and a debug console.
# It also saves settings to a file and restores them on startup.
# Author: Rise-KuN
# Version: 1.0

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QToolBar, 
    QPushButton, QDialog, QVBoxLayout, QTabWidget,
    QWidget, QLabel, QComboBox, QRadioButton,
    QButtonGroup, QFrame, QHBoxLayout, QSizePolicy,
    QFontComboBox, QSpinBox, QGroupBox, QPlainTextEdit,
    QDockWidget, QCheckBox, QStyle
)
from PyQt6.QtCore import Qt, QSettings, QDir
from PyQt6.QtGui import (
    QFont, QTextCursor, QTextOption, 
    QPalette, QColor, QTextCharFormat, 
    QTextBlockFormat, QIcon
)
import sys
import os
import ctypes
from datetime import datetime

class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor")
        
        # Initialize debug console
        self.debug_console = None
        self.debug_dock = None
        
        # Default settings
        self.font_name = "Arial"
        self.font_size = 16
        self.theme_mode = "Dark"
        self.text_content = ""
        self.show_debug = False
        
        # Load settings
        self.load_settings()
        
        # Set window icon properly
        self._set_window_icon()
        
        # Initialize debug console if enabled
        if self.show_debug:
            self._init_debug_console()
            self.log_debug("Application started")
        
        # Apply theme based on settings
        self.apply_theme()
        
        # Initialize UI
        self.setup_ui()
        self.apply_font()
        
        # Set text content
        self.text_area.setPlainText(self.text_content)

    def _init_debug_console(self):
        """Initialize debug console"""
        try:
            self.debug_console = QPlainTextEdit()
            self.debug_console.setReadOnly(True)
            self.debug_dock = QDockWidget("Debug Console", self)
            self.debug_dock.setWidget(self.debug_console)
            self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.debug_dock)
            self.debug_dock.setVisible(self.show_debug)
        except Exception as e:
            print(f"Failed to initialize debug console: {e}")

    def log_debug(self, message):
        """Add a timestamped debug message to the console"""
        if not self.show_debug or self.debug_console is None:
            return
            
        try:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.debug_console.appendPlainText(f"[{timestamp}] {message}")
            self.debug_console.ensureCursorVisible()
        except Exception as e:
            print(f"Debug logging failed: {e}")

    def _set_window_icon(self):
        """Properly set window icon with multiple fallback options"""
        try:
            icon_paths = [
                os.path.join(os.path.dirname(__file__), "icon.ico"),
                os.path.join(QDir.currentPath(), "icon.ico"),
                os.path.join(QDir.homePath(), "icon.ico"),
                "icon.ico"
            ]
            
            for path in icon_paths:
                if os.path.exists(path):
                    self.setWindowIcon(QIcon(path))
                    self.log_debug(f"Icon loaded from: {path}")
                    return
            
            # Fallback to embedded icon if available
            self.setWindowIcon(self.style().standardIcon(
                QStyle.StandardPixmap.SP_DesktopIcon))
            self.log_debug("Using fallback system icon")
        except Exception as e:
            self.log_debug(f"Error setting icon: {str(e)}")
        
    def setup_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
        
        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)
        
        # Settings button
        self.btn_settings = QPushButton("⚙")
        self.btn_settings.clicked.connect(self.open_settings)
        self.toolbar.addWidget(self.btn_settings)
        
        # Text area
        self.text_area = QTextEdit()
        self.text_area.setFrameShape(QFrame.Shape.NoFrame)
        self.text_area.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        layout.addWidget(self.text_area)
    
    def apply_theme(self, theme=None):
        if theme is not None:
            self.theme_mode = theme
            
        if self.theme_mode == "Dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QToolBar {
                    background-color: #252525;
                    border: none;
                    padding: 5px;
                }
                QTextEdit {
                    background-color: #1e1e1e;
                    color: white;
                    selection-background-color: #0078d7;
                    selection-color: white;
                    border: none;
                }
                QPushButton {
                    background-color: #333;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #444;
                }
                QPushButton:checked {
                    background-color: #0078d7;
                }
                QDialog {
                    background-color: #252525;
                }
                QLabel {
                    color: white;
                }
                QGroupBox {
                    color: white;
                    border: 1px solid #444;
                    margin-top: 10px;
                    padding-top: 15px;
                }
                QComboBox, QSpinBox, QFontComboBox {
                    background-color: #333;
                    color: white;
                    border: 1px solid #555;
                    padding: 3px;
                }
                QTabWidget::pane {
                    border: none;
                }
                QTabBar::tab {
                    background: #252525;
                    color: white;
                    padding: 8px;
                    border: none;
                }
                QTabBar::tab:selected {
                    background: #333;
                }
                QRadioButton {
                    color: white;
                    padding: 5px;
                }
            """)
        elif self.theme_mode == "Light":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ffffff;
                }
                QToolBar {
                    background-color: #f0f0f0;
                    border: none;
                    padding: 5px;
                }
                QTextEdit {
                    background-color: #ffffff;
                    color: black;
                    selection-background-color: #0078d7;
                    selection-color: white;
                    border: none;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: black;
                    border: none;
                    padding: 5px 10px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:checked {
                    background-color: #0078d7;
                    color: white;
                }
                QDialog {
                    background-color: #f0f0f0;
                }
                QLabel {
                    color: black;
                }
                QGroupBox {
                    color: black;
                    border: 1px solid #ccc;
                    margin-top: 10px;
                    padding-top: 15px;
                }
                QComboBox, QSpinBox, QFontComboBox {
                    background-color: #ffffff;
                    color: black;
                    border: 1px solid #ccc;
                    padding: 3px;
                }
                QTabWidget::pane {
                    border: none;
                }
                QTabBar::tab {
                    background: #f0f0f0;
                    color: black;
                    padding: 8px;
                    border: none;
                }
                QTabBar::tab:selected {
                    background: #ffffff;
                }
                QRadioButton {
                    color: black;
                    padding: 5px;
                }
            """)
        else:  # System - try to detect
            # For now, default to dark if we can't detect system theme
            self.apply_theme("Dark")
    
    def apply_font(self):
        font = QFont(self.font_name, self.font_size)
        self.text_area.setFont(font)

    def open_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Settings")
        settings_dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout(settings_dialog)
        layout.setContentsMargins(10, 10, 10, 10)
        
        notebook = QTabWidget()
        layout.addWidget(notebook)
        
        # Themes tab
        themes_tab = QWidget()
        notebook.addTab(themes_tab, "Themes")
        
        themes_layout = QVBoxLayout(themes_tab)
        themes_layout.setContentsMargins(5, 5, 5, 5)
        themes_layout.setSpacing(10)
        
        # Theme selection in a group box
        theme_group = QGroupBox("Theme")
        theme_group_layout = QVBoxLayout()
        theme_group_layout.setContentsMargins(10, 15, 10, 10)
        theme_group_layout.setSpacing(5)
        
        self.theme_group = QButtonGroup()
        
        system_radio = QRadioButton("System")
        dark_radio = QRadioButton("Dark")
        light_radio = QRadioButton("Light")
        
        self.theme_group.addButton(system_radio, 0)
        self.theme_group.addButton(dark_radio, 1)
        self.theme_group.addButton(light_radio, 2)
        
        theme_group_layout.addWidget(system_radio)
        theme_group_layout.addWidget(dark_radio)
        theme_group_layout.addWidget(light_radio)
        theme_group.setLayout(theme_group_layout)
        
        themes_layout.addWidget(theme_group)
        themes_layout.addStretch()
        
        # Set current selection
        if self.theme_mode == "System":
            system_radio.setChecked(True)
        elif self.theme_mode == "Dark":
            dark_radio.setChecked(True)
        else:
            light_radio.setChecked(True)
        
        # Fonts tab
        fonts_tab = QWidget()
        notebook.addTab(fonts_tab, "Fonts")
        
        # Font selection
        font_layout = QVBoxLayout(fonts_tab)
        font_layout.setContentsMargins(5, 5, 5, 5)
        font_layout.setSpacing(10)
        
        font_group = QGroupBox("Font Settings")
        font_group_layout = QVBoxLayout()
        font_group_layout.setContentsMargins(10, 15, 10, 10)
        font_group_layout.setSpacing(5)
        
        font_label = QLabel("Font:")
        font_group_layout.addWidget(font_label)
        
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(self.font_name))
        font_group_layout.addWidget(self.font_combo)
        
        size_label = QLabel("Size:")
        font_group_layout.addWidget(size_label)
        
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(self.font_size)
        font_group_layout.addWidget(self.size_spin)
        
        # Preview
        preview_label = QLabel("Preview:")
        font_group_layout.addWidget(preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlainText("This is a preview of the selected font and size.")
        self.preview_text.setMaximumHeight(80)
        font_group_layout.addWidget(self.preview_text)
        
        font_group.setLayout(font_group_layout)
        font_layout.addWidget(font_group)
        font_layout.addStretch()
        
        # New Debug tab
        debug_tab = QWidget()
        notebook.addTab(debug_tab, "Debug")
        
        debug_layout = QVBoxLayout(debug_tab)
        debug_layout.setContentsMargins(5, 5, 5, 5)
        debug_layout.setSpacing(10)
        
        debug_group = QGroupBox("Debug Settings")
        debug_group_layout = QVBoxLayout()
        debug_group_layout.setContentsMargins(10, 15, 10, 10)
        debug_group_layout.setSpacing(10)
        
        self.debug_checkbox = QCheckBox("Show Debug Console")
        self.debug_checkbox.setChecked(self.show_debug)
        debug_group_layout.addWidget(self.debug_checkbox)
        
        debug_group.setLayout(debug_group_layout)
        debug_layout.addWidget(debug_group)
        debug_layout.addStretch()
        
        # Connect signals
        self.font_combo.currentFontChanged.connect(self.update_preview)
        self.size_spin.valueChanged.connect(self.update_preview)
        
        # Save button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(lambda: self.save_settings(settings_dialog))
        layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Set initial preview
        self.update_preview()
        
        settings_dialog.exec()

    def update_preview(self):
        font = self.font_combo.currentFont()
        font.setPointSize(self.size_spin.value())
        self.preview_text.setFont(font)

    def save_settings(self, dialog):
        # Get theme selection
        theme_id = self.theme_group.checkedId()
        if theme_id == 0:
            self.theme_mode = "System"
        elif theme_id == 1:
            self.theme_mode = "Dark"
        else:
            self.theme_mode = "Light"
        
        self.font_name = self.font_combo.currentFont().family()
        self.font_size = self.size_spin.value()
        
        # Get debug setting
        new_debug_setting = self.debug_checkbox.isChecked()
        debug_setting_changed = (new_debug_setting != self.show_debug)
        self.show_debug = new_debug_setting
        
        # Apply changes
        self.apply_theme()
        self.apply_font()
        
        # Handle debug console visibility
        if debug_setting_changed:
            if self.show_debug:
                self._init_debug_console()
                self.log_debug("Debug console enabled")
            elif self.debug_dock is not None:
                self.debug_dock.setVisible(False)
        
        # Save settings to file
        self.save_settings_to_file()
        
        dialog.close()
    
    def save_settings_to_file(self):
        settings = QSettings("TextEditor", "Settings")
        settings.setValue("font_name", self.font_name)
        settings.setValue("font_size", self.font_size)
        settings.setValue("theme_mode", self.theme_mode)
        settings.setValue("text_content", self.text_area.toPlainText())
        settings.setValue("window_geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())
        settings.setValue("show_debug", self.show_debug)
    
    def load_settings(self):
        settings = QSettings("TextEditor", "Settings")
        
        # Load settings with defaults if not found
        self.font_name = settings.value("font_name", "Arial")
        self.font_size = int(settings.value("font_size", 16))
        self.theme_mode = settings.value("theme_mode", "Dark")
        self.text_content = settings.value("text_content", "")
        self.show_debug = settings.value("show_debug", "false") == "true"
        
        # Load window geometry and state
        geometry = settings.value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.setGeometry(100, 100, 800, 600)
            
        state = settings.value("window_state")
        if state:
            self.restoreState(state)
    
    def closeEvent(self, event):
        # Save current text content before closing
        self.text_content = self.text_area.toPlainText()
        self.save_settings_to_file()
        event.accept()

def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    
    # Set application icon
    try:
        app_icon = QIcon('icon.ico')
        app.setWindowIcon(app_icon)
    except Exception as e:
        print(f"Error setting application icon: {e}")
    
    # Set application ID for Windows
    if sys.platform == 'win32':
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                'com.rise.TextEditor.1')
        except Exception as e:
            print(f"Error setting AppUserModelID: {e}")
    
    editor = TextEditorApp()
    editor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()