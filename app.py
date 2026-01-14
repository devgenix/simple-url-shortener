from flask import Flask, request, redirect, render_template, url_for
import string
import random
import os

app = Flask(__name__)

# In-memory storage for URLs
url_map = {}

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if not original_url:
            return "Please provide a URL", 400
        
        # Simple validation: ensure it starts with http
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url

        short_code = generate_short_code()
        url_map[short_code] = original_url
        
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    original_url = url_map.get(short_code)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    # EKS/Containers usually expect port 8080 or 5000
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
