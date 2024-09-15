import requests
from datetime import date
from datetime import datetime
import json
from dateutil.relativedelta import relativedelta
import pandas as pd

# student data - will be transferred to database
students_username = [
           'yaohengli',
           'chengliam',
           'blakey0313',
           'akfunchess66',
           'leolren', 
           'ArthurJin',
           'terryjmoon',
           'jingyinghan',
           'Ethanlu001',

           'Jasminezhao777',
           'Justinzhao777',
           'Dingcheng0',
           'drymerrymagician',
           'sweetpotato48',
           
           'chessloverma',
           #'evejyl77',
           'Gavin_ML',
           'VickieNickie',
           'EricLangFeng',
           'Ella_2015_ella',
           'Elsawang0112',
           'JaydenW0403'
]

def get_user_stats(username, 
                   user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}):
    """
    purpose:
    get stas of specific chess.com player
    
    input:
    username - username of the chess.com player
    # to request chess.com API
       user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}
    
    output:
    user stats
    """
    url = "https://api.chess.com/pub/player/{username}/stats".format(username = username)
    stats_request = requests.get(url, headers = user_agent)
    stats_json = stats_request.json()
    return stats_json

def get_user_rapid_current_rating(username, 
                                  user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}):
    """
    purpose:
    get chess.com user current rating of rapid games
    
    input:
    username - username of the chess.com player
    # to request chess.com API
       user_agent = {'User-Agent': 'username: tianminlyu, email: tianminlyu@gmail.com'}
    
    output:
    rapid_rating,
    retrive_time
    """
    rapid_rating = get_user_stats(username)['chess_rapid']['last']['rating']
    retrive_time = now = datetime.utcnow().strftime("%b %d %Y %H:%M:%S")
    return rapid_rating, retrive_time

def rating_collect():
    students = lowercase_student(students_username)
    ratings = []
    retrieve_time = []
    for student in students:
        print(student)
        ratings.append(get_user_rapid_current_rating(student)[0])
        retrieve_time.append(get_user_rapid_current_rating(student)[1])
    return students, ratings, retrieve_time

def lowercase_student(student_list):
    """
    to lowercase all the username
    
    input - list, list of student username, regardless upper or lower case
    
    output - list, list of student username, lower case
    """
    
    lower_students = [x.lower() for x in student_list]
    
    return lower_students

def to_pandas_rating(fetched_data):
    """
    Import fetched game data into a pandas dataframe
    
    and then sort and drop duplicates
    """
    df = pd.DataFrame()
    df['username'] = fetched_data[0]
    df['rapid_rating'] = fetched_data[1]
    df['collect_time'] = fetched_data[2]
    df = df.astype('str')
    df['rapid_rating'] = df['rapid_rating'].astype('int')
    df['collect_time'] = pd.to_datetime(df['collect_time'])
    df = df.drop_duplicates()
    df = df.sort_values(by = ['rapid_rating','collect_time'], ascending = [False,False])
    
    return df

