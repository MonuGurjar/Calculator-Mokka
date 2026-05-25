import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class GarudaMokkaCalc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator-mokka")
        self.setMinimumSize(400, 600)
        self.resize(450, 700)
        
        # Main central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        
        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setText("0")
        self.main_layout.addWidget(self.display)
        
        # Grid layout for buttons
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.main_layout.addLayout(self.grid_layout)
        
        self.create_buttons()
        self.load_stylesheet()

        # State
        self.current_input = ""
        self.last_result_shown = False
        
        # Enable focus for key events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(__file__), "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())
                
    def create_buttons(self):
        buttons = [
            ('C', 0, 0, 1, 1, 'operator'), ('+/-', 0, 1, 1, 1, 'operator'), ('%', 0, 2, 1, 1, 'operator'), ('/', 0, 3, 1, 1, 'operator'),
            ('7', 1, 0, 1, 1, 'number'), ('8', 1, 1, 1, 1, 'number'), ('9', 1, 2, 1, 1, 'number'), ('*', 1, 3, 1, 1, 'operator'),
            ('4', 2, 0, 1, 1, 'number'), ('5', 2, 1, 1, 1, 'number'), ('6', 2, 2, 1, 1, 'number'), ('-', 2, 3, 1, 1, 'operator'),
            ('1', 3, 0, 1, 1, 'number'), ('2', 3, 1, 1, 1, 'number'), ('3', 3, 2, 1, 1, 'number'), ('+', 3, 3, 1, 1, 'operator'),
            ('0', 4, 0, 1, 2, 'number'), ('.', 4, 2, 1, 1, 'number'), ('=', 4, 3, 1, 1, 'operator')
        ]
        
        for btn_text, row, col, rowSpan, colSpan, btn_class in buttons:
            btn = QPushButton(btn_text)
            btn.setSizePolicy(btn.sizePolicy().Policy.Expanding, btn.sizePolicy().Policy.Expanding)
            
            # Apply styling properties
            if btn_text == '=':
                btn.setObjectName("btn_equal")
            else:
                btn.setProperty("buttonClass", btn_class)
                
            # Allow buttons to pass focus back to main window so keys keep working
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
            btn.clicked.connect(self.on_button_clicked)
            self.grid_layout.addWidget(btn, row, col, rowSpan, colSpan)

    def keyPressEvent(self, event):
        key_text = event.text()
        key_code = event.key()
        
        if key_code in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.process_input('=')
        elif key_code == Qt.Key.Key_Backspace:
            self.process_backspace()
        elif key_code == Qt.Key.Key_Escape:
            self.process_input('C')
        elif key_text in "0123456789.+-*/%":
            self.process_input(key_text)
        else:
            super().keyPressEvent(event)

    def on_button_clicked(self):
        sender = self.sender()
        self.process_input(sender.text())

    def process_input(self, text):
        if text == 'C':
            self.current_input = ""
            self.display.setText("0")
        elif text == '=':
            self.evaluate_expression()
        elif text == '+/-':
            self.toggle_sign()
        elif text == '%':
            self.percentage()
        else:
            if self.last_result_shown and (text.isdigit() or text == '.'):
                self.current_input = text
                self.last_result_shown = False
            else:
                if self.current_input == "0" and text.isdigit():
                    self.current_input = text
                else:
                    self.current_input += text
                self.last_result_shown = False
            self.display.setText(self.current_input)
            
    def process_backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input or self.current_input == "-":
                self.current_input = ""
                self.display.setText("0")
            else:
                self.display.setText(self.current_input)

    def evaluate_expression(self):
        try:
            if not self.current_input:
                return
                
            expression = self.current_input
            allowed_chars = "0123456789+-*/.% "
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters")
                
            result = eval(expression)
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            self.display.setText(str(result))
            self.current_input = str(result)
            self.last_result_shown = True
        except Exception:
            self.display.setText("Error")
            self.current_input = ""
            self.last_result_shown = True

    def toggle_sign(self):
        if self.current_input:
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.display.setText(self.current_input)

    def percentage(self):
        try:
            if self.current_input:
                result = float(eval(self.current_input)) / 100
                if result.is_integer():
                    result = int(result)
                self.current_input = str(result)
                self.display.setText(self.current_input)
        except Exception:
            self.display.setText("Error")
            self.current_input = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GarudaMokkaCalc()
    window.show()
    sys.exit(app.exec())
