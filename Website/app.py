from flask import Flask, render_template, request
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.map_engine import mbtiles  # Your MBTiles blueprint

app = Flask(__name__)
app.register_blueprint(mbtiles)  # Register the map tile server

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ai', methods=['GET', 'POST'])
def ask_ai():
    response = ""
    if request.method == 'POST':
        user_input = request.form['question']
        try:
            res = requests.post(OLLAMA_URL, json={
                "model": MODEL_NAME,
                "prompt": user_input,
                "stream": False
            })
            response = res.json().get("response", "⚠️ No response from AI.")
        except Exception as e:
            response = f"⚠️ AI error: {e}"
    return render_template('ai.html', response=response)

@app.route('/map')
def offline_map():
    return render_template('map.html')

if __name__ == '__main__':
    print("✅ Flask is starting with Ollama + Offline Map...")
    app.run(debug=True)






