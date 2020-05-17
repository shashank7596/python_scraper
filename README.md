Scraper Libraries.

Windows

export PYTHONPATH=/path/to/parent:$PYTHONPATH   

### Run below venv commands only if you want to run in virtual environment otherwise ignore
python -m virtualenv venv
source venv/Scripts/activate
###

pip3 install -r requirements.txt #Installs all the required python packages
python setup.py develop #Setup the API and required configurations to run web service. "develop" is the environment name passed as argument to the api to setup the required api environment
python rest/app.py

Linux/Cent OS Machine

export PYTHONPATH=/path/to/parent:$PYTHONPATH   

### Run below venv commands only if you want to run in virtual environment otherwise ignore
virtualenv -p python venv
source venv/bin/activate
###

pip3 install -r requirements.txt
python setup.py develop
python rest/app.py