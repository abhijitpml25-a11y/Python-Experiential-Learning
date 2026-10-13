import pytest
from app import app, calculate_expression, CalculationError


@pytest.mark.parametrize(("expression", "expected"), [
    ("12 + 8 * 2", 28),
    ("(12 + 8) / 4", 5),
    ("sqrt(81)", 9),
    ("sin(30)", 0.5),
    ("log(100)", 2),
    ("2^8", 256),
    ("factorial(5)", 120),
    ("pi * 2", pytest.approx(6.283185307179586)),
])
def test_supported_expressions(expression, expected):
    assert calculate_expression(expression) == expected


@pytest.mark.parametrize("expression", ["", "1/0", "sqrt(-1)", "unknown(3)", "__import__('os')"])
def test_invalid_expressions(expression):
    with pytest.raises(CalculationError):
        calculate_expression(expression)


def test_calculate_endpoint():
    client = app.test_client()
    response = client.post("/calculate", json={"expression": "2 + 3"})
    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_health_endpoint():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
