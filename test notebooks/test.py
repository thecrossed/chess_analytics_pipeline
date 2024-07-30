import cloud_sql_connect as conn
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text

# Function call to get DB password ino a local varaiable  
db_password = conn.access_secret_version('rcc-game-result', 'cloudsql_pwd','1')

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn():
    conn= connector.connect(
        "rcc-game-result:europe-west10:rcc-sql",
        "pymysql",
        user="tianmin",
        password=db_password,
        db="rcc"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

def return_username(number):
    """
    return the chess.com username with the number in the student_chess_com table
    """
    with pool.connect() as db_conn:
        
        # select table student_chess_com
        query = """SELECT chess_com_username 
                    FROM student_chess_com
                    LIMIT {number};
                """.format(number = number)
        result = db_conn.execute(sqlalchemy.text(query)).fetchall()
        username_lst = []
        # Do something with the results
        for row in result:
            row_str = str(row[0])
            username = row_str.split("\r")[0]
            username_lst.append(username)
    return username_lst

# print(return_username(2))

def number_username():
    """
    return the number of unique chess.com username in the student_chess_com table
    """
    with pool.connect() as db_conn:
        
        # select table student_chess_com
        query = """SELECT count(chess_com_username) 
                    FROM student_chess_com;
                """
        result = db_conn.execute(sqlalchemy.text(query)).fetchall()
        username_lst = []
        # Do something with the results
        for row in result:
            num_row = int(row[0])
    print("Number of username is {num}".format(num = num_row))
    return num_row

number_username = number_username()
username_lst = return_username(number_username)
print(username_lst)