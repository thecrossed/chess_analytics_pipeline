import logging
import logging.handlers
import os
import io
import pandas as pd
import numpy as np
import requests
import json
# from chessdotcom import get_player_profile, get_player_stats, get_player_game_archives  (not working)
import chess.pgn
from converter.pgn_data import PGNData
import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import sys
import chess_dot_com_api as capi
import googlesheet as g
import data
import ratings
from pgn_parser import pgn, parser

    
# main function    
def main(): 
    collected_data = data.game_data_collect()
    df = g.to_pandas_df(collected_data)
    print("game is converted into pandas")
    print(df.head(1)
    g.upload_df("2023fall_game", df, '1YbU3GZq58mWu5Kl4l4gPhq96aohmk8gFxbzGr6cpA7o')

    collected_move = data.move_data_collect()
    df_move = g.to_pandas_move(collected_move)
    print("move is converted into pandas")
    g.upload_df("2023fall_move", df_move, '1YbU3GZq58mWu5Kl4l4gPhq96aohmk8gFxbzGr6cpA7o')

    rating = ratings.rating_collect()
    df_rating = ratings.to_pandas_rating(rating)
    print("rating is converted into pandas")
    print(df_rating.head(1)
    g.upload_df("rcc_rating", df_rating, '1YbU3GZq58mWu5Kl4l4gPhq96aohmk8gFxbzGr6cpA7o')

if __name__ == "__main__":
    main()

