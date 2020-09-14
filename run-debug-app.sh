!#/bin/bash

source venv/bin/activate;
export FLASK_DEBUG=true;
export FLASK_APP=app;
flask run
