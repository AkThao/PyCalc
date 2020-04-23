# PyCalc

Simple numerical calculator built with Python3 and PyQt5.
Based on tutorial from https://realpython.com/python-pyqt-gui-calculator/


## To run
`python3 pycalc.py`


## Improvements
I have added 3 main improvements over the default tutorial version:
1) After evaluating an expression, clear the screen when a new one is entered, rather than appending the new expression to the old result.
2) Swap the `00` button with the `.` button and replace `00` with `ANS`, which allows the user to substitute the previous result into a new expression, in the same fashion as a handheld calculator.
3) Allow the user to enter an expression via keyboard as well as clicking the buttons. However, due to the use of `eval()`, this poses a major security risk. Therefore, I have added input validation using regex to limit the character input to acceptable characters (numbers and the same mathematical operations present on the buttons).

(Also made the calculator and buttons wider to fit `ANS`.)


## Further possible improvements
1) Add more mathematical functions.
2) Change the colour scheme or add functionality for the user to do so.
