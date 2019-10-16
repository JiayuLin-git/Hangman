#Environment
Python3.7

Module used in this program:
- json
- re
- requests
- sys

If you are not install them, run command below in the command line: 
> pip install [module name] 

#Running method
Download programming file to local computer, unzip and run it from command line:
> python ./hangman.py [input email address] [input rounds of playing]

#Gaming logic
The whole program can be divided into four parts:
- DictManager

    DictManager is the class to manager and process dictionary using in the game, 
    which include the whole dictionary and the dictionary package get from web service.
- RequestManager

    RequestManager is the class to deal with the webservice, include get and update
    the json package and load them to dictionary type object. In case of error,
    get and update functions have three time of retry.
- RoundManager

    RoundManager is the class to manage every round we plays.\
    It include the main logic of the whole game.\
    Every time we have a try of a letter, and get a update state of guessing result,
    if the new state is different from the old one, make this guess correct.\
    Seperate the state into several words, from the letter's position in the words, 
    we can select some words which meet the requirement to create a smaller dictionary,
    then we could use this new dictionary to calculate probability of every remaining letter.
    The letter which get highest probability would become word we guess next.\
    Also, when the status turns to 'Dead' or 'Free', this round is over.
    
          
- RunManager
    
    RunManager is the class to manager the whole games with multiple rounds.
