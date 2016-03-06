import flask
import json 

app = flask.Flask(__name__)

@app.route('/')
def index():
	data = open('./tmp/com_data.json', 'r').read()
	geodata = open('./tmp/geojson_com_data.json', 'r').read()
	timelineURL = flask.url_for('static', filename='Leaflet.TimeDimension/src')
	dateUrl = flask.url_for('static', filename = 'iso8601-js-period')
	return flask.render_template("map.html", geodata=geodata, turl = timelineURL, durl = dateUrl)
	
if __name__ == '__main__':
	app.debug = True
	app.run()