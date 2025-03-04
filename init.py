from flask import Flask
from flask_cors import CORS
from models.achievement import Achievement
from models.badge import Badge
from models.challenge import Challenge
import db
from datetime import datetime, timedelta

# Create Flask app instance
app = Flask(__name__)

# Configure CORS
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"]
     }},
     supports_credentials=True)

def init_achievements():
    # Initialize default achievements
    
    achievements = [

        # Quiz Achievements
        Achievement(
            title="Quiz Novice",
            description="Complete your first quiz",
            icon="🎓",
            category="quiz",
            xp_reward=50,
            conditions={"quizzes_completed": 1}
        ),
        Achievement(
            title="Quiz Expert",
            description="Complete 10 quizzes",
            icon="🧠",
            category="quiz",
            xp_reward=200,
            conditions={"quizzes_completed": 10}
        ),
        Achievement(
            title="Perfect Score",
            description="Get a 100% score on any quiz",
            icon="🏆",
            category="quiz",
            xp_reward=150,
            conditions={"perfect_score": True}
        ),

        # Streak Achievements
        Achievement(
            title="Daily Learner",
            description="Maintain a 3-day learning streak",
            icon="🔥",
            category="streak",
            xp_reward=100,
            conditions={"streak_days": 3}
        ),
        Achievement(
            title="Committed Scholar",
            description="Maintain a 7-day learning streak",
            icon="⚡",
            category="streak",
            xp_reward=250,
            conditions={"streak_days": 7}
        ),

        # Category Achievements
        Achievement(
            title="Programming Enthusiast",
            description="Complete 5 programming quizzes",
            icon="💻",
            category="programming",
            xp_reward=150,
            conditions={"category_quizzes": {"programming": 5}}
        ),

        # Challenge Achievements
        Achievement(
            title="Challenger",
            description="Complete your first challenge",
            icon="🏁",
            category="challenge",
            xp_reward=100,
            conditions={"challenges_completed": 1}
        ),

        # Badge Achievements
        Achievement(
            title="Badge Collector",
            description="Collect 5 badges",
            icon="🎖️",
            category="badge",
            xp_reward=200,
            conditions={"badges_collected": 5}
        )

        # Add more achievements here

    ]

    # Insert into database
    for achievement in achievements: 
        # Check if achievement exists already
        existing = db.gamificationdb.achievements.find_one({"title": achievement.title})
        if not existing:
            db.gamificationdb.achievements.insert_one(achievement.to_dict())

def init_badges():
    # Initialize default badges

    badges = [
        Badge(
            name="Quick Learner",
            description="Complete a quiz in under 2 minutes",
            icon="⚡",
            category="speed",
            rarity="uncommon"
        ),
        Badge(
            name="Math Master",
            description="Excel in mathematics quizzes",
            icon="➗",
            category="mathematics",
            rarity="rare"
        ),
        Badge(
            name="Code Wizard",
            description="Excel in programming quizzes",
            icon="🧙",
            category="programming",
            rarity="epic"
        ),
    ]

    # Insert into database
    for badge in badges: 
        # Check if badge exists already
        existing = db.gamificationdb.badges.find_one({"name": badge.name})
        if not existing:
            db.gamificationdb.badges.insert_one(badge.to_dict())

def init_challenges():
    # Initialize default challenges

    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    challenges = [
        Challenge(
            title="Daily Quiz Master",
            description="Complete 3 quizzes today",
            category="daily",
            start_date=today,
            end_date=tomorrow,
            reward_xp=150,
            requirements={"quizzes_completed": 3}
        ),
        Challenge(
            title="Perfect Score Challenge",
            description="Get a 100% score on any quiz today",
            category="daily",
            start_date=today,
            end_date=tomorrow,
            reward_xp=200,
            requirements={"perfect_score": True}
        ),
    ]

    # Insert into database
    for challenge in challenges: 
        db.gamificationdb.challenges.insert_one(challenge.to_dict())



# Run initialization
if __name__ == "__main__":
    init_achievements()
    init_badges()
    init_challenges()