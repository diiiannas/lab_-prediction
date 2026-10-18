import random
from flask import Flask, render_template, request

app = Flask(__name__)

posesheniya = 0

ANSWERS = [
    "Определённо да",
    "Спроси позже",
    "Нет сомнений",
    "Нет",
    "Сомнения присутствуют",
]


@app.route("/", methods=["GET"])
def index():
    global posesheniya
    posesheniya += 1
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    question = request.form.get("question", "").strip()
    answer = random.choice(ANSWERS)
    return render_template("index.html", question=question, answer=answer)

@app.route("/metrics")
def metrics():
    metric_text = "# HELP posesheniya_total Общее количество посещений сайта\n"
    metric_text += "# TYPE posesheniya_total counter\n"
    metric_text += f"posesheniya_total {posesheniya}\n"
    return metric_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
