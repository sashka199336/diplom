from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def calculator():
    """
    Главная страница калькулятора.

    Возвращает HTML-страницу с пользовательским интерфейсом калькулятора.
    """
    return render_template("calculator.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Обрабатывает вычисления, получаемые из POST-запроса.

    Получает математическое выражение из JSON-запроса
    и вычисляет результат. Если выражение некорректно,
    возвращает сообщение об ошибке.

    Returns:
        JSON-объект с результатом вычисления или ошибкой.
    """
    try:
        # Получение математического выражения из POST-запроса
        expression = request.json.get("expression", "")

        # Вычисление выражения
        result = eval(expression)  # Будьте осторожны с eval (см. замечания ниже)

        return jsonify({"result": result})
    except Exception:
        return jsonify({"error": "Ошибка в выражении!"}), 400


if __name__ == "__main__":
    app.run(debug=True)