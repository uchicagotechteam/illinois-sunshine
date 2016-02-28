import flask
import json 

app = flask.Flask(__name__)

@app.route('/')
def index():
	data = open('./tmp/com_data.json', 'r').read()
	geodata = open('./tmp/geojson_com_data.json', 'r').read()
	return flask.render_template("map.html", geodata=geodata)
	
if __name__ == '__main__':
	app.debug = True
	app.run()