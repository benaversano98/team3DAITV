from createdb import *


def crea_tabelle(connection):
    create_movies = """
    CREATE TABLE IF NOT EXISTS `movies` (
    `movie_id` int PRIMARY KEY,
    `title` varchar(255) NOT NULL,
    `alternative_title` VARCHAR(255),
    `year` INT
    );
    """

    create_genres = """
    CREATE TABLE IF NOT EXISTS `genres` (
    `genre_id` int AUTO_INCREMENT PRIMARY KEY,
    `genre` VARCHAR(255) NOT NULL
    );
    """

    create_genres_movies = """
        CREATE TABLE `genres_movies` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `movie_id` INT,
        `genre_id` INT,
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
        );
    """

    create_users = """
    CREATE TABLE IF NOT EXISTS `users` (
    `user_id` int AUTO_INCREMENT PRIMARY KEY,
    `gender` VARCHAR(10) CHECK (gender IN ('M','F','X')),
    `age` INT,
    `cap` VARCHAR(255),
    `work` VARCHAR(255)
    );
    """

    create_ratings = """
    CREATE TABLE IF NOT EXISTS `ratings` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT,
    `movie_id` INT,
    `rating` INT,
    `timestamp` BIGINT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
    );
    """
    execute_query(connection, create_movies)
    execute_query(connection, create_genres)
    execute_query(connection, create_genres_movies)
    execute_query(connection, create_users)
    execute_query(connection, create_ratings)

