DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS genres;

CREATE TABLE genres
(
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE tracks
(
    id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title    TEXT    NOT NULL,
    artist   TEXT    NOT NULL,
    genre_id INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    FOREIGN KEY (genre_id) REFERENCES genres (id)
)
