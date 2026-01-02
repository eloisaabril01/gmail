from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gmail Automation Webapp</title>
        <style>
            body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; background-color: #f0f2f5; }
            .container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
            h1 { color: #1a73e8; margin-bottom: 1.5rem; }
            button { background-color: #1a73e8; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px; transition: background 0.3s; }
            button:hover { background-color: #1557b0; }
            #status { margin-top: 1.5rem; white-space: pre-wrap; text-align: left; background: #f8f9fa; padding: 1rem; border-radius: 4px; display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Gmail Creator</h1>
            <p>Click the button below to start the automated account creation process.</p>
            <button id="runBtn">Create Random Gmail</button>
            <div id="status"></div>
        </div>
        <script>
            document.getElementById('runBtn').addEventListener('click', async () => {
                const btn = document.getElementById('runBtn');
                const status = document.getElementById('status');
                btn.disabled = true;
                btn.innerText = 'Creating...';
                status.style.display = 'block';
                status.innerText = 'Starting automation...';
                
                try {
                    const response = await fetch('/run-automation', { method: 'POST' });
                    const result = await response.json();
                    status.innerText = result.output || result.error;
                } catch (e) {
                    status.innerText = 'Error: ' + e.message;
                } finally {
                    btn.disabled = false;
                    btn.innerText = 'Create Random Gmail';
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/run-automation', methods=['POST'])
def run_automation():
    try:
        # Run the script and capture output in real-time
        process = subprocess.Popen(
            ['python', 'gmail_automation.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        full_output = []
        for line in process.stdout:
            print(line, end='')  # Print to server console
            full_output.append(line)
        
        process.wait()
        return jsonify({'output': ''.join(full_output)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Replit requires 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
