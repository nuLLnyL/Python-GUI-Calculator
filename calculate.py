from tkinter import *
import ast
import operator

# =========================
# WINDOW
# =========================

root = Tk()
root.title("🎀 Jenlyn Paler's Calculator 🎀")
root.geometry("400x550")
root.configure(bg="#FCE4EC")
root.resizable(True, True)

# =========================
# SAFE EVALUATOR
# =========================

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def safe_eval(expression):
    def evaluate(node):

        if isinstance(node, ast.Constant):
            return node.value

        elif isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            op_func = operators.get(type(node.op))

            if op_func is None:
                raise TypeError("Unsupported operator")

            return op_func(left, right)

        elif isinstance(node, ast.UnaryOp):
            op_func = operators.get(type(node.op))

            if op_func is None:
                raise TypeError("Unsupported operator")

            return op_func(evaluate(node.operand))

        raise TypeError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


# =========================
# ENTRY
# =========================

entry = Entry(
    root,
    font=("Comic Sans MS", 30, "bold"),
    justify="right",
    bg="#FFF8FB",
    fg="#C2185B",
    borderwidth=5
)

entry.grid(
    row=0,
    column=0,
    columnspan=4,
    padx=10,
    pady=10,
    sticky="nsew"
)

# =========================
# FUNCTIONS
# =========================

def button_click(value):
    current = entry.get()
    operators_list = ["+", "-", "×", "÷"]

    # Allow negative number at beginning
    if value == "-" and current == "":
        entry.insert(END, "-")
        return

    # Handle operators
    if value in operators_list:

        if current == "":
            return

        last = current[-1]

        if last in operators_list:

            # Allow negative numbers after operators
            if value == "-" and last != "-":
                entry.insert(END, "-")

            return

    # Prevent multiple decimal points
    if value == ".":

        parts = (
            current.replace("+", " ")
            .replace("-", " ")
            .replace("×", " ")
            .replace("÷", " ")
            .split()
        )

        if parts and "." in parts[-1]:
            return

        # Auto-add leading zero
        if current == "" or current[-1] in operators_list:
            entry.insert(END, "0")

    entry.insert(END, str(value))


def button_clear():
    entry.delete(0, END)


def button_backspace():
    current = entry.get()

    if current:
        entry.delete(0, END)
        entry.insert(0, current[:-1])


def button_equal():

    try:

        expression = entry.get()

        if not expression:
            return

        # Convert display symbols to Python operators
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")

        if expression[-1] in ["+", "*", "/"]:
            return

        if expression == "-":
            return

        result = safe_eval(expression)

        # Remove unnecessary .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        entry.delete(0, END)
        entry.insert(0, result)

    except ZeroDivisionError:
        entry.delete(0, END)
        entry.insert(0, "Cannot Divide by 0")

    except Exception:
        entry.delete(0, END)
        entry.insert(0, "Error")


# =========================
# BUTTON STYLES
# =========================

btn_num = {
    "font": ("Comic Sans MS", 14, "bold"),
    "bg": "#F8BBD0",
    "fg": "#6A1B4D",
    "width": 5,
    "height": 2
}

btn_op = {
    "font": ("Comic Sans MS", 14, "bold"),
    "bg": "#F48FB1",
    "fg": "white",
    "width": 5,
    "height": 2
}

# =========================
# BUTTONS
# =========================

button_0 = Button(root, text="0", command=lambda: button_click(0), **btn_num)
button_1 = Button(root, text="1", command=lambda: button_click(1), **btn_num)
button_2 = Button(root, text="2", command=lambda: button_click(2), **btn_num)
button_3 = Button(root, text="3", command=lambda: button_click(3), **btn_num)
button_4 = Button(root, text="4", command=lambda: button_click(4), **btn_num)
button_5 = Button(root, text="5", command=lambda: button_click(5), **btn_num)
button_6 = Button(root, text="6", command=lambda: button_click(6), **btn_num)
button_7 = Button(root, text="7", command=lambda: button_click(7), **btn_num)
button_8 = Button(root, text="8", command=lambda: button_click(8), **btn_num)
button_9 = Button(root, text="9", command=lambda: button_click(9), **btn_num)

button_add = Button(root, text="+", command=lambda: button_click("+"), **btn_op)

button_subtract = Button(
    root,
    text="-",
    command=lambda: button_click("-"),
    **btn_op
)

button_multiply = Button(
    root,
    text="×",
    command=lambda: button_click("×"),
    **btn_op
)

button_divide = Button(
    root,
    text="÷",
    command=lambda: button_click("÷"),
    **btn_op
)

button_decimal = Button(
    root,
    text=".",
    font=("Comic Sans MS", 14, "bold"),
    bg="#F9A8D4",
    fg="white",
    width=5,
    height=2,
    command=lambda: button_click(".")
)

button_clear_btn = Button(
    root,
    text="C",
    font=("Comic Sans MS", 14, "bold"),
    bg="#FF8FA3",
    fg="white",
    width=5,
    height=2,
    command=button_clear
)

button_backspace_btn = Button(
    root,
    text="⌫",
    font=("Comic Sans MS", 14, "bold"),
    bg="#D8B4F8",
    fg="#4A235A",
    width=5,
    height=2,
    command=button_backspace
)

button_equal_btn = Button(
    root,
    text="=",
    font=("Comic Sans MS", 14, "bold"),
    bg="#EC4899",
    fg="white",
    width=5,
    height=2,
    command=button_equal
)

# =========================
# RESPONSIVE GRID
# =========================

for i in range(4):
    root.grid_columnconfigure(i, weight=1)

for i in range(6):
    root.grid_rowconfigure(i, weight=1)

# Row 1
button_clear_btn.grid(row=1, column=0, sticky="nsew", padx=3, pady=3)
button_backspace_btn.grid(row=1, column=1, sticky="nsew", padx=3, pady=3)
button_divide.grid(row=1, column=2, sticky="nsew", padx=3, pady=3)
button_multiply.grid(row=1, column=3, sticky="nsew", padx=3, pady=3)

# Row 2
button_7.grid(row=2, column=0, sticky="nsew", padx=3, pady=3)
button_8.grid(row=2, column=1, sticky="nsew", padx=3, pady=3)
button_9.grid(row=2, column=2, sticky="nsew", padx=3, pady=3)
button_subtract.grid(row=2, column=3, sticky="nsew", padx=3, pady=3)

# Row 3
button_4.grid(row=3, column=0, sticky="nsew", padx=3, pady=3)
button_5.grid(row=3, column=1, sticky="nsew", padx=3, pady=3)
button_6.grid(row=3, column=2, sticky="nsew", padx=3, pady=3)
button_add.grid(row=3, column=3, sticky="nsew", padx=3, pady=3)

# Row 4
button_1.grid(row=4, column=0, sticky="nsew", padx=3, pady=3)
button_2.grid(row=4, column=1, sticky="nsew", padx=3, pady=3)
button_3.grid(row=4, column=2, sticky="nsew", padx=3, pady=3)

button_equal_btn.grid(
    row=4,
    column=3,
    rowspan=2,
    sticky="nsew",
    padx=3,
    pady=3
)

# Row 5
button_0.grid(
    row=5,
    column=0,
    columnspan=2,
    sticky="nsew",
    padx=3,
    pady=3
)

button_decimal.grid(
    row=5,
    column=2,
    sticky="nsew",
    padx=3,
    pady=3
)

root.mainloop()