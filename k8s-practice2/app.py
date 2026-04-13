from flask import Flask
import os

app = Flask(__name__)

@app.get("/")
def index():
    name = os.getenv("NAME", "World")
    return f"<h1>Hello {name}</h1>"

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)