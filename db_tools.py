import sqlite3, click, csv
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row tells the connection to return rows that behave like dicts.
        # This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def create_db():
    db = get_db()

    with current_app.open_resource('create_db.sql') as sql_script:
        db.executescript(sql_script.read().decode('utf8'))


def fill_db():
    db = get_db()
    with current_app.open_resource('data.csv', 'r') as csv_file:  # open CSV file
        csv_reader = csv.reader(csv_file)  # get iterator
        genre_list = []

        csv_reader.__next__()  # skip the first (title) line
        for line in csv_reader:
            if line:
                title, artist, genre, duration = line

                if genre not in genre_list:
                    genre_list.append(genre)
                    genre_id = genre_list.index(genre) + 1

                    db.execute('INSERT INTO genres (id, title) VALUES (?, ?)', (genre_id, genre))
                    # print(f"{genre_id} : {genre} inserted")

                genre_id = genre_list.index(genre) + 1
                db.execute('INSERT INTO tracks (title, artist, genre_id, duration) VALUES (?, ?, ?, ?)',
                           (title, artist, genre_id, duration))
                # print(f"{title} : {artist} : {genre_id} : {genre} : {duration} inserted")
    db.commit()

@click.command('create-db')
def create_db_command():
    """Clear the existing data and create new tables."""
    create_db()
    click.echo('Initialized the database.')


@click.command('fill-db')
def fill_db_command():
    """Fill DB with new values"""
    fill_db()
    click.echo('DB filled with new values successful')
