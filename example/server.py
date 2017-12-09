
from flask import Flask, render_template, make_response
from flask_hashcash import validate_work
app = Flask(__name__)

# make session server-side to prevent replay attacks
# be sure to do this. otherwise it's all pointless
from flask_session import Session
SESSION_TYPE = 'filesystem' # consider changing this to 'redis'
app.config.from_object(__name__)
Session(app)

# in case user browse too fast show loading page
def loading_solution_response():
	return make_response(render_template('loading.html'))

@app.route('/')
@validate_work(difficulty = 5, wrong_solution_response = loading_solution_response)
def index():
    return render_template('index.html')

@app.route('/api')
@validate_work(difficulty = 5)
def api():
    return 'Success !'

app.run()