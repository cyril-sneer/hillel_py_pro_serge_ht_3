#! .venv/bin/python3

import os
from flask import Flask, render_template, request, session, g, url_for, current_app
import db_tools


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'tracks.sqlite'),
    # CSV_DATA=os.path.join(app.root_path, 'data.csv'),
    DEBUG=True
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


app.cli.add_command(db_tools.create_db_command)
app.cli.add_command(db_tools.fill_db_command)
app.teardown_appcontext(db_tools.close_db)


# a simple page that says hello - just for test is it work ))
@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/')  # root
def index():
    return render_template('index.html',
                           title='Main Page')


if __name__ == '__main__':
    app.run(debug=True)
