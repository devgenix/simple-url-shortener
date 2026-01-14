from flask import Flask, request, redirect, render_template_string
import string
import random

app = Flask(__name__)
url_map = {}

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if not original_url:
            return "Please provide a URL", 400
        
        short_id = generate_short_id()
        url_map[short_id] = original_url
        short_url = request.host_url + short_id
        return f'Shortened URL: <a href="{short_url}">{short_url}</a>'
    
    return '''
        <form method="post">
            <input type="text" name="url" placeholder="Enter URL to shorten" style="width: 300px;">
            <input type="submit" value="Shorten">
        </form>
    '''

@app.route('/<short_id>')
def redirect_to_url(short_id):
    original_url = url_map.get(short_id)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    # Listen on all interfaces for Docker/K8s
    app.run(host='0.0.0.0', port=5000)