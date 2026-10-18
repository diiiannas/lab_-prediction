import random
import psutil
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

@app.route("/metrics/resources")
def metrics_resources():

    cpu_percent = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    memory_used = memory.used / (1024 * 1024)
    memory_total = memory.total / (1024 * 1024)
    memory_percent = memory.percent

    disk = psutil.disk_usage('/')
    disk_used = disk.used / (1024 * 1024 * 1024)
    disk_total = disk.total / (1024 * 1024 * 1024)
    disk_percent = disk.percent
    
    metric_text = f"""# HELP cpu_usage_percent CPU usage percentage
# TYPE cpu_usage_percent gauge
cpu_usage_percent {cpu_percent}

# HELP memory_used_mb Memory used in MB
# TYPE memory_used_mb gauge
memory_used_mb {memory_used:.2f}

# HELP memory_total_mb Memory total in MB
# TYPE memory_total_mb gauge
memory_total_mb {memory_total:.2f}

# HELP memory_usage_percent Memory usage percentage
# TYPE memory_usage_percent gauge
memory_usage_percent {memory_percent}

# HELP disk_used_gb Disk used in GB
# TYPE disk_used_gb gauge
disk_used_gb {disk_used:.2f}

# HELP disk_total_gb Disk total in GB
# TYPE disk_total_gb gauge
disk_total_gb {disk_total:.2f}

# HELP disk_usage_percent Disk usage percentage
# TYPE disk_usage_percent gauge
disk_usage_percent {disk_percent}
"""
     return metric_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
