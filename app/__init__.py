import os
from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def hello():
    return 'Hello World!', 200

@app.route('/env')
def env_test():
    return str(os.environ['APP_SETTINGS']), 200


if __name__=='__main__':
    app.run()
