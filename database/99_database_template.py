import mysql.connector
import mysql
import re
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "adminadmin",
    database = 'vocab'
)

cursor = conn.cursor()
cursor.execute("SHOW DATABASES")

found = False

for db in cursor:
    pattern = "[(,')]"
    db_string = re.sub(pattern, "",str(db))
    if (db_string == 'vocab'):
        found = True
        print("database vocab exists")
if (not found):
    cursor.execute("CREATE DATABASE vocab")

sql = "DROP TABLE IF EXISTS vocab_table"
cursor.execute(sql)

sql = "CREATE TABLE vocab_table(word VARCHAR(255), definition VARCHAR(255))"
cursor.execute(sql)


fh = open("/Users/jasminezhu/Desktop/mysql_python_database_guide_project/Vocabulary_list.csv","r")

wd_list = fh.readlines()

#print(wd_list)

wd_list.pop(0)

vocab_list = []

for rawstring in wd_list:
    word, defenition = rawstring.split(",",1)
    defenition = defenition.rstrip()
    vocab_list.append({word, defenition})
    sql = " INSERT INTO vocab_table(word, definition) VALUES(%s, %s)"
    values = (word, defenition)
    cursor.execute(sql, values)
    conn.commit()
    print("Inserted " + str(cursor.rowcount) + " row into vocab_table")
# print(vocab_list)

sql = "SELECT * FROM vocab_table WHERE word = %s;"
value = ('boisterous',)

cursor.execute(sql,value)

result = cursor.fetchall()

for row in result:
    print(row)

