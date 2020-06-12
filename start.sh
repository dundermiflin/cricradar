#!/bin/bash
#sudo services mongodb start
source ../bin/activate
cd backend/
python server.py &
cd ../frontend
npm start
