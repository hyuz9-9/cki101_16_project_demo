from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '我是功能-'

if __name__ == '__main__':
    # Flask listens on 5000 port
    app.run(host='0.0.0.0', port=5000)
