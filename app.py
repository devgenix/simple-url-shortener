import redis
import os
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# Use environment variable for Redis host, default to localhost for local dev
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form['url']
    if not url:
        return redirect('/')
    
    import hashlib
    short_id = hashlib.md5(url.encode()).hexdigest()[:6]
    r.set(short_id, url)
    
    return render_template('index.html', short_url=f"{request.host_url}{short_id}")

@app.route('/<short_id>')
def resolve(short_id):
    url = r.get(short_id)
    if url:
        return redirect(url.decode())
    return "URL not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
