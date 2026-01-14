from flask import Flask, request, redirect, render_template
import string
import random
import os

app = Flask(__name__)

# Dictionary to store short URLs and their corresponding long URLs
url_mapping = {}

def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        if not long_url:
            return "Please provide a URL", 400
        
        short_id = generate_short_id()
        url_mapping[short_id] = long_url
        
        short_url = request.host_url + short_id
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/health')
def health_check():
    return {"status": "healthy"}, 200

@app.route('/<short_id>')
def redirect_to_url(short_id):
    long_url = url_mapping.get(short_id)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
