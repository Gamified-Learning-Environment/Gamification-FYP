from flask import Flask, request, jsonify # Various flask modules
from init import app # Initialize Flask app
import db # Database
from bson import ObjectId # For using ObjectId in mongoDB

# Test route to verify connection
@app.route('/', methods=['GET'])
def home():
    print('Successful connection to Gamification Service')
    return "Gamification Service"

# Import models
#from models.achievement import Achievement
#from models.badge import Badge
#from models.player import Player
#from models.challenge import Challenge
#from models.streak import Streak





# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=9091) 
