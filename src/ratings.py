import requests
from datetime import date
from datetime import datetime
import json
from dateutil.relativedelta import relativedelta
import pandas as pd

# student data - will be transferred to database
students_username = ['yaohengli',
           'chengliam',
           'blakey0313',
           'akfunchess66',

           'Leo20166',
           'Jasminezhao777',
           'Justinzhao777',
           'QuantumInnovator',
           'Jason-Ma',
           
           'chessloverma',
           'AndyAAYY',          
           'whatwhywhywhat',
           'TheChessBoi9999',
           'Gavin_ML']

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
    return student_list, ratings, retrieve_time

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
    df['用户名'] = fetched_data[0]
    df['快棋分数'] = fetched_data[1]
    df['采集时间'] = fetched_data[2]
    df = df.astype('str')
    df['快棋分数'] = df['快棋分数'].astype('int')
    df['采集时间'] = pd.to_datetime(df['采集时间'])
    df = df.drop_duplicates()
    df = df.sort_values(by = ['快棋分数','采集时间'], ascending = [False,False])
    
    return df

