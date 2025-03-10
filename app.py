from flask import Flask, request, jsonify # Various flask modules
from init import app # Initialize Flask app
import db # Database
from bson import ObjectId # For using ObjectId in mongoDB
from datetime import datetime # For date and time operations
import logging # For logging achievements
from utils import prepare_for_json, JSONEncoder

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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Update flask JSON encoder to handle ObjectId
app.json_encoder = JSONEncoder

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

# Alternative method for getting detailed player stats including level, XP, achievements, and category progress
@app.route('/api/users/<user_id>/stats', methods=['GET'])
def get_player_stats(user_id):
    try:
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        # Get player's achievements count
        achievements_count = len(player.get('achievements', []))
        
        # Get streaks
        streaks = db.gamificationdb.streaks.find_one({'user_id': user_id, 'category': None})
        streak_days = streaks.get('current_streak', 0) if streaks else 0
        
        # Get quizzes completed and perfect scores from the results database (if available)
        # This might require cross-service communication
        quizzes_completed = player.get('quizzes_completed', 0)
        quizzes_perfect = player.get('perfect_scores', 0)
        
        # Get category progress
        category_levels = player.get('category_levels', {})
        category_progress = []
        
        for category, data in category_levels.items():
            category_progress.append({
                'category': category,
                'level': data.get('level', 1),
                'xp': data.get('xp', 0),
                'totalXpRequired': 500 * data.get('level', 1)  # Assuming 500 * level for next level
            })
            
        # Create response object with all player stats
        stats = {
            'level': player.get('current_level', 1),
            'xp': player.get('xp', 0),
            'totalXpRequired': 500 * player.get('current_level', 1),  # Assuming 500 * level for next level
            'streakDays': streak_days,
            'quizzesCompleted': quizzes_completed,
            'quizzesPerfect': quizzes_perfect,
            'totalAchievements': achievements_count,
            'categoryProgress': category_progress
        }
        
        return jsonify(stats), 200
    except Exception as e:
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
    
