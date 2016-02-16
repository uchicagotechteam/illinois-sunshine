import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
	return flask.render_template("index.html")
	#return 'hello,world'
	
if __name__ == '__main__':
	app.debug = True
	app.run()