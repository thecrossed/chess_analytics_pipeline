import cloud_sql_connect as conn
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text
import requests
from datetime import date
from datetime import datetime
import json
from dateutil.relativedelta import relativedelta
import pandas as pd

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


def lowercase_student(student_list):
    """
    to lowercase all the username
    
    input - list, list of student username, regardless upper or lower case
    
    output - list, list of student username, lower case
    """
    
    lower_students = [x.lower() for x in student_list]
    
    return lower_students

def last_n_month(n):
    """
    purpose:
    return the month as yyyy/mm format of the past n months from now
    
    input -
    n: number of months from past
    
    output -
    a list of month with yyyy/mm format
    """
    months_lst = []
    for num in range(n):
        months = date.today() + relativedelta(months=-num)
        if months.month <= 9:
            months_lst.append(str(months.year) + "/"+ "0" + str(months.month))
        else:
            months_lst.append(str(months.year) + "/"+ str(months.month))
    return months_lst

def get_user_archives(username, 
                      nr_months,
                     user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}):
    """
    purpose:
    get archive monthly files of specific chess.com player
    
    input:
    username - username of the chess.com player
    nr_months - integer, nummber of past months that we want to get the archives
    # to request chess.com API
       user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}
    
    output:
    target_month - files of archives according to months parameter
    """
    url = "https://api.chess.com/pub/player/{username}/games/archives".format(username = username)
    archive_request = requests.get(url, headers = user_agent)
    archives = archive_request.json()['archives']
    past_months = last_n_month(nr_months)
    target_month = []
    for archive in archives:
        if archive[-7:] in past_months:
            target_month.append(archive)
    return target_month
    
def get_archive_games(filename,
                     user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}):
    """
    purpose:
    
    return games in one archive file
    
    input:
    filename - filename that contains game urls
    
    output: 
    """
    games = requests.get(filename,headers = user_agent).json()['games']
    return games

def game_data_collect(students_username, month = 1):
    """
    collect game data for each student from the json raw data -
    end_times
    white_players
    black_players
    time_controls
    urls
    """
    end_times = []
    white_players = []
    black_players = []
    time_controls = []
    urls = []
    results = []
    white_rating = []
    black_rating = []
    white_accuracy = []
    black_accuracy = []
    
    students = lowercase_student(students_username)
    for student in students:
        print(student.upper())
        archives = get_user_archives(student, month)
        #print(archives)
        for archive in archives[::-1]:
            games = get_archive_games(archive)
            for game in games[::-1]:
                #print(game)
                # need to loose the logic to include all games
                if (game['white']['username'].lower() == student.lower() and game['black']['username'].lower() in students):
                    end_time = datetime.utcfromtimestamp(game['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                    print(end_time)
                    print("[w]" + student)
                    print("[b]" + game['black']['username'])
                    print("time control: " + game['time_control'])
                    print(game['pgn'].split("\n")[-2].split(" ")[-1]) # result
                    print("          ")
                    
                    end_times.append(end_time)
                    white_players.append(student.lower())
                    black_players.append(game['black']['username'].lower())
                    time_controls.append(game['time_control'])
                    urls.append(game['url'])
                    results.append(game['pgn'].split("\n")[-2].split(" ")[-1])
                    white_rating.append(game['white']['rating'])
                    black_rating.append(game['black']['rating'])
                    try:
                        white_accuracy.append(game['accuracies']['white'])
                        black_accuracy.append(game['accuracies']['black'])
                    except:
                        white_accuracy.append('unknown')
                        black_accuracy.append('unknown')
                    
                elif (game['black']['username'].lower() == student.lower() and game['white']['username'].lower() in students):
                    end_time = datetime.utcfromtimestamp(game['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                    print(end_time)
                    print("[w]" + game['white']['username'])
                    print("[b]" + student)
                    print("time control: " + game['time_control'])
                    print(game['pgn'].split("\n")[-2].split(" ")[-1])
                    print("          ")
                    
                    end_times.append(end_time)
                    white_players.append(game['white']['username'].lower())
                    black_players.append(student.lower())
                    time_controls.append(game['time_control'])
                    urls.append(game['url'])
                    results.append(game['pgn'].split("\n")[-2].split(" ")[-1])
                    white_rating.append(game['white']['rating'])
                    black_rating.append(game['black']['rating'])
                    try:
                        white_accuracy.append(game['accuracies']['white'])
                        black_accuracy.append(game['accuracies']['black'])
                    except:
                        white_accuracy.append('unknown')
                        black_accuracy.append('unknown')

    print("---------")
    return end_times, white_players, black_players, time_controls, urls, results, white_rating, black_rating, white_accuracy, black_accuracy

def to_pandas_df(fetched_data):
    """
    Import fetched game data into a pandas dataframe
    
    and then sort and drop duplicates
    """
    df = pd.DataFrame()
    df['end_time'] = fetched_data[0]
    df['white_player_username'] = fetched_data[1]
    df['black_player_username'] = fetched_data[2]
    df['time_control'] = fetched_data[3]
    df['url'] = fetched_data[4]
    df['result'] = fetched_data[5]
    df['white_rating'] = fetched_data[6]
    df['black_rating'] = fetched_data[7]
    df['white_accuracy'] = fetched_data[8]
    df['black_accuracy'] = fetched_data[9]
    df = df.sort_values(by = 'end_time', ascending = False)
    df = df.drop_duplicates()
    
    return df


def create_game_table(df):
    with pool.connect() as db_conn:
        
        # Drop Table
        drop_query = "DROP TABLE IF EXISTS games"
        db_conn.execute(sqlalchemy.text(drop_query))
        # Create Table
        create_query = """
                       CREATE TABLE games(end_time TIMESTAMP, 
                                          white_player_username VARCHAR(128),
                                          black_player_username VARCHAR(128),
                                          time_control VARCHAR(64),
                                          url VARCHAR(255),
                                          result VARCHAR(16),
                                          white_rating INT,
                                          black_rating INT,
                                          white_accuracy FLOAT,
                                          black_accuracy FLOAT)
                       """
        db_conn.execute(sqlalchemy.text(create_query))
        df.to_sql(name='games',con=db_conn,if_exists='append',index = False)
        db_conn.commit()
        db_conn.close()
        # insert statement (DML statement for data load)
        """
        insert_stmt = sqlalchemy.text(
        "INSERT INTO basic_dtls VALUES (1, 'Jack')")
        db_conn.execute(insert_stmt)
        db_conn.commit()
        """


number_username = number_username()

username_lst = return_username(number_username)

game_collection = game_data_collect(username_lst)

game_df = to_pandas_df(game_collection)

print(game_df.head(1))

create_game_table(game_df)





