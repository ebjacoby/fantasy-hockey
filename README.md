# fantasy_hockey.py
fantasy hockey tool

## Setup

### Repo Setup

Navigate to https://github.com/ebjacoby/fantasy-hockey and clone the repository to your desktop.


After cloning the repo (make sure to save it in a directory similar to that shown below), navigate there from the command-line:

```sh
cd ~/Desktop/Github/fantasy-hockey
```

### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n hockey-env python=3.7 # (first time only)
conda activate hockey-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file, included in the cloned repository:

```sh
pip install -r requirements.txt
```
If the requirements.txt does not properly install for whatever reason, each quality must be installed by pip separately... :)

### API/ENV Setup

There are no APIs to set up! This app draws data from another users API, readable in JSON format. 

There is an environemnt variable named 'ID.env' but this can remain static - it is only used to acquire headers for a dictionary, created by the app. It, therefore, does not need to be included in the .gitignore. 

Before you run, however, please input the following in the command line:

```sh
export ID=8473544
```

(For information's sake) The specifications for the api used to form the data in JSON format is shown below:
'https://github.com/erunion/sport-api-specifications/tree/master/nhl'


## Run the Apps

There are two apps to run:

### 1. fantasy_hockey.py

Note, this app will take some time to work (approx 2-3 min)

To run the app, type the following into the command line:

```sh
python app/fantasy_hockey.py
```

The app will request an input for the season (specific format: 'YYYYYYYY' or e.g. '20192020') for which you would like to predict player rankings (according to goals, assists, shots on goal, blocks, etc). The output is given in a csv file in the 'data' directory. It will overwrite each time the app is run. 

### 2. player_search.py

To run the app, type the following in to the command line:

```sh
python app/player_search.py
```

The app will request input from the user. It will require the season (specific format: 'YYYYYYYY' or e.g. '20192020') for which you would like to predict player stats, and the player (the input will be matched up against a list of current players) for which the program will gather the stats (for 3 seasons). The app will display an output on the command line, detailing the predictions for this player for the year requested.

