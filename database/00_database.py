import mysql.connector
import mysql
import re
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "adminadmin",
    database = 'rcc'
)

cursor = conn.cursor()
cursor.execute("SHOW DATABASES")

found = False

for db in cursor:
    pattern = "[(,')]"
    db_string = re.sub(pattern, "",str(db))
    if (db_string == 'rcc'):
        found = True
        print("database rcc exists")
if (not found):
    cursor.execute("CREATE DATABASE rcc")