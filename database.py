"""
Phase 3 Project 2

Database:

Movies with id, title, release_timestamp
Users with username
Watched with users_username, movie_id - Used as a bridge table between movies and users to get watched movies by a user.
"""

import os
import psycopg2
import datetime
from dotenv import load_dotenv

load_dotenv()


#Changing INTEGER to SERIAL : guaranteed unique autoincrement
#Change (?) to (%s)
#Change connection.execute() to cursor.execute


# Constant vars
CREATE_MOVIES_TABLE = '''CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT, 
    release_timestamp REAL
    );'''
CREATE_USERS_TABLE = '''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);'''
CREATE_WATCHED_TABLE = '''CREATE TABLE IF NOT EXISTS watched (
    users_username TEXT,
    movies_id INTEGER,
    FOREIGN KEY(users_username) REFERENCES users(username),
    FOREIGN KEY(movies_id) REFERENCES movies(id));'''

INSERT_MOVIE = "INSERT INTO movies(title, release_timestamp) VALUES (%s,%s);"
INSERT_NEW_USER = "INSERT INTO users(username) VALUES (%s);"
SELECT_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"

SELECT_WATCHED_MOVIES = '''SELECT movies.* FROM movies
    JOIN watched ON movies.id = watched.movies_id
    JOIN users ON watched.users_username = users.username
    WHERE users.username = %s;'''

INSERT_WATCHED_MOVE = "INSERT INTO watched(users_username, movies_id) VALUES (%s,%s);"
CHECK_MOVIE_EXISTS = "SELECT * FROM movies WHERE id = %s;"
CHECK_USER_EXISTS = "SELECT username FROM users WHERE username = %s;"

connection = psycopg2.connect(os.environ['DATABASE_URL'])

def normalize_username(username):
    # put other norms here.
    return username.lower()

def create_tables():
    with connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_MOVIES_TABLE)
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(CREATE_WATCHED_TABLE)


def add_movie(title, release_timestamp):
    with connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_MOVIE, (title, release_timestamp))


def add_user(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_NEW_USER, (normalize_username(username),))


def view_movies(upcoming=False):
    cursor = connection.cursor()
    if not upcoming:
        cursor.execute(SELECT_MOVIES)
    else:
        today_timestamp = datetime.datetime.today().timestamp()
        cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
    return cursor.fetchall()


def view_watched_movies(username):
    cursor = connection.cursor()
    cursor.execute(SELECT_WATCHED_MOVIES, (normalize_username(username), ))
    return cursor.fetchall()


def watch_movie(movie_id, username):
    cursor = connection.cursor();
    if movie_exists(movie_id):
        with connection:
            cursor.execute(INSERT_WATCHED_MOVE, (normalize_username(username), movie_id))
        return True
    else:
        return False


def movie_exists(movie_id): # change this
    cursor = connection.cursor()
    cursor.execute(CHECK_MOVIE_EXISTS, (movie_id,))
    if cursor.fetchone() is not None:
        return True
    else:
        return False


def user_exists(username):
    cursor = connection.cursor()
    cursor.execute(CHECK_USER_EXISTS, (normalize_username(username),))
    if cursor.fetchone() is not None:
        return True
    else:
        return False

