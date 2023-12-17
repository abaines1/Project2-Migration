import database
import datetime

menu = '''\nPlease select one of the following options:
1. Add new movie.
2. View upcoming movies.
3. View all movies.
4. Watch a movie.
5. View watched Movies.
6. Add user to app.
7. Exit

Your selection: '''
welcome = "Welcome to the Netflix Watchlist App!"


def prompt_add_movie():
    title = input("Title of movie: ")
    release_date = input("Release date (mm-dd-YYYY): ")
    try:
        date_object = datetime.datetime.strptime(release_date, "%m-%d-%Y")
        release_timestamp = date_object.timestamp()
    except ValueError:
        print("Wrong date format, try again.")
        return None

    database.add_movie(title, release_timestamp)


def print_movie_list(header, movies):
    print(f"--- {header} ---")
    for _id, title, release_timestamp in movies:
        date_object = datetime.datetime.fromtimestamp(release_timestamp)
        human_readable = date_object.strftime("%b %d %Y")
        print(f"{_id}: {title} on ({human_readable})\n")
    print("----------")


def prompt_add_user():
    error_flag = True # A flag used to continuously loop through the inner menu item until a correct username is given
    while error_flag:
        new_username = input("What username do you want: ")
        if database.user_exists(new_username):
            print("Username already exists. Try again.")
        else:
            database.add_user(new_username)
            print(f"New username ({new_username}) added to app!")
            error_flag = False


def prompt_view_watched_movies():
    username_doesnt_exist = True # A flag used to continuously loop until username exists.
    while username_doesnt_exist:
        username = input("Who's watched movie list do you want to see: ")
        if database.user_exists(username):
            return username # note, I do not need to flip the bool because the return sthatment ends the loop.
        else:
            print("Username doesn't exists. Try again.")


def prompt_watched_movie():
    movie_id = input("What is the ID of the movie you watched: ")
    username = input("What is your username: ")
    watched_operation = database.watch_movie(movie_id, username)
    if watched_operation:
        print(f"Movie with ID {movie_id} was marked as watched by {username}!")
    else:
        print(f"Movie with ID {movie_id} does not exist.")

print(welcome)
database.create_tables()

# <-------- Main, program starts here.
while (user_input := input(menu)) != "7":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        upcoming_movies = database.view_movies(upcoming=True)
        print_movie_list("Upcoming", upcoming_movies)
    elif user_input == "3":
        all_movies = database.view_movies()
        print_movie_list("All", all_movies)
    elif user_input == "4":
        prompt_watched_movie()
    elif user_input == "5":
        username = prompt_view_watched_movies()
        watched_movies = database.view_watched_movies(username)
        print_movie_list(f"{username}'s Watched List", watched_movies)
    elif user_input == "6":
        prompt_add_user()
    else:
        print("Invalid input. please try again.")
