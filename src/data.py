import chess_dot_com_api as capi
import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pgn_parser import pgn, parser

# student data - will be transferred to database
students_username = ['yaohengli',
           'chengliam',
           'blakey0313',
           'akfunchess66',

           'Leo20166',
           'Jasminezhao777',
           'Justinzhao777',
           'QuantumInnovator',
           'Newinnovator',
           'Jason-Ma',
           'Dingcheng0',
           
           'chessloverma',
           'AndyAAYY',          
           'whatwhywhywhat',
           'charliezienyang',
           'TheChessBoi9999',
           'evejyl77',
           'Gavin_ML']

def lowercase_student(student_list):
    """
    to lowercase all the username
    
    input - list, list of student username, regardless upper or lower case
    
    output - list, list of student username, lower case
    """
    
    lower_students = [x.lower() for x in student_list]
    
    return lower_students


def game_data_collect():
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
        archives = capi.get_user_archives(student,2)
        #print(archives)
        for archive in archives[::-1]:
            games = capi.get_archive_games(archive)
            for game in games[::-1]:
                #print(game)
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

def move_data_collect():
    """
    collect move data for each game from the json raw data -

    """
    end_times = []
    urls = []
    move_num = []
    move = []
    clk = []
    
    students = lowercase_student(students_username)
    for student in students:
        print(student.upper())
        archives = capi.get_user_archives(student,2)
        #print(archives)
        for archive in archives[::-1]:
            games = capi.get_archive_games(archive)
            for game in games[::-1]:
                #print(game)
                if (game['white']['username'].lower() == student.lower() and game['black']['username'].lower() in students):
                    url = game['url']
                    end_time = datetime.utcfromtimestamp(game['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                    moves = parser.parse(game['pgn'] , actions=pgn.Actions())
                    move_text = moves.movetext
                    for i in range(len(move_text) - 1):
                        if i % 2 == 0:
                            
                            move_num.append( int(i / 2) + 1 )
                            move.append(str(move_text[i]).split("{")[0].split(".")[-1])
                            clk.append(str(move_text[i]).split("%clk ")[-1].split("]}")[0])
                            urls.append(url)
                            end_times.append(end_time)
                        else:
                            move_num.append( int(i / 2) + 1 )
                            move.append(str(move_text[i]).split("{")[0].split("...")[-1])
                            clk.append(str(move_text[i]).split("%clk ")[-1].split("]}")[0])
                            urls.append(url)
                            end_times.append(end_time)

                            


                    
                elif (game['black']['username'].lower() == student.lower() and game['white']['username'].lower() in students):
                    url = game['url']
                    end_time = datetime.utcfromtimestamp(game['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                    moves = parser.parse(game['pgn'] , actions=pgn.Actions())
                    move_text = moves.movetext
                    for i in range(len(move_text) - 1):
                        if i % 2 == 0:
                            
                            move_num.append( int(i / 2) + 1 )
                            move.append(str(move_text[i]).split("{")[0].split(".")[-1])
                            clk.append(str(move_text[i]).split("%clk ")[-1].split("]}")[0])
                            urls.append(url)
                            end_times.append(end_time)
                        else:
                            move_num.append( int(i / 2) + 1 )
                            move.append(str(move_text[i]).split("{")[0].split("...")[-1])
                            clk.append(str(move_text[i]).split("%clk ")[-1].split("]}")[0])
                            urls.append(url)
                            end_times.append(end_time)






    print("---------")
    return move_num, move, clk, urls, end_times
