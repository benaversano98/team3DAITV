from createdb import *


def crea_tabelle(connection):
    create_movies = """
    CREATE TABLE IF NOT EXISTS `movies` (
    `movie_id` int PRIMARY KEY,
    `title` varchar(255) NOT NULL,
    `alternative_title` VARCHAR(255),
    `year` INT,
    `media_rating` FLOAT(3,2)
    );
    """

    create_genres = """
    CREATE TABLE IF NOT EXISTS `genres` (
    `genre_id` int AUTO_INCREMENT PRIMARY KEY,
    `genre` VARCHAR(255) NOT NULL
    );
    """

    create_genres_movies = """
        CREATE TABLE IF NOT EXISTS `genres_movies` (
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

    create_cities = """
    CREATE TABLE IF NOT EXISTS `cities` (
    `id_city` INT PRIMARY KEY,
    `cap` VARCHAR(255),
    `city` VARCHAR(255)
    )
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

    alter_users = """
    ALTER TABLE users
    ADD COLUMN fasciaeta VARCHAR(20);
    """

    trigger_fascaieta = """
    CREATE TRIGGER up_fasciaeta
    BEFORE INSERT ON users
    FOR EACH ROW
    BEGIN
        SET NEW.fasciaeta = CASE
            WHEN NEW.age < 18 THEN 'under 18'
            WHEN NEW.age >= 18 AND NEW.age <= 24 THEN '18-24'
            WHEN NEW.age >= 25 AND NEW.age <= 34 THEN '25-34'
            WHEN NEW.age >= 35 AND NEW.age <= 44 THEN '35-44'
            WHEN NEW.age >= 45 AND NEW.age <= 54 THEN '25-34'
            ELSE 'over 55'
            END;
    END;
    """

    trigger_cities = """
    CREATE TRIGGER up_city
    BEFORE INSERT ON users
    FOR EACH ROW
    BEGIN
        SET NEW.city = (SELECT city 
        FROM cities 
        JOIN users 
        ON users.cap = cities.cap)
    END;
    """

    execute_query(connection, create_movies)
    execute_query(connection, create_genres)
    execute_query(connection, create_genres_movies)
    execute_query(connection, create_users)
    execute_query(connection, create_cities)
    execute_query(connection, create_ratings)

    execute_query(connection, alter_users)
    execute_query(connection, trigger_fascaieta)