# Endpoint compatibility for user achievements (alias for existing endpoint)
@app.route('/api/users/<user_id>/achievements', methods=['GET'])
def get_user_achievements(user_id):
    """Get all achievements unlocked by a user"""
    try:
        # Get player data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        # Get earned achievement IDs
        earned_achievements_ids = player.get('achievements', [])
        
        # Get full achievement details
        achievements = []
        for achievement_id in earned_achievements_ids:
            achievement = db.gamificationdb.achievements.find_one({'achievement_id': achievement_id})
            if achievement:
                # Convert ObjectId to string
                achievement['_id'] = str(achievement['_id'])
                # Add date unlocked (assuming you store this information)
                achievement['dateUnlocked'] = achievement.get('date_unlocked', datetime.now().isoformat())
                achievements.append(achievement)
        
        return jsonify(achievements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Award achievement to player by user_id and achievement_id
@app.route('/api/player/<user_id>/achievements', methods=['POST'])
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
    
# Check for achievements based on player activity data submitted
@app.route('/api/player/<user_id>/check-achievements', methods=['POST']) 
def check_achievements(user_id):
    try:
        # Define data first before using it
        data = request.json
        awarded_achievements = []

        # Get player data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
        
        earned_achievements = player.get('achievements', [])

        # Get current stats
        quizzes_completed = player.get('quizzes_completed', 0)
        perfect_scores = player.get('perfect_scores', 0)
        current_level = player.get('current_level', 1)

        if data.get('perfect_score', False): # If perfect score, increment perfect scores
            logger.info(f"Perfect score detected for user {user_id}")
            perfect_scores += 1
            db.gamificationdb.players.update_one(
                {'user_id': user_id}, 
                {'$inc': {'perfect_scores': 1}}
            )
                
        
        # Update with new data if provided
        if data.get('quiz_completed', False):
            quizzes_completed += 1
            db.gamificationdb.players.update_one(
                {'user_id': user_id}, 
                {'$inc': {'quizzes_completed': 1}}
            )
        
        # Track unique categories
        if data.get('category'):
            category = data.get('category')
            db.gamificationdb.players.update_one(
                {'user_id': user_id},
                {'$addToSet': {'completed_categories': category}}  # $addToSet ensures uniqueness
            )
            # Re-fetch player to get updated categories
            player = db.gamificationdb.players.find_one({'user_id': user_id})
        
        # Get streak information
        streak_data = db.gamificationdb.streaks.find_one({'user_id': user_id, 'category': None})
        current_streak = streak_data.get('current_streak', 0) if streak_data else 0
            
        # Find applicable achievements that haven't been earned yet
        achievements = list(db.gamificationdb.achievements.find({
            'achievement_id': {'$nin': earned_achievements}
        }))
        
        for achievement in achievements:
            # Convert MongoDB ObjectId to string
            achievement['_id'] = str(achievement['_id'])
            conditions = achievement.get('condition', {})
            should_award = False
            
            # Check different condition types
            if 'quizzes_completed' in conditions and quizzes_completed >= conditions['quizzes_completed']:
                should_award = True
                
            elif 'perfect_score' in conditions and data.get('perfect_score', False):
                should_award = True
                
            elif 'perfect_scores' in conditions and perfect_scores >= conditions['perfect_scores']:
                should_award = True
                
            elif 'streak_days' in conditions and current_streak >= conditions['streak_days']:
                should_award = True
                
            elif 'level' in conditions and current_level >= conditions['level']:
                should_award = True
                
            elif 'time_under' in conditions and data.get('completion_time') and data.get('completion_time') < conditions['time_under']:
                should_award = True
                
            elif 'unique_categories' in conditions:
                unique_categories = len(player.get('completed_categories', []))
                if unique_categories >= conditions['unique_categories']:
                    should_award = True
            
            # Award achievement if conditions are met
            if should_award:
                # Log achievement award
                logger.info(f"Awarding achievement {achievement['title']} to user {user_id}")
                achievement_id = str(achievement['achievement_id'])
                # Award achievement to player
                db.gamificationdb.players.update_one(
                    {'user_id': user_id},
                    {'$addToSet': {'achievements': achievement_id},
                     '$inc': {'xp': achievement.get('xp_reward', 0)}}
                )
                
                # Create award result
                award_result = {
                    'achievement_id': achievement_id,
                    'title': achievement.get('title'),
                    'description': achievement.get('description'),
                    'xp_earned': achievement.get('xp_reward', 0)
                }
                awarded_achievements.append({
                    'achievement': achievement,
                    'award_result': award_result
                })
        
        return jsonify({
            'awarded_achievements': prepare_for_json(awarded_achievements),
            'stats': {
                'quizzes_completed': quizzes_completed,
                'perfect_scores': perfect_scores,
                'streak': current_streak,
                'level': current_level
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Debug endpoint to see a player's earned achievements with details
@app.route('/api/debug/player/<user_id>/achievements', methods=['GET'])
def debug_player_achievements(user_id):
    """Debug endpoint to see a player's earned achievements with details"""
    try:
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        earned_achievement_ids = player.get('achievements', [])
        
        # Get full achievement details
        earned_achievements = []
        for aid in earned_achievement_ids:
            achievement = db.gamificationdb.achievements.find_one({'achievement_id': aid})
            if achievement:
                achievement['_id'] = str(achievement['_id'])
                earned_achievements.append(achievement)
        
        # Get unearned achievements
        unearned_achievements = list(db.gamificationdb.achievements.find({
            'achievement_id': {'$nin': earned_achievement_ids}
        }))
        for achievement in unearned_achievements:
            achievement['_id'] = str(achievement['_id'])
            
        return jsonify({
            'player_id': user_id,
            'earned_count': len(earned_achievements),
            'earned_achievements': earned_achievements,
            'unearned_count': len(unearned_achievements),
            'unearned_achievements': unearned_achievements
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Streak Endpoints

# Update player streak by user_id
@app.route('/api/player/<user_id>/streak', methods=['POST'])
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


# Challenge Endpoints

# Get all challenges from database
@app.route('/api/challenges', methods=['GET']) 
def get_active_challenges(): 
    try: 
        # Get date
        today = datetime.now()

        # Find active challenges
        challenges = list(db.gamificationdb.challenges.find({
            'start_date': {'$lte': today}, # Start date is less than or equal to today
            'end_date': {'$gte': today} # End date is greater than or equal to today
        }))

        # Convert object Ids to strings
        for challenge in challenges:
            challenge['_id'] = str(challenge['_id'])

        return jsonify(challenges), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Complete challenge by user_id and challenge_id
@app.route('/api/player/<user_id>/challenges/<challenges_id>', methods=['POST']) 
def complete_challenge(user_id, challenge_id): 
    try: 
        # Find challenge
        challengeData = db.gamificationdb.challenges.find_one({'challenge_id': challenge_id})
        if not challengeData: # Return error if challenge not found
            return jsonify({'error': 'Challenge not found'}), 404
        
        # Find player
        playerData = db.gamificationdb.players.find_one({'user_id': user_id})
        if not playerData: # Return error if player not found
            return jsonify({'error': 'Player not found'}), 404
        
        # Check if player has already completed the challenge
        completedChallenges = playerData.get('completed_challenges', [])
        if challenge_id in completedChallenges:
            return jsonify({'error': 'Challenge already completed'}), 400
        
        # Award player
        xp_reward = challengeData.get('xp_reward', 0) # Get xp reward from challenge
        badge_rewards = challengeData.get('reward_badges', []) # Get badge rewards from challenge

        update_fields = { # Update fields for player document
            '$push': {'completed_challenges': challenge_id},
            '$inc': {'xp': xp_reward}
        }

        if badge_rewards: 
            if 'badges' not in playerData: 
                update_fields['$set'] = {'badges': badge_rewards}
            else:
                update_fields['$push']['badges'] = {'$each': badge_rewards}

        # Update player document in db
        db.gamificationdb.players.update_one({'user_id': user_id}, update_fields)

        response = { # Response data, including challenge id, xp reward and badge rewardss
            'challenge_completed': challenge_id,
            'xp_earned': xp_reward,
            'badges_earned': badge_rewards
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Get tracked challenges for a user
@app.route('/api/users/<user_id>/tracked-challenges', methods=['GET'])
def get_tracked_challenges(user_id):
    """Get all challenges being tracked by a user"""
    try:
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        tracked_challenges_ids = player.get('tracked_challenges', [])
        tracked_challenges = []
        
        # Get complete challenge information with progress
        for challenge_id in tracked_challenges_ids:
            challenge = db.gamificationdb.challenges.find_one({'_id': ObjectId(challenge_id)})
            if challenge:
                # Convert ObjectId to string
                challenge['_id'] = str(challenge['_id'])
                
                # Add progress information
                challenge_progress = db.gamificationdb.challenge_progress.find_one({
                    'user_id': user_id,
                    'challenge_id': challenge_id
                })
                
                if challenge_progress:
                    challenge['progress'] = challenge_progress.get('progress', 0)
                else:
                    challenge['progress'] = 0
                    
                tracked_challenges.append(challenge)
        
        return jsonify(tracked_challenges), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Track a challenge
@app.route('/api/users/<user_id>/tracked-challenges', methods=['POST'])
def track_challenge(user_id):
    """Add a challenge to user's tracked challenges"""
    try:
        data = request.json
        challenge_id = data.get('challengeId')
        
        if not challenge_id:
            return jsonify({'error': 'Challenge ID is required'}), 400
            
        # Verify the challenge exists
        challenge = db.gamificationdb.challenges.find_one({'_id': ObjectId(challenge_id)})
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
            
        # Verify the user exists
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        # Check if user is already tracking this challenge
        tracked_challenges = player.get('tracked_challenges', [])
        if challenge_id in tracked_challenges:
            return jsonify({'message': 'Challenge is already being tracked'}), 200
            
        # Check if user has reached the maximum number of tracked challenges (3)
        if len(tracked_challenges) >= 3:
            return jsonify({'error': 'Maximum number of tracked challenges reached (3)'}), 400
            
        # Add challenge to tracked challenges
        db.gamificationdb.players.update_one(
            {'user_id': user_id}, 
            {'$push': {'tracked_challenges': challenge_id}}
        )
        
        # Initialize challenge progress
        db.gamificationdb.challenge_progress.insert_one({
            'user_id': user_id,
            'challenge_id': challenge_id,
            'progress': 0,
            'last_updated': datetime.now()
        })
        
        return jsonify({
            'message': 'Challenge is now being tracked',
            'challenge_id': challenge_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Untrack a challenge
@app.route('/api/users/<user_id>/tracked-challenges/<challenge_id>', methods=['DELETE'])
def untrack_challenge(user_id, challenge_id):
    """Remove a challenge from user's tracked challenges"""
    try:
        # Verify the user exists
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        # Remove challenge from tracked challenges
        db.gamificationdb.players.update_one(
            {'user_id': user_id}, 
            {'$pull': {'tracked_challenges': challenge_id}}
        )
        
        # Remove challenge progress
        db.gamificationdb.challenge_progress.delete_one({
            'user_id': user_id,
            'challenge_id': challenge_id
        })
        
        return jsonify({
            'message': 'Challenge is no longer being tracked',
            'challenge_id': challenge_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Redirect completion endpoint to match frontend expectations
@app.route('/api/challenges/<challenge_id>/complete', methods=['POST'])
def complete_challenge_redirect(challenge_id):
    """Complete a challenge (new URL format)"""
    try:
        data = request.json
        user_id = data.get('userId')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        # Use the existing function by calling it directly
        return complete_challenge(user_id, challenge_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get player stats for a specific category
@app.route('/api/player/<user_id>/category/<category>', methods=['GET'])
def get_category_stats(user_id, category):
    """Get player's stats for a specific category"""
    try:
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        category_levels = player.get('category_levels', {})
        category_level = category_levels.get(category, {'level': 1, 'xp': 0})
        
        # Get category-specific achievements and badges
        achievements = list(db.gamificationdb.achievements.find({'category': category}))
        for achievement in achievements:
            achievement['_id'] = str(achievement['_id'])
            achievement['earned'] = achievement['_id'] in player.get('achievements', [])
            
        badges = list(db.gamificationdb.badges.find({'category': category}))
        for badge in badges:
            badge['_id'] = str(badge['_id'])
            badge['earned'] = badge['_id'] in player.get('badges', [])
            
        return jsonify({
            'level': category_level.get('level', 1),
            'xp': category_level.get('xp', 0),
            'next_level_xp': 500 * category_level.get('level', 1),
            'achievements': achievements,
            'badges': badges
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Initialize achievements in database
def init_achievements():
    """Initialize achievements in the database on app startup"""
    try:
        # Only run if achievements collection is empty
        if db.gamificationdb.achievements.count_documents({}) == 0:
            from seed_achievements import seed_achievements
            seed_achievements()
    except Exception as e:
        print(f"Error initializing achievements: {str(e)}")

# Call the initialization function
init_achievements()

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=9091) 
