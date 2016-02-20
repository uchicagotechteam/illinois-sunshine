import flask
import json 

app = flask.Flask(__name__)

@app.route('/')
def index():
	data = open('./tmp/com_data.json', 'r').read()
	
	return flask.render_template("map.html", data=data)
	#return 'hello,world'
	
if __name__ == '__main__':
	app.debug = True
	app.run()