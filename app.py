from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    print('Hello, World!')
    return 'Hello, World!'

@app.route('/html')
def hello_html():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=1508)