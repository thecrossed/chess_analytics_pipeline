import mysql.connector
import mysql
import re

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "adminadmin",
    database = 'rcc'
)

cursor = conn.cursor(buffered=True)

sql = "DROP TABLE IF EXISTS move"
cursor.execute(sql)

sql = "DROP TABLE IF EXISTS game"
cursor.execute(sql)

sql = "DROP TABLE IF EXISTS student"
cursor.execute(sql)

sql = "DROP TABLE IF EXISTS class"
cursor.execute(sql)

sql =   """
        CREATE TABLE class 
        (
            class_id INT Not null,
            term VARCHAR(32),
            level VARCHAR(32),
            start_date DATETIME,
            end_date DATETIME,
            PRIMARY KEY (class_id)
        );
        """

cursor.execute(sql)


sql =   """
        CREATE TABLE student (
        student_id INT Not null,
        class_id INT Not null,
        student_realname VARCHAR(100),
        student_username VARCHAR(100),
        loadtime timestamp,
        PRIMARY KEY (student_id),
        FOREIGN KEY (class_id) REFERENCES class (class_id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """

cursor.execute(sql)



sql =   """
        CREATE TABLE game (
        student_id INT Not null,
        student_username VARCHAR(100),
        game_id INT Not null,
        url VARCHAR(100),
        chesscom_uuid VARCHAR(100) Not null,
        start_time timestamp,
        end_time timestamp,
        time_control VARCHAR(100),
        rated BINARY(3),
        white_username VARCHAR(100),
        white_rating INT,
        black_username VARCHAR(100),
        black_rating INT,
        result FLOAT,
        fen VARCHAR(255),
        initial_setup VARCHAR(255),
        white_accuracy FLOAT,
        black_accuracy FLOAT,
        loadtime timestamp,
        PRIMARY KEY (game_id),
        FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """

cursor.execute(sql)



sql =   """
        CREATE TABLE move (
        game_id INT Not null,
        move_id INT Not null,
        move_number INT,
        side VARCHAR(16),
        used_time FLOAT,
        PRIMARY KEY (move_id),
        FOREIGN KEY (game_id) REFERENCES game (game_id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """

cursor.execute(sql)