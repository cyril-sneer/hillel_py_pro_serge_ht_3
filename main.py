#! .venv/bin/python3

import os
from flask import Flask, render_template, request
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


@app.route('/')  # root
def index():
    db = db_tools.get_db()
    sql_req = 'SELECT title FROM genres'
    genres_list = [item['title'] for item in db.execute(sql_req).fetchall()]
    return render_template('index.html',
                           title='Main Page',
                           genres=genres_list)


@app.route('/names/')  # Количество уникальных исполнителей
def show_unique_artists_qty():
    db = db_tools.get_db()
    sql_req = 'SELECT COUNT(DISTINCT artist) FROM tracks'
    artists_qty = db.execute(sql_req).fetchone()[0]
    return render_template('show_uniq_qty.html',
                           title='Количество уникальных исполнителей',
                           uniq_artists_qty=artists_qty)


@app.route('/tracks/')  # Показать количество треков
def show_tracks_qty():
    db = db_tools.get_db()
    sql_req = 'SELECT COUNT(title) FROM tracks'
    tracks_qty = db.execute(sql_req).fetchone()[0]
    return render_template('show_tracks_qty.html',
                           title="Количество треков",
                           total_tracks=tracks_qty)


@app.route('/tracks/genres/')  # Показать количество треков в определенном жанре
def show_genred_tracks_qty():
    genre_title = request.args.get('genre')
    db = db_tools.get_db()
    sql_req = f"""
    SELECT COUNT(tracks.title) FROM genres
    JOIN tracks on tracks.genre_id = genres.id
    WHERE genres.title LIKE '{genre_title}' 
    """
    genred_tracks_qty = db.execute(sql_req).fetchone()[0]
    return render_template('show_genred_tracks_qty.html',
                           titile='Количество треков в жанре',
                           genre=genre_title,
                           tracks_qty=genred_tracks_qty)


@app.route('/tracks-sec/')  # Показать названия треков и их продолжительность
def show_tracks_and_duration():
    db = db_tools.get_db()
    # sql_req = 'SELECT artist, title, duration FROM tracks'
    sql_req = """SELECT tracks.title, artist, genres.title, duration 
                 FROM genres JOIN tracks on tracks.genre_id = genres.id"""
    tracks_with_duration = db.execute(sql_req).fetchall()

    return render_template('show_tracks_and_duration.html',
                           title='Список треков',
                           tracks_list=tracks_with_duration)


@app.route('/tracks-sec/statistics/')  # Показать среднюю и общую продолжительности треков
def show_aver_and_total_duration():
    db = db_tools.get_db()
    sql_req = 'SELECT AVG(duration) FROM tracks'
    aver_duration = db.execute(sql_req).fetchone()[0]
    sql_req = 'SELECT SUM(duration) FROM tracks'
    total_duration = db.execute(sql_req).fetchone()[0]
    return render_template('show_aver_and_total_duration.html',
                           title='Продолжительность треков',
                           aver=aver_duration,
                           total=total_duration)


if __name__ == '__main__':
    app.run(debug=True)
