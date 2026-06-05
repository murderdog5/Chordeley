import webview
import os
import threading
import uvicorn
from api import app

def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)

t = threading.Thread(target=run_api, daemon=True)
t.start()

html_path = os.path.join(os.path.dirname(__file__),"static","index.html")

window = webview.create_window(
    title="Chordeley",
    url=f"file://{html_path}",
    width=1200,
    height=800,
)

webview.start(debug=True)