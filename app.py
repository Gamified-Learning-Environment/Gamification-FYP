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
from models.achievement import Achievement
from models.badge import Badge
from models.player import Player
from models.challenge import Challenge
from models.streak import Streak

# Player Endpoints

# Get player profile by user_id, create new player if it doesn't exist
@app.route('/api/player/<user_id>', methods=['GET'])
def get_player(user_id): 
    try:
        # Get player data from the database 
        playerData = db.gamificationdb.players.find_one({'user_id': user_id})
        
        if playerData: # If player data is found, return it
            return jsonify(playerData), 200
        else: 
            # Create new player profile if it doesn't exist
            newPlayer = Player(user_id=user_id, username=request.args.get('username', 'Player')).to_dict()
            db.gamificationdb.players.insert_one(newPlayer) # Insert new player into database
            return jsonify(newPlayer), 201 # Return the new player profile, 201 for created status
    except Exception as e: # Catch any exceptions and return error
        return jsonify({'error': str(e)}), 500 
    
# Update player xp by user_id and xp amount
@app.route('/api/player/<user_id>/xp', methods=['POST'])
def add_player_xp(user_id): 
    try: 
        data = request.json
        xpAmount = data.get('xp', 0) # Get xp amount from request data

        # Find player
        playerData = db.gamificationdb.players.find_one({'user_id': user_id})
        if not playerData: # If player not found, return error
            return jsonify({'error': 'Player not found'}), 404
        
        # Update player xp
        current_xp = playerData.get('xp', 0) # Get current xp
        current_level = playerData.get('current_level', 1) # Get current level
        new_xp = current_xp + xpAmount # Calculate new xp

        # Check for level up
        level_up = False # Initialize level up flag
        while True: # Loop to check for level up
            next_level_xp = 1000 * (current_level * 0.5)
            if new_xp >= next_level_xp: # If xp is greater than next level xp, level up
                current_level += 1
                new_xp -= next_level_xp
                level_up = True
            else: # If xp is not enough for level up, break loop
                break

        # Update player document in db
        db.gamificationdb.players.update_one({'user_id': user_id}, {
            '$set': {'xp': new_xp, 'current_level': current_level}
        })

        response = { # Response data, including new xp, level and level up flag
            'new_xp': new_xp,
            'new_level': current_level,
            'level_up': level_up
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Achievement Endpoints

# Get all achievements from database, return as JSON
@app.route('/api/achievements', methods=['GET'])
def get_achievements():
    try:
        achievements = list(db.gamificationdb.achievements.find({})) # Get all achievements from database
        for achievement in achievements: # Convert ObjectId to string for JSON serialization
            achievement['_id'] = str(achievement['_id'])
        return jsonify(achievements), 200
    except Exception as e: # Catch any exceptions and return error
        return jsonify({'error': str(e)}), 500
    
# Get player achievements by user_id
@app.route('/api/player/<user_id>/achievements', methods=['GET']) 
def get_player_achievements(user_id): 
    try: 
        playerData = db.gamificationdb.players.find_one({'user_id': user_id}) # Find player
        if not playerData: # Return error if player not found
            return jsonify({'error': 'Player not found'}), 404
        
        earnedAchievements = playerData.get('achievements', []) # Get player's earned achievements
        return jsonify(earnedAchievements), 200
    except Exception as e: # Catch any exceptions and return error
        return jsonify({'error': str(e)}), 500
    
# Award achievement to player by user_id and achievement_id
@app.route('api/player/<user_id>/achievements', methods=['POST'])
def award_achievement(user_id):
    try: 
        data = request.json
        achievement_id = data.get('achievement_id') # Get achievement id from request data

        # Find achievement
        achievementData = db.gamificationdb.achievements.find_one({'achievement_id': achievement_id})
        if not achievementData: # Return error if achievement not found
            return jsonify({'error': 'Achievement not found'}), 404
        
        # Find player
        playerData = db.gamificationdb.players.find_one({'user_id': user_id})
        if not playerData: # Return error if player not found
            return jsonify({'error': 'Player not found'}), 404
        
        # Check if player has already earned the achievement
        if achievement_id in playerData.get('achievements', []):
            return jsonify({'error': 'Achievement already earned'}), 400
        
        # Award achievement to player and xp
        xp_reward = achievementData.get('xp_reward', 0) # Get xp reward from achievement

        # Update player document in db
        db.gamificationdb.players.update_one({'user_id': user_id}, {
            '$push': {'achievements': achievement_id},
            '$inc': {'xp': xp_reward}
        })

        # Check for level up
        current_xp = playerData.get('xp', 0) + xp_reward # Get current xp
        current_level = playerData.get('current_level', 1) # Get current level
        level_up = False # Initialize level up flag

        while True: # Loop to check for level up
            next_level_xp = 1000 * (current_level * 0.5)
            if current_xp >= next_level_xp: # If xp is greater than next level xp, level up
                current_level += 1
                level_up = True
            else: # If xp is not enough for level up, break loop
                break
        
        if level_up: # Update player level if level up
            db.gamificationdb.players.update_one(
                {'user_id': user_id},
                {'$set': {'current_level': current_level}}
            )
        
        response = { # Response data, including achievement, xp reward, level up flag and new level
            'achievement': achievementData, # Return achievement data
            'xp_earned': xp_reward, 
            'level_up': level_up, # Return level up flag
            'new_level': current_level if level_up else None # Return new level if level up achieved
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Streak Endpoints

@app.route('api/player/<user_id>/streak', methods=['POST'])
def update_player_streak(user_id): 
    try: 
        data = request.json
        category = data.get('category', None) # Optional category for streak

        # Find existing streak
        query = {'user_id': user_id}
        if category: # If category is provided, add to query
            query['category'] = category 

        # Get streak data from database
        streakData = db.gamificationdb.streaks.find_one(query)

        if streakData: # If streak data found

            streak = Streak( # Create streak object from data
                user_id=streakData.get('user_id'),
                category=streakData.get('category'),
                current_streak=streakData.get('current_streak', 0),
                highest_streak=streakData.get('highest_streak', 0),
                last_activity_date=streakData.get('last_activity_date')
            )
            streak.update_streak() # Update streak

            # Save updated streak
            db.gamificationdb.streaks.update_one(
                query,  # Query to find streak
                {'$set': streak.to_dict()} # Update streak data
            )

            return jsonify(streak.to_dict()), 200 # Return updated streak data with success status
        else:
            # Create new streak
            streak = Streak(
                user_id=user_id,
                category=category,
                current_streak=1,
                highest_streak=1
            )

            # Save new streak
            db.gamificationdb.streaks.insert_one(streak.to_dict())

            return jsonify(streak.to_dict()), 201 # Return new streak data with created status
    except Exception as e:
        return jsonify({'error': str(e)}), 500





# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=9091) 
