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
from models.streak import Streak

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Update flask JSON encoder to handle ObjectId
app.json_encoder = JSONEncoder

# Player Endpoints

# Get player profile by user_id, create new player if it doesn't exist
@app.route('/api/player/<user_id>/<username>', methods=['GET'])
def get_player(user_id, username): 
    try:
        # Get player data from the database 
        print(f"Retrieving player data with user_id: {user_id} and username: {username}")
        playerData = db.gamificationdb.players.find_one({'user_id': user_id})
        
        if playerData: # If player data is found, return it
            # Convert ObjectId to string before sending to JSON
            playerData['_id'] = str(playerData['_id'])
            # Process any other ObjectId fields
            return jsonify(prepare_for_json(playerData)), 200
        else: 
            print(f"Creating new player data for user_id: {user_id} with username: {username}")
            # Create new player profile if it doesn't exist
            newPlayer = Player(user_id=user_id, username=username).to_dict()
            db.gamificationdb.players.insert_one(newPlayer) # Insert new player into database
            return jsonify(newPlayer), 201 # Return the new player profile, 201 for created status
    except Exception as e: # Catch any exceptions and return error
        print(f"Error getting player with user_id {user_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500 

# Alternative method for getting detailed player stats including level, XP, achievements, and category progress
@app.route('/api/users/<user_id>/<username>/stats', methods=['GET'])
def get_player_stats(user_id, username):
    try:
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            print(f"Creating new player data for user_id: {user_id} with username: {username}")
            # Create new player profile if it doesn't exist
            newPlayer = Player(user_id=user_id, username=username).to_dict()
            db.gamificationdb.players.insert_one(newPlayer) # Insert new player into database
            return jsonify(newPlayer), 201 # Return the new player profile, 201 for created status
            
        # Get player's achievements count
        achievements_count = len(player.get('achievements', []))
        
        # Get streaks
        streaks = db.gamificationdb.streaks.find_one({'user_id': user_id, 'category': None})
        streak_days = streaks.get('current_streak', 0) if streaks else 0
        
        # Get quizzes completed and perfect scores from the results database (if available)
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
                'totalXpRequired': 500 * data.get('level', 1)  # 500 * level for next level
            })
            
        # Create response object with all player stats
        stats = {
            'level': player.get('current_level', 1),
            'xp': player.get('xp', 0),
            'totalXpRequired': 500 * player.get('current_level', 1),  # 500 * level for next level
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
    

@app.route('/api/player/<user_id>/category/<category>/xp', methods=['POST'])
def add_category_xp(user_id, category):
    try: 
        data = request.json
        xpAmount = data.get('xp', 0)

        # Find Player
        playerData = db.gamificationdb.players.find_one({'user_id': user_id})
        if not playerData:
            return jsonify({'error': 'Player not found'}), 404
        
        # Convert to Player Object
        player = Player(
            user_id=playerData.get('user_id'),
            username=playerData.get('username'),
            current_level=playerData.get('current_level', 1),
            xp=playerData.get('xp', 0),
            category_levels=playerData.get('category_levels', {})
        )

        # Add XP to category
        result = player.add_category_xp(category, xpAmount)

        # Update player document in db
        db.gamificationdb.players.update_one(
            {'user_id': user_id},
            {'$set': {'category_levels': player.category_levels}}
        )

        # Check for category level badges if level up occurred
        awarded_badges = []
        if result["level_up"]:
            new_level = result["new_level"]
            
            # Find badges that match this category level milestone
            level_badges = list(db.gamificationdb.badges.find({
                "category_type": category.lower(),
                "level_requirement": new_level
            }))
            
            for badge in level_badges:
                if badge["badge_id"] not in playerData.get("badges", []):
                    # Award the badge
                    db.gamificationdb.players.update_one(
                        {'user_id': user_id},
                        {'$addToSet': {'badges': badge["badge_id"]}}
                    )
                    badge["_id"] = str(badge["_id"])
                    badge["earned"] = True
                    awarded_badges.append(badge)

        # Return updated info
        return jsonify({
            "category": category,
            "level_up": result["level_up"],
            "new_level": result["new_level"],
            "new_xp": result["new_xp"],
            "next_level_xp": 500 * result["new_level"]  # Same calculation as in add_category_xp
        }), 200
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
@app.route('/api/player/<user_id>/achievements', methods=['GET'])
def get_user_achievements(user_id):
    """Get all achievements unlocked by a user"""
    try:
        # Get player data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            # Return empty array instead of 404 to prevent frontend errors
            return jsonify([{'error': 'Player not found'}]), 404
            
        # Get earned achievement IDs
        earned_achievements_ids = player.get('achievements', [])
        
        # Get full achievement details
        achievements = []
        for achievement_id in earned_achievements_ids:
            achievement = db.gamificationdb.achievements.find_one({'achievement_id': achievement_id})
            if achievement:
                # Convert ObjectId to string for JSON serialization
                achievement['_id'] = str(achievement['_id'])
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
        awarded_badges = []

        # Initialize category_progress here so it's always defined
        category_progress = {
            'category': None,
            'level_up': False,
            'new_level': 1,
            'xp_earned': 0
        }

        # Get player data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
        
        earned_achievements = player.get('achievements', [])
        earned_badges = player.get('badges', [])

        # Get current stats
        quizzes_completed = player.get('quizzes_completed', 0)
        perfect_scores = player.get('perfect_scores', 0)
        current_level = player.get('current_level', 1)

        print(f"Achievement check data: {data}")
        print(f"Perfect score flag: {data.get('perfect_score', False)}")

        if data.get('perfect_score', False): # If perfect score, increment perfect scores
            logger.info(f"Perfect score detected for user {user_id}")
            perfect_scores += 1
            db.gamificationdb.players.update_one(
                {'user_id': user_id}, 
                {'$inc': {'perfect_scores': 1}}
            )

            # Check for Perfect Score badge
            perfect_badge = db.gamificationdb.badges.find_one({'name': 'Perfect Score'})
            if perfect_badge and perfect_badge['badge_id'] not in earned_badges:
                logger.info(f"Awarding Perfect Score badge to user {user_id}")
                
                # Award badge to player
                db.gamificationdb.players.update_one(
                    {'user_id': user_id},
                    {'$addToSet': {'badges': perfect_badge['badge_id']}}
                )
                
                # Format badge for response
                perfect_badge['_id'] = str(perfect_badge['_id'])
                perfect_badge['earned'] = True
                awarded_badges.append(perfect_badge)

        # Force check for perfect score achievements
        perfect_score_achievements = list(db.gamificationdb.achievements.find({
            'achievement_id': {'$nin': earned_achievements},
            'condition.perfect_score': True
        }))

        # Explicitly award perfect score achievements
        for achievement in perfect_score_achievements:
            achievement['_id'] = str(achievement['_id'])
            achievement_id = str(achievement['achievement_id'])
            
            # Award achievement to player
            db.gamificationdb.players.update_one(
                {'user_id': user_id},
                {'$addToSet': {'achievements': achievement_id},
                '$inc': {'xp': achievement.get('xp_reward', 0)}}
            )
            
            # Add to awarded achievements
            award_result = {
                'achievement_id': achievement_id,
                'title': achievement.get('title'),
                'description': achievement.get('description'),
                'icon': achievement.get('icon', '🏆'),
                'xp_earned': achievement.get('xp_reward', 0)
            }
            awarded_achievements.append({
                'achievement': achievement,
                'award_result': award_result
            })
            logger.info(f"Awarded perfect score achievement {achievement['title']} to user {user_id}")
                
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

        # Check for category level achievements
        category_levels = player.get('category_levels', {})
        highest_category_level = 0
        categories_at_level_3 = 0
        
        for cat, data in category_levels.items():
            level = data.get('level', 1)
            highest_category_level = max(highest_category_level, level)
            if level >= 3:
                categories_at_level_3 += 1
        
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

            elif 'time_under' in conditions and data.get('completion_time') and data.get('completion_time') < conditions['time_under']:
                should_award = True
                
            elif 'unique_categories' in conditions:
                unique_categories = len(player.get('completed_categories', []))
                if unique_categories >= conditions['unique_categories']:
                    should_award = True
                    
            # Category level achievement check
            elif 'category_level' in conditions:
                required_level = conditions['category_level']
                if highest_category_level >= required_level:
                    should_award = True
            
            # Check for diverse categories achievement
            elif 'diverse_categories' in conditions:
                condition = conditions['diverse_categories']
                required_level = condition.get('level', 3)
                required_count = condition.get('count', 5)
                
                if categories_at_level_3 >= required_count:
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

                # Only check for matching badges for achievements that were just awarded
                matching_badge = db.gamificationdb.badges.find_one({'name': achievement.get('title')})
                if matching_badge and matching_badge['badge_id'] not in earned_badges:
                    logger.info(f"Awarding {matching_badge['name']} badge to user {user_id}")
                
                # Award badge to player
                db.gamificationdb.players.update_one(
                    {'user_id': user_id},
                    {'$addToSet': {'badges': matching_badge['badge_id']}}
                )
                
                # Format badge for response
                matching_badge['_id'] = str(matching_badge['_id'])
                matching_badge['earned'] = True
                awarded_badges.append(matching_badge)

             # Add category XP if category is provided
            category = data.get('category')
            if category and data.get('quiz_completed', False):
                # Calculate category XP - can be based on score percentage
                score_percentage = data.get('score_percentage', 0)
                category_xp = int(50 + (score_percentage * 0.5))  # Base XP + bonus based on score
                
                # Find player
                player_doc = db.gamificationdb.players.find_one({'user_id': user_id})
                if player_doc:
                    player = Player(
                        user_id=player_doc['user_id'],
                        username=player_doc.get('username'),
                        current_level=player_doc.get('current_level', 1),
                        xp=player_doc.get('xp', 0),
                        category_levels=player_doc.get('category_levels', {})
                    )
                    
                    # Add category XP
                    category_result = player.add_category_xp(category, category_xp)
                    
                    # Update database
                    db.gamificationdb.players.update_one(
                        {'user_id': user_id},
                        {'$set': {'category_levels': player.category_levels}}
                    )
                    
                    # Add category progress to response
                    category_progress = {
                        'category': category,
                        'level_up': category_result['level_up'],
                        'new_level': category_result['new_level'],
                        'xp_earned': category_xp
                    }
        
        return jsonify({
            'awarded_achievements': prepare_for_json(awarded_achievements),
            'awarded_badges': prepare_for_json(awarded_badges),
            'stats': {
                'quizzes_completed': quizzes_completed,
                'perfect_scores': perfect_scores,
                'streak': current_streak,
                'level': current_level,
                'category_progress': category_progress
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


# Badge Endpoints

@app.route('/api/player/<user_id>/badges', methods=['GET'])
def get_player_badges(user_id):
    try:
        # Get player data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify([]), 200  # Return empty array instead of 404 for frontend compatibility
            
        # Get earned badge IDs
        earned_badge_ids = player.get('badges', [])
        
        # Get all badges
        all_badges = list(db.gamificationdb.badges.find({}))
        
        # Format badges with earned status
        formatted_badges = []
        for badge in all_badges:
            badge['_id'] = str(badge['_id'])
            badge['earned'] = badge['badge_id'] in earned_badge_ids
            formatted_badges.append(badge)
        
        return jsonify(formatted_badges), 200
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


# Campaign Endpoints

# Get all campaigns
@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    try:
        # Get the user's level if a user_id is provided
        user_id = request.args.get('user_id')
        user_level = 1
        
        if user_id:
            player = db.gamificationdb.players.find_one({'user_id': user_id})
            if player:
                user_level = player.get('current_level', 1)
        
        # Find campaigns that the user has the required level for
        campaigns = list(db.gamificationdb.campaigns.find({
            'required_level': {'$lte': user_level}
        }))
        
        # Convert ObjectIds to strings
        for campaign in campaigns:
            campaign['_id'] = str(campaign['_id'])
        
        return jsonify(campaigns), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get campaign by ID
@app.route('/api/campaigns/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    try:
        campaign = db.gamificationdb.campaigns.find_one({'campaign_id': campaign_id})
        
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
            
        campaign['_id'] = str(campaign['_id'])
        
        return jsonify(campaign), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all quests for a campaign
@app.route('/api/campaigns/<campaign_id>/quests', methods=['GET'])
def get_campaign_quests(campaign_id):
    try:
        quests = list(db.gamificationdb.quests.find({'campaign_id': campaign_id}).sort('order', 1))
        
        if not quests:
            return jsonify([]), 200
            
        for quest in quests:
            quest['_id'] = str(quest['_id'])
        
        return jsonify(quests), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get user's campaign progress
@app.route('/api/users/<user_id>/campaigns', methods=['GET'])
def get_user_campaigns(user_id):
    try:
        # Get player data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        # Get user campaign progress
        user_campaigns = list(db.gamificationdb.user_campaigns.find({'user_id': user_id}))
        
        # Format and return the data
        result = []
        for user_campaign in user_campaigns:
            campaign = db.gamificationdb.campaigns.find_one({'campaign_id': user_campaign.get('campaign_id')})
            
            if campaign:
                # Convert ObjectIds to strings
                campaign['_id'] = str(campaign['_id'])
                
                # Get completed quests
                completed_quests = user_campaign.get('completed_quest_ids', [])
                current_quest_id = user_campaign.get('current_quest_id')
                
                # Get all quests
                quests = list(db.gamificationdb.quests.find({
                    'campaign_id': campaign['campaign_id']
                }).sort('order', 1))
                
                # Format quests with completion status
                formatted_quests = []
                current_quest_index = 0
                
                for i, quest in enumerate(quests):
                    formatted_quest = {
                        'id': quest['quest_id'],
                        'title': quest['title'],
                        'description': quest['description'],
                        'completed': quest['quest_id'] in completed_quests,
                        'order': quest['order']
                    }
                    
                    if quest['quest_id'] == current_quest_id:
                        current_quest_index = i
                        
                    formatted_quests.append(formatted_quest)
                
                # Construct final response
                result.append({
                    'campaign': campaign,
                    'isActive': user_campaign.get('is_active', False),
                    'startedAt': user_campaign.get('started_at'),
                    'quests': formatted_quests,
                    'currentQuestIndex': current_quest_index,
                    'progress': len(completed_quests) / len(quests) * 100 if quests else 0
                })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Set active campaign
@app.route('/api/users/<user_id>/campaigns/<campaign_id>/activate', methods=['POST'])
def activate_campaign(user_id, campaign_id):
    try:
        # Get player data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
            
        # Debug output
        print(f"Looking for campaign with ID: {campaign_id}")
        
        # Try multiple ways to find the campaign
        campaign = None
        
        # First try with campaign_id field
        campaign = db.gamificationdb.campaigns.find_one({'campaign_id': campaign_id})
        
        # If not found, try with MongoDB _id (as ObjectId or string)
        if not campaign:
            try:
                from bson import ObjectId
                obj_id = ObjectId(campaign_id)
                campaign = db.gamificationdb.campaigns.find_one({'_id': obj_id})
                print(f"Found campaign using ObjectId: {campaign['title'] if campaign else 'Not found'}")
            except Exception as e:
                print(f"Error converting to ObjectId: {str(e)}")
        
        if not campaign:
            return jsonify({'error': 'Campaign not found', 'id_used': campaign_id}), 404
            
        # Check if player has required level
        if player.get('current_level', 1) < campaign.get('required_level', 1):
            return jsonify({'error': 'Player level too low for this campaign'}), 403
        
        # Set all campaigns to inactive
        db.gamificationdb.user_campaigns.update_many(
            {'user_id': user_id},
            {'$set': {'is_active': False}}
        )
        
        # Check if user already has this campaign
        user_campaign = db.gamificationdb.user_campaigns.find_one({
            'user_id': user_id,
            'campaign_id': campaign_id
        })
        
        if user_campaign:
            # Update existing campaign to active
            db.gamificationdb.user_campaigns.update_one(
                {'_id': user_campaign['_id']},
                {'$set': {'is_active': True}}
            )
        else:
            # Start new campaign
            first_quest = db.gamificationdb.quests.find_one(
                {'campaign_id': campaign_id},
                sort=[('order', 1)]
            )
            
            first_quest_id = first_quest['quest_id'] if first_quest else None
            
            # Create user campaign record
            user_campaign = {
                'user_id': user_id,
                'campaign_id': campaign_id,
                'is_active': True,
                'started_at': datetime.now().isoformat(),
                'completed_quest_ids': [],
                'current_quest_id': first_quest_id
            }
            
            db.gamificationdb.user_campaigns.insert_one(user_campaign)
        
        return jsonify({'success': True, 'message': 'Campaign activated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Debug endpoint to see all campaign IDs
@app.route('/api/debug/campaigns', methods=['GET'])
def debug_campaigns():
    """Debug endpoint to see all campaign IDs"""
    try:
        campaigns = list(db.gamificationdb.campaigns.find({}, {
            '_id': 1, 'campaign_id': 1, 'title': 1
        }))
        
        result = []
        for campaign in campaigns:
            result.append({
                'mongo_id': str(campaign['_id']),
                'campaign_id': campaign.get('campaign_id', 'not_set'),
                'title': campaign.get('title', 'Untitled')
            })
            
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Complete quest objective
@app.route('/api/users/<user_id>/quests/<quest_id>/progress', methods=['POST'])
def update_quest_progress(user_id, quest_id):
    try:
        data = request.json
        objective_type = data.get('objective_type')
        progress = data.get('progress', 1)
        
        # Get player data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player:
            return jsonify({'error': 'Player not found'}), 404
        
        # Get quest data
        quest = db.gamificationdb.quests.find_one({'quest_id': quest_id})
        if not quest:
            return jsonify({'error': 'Quest not found'}), 404
            
        # Get campaign data
        campaign = db.gamificationdb.campaigns.find_one({'campaign_id': quest['campaign_id']})
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
            
        # Get user campaign data
        user_campaign = db.gamificationdb.user_campaigns.find_one({
            'user_id': user_id,
            'campaign_id': quest['campaign_id']
        })
        
        if not user_campaign:
            return jsonify({'error': 'User is not participating in this campaign'}), 404
            
        if quest['quest_id'] != user_campaign.get('current_quest_id'):
            return jsonify({'error': 'This is not the current quest'}), 400
        
        if not objective_type:
            logger.error(f"Missing objective_type in request for quest {quest_id}")
            return jsonify({'error': 'Missing objective_type parameter'}), 400
            
        # Log progress updates for debugging
        logger.info(f"Updating quest {quest_id} progress for user {user_id} - Objective: {objective_type}, Progress: {progress}")
        
        # Track if any objectives were actually updated
        updated = False
        
        for objective in quest.get('objectives', []):
            if objective['type'] == objective_type:
                objective['current'] = min(objective.get('current', 0) + progress, objective['required'])
                updated = True
                
        if not updated:
            logger.warning(f"No matching objective of type {objective_type} found in quest {quest_id}")
            
        # Update objective progress
        objectives_completed = True
        quest_completed = False
        
        for objective in quest.get('objectives', []):
            if objective['type'] == objective_type:
                objective['current'] = objective.get('current', 0) + progress
                
                if objective['current'] < objective['required']:
                    objectives_completed = False
                    
        # If all objectives completed, mark quest as complete
        if objectives_completed:
            # Update user_campaigns record
            db.gamificationdb.user_campaigns.update_one(
                {'_id': user_campaign['_id']},
                {'$push': {'completed_quest_ids': quest['quest_id']}}
            )
            
            # Award XP
            xp_reward = quest.get('xp_reward', 50)
            current_xp = player.get('xp', 0)
            current_level = player.get('current_level', 1)
            
            # Add XP
            db.gamificationdb.players.update_one(
                {'user_id': user_id},
                {'$inc': {'xp': xp_reward}}
            )
            
            # Check for level up
            level_up = False
            new_level = current_level
            new_xp = current_xp + xp_reward
            
            while True:
                next_level_xp = 1000 * (new_level * 0.5)
                if new_xp >= next_level_xp:
                    new_level += 1
                    new_xp -= next_level_xp
                    level_up = True
                else:
                    break
                    
            if level_up:
                db.gamificationdb.players.update_one(
                    {'user_id': user_id},
                    {'$set': {'current_level': new_level, 'xp': new_xp}}
                )
            
            # Apply customization rewards
            if quest.get('customization_rewards'):
                # Update player's customization options
                db.gamificationdb.players.update_one(
                    {'user_id': user_id},
                    {'$push': {'customization_options': {'$each': quest['customization_rewards']}}}
                )
            
            # Set next quest as current if there is one
            next_quest = db.gamificationdb.quests.find_one({
                'campaign_id': quest['campaign_id'],
                'order': {'$gt': quest['order']}
            }, sort=[('order', 1)])
            
            if next_quest:
                db.gamificationdb.user_campaigns.update_one(
                    {'_id': user_campaign['_id']},
                    {'$set': {'current_quest_id': next_quest['quest_id']}}
                )
                
                quest_completed = True
            else:
                # Campaign completed
                # Award campaign completion rewards
                campaign_xp = campaign.get('xp_reward', 100)
                
                # Add campaign XP
                db.gamificationdb.players.update_one(
                    {'user_id': user_id},
                    {'$inc': {'xp': campaign_xp}}
                )
                
                # Apply campaign customization rewards
                if campaign.get('customization_rewards'):
                    db.gamificationdb.players.update_one(
                        {'user_id': user_id},
                        {'$push': {'customization_options': {'$each': campaign['customization_rewards']}}}
                    )
                
                quest_completed = True
        
        # Save updated quest
        db.gamificationdb.quests.update_one(
            {'quest_id': quest_id},
            {'$set': {'objectives': quest['objectives']}}
        )
        
        return jsonify({
            'success': True,
            'quest_completed': quest_completed,
            'objectives_completed': objectives_completed
        }), 200
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

# Initialize campaigns in database
def init_campaigns():
    """Initialize campaigns in the database on app startup"""
    try:
        # Only run if campaigns collection is empty
        if db.gamificationdb.campaigns.count_documents({}) == 0:
            from seed_campaigns import seed_campaigns
            seed_campaigns()
    except Exception as e:
        print(f"Error initializing campaigns: {str(e)}")


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get all players sorted by various stats for the leaderboard"""
    try:
        # Get all players from the database
        players = list(db.gamificationdb.players.find({}))
        
        # Prepare player data for leaderboard
        leaderboard_data = []
        for player in players:
            # Convert ObjectId to string for JSON serialization
            player['_id'] = str(player['_id'])
            
            # Create a leaderboard entry with necessary fields
            leaderboard_entry = {
                '_id': player['_id'],
                'user_id': player['user_id'],
                'username': player.get('username', 'Unknown Player'),
                'level': player.get('current_level', 1),
                'xp': player.get('xp', 0),
                'streakDays': 0,  # Will be populated below
                'quizzesCompleted': player.get('quizzes_completed', 0),
                'quizzesPerfect': player.get('perfect_scores', 0),
                'totalAchievements': len(player.get('achievements', [])),
                'profileImage': player.get('profile_image', None),
                'imageUrl': player.get('image_url', None)
            }

            try:
                user_data = db.userdb.usercollection.find_one({'_id': ObjectId(player['user_id'])})
                if user_data and 'imageUrl' in user_data and not leaderboard_entry['profileImage']:
                    leaderboard_entry['imageUrl'] = user_data['imageUrl']
            except Exception as e:
                app.logger.error(f"Error fetching user details for leaderboard: {e}")
            
            # Get player's current streak if available
            streak = db.gamificationdb.streaks.find_one({
                'user_id': player['user_id'],
                'category': None  # Get the overall streak, not category-specific
            })
            if streak:
                leaderboard_entry['streakDays'] = streak.get('current_streak', 0)
            
            leaderboard_data.append(leaderboard_entry)
        
        return jsonify(leaderboard_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/player/<user_id>/customization', methods=['GET'])
def get_player_customization(user_id):
    try:
        # Get player customization data
        player = db.gamificationdb.players.find_one({'user_id': user_id})
        if not player or 'customization' not in player:
            return jsonify({
                'theme': {
                    'primaryColor': '#8b5cf6',
                    'accentColor': '#f0abfc',
                    'cardStyle': 'default',
                    'showLevel': True,
                    'showStreaks': True,
                    'showAchievements': True,
                    'backgroundPattern': 'none',
                    'fontStyle': 'default'
                },
                'displayBadges': []
            }), 200
        
        return jsonify(player['customization']), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/player/<user_id>/customization', methods=['POST'])
def update_player_customization(user_id):
    try:
        # Get request data
        customization_data = request.json
        
        # Validate the data (simplified validation)
        if not isinstance(customization_data, dict):
            return jsonify({'error': 'Invalid customization data'}), 400
        
        # Update player customization
        result = db.gamificationdb.players.update_one(
            {'user_id': user_id},
            {'$set': {'customization': customization_data}},
            upsert=True
        )
        
        return jsonify(customization_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Call the initialization function
init_achievements()
init_campaigns()

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=9091) 
