from flask import Flask
from flask_cors import CORS
from models.achievement import Achievement
from models.badge import Badge
import db
from datetime import datetime, timedelta

# Create Flask app instance
app = Flask(__name__)

# Configure CORS
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000", "https://exper-frontend-production.up.railway.app"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization", "Accept"],
         "expose_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True,
         "allow_credentials": True,
         "max_age": 120
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


# Initialize campaigns in database
def init_campaigns():
    """Initialize campaigns in the database on app startup"""
    from models.campaign import Campaign
    from models.quest import Quest
    
    # Check if campaigns already exist
    existing_campaigns = db.gamificationdb.campaigns.count_documents({})
    
    if existing_campaigns > 0:
        print(f"Found {existing_campaigns} existing campaigns, skipping initialization")
        return
    
    print("Initializing campaigns...")
    
    # Campaign 1: Quiz Creator
    quiz_creator = Campaign(
        title="Quiz Master Creator",
        description="Learn to create engaging and effective quizzes",
        theme={
            "primaryColor": "#9333ea",  # Purple
            "secondaryColor": "#c4b5fd"
        },
        category="creation",
        required_level=1,
        xp_reward=200,
        customization_rewards=[
            {"type": "avatar_frame", "id": "quiz_master_frame"}
        ]
    ).to_dict()
    
    db.gamificationdb.campaigns.insert_one(quiz_creator)
    
    # Quests for Quiz Creator campaign
    quests = [
        Quest(
            campaign_id=quiz_creator["campaign_id"],
            title="First Steps",
            description="Create your first quiz",
            order=0,
            xp_reward=50,
            objectives=[
                {
                    "type": "create_quiz",
                    "description": "Create your first quiz",
                    "current": 0,
                    "required": 1
                }
            ]
        ),
        Quest(
            campaign_id=quiz_creator["campaign_id"],
            title="Add Some Images",
            description="Create a quiz with at least 3 images",
            order=1,
            xp_reward=75,
            objectives=[
                {
                    "type": "quiz_with_images",
                    "description": "Add at least 3 images to a quiz",
                    "current": 0,
                    "required": 1
                }
            ],
            customization_rewards=[
                {"type": "avatar_background", "id": "quiz_creator_bg"}
            ]
        ),
        Quest(
            campaign_id=quiz_creator["campaign_id"],
            title="AI Assistant",
            description="Create a quiz using AI generation",
            order=2,
            xp_reward=100,
            objectives=[
                {
                    "type": "create_ai_quiz",
                    "description": "Create a quiz using AI generation",
                    "current": 0,
                    "required": 1
                }
            ]
        ),
        Quest(
            campaign_id=quiz_creator["campaign_id"],
            title="Quiz Portfolio",
            description="Create 5 quizzes in total",
            order=3,
            xp_reward=150,
            objectives=[
                {
                    "type": "create_quiz",
                    "description": "Create quizzes",
                    "current": 0,
                    "required": 5
                }
            ],
            customization_rewards=[
                {"type": "title", "id": "quiz_creator"}
            ]
        )
    ]
    
    for quest in quests:
        db.gamificationdb.quests.insert_one(quest.to_dict())
    
    # Campaign 2: Science Explorer
    science_explorer = Campaign(
        title="Science Explorer",
        description="Master scientific knowledge through quizzes",
        theme={
            "primaryColor": "#2563eb",  # Blue
            "secondaryColor": "#93c5fd"
        },
        category="science",
        required_level=2,
        xp_reward=250,
        customization_rewards=[
            {"type": "avatar", "id": "scientist_avatar"}
        ]
    ).to_dict()
    
    db.gamificationdb.campaigns.insert_one(science_explorer)
    
    # Quests for Science Explorer
    quests = [
        Quest(
            campaign_id=science_explorer["campaign_id"],
            title="Beginner Scientist",
            description="Complete 3 science quizzes",
            order=0,
            xp_reward=50,
            objectives=[
                {
                    "type": "complete_category_quiz",
                    "category": "science",
                    "description": "Complete science quizzes",
                    "current": 0,
                    "required": 3
                }
            ]
        ),
        Quest(
            campaign_id=science_explorer["campaign_id"],
            title="Perfect Score",
            description="Get a perfect score on a science quiz",
            order=1,
            xp_reward=100,
            objectives=[
                {
                    "type": "perfect_category_quiz",
                    "category": "science",
                    "description": "Get 100% on a science quiz",
                    "current": 0,
                    "required": 1
                }
            ],
            customization_rewards=[
                {"type": "badge", "id": "science_perfect"}
            ]
        ),
        Quest(
            campaign_id=science_explorer["campaign_id"],
            title="Science Expert",
            description="Complete 10 science quizzes with an average score of 80% or higher",
            order=2,
            xp_reward=150,
            objectives=[
                {
                    "type": "complete_category_quiz_with_score",
                    "category": "science",
                    "min_score": 80,
                    "description": "Complete science quizzes with high scores",
                    "current": 0,
                    "required": 10
                }
            ]
        )
    ]
    
    for quest in quests:
        db.gamificationdb.quests.insert_one(quest.to_dict())
    
    # Campaign 3: Streak Master
    streak_master = Campaign(
        title="Streak Master",
        description="Build your consistency and daily learning habit",
        theme={
            "primaryColor": "#dc2626",  # Red
            "secondaryColor": "#fca5a5"
        },
        category="consistency",
        required_level=1,
        xp_reward=300,
        customization_rewards=[
            {"type": "profile_effect", "id": "flame_aura"}
        ]
    ).to_dict()
    
    db.gamificationdb.campaigns.insert_one(streak_master)
    
    # Quests for Streak Master
    quests = [
        Quest(
            campaign_id=streak_master["campaign_id"],
            title="First Week",
            description="Maintain a 7-day streak",
            order=0,
            xp_reward=75,
            objectives=[
                {
                    "type": "maintain_streak",
                    "description": "Log in and complete at least one quiz every day",
                    "current": 0,
                    "required": 7
                }
            ],
            customization_rewards=[
                {"type": "badge", "id": "weekly_streak"}
            ]
        ),
        Quest(
            campaign_id=streak_master["campaign_id"],
            title="Two Week Challenge",
            description="Maintain a 14-day streak",
            order=1,
            xp_reward=150,
            objectives=[
                {
                    "type": "maintain_streak",
                    "description": "Log in and complete at least one quiz every day",
                    "current": 0,
                    "required": 14
                }
            ]
        ),
        Quest(
            campaign_id=streak_master["campaign_id"],
            title="Month Master",
            description="Maintain a 30-day streak",
            order=2,
            xp_reward=300,
            objectives=[
                {
                    "type": "maintain_streak",
                    "description": "Log in and complete at least one quiz every day",
                    "current": 0,
                    "required": 30
                }
            ],
            customization_rewards=[
                {"type": "title", "id": "streak_master"}
            ]
        )
    ]
    
    for quest in quests:
        db.gamificationdb.quests.insert_one(quest.to_dict())
    
    print("Campaign initialization complete")


# Run initialization
if __name__ == "__main__":
    init_achievements()
    init_badges()
    init_campaigns()