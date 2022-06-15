from tkinter import *
from tkmacosx import Button
import math


class Calculator:

    window = None
    inputText = "0"
    afterEq = False

    # lists of all operands and numbers
    operands = ["/", "*", "-", "+"]
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

    # dictionary of number buttons with their (row, column)
    numPos = {7: (1, 0), 8: (1, 1), 9: (1, 2),
              4: (2, 0), 5: (2, 1), 6: (2, 2),
              1: (3, 0), 2: (3, 1), 3: (3, 2)}

    # dictionary of operand buttons with their (row, column)
    opPos = {"÷": (0, 3, "/"), "×": (1, 3, "*"), "-": (2, 3, "-"), "+": (3, 3, "+")}

    # constructor
    def __init__(self):

        # creates the window in which the calculator will be placed
        self.window = Tk()
        self.window.title("Calculator")
        self.window.geometry("360x550")
        self.window.resizable(False, False)  # False means cannot resize window

        # create label to display equation
        self.displayLabel = Label(self.window, text="0", font=("Arial", 40), fg="black", bg="#EEEEEE", height=2)
        self.displayLabel.pack()

        # sets button colors to be used later
        numbers_main = "#444444"
        numbers_back = "#7C7C7C"
        AC_main = "#16558F"
        AC_back = "#5B88B0"
        operand_main = "#00B4D8"
        operand_back = "#90E0EF"
        backspace_main = "#999999"
        backspace_back = "#B7B7B7"
        equals_main = "#0583D2"
        equals_back = "#69B4E4"

        # create frame to display buttons
        self.buttonFrame = Frame(self.window, bg="black")
        self.buttonFrame.pack()

        # creates each number button 1-9 and adds them to frame
        for key, value in self.numPos.items():
            self.create_button(btn=str(key), rw=value[0], cl=value[1], clsp=1, col=numbers_main, acol=numbers_back, wid=70,
                               fsize=30, cmd=lambda x=key: self.press(str(x)))

        # creates number button 0 and adds it to the frame
        self.create_button(btn="0", rw=4, cl=0, clsp=2, col=numbers_main, acol=numbers_back, wid=160, fsize=30,
                           cmd=lambda: self.press("0"))

        # creates each operand button and adds them to the frame
        for key, value in self.opPos.items():
            self.create_button(btn=key, rw=value[0], cl=value[1], clsp=1, col=operand_main, acol=operand_back, wid=70,
                               fsize=40, cmd=lambda x=value[2]: self.press(str(x)))

        # creates all clear button and adds it to the frame
        self.create_button(btn="A/C", rw=0, cl=0, clsp=1, col=AC_main, acol=AC_back, wid=70, fsize=30,
                           cmd=self.clear)

        # creates backspace button and adds it to the frame
        self.create_button(btn="Backspace", rw=0, cl=1, clsp=2, col=backspace_main, acol=backspace_back, wid=160, fsize=30,
                           cmd=self.back)

        # creates decimal button and adds it to the frame
        self.create_button(btn=".", rw=4, cl=2, clsp=1, col=numbers_main, acol=numbers_back, wid=70, fsize=45,
                           cmd=lambda: self.press("."))

        # creates the "equals" button and adds it to the frame
        self.create_button(btn="=", rw=4, cl=3, clsp=1, col=equals_main, acol=equals_back, wid=70, fsize=40, cmd=self.equals)

        # gives keyboard number buttons same functionality as number buttons in window
        for num in self.nums:
            self.window.bind(num, lambda event, x=num: self.press(x))

        # gives keyboard operand buttons same functionality as operand buttons in window
        for op in self.operands:
            self.window.bind(op, lambda event, x=op: self.press(x))

        # gives keyboard enter and delete buttons same functionality as equals and backspace buttons in window
        self.window.bind("<Return>", lambda event: self.equals())
        self.window.bind("<BackSpace>", lambda event: self.back())

    # method that is called whenever a number or operand button is pressed
    def press(self, btn):

        # won't allow input if length of text reaches width of window
        if len(self.inputText) >= 15:
            return

        # replaces default text "0" with new input as long as input is not "."
        elif self.inputText == "0" and btn != ".":
            self.inputText = btn

        # runs right after equal button is hit so that text can be completely reset
        elif self.afterEq:

            # runs if next button hit is a number, so that equation is reset
            if btn in self.nums:
                if btn == ".":
                    self.inputText = "0."
                else:
                    self.inputText = btn

            # runs if next button hit is an operand so that it is added to equation
            else:
                self.inputText += btn

            self.afterEq = False

        # runs if input is to be added to equation as normal
        else:
            self.inputText += btn

        self.displayLabel["text"] = self.inputText

    # method that resets the text displayed in the label to "0"
    def clear(self):

        # resets variable that holds if equation had just happened
        if self.afterEq:
            self.afterEq = False

        self.inputText = "0"
        self.displayLabel["text"] = self.inputText

    # method that deletes the last character entered
    def back(self):

        # resets variable that holds if equation had just happened
        if self.afterEq:
            self.afterEq = False

        self.inputText = self.inputText[:len(self.inputText)-1]

        # if last character is deleted, resets text to default state
        if self.inputText == "":
            self.inputText = "0"

        self.displayLabel["text"] = self.inputText

    # method that runs when equal button is selected and solves entered equation
    def equals(self):

        # attempts to evaluate the string that the user has entered
        try:
            # evaluate the equation
            self.inputText = str(eval(self.inputText))

            # rounds equation so that long decimals won't go past end of label
            digits = int(math.log10(abs(float(self.inputText))))+1
            temp2 = float(self.inputText)
            self.inputText = str(round(temp2, 14 - digits))

            # if there is an unnecessary decimal (.0) at the end, removes this
            if self.inputText[-2:len(self.inputText)] == ".0":
                self.inputText = self.inputText[:-2]

            # signifies that an equation just occurred
            self.afterEq = True
            self.displayLabel["text"] = self.inputText

        # exception caught if string has invalid syntax
        except SyntaxError:
            self.inputText = "0"
            self.displayLabel["text"] = "Syntax Error"

        # exception caught if division by zero is attempted
        except ZeroDivisionError:
            self.inputText = "0"
            self.displayLabel["text"] = "Zero Division Error"

        except:
            self.inputText = "0"
            self.displayLabel["text"] = "Syntax Error"

    # method that creates a button and adds it to the frame at desired location
    def create_button(self, btn, rw, cl, clsp, col, acol, wid, fsize, cmd):
        button = Button(self.buttonFrame, text=btn, font=("Arial", fsize, "bold"), command=cmd, relief=RAISED, bd=10,
                        fg="white", bg=col, width=wid, height=70, activebackground=acol)
        button.grid(row=rw, column=cl, columnspan=clsp)
        return button

    # method that displays the window
    def live(self):
        self.window.mainloop()


# main that runs and instantiates a calculator object, then displays it to the screen
if __name__ == "__main__":
    myCalc = Calculator()
    myCalc.live()

