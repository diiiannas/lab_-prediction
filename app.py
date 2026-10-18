import random
from flask import Flask, render_template, request

app = Flask(__name__)

vsego_predskazaniy = 0

ANSWERS = [
    "Определённо да",
    "Спроси позже",
    "Нет сомнений",
    "Нет",
    "Сомнения присутствуют",
]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    global vsego_predskazaniy
    
    question = request.form.get("question", "").strip()
    answer = random.choice(ANSWERS)
    
    vsego_predskazaniy += 1
    
    return render_template("index.html", question=question, answer=answer)

@app.route("/metrics")
def metrics():
    metric_text = "# HELP vsego_predskazaniy Total predictions\n"
    metric_text += "# TYPE vsego_predskazaniy counter\n"
    metric_text += f"vsego_predskazaniy {vsego_predskazaniy}\n"
    return metric_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
