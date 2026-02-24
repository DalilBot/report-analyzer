"""
Daily Report Analyzer - Standalone Web App
Analyzes school daily reports (PDF) using Google Gemini AI
Extracts homework & reminders with 7-day memory
"""
import os
import json
import uuid
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

from utils.report_analyzer import ReportAnalyzer
from utils.report_memory import ReportMemory
from utils.report_fetcher import download_daily_report

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['DOWNLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'downloads')

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Initialize services
analyzer = ReportAnalyzer()
memory = ReportMemory()

ALLOWED_EXTENSIONS = {'pdf'}

# Track fetch status
fetch_state = {
    'running': False,
    'status': '',
    'progress': 0,
    'result': None,      # path to downloaded file
    'error': None
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_report():
    """Upload and analyze a daily report PDF"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Only PDF files are allowed'}), 400

    try:
        # Save file temporarily
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Analyze with Gemini
        result = analyzer.analyze(filepath)

        # Clean up uploaded file
        try:
            os.remove(filepath)
        except OSError:
            pass

        if result.get('error'):
            return jsonify({'success': False, 'error': result['error']}), 500

        # Store in memory
        report_date = datetime.now().strftime('%Y-%m-%d')
        memory.add_report(report_date, result)

        return jsonify({
            'success': True,
            'data': result,
            'date': report_date,
            'message': 'Report analyzed successfully!'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/memory')
def get_memory():
    """Get stored homework & reminders from the last 7 days"""
    data = memory.get_all()
    summary = memory.get_summary()
    return jsonify({'success': True, 'data': data, 'summary': summary})


@app.route('/api/homework/<hw_id>/toggle', methods=['POST'])
def toggle_homework(hw_id):
    """Toggle homework completion status"""
    success = memory.toggle_homework(hw_id)
    return jsonify({'success': success})


@app.route('/api/memory/clear', methods=['POST'])
def clear_memory():
    """Clear all stored data"""
    memory.clear()
    return jsonify({'success': True, 'message': 'Memory cleared'})


@app.route('/api/settings/key', methods=['POST'])
def save_api_key():
    """Save the Gemini API key to .env"""
    data = request.json
    key = data.get('key', '').strip()
    if not key:
        return jsonify({'success': False, 'error': 'No key provided'}), 400

    env_path = os.path.join(os.path.dirname(__file__), '.env')

    # Read existing .env or start fresh
    lines = []
    key_found = False
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('GEMINI_API_KEY='):
                    lines.append(f'GEMINI_API_KEY={key}\n')
                    key_found = True
                else:
                    lines.append(line)

    if not key_found:
        lines.append(f'GEMINI_API_KEY={key}\n')

    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    # Update the running process environment
    os.environ['GEMINI_API_KEY'] = key

    return jsonify({'success': True, 'message': 'API key saved!'})


@app.route('/api/settings/classera', methods=['POST'])
def save_classera_creds():
    """Save Classera credentials to .env"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400

    env_path = os.path.join(os.path.dirname(__file__), '.env')
    lines = []
    found_user = False
    found_pass = False

    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('CLASSERA_USERNAME='):
                    lines.append(f'CLASSERA_USERNAME={username}\n')
                    found_user = True
                elif line.strip().startswith('CLASSERA_PASSWORD='):
                    lines.append(f'CLASSERA_PASSWORD={password}\n')
                    found_pass = True
                else:
                    lines.append(line)

    if not found_user:
        lines.append(f'CLASSERA_USERNAME={username}\n')
    if not found_pass:
        lines.append(f'CLASSERA_PASSWORD={password}\n')

    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    os.environ['CLASSERA_USERNAME'] = username
    os.environ['CLASSERA_PASSWORD'] = password

    return jsonify({'success': True, 'message': 'Classera credentials saved!'})


@app.route('/api/fetch', methods=['POST'])
def fetch_report():
    """Start fetching daily report from Classera (runs in background)"""
    global fetch_state

    if fetch_state['running']:
        return jsonify({'success': False, 'error': 'Fetch already in progress'}), 409

    username = os.environ.get('CLASSERA_USERNAME', '')
    password = os.environ.get('CLASSERA_PASSWORD', '')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Classera credentials not configured. Set them in Settings.'}), 400

    fetch_state = {'running': True, 'status': 'Starting...', 'progress': 0, 'result': None, 'error': None}

    def do_fetch():
        global fetch_state
        steps = {
            'Starting browser': 10,
            'Logging in to Classera': 30,
            'Navigating to document library': 50,
            'Found': 60,
            'Downloading file': 75,
            'Downloaded': 100,
        }
        def on_status(msg):
            global fetch_state
            fetch_state['status'] = msg
            for key, prog in steps.items():
                if key.lower() in msg.lower():
                    fetch_state['progress'] = prog
                    break

        try:
            result = download_daily_report(
                username=username,
                password=password,
                download_path=app.config['DOWNLOAD_FOLDER'],
                on_status=on_status
            )
            if result:
                fetch_state['result'] = result
                fetch_state['status'] = 'Report downloaded!'
                fetch_state['progress'] = 100
            else:
                fetch_state['error'] = 'Failed to download report'
                fetch_state['status'] = 'Failed'
        except Exception as e:
            fetch_state['error'] = str(e)
            fetch_state['status'] = 'Error'
        finally:
            fetch_state['running'] = False

    thread = threading.Thread(target=do_fetch, daemon=True)
    thread.start()

    return jsonify({'success': True, 'message': 'Fetch started'})


@app.route('/api/fetch/status')
def fetch_status():
    """Get current fetch progress"""
    return jsonify({
        'running': fetch_state['running'],
        'status': fetch_state['status'],
        'progress': fetch_state['progress'],
        'has_file': fetch_state['result'] is not None,
        'error': fetch_state['error']
    })


@app.route('/api/analyze/fetched', methods=['POST'])
def analyze_fetched():
    """Analyze the most recently fetched report"""
    # Check for a fetched file
    filepath = fetch_state.get('result')

    # If no fetch result, check downloads folder for any PDF
    if not filepath or not os.path.exists(filepath):
        dl_dir = app.config['DOWNLOAD_FOLDER']
        if os.path.exists(dl_dir):
            pdfs = [f for f in os.listdir(dl_dir) if f.lower().endswith('.pdf')]
            if pdfs:
                filepath = os.path.join(dl_dir, pdfs[0])

    if not filepath or not os.path.exists(filepath):
        return jsonify({'success': False, 'error': 'No fetched report found. Fetch one first!'}), 404

    try:
        result = analyzer.analyze(filepath)

        if result.get('error'):
            return jsonify({'success': False, 'error': result['error']}), 500

        report_date = datetime.now().strftime('%Y-%m-%d')
        memory.add_report(report_date, result)

        return jsonify({
            'success': True,
            'data': result,
            'date': report_date,
            'filename': os.path.basename(filepath),
            'message': 'Fetched report analyzed!'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health')
def health():
    """Health check for deployment"""
    key = os.environ.get('GEMINI_API_KEY', '')
    has_key = bool(key) and key != 'your_gemini_api_key_here'
    has_classera = bool(os.environ.get('CLASSERA_USERNAME')) and bool(os.environ.get('CLASSERA_PASSWORD'))
    return jsonify({
        'status': 'ok',
        'gemini_configured': has_key,
        'classera_configured': has_classera,
        'timestamp': datetime.now().isoformat()
    })


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
