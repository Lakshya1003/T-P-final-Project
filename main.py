from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
from assistant import BlueberryAssistant

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

assistant_thread = None
assistant = None

def ui_callback(sender, message):
    """Callback to send messages to the frontend."""
    print(f"Sending to UI: {sender}: {message}")
    socketio.emit('message', {'sender': sender, 'text': message})

def start_assistant():
    global assistant
    assistant = BlueberryAssistant(ui_callback=ui_callback)
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
from assistant import BlueberryAssistant

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

assistant_thread = None
assistant = None

def ui_callback(sender, message):
    """Callback to send messages to the frontend."""
    print(f"Sending to UI: {sender}: {message}")
    socketio.emit('message', {'sender': sender, 'text': message})

def start_assistant():
    global assistant
    assistant = BlueberryAssistant(ui_callback=ui_callback)
    assistant.run()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_listen')
def handle_start_listen():
    """Handle manual trigger from UI."""
    print("Received manual trigger from UI")
    if assistant:
        assistant.trigger()

if __name__ == '__main__':
    # Start assistant in a separate thread
    if not assistant_thread:
        assistant_thread = threading.Thread(target=start_assistant, daemon=True)
        assistant_thread.start()
    
    socketio.run(app, debug=True, port=5000, use_reloader=False)