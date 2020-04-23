#!/usr/bin/env python3

""" PyCalc is a simple calculator built using Python and PyQt5 """

import sys
from functools import partial

# Import QApplication and required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt

__version__ = "0.3"
__author__ = "Akaash Thao"

ERROR_MSG = "ERROR" # Display this in case of invalid maths expression


##############
#### VIEW ####
##############

# Create a subclass of QMainWindow to setup the calculator's GUI
class PyCalcUI(QMainWindow):
    """PyCalc's View (GUI)"""
    def __init__(self):
        super().__init__()

        self.is_answer_displayed = False

        # Set some main window properties
        self.setWindowTitle("PyCalc")
        self.setFixedSize(335, 235)

        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Create the display and the buttons
        self._createDisplay()
        self._createButtons()

    # Private methods for setting up the GUI
    def _createDisplay(self):
        """Create the dislpay"""
        # Create the display widget
        self.display = QLineEdit()

        # Set some display properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """Create the buttons"""
        self.buttons = {}
        buttonsLayout = QGridLayout()

        # Button text | position on the QGridLayout
        buttons = {
            "7": (0, 0),
            "8": (0, 1),
            "9": (0, 2),
            "*": (0, 3),
            "/": (0, 4),
            "4": (1, 0),
            "5": (1, 1),
            "6": (1, 2),
            "+": (1, 3),
            "-": (1, 4),
            "1": (2, 0),
            "2": (2, 1),
            "3": (2, 2),
            "(": (2, 3),
            ")": (2, 4),
            "0": (3, 0),
            ".": (3, 1),
            "ANS": (3, 2),
            "=": (3, 3),
            "C": (3, 4),
        }

        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(60, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)

    # These three methods are used for updating the display and form the GUI public interface
    def setDisplayText(self, text):
        """Set display's text"""
        self.display.setText(text)
        self.display.repaint()

    def getDisplayText(self):
        """Get display's text"""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display"""
        self.setDisplayText("")
        self.is_answer_displayed = False


####################
#### CONTROLLER ####
####################

# Create a Controller class to connect the GUI and the model
class PyCalcCtrl:
    """PyCalc Controller class"""
    def __init__(self, view, model):
        """Controller initialiser"""
        # Give PyCalcCtrl an instance of the view PyCalcUI and access to it's public interface
        self._view = view
        # Also give PyCalcCtrl an instance of the model used to evaluate maths expressions input into the calculator
        self._evaluate = model

        self.last_answer = self._view.getDisplayText()

        # Connect signals and slots
        self._connectSignals()

    def _calculateResult(self):
        """Evaluate expressions"""
        result = self._evaluate(expression=self._view.getDisplayText())
        self._view.setDisplayText(result)
        self._view.is_answer_displayed = True
        if result != ERROR_MSG:
            self.last_answer = result

    def _buildExpression(self, sub_exp):
        """Build expressions"""
        if self._view.getDisplayText() == ERROR_MSG:
            self._view.clearDisplay()

        # If an answer has just been displayed, clear the screen so a new expression can be entered
        if self._view.is_answer_displayed == True:
            self._view.clearDisplay()

        # Combine what is already in the display with what is entered on each key press
        if sub_exp == "ANS":
            expression = self._view.getDisplayText() + self.last_answer
        else:
            expression = self._view.getDisplayText() + sub_exp
        # Update the display in response to user input
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots"""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {"=", "C", "ANS"}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons["C"].clicked.connect(self._view.clearDisplay)
        self._view.buttons["="].clicked.connect(self._calculateResult)
        self._view.buttons["ANS"].clicked.connect(partial(self._buildExpression, "ANS"))
        self._view.display.returnPressed.connect(self._calculateResult)


###############
#### MODEL ####
###############

# Create a Model to handle the calculator's operation
def evaluateExpression(expression):
    """Evaluate an expression"""
    try:
        # eval function evaluates the given expression as Python code
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG

    return result


# Client code
def main():
    """Main function"""
    # Create an instance of QApplication
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = PyCalcUI()
    view.show()
    # Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(view=view, model=model)
    # Execute the calculator's main loop
    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()