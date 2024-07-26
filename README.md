# chess_analytics_pipeline

## Purpose

This repo aims at building the game analytics work of the RCC chess players.

## Description

1. .github/workflows

It stores the schedule and workflow of github actions. One can adjust the time for the automated pipeline to work.

2. .ipython_checkpoints

It stores the status of the chess_game_result.ipynb file

3. test notebooks

Storing ipynb for testing and exploratory purpose

4. deprecated
   
code or data that are not any longer in use

5. output data

6. src

files storing python code

7. requirements.txt

It stores the python package that need to be installed

8. status.log

Log the message when the workflow runs.


## Project
Generate game results for BO, BP and talented 2023 fall classes

RCC club have weekly round-robin chess games for each class. Currently, teaching assistants need to visit the profile page of chess.com of each player to record the game result into a google spreadsheet. This project aims to automate the work by calling chess.com API to get the games data and log it into a csv file which teaching assistants can download from this repo and upload to the google spreadsheet. Sending game and result dataframe to [RCC_tianmin_students_games](https://docs.google.com/spreadsheets/d/1YbU3GZq58mWu5Kl4l4gPhq96aohmk8gFxbzGr6cpA7o/edit#gid=1280403112) 

## Pipeline

[link](https://drive.google.com/file/d/1scKuLYX9Ru3brCN58rqtqh7iPX5nqGgv/view?usp=sharing)

## Contact person

tianminlyu@gmail.com
