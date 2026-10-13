import ast
import math
import operator
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Only explicitly approved operations are available to the expression evaluator.
_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_CONSTANTS = {"pi": math.pi, "e": math.e, "tau": math.tau}
_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atan": lambda x: math.degrees(math.atan(x)),
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "factorial": math.factorial,
    "exp": math.exp,
}


class CalculationError(ValueError):
    """Raised when an expression is invalid or outside the supported operations."""


def _evaluate_node(node):
    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.Name) and node.id in _CONSTANTS:
        return _CONSTANTS[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise CalculationError("Exponent is too large.")
        return _BINARY_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate_node(node.operand))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _FUNCTIONS:
        if node.keywords or len(node.args) != 1:
            raise CalculationError("Functions accept exactly one argument.")
        argument = _evaluate_node(node.args[0])
        if node.func.id == "factorial" and (not isinstance(argument, (int, float)) or not float(argument).is_integer() or argument < 0 or argument > 170):
            raise CalculationError("Factorial requires a whole number from 0 to 170.")
        return _FUNCTIONS[node.func.id](argument)
    raise CalculationError("Unsupported expression. Use numbers, operators, constants, and supported functions.")


def calculate_expression(expression):
    if not isinstance(expression, str) or not expression.strip():
        raise CalculationError("Enter a mathematical expression.")
    if len(expression) > 250:
        raise CalculationError("Expression is too long.")
    # Permit only characters needed for math expressions; names are validated by the AST evaluator.
    allowed = set("0123456789.+-*/%() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
    if any(char not in allowed for char in expression):
        raise CalculationError("Expression contains unsupported characters.")
    try:
        tree = ast.parse(expression.replace("^", "**"), mode="eval")
        result = _evaluate_node(tree)
    except ZeroDivisionError:
        raise CalculationError("Cannot divide by zero.")
    except OverflowError:
        raise CalculationError("The result is too large to calculate.")
    except (SyntaxError, TypeError):
        raise CalculationError("Invalid expression. Check the syntax.")
    except ValueError as exc:
        if isinstance(exc, CalculationError):
            raise
        raise CalculationError("Math domain error. Check the function input.")
    except (NameError, AttributeError):
        raise CalculationError("Unknown function or constant.")
    if isinstance(result, complex) or not math.isfinite(float(result)):
        raise CalculationError("The result is outside the supported numeric range.")
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return result


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/calculate")
def calculate():
    data = request.get_json(silent=True) or request.form
    expression = data.get("expression", "")
    try:
        result = calculate_expression(expression)
        return jsonify({"ok": True, "expression": expression, "result": result})
    except CalculationError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
