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

sql = "DROP TABLE IF EXISTS student"
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
