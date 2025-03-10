# This script seeds the database with achievement definitions
# It is intended to be run once to populate the database with achievements
from init import app
import db
import uuid
from datetime import datetime

# Achievement definitions to add to the database
achievements = [
    # Quiz completion achievements
    { 
        "achievement_id": str(uuid.uuid4()),
        "title": "First Steps", 
        "description": "Complete your first quiz", 
        "icon": "🎯",
        "requirement": "Complete 1 quiz",
        "xp_reward": 50,
        "condition": {"quizzes_completed": 1},
        "created_at": datetime.now()
    },
    { 
        "achievement_id": str(uuid.uuid4()),
        "title": "Quiz Enthusiast", 
        "description": "Complete 10 quizzes", 
        "icon": "🔥",
        "requirement": "Complete 10 quizzes",
        "xp_reward": 100,
        "condition": {"quizzes_completed": 10},
        "created_at": datetime.now()
    },
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Quiz Master",
        "description": "Complete 50 quizzes",
        "icon": "🏆",
        "requirement": "Complete 50 quizzes",
        "xp_reward": 250,
        "condition": {"quizzes_completed": 50},
        "created_at": datetime.now()
    },
    
    # Accuracy achievements
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Perfect Score",
        "description": "Score 100% on a quiz",
        "icon": "⭐",
        "requirement": "Get a perfect score",
        "xp_reward": 100,
        "condition": {"perfect_score": True},
        "created_at": datetime.now()
    },
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Accuracy Expert",
        "description": "Score 5 perfect quizzes",
        "icon": "🥇",
        "requirement": "Get 5 perfect scores",
        "xp_reward": 200,
        "condition": {"perfect_scores": 5},
        "created_at": datetime.now()
    },
    
    # Streak achievements
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Getting Started",
        "description": "Maintain a 3-day streak",
        "icon": "🔥",
        "requirement": "3-day streak",
        "xp_reward": 75,
        "condition": {"streak_days": 3},
        "created_at": datetime.now()
    },
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Commitment",
        "description": "Maintain a 7-day streak",
        "icon": "🔥",
        "requirement": "7-day streak",
        "xp_reward": 150,
        "condition": {"streak_days": 7},
        "created_at": datetime.now()
    },
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Dedication",
        "description": "Maintain a 30-day streak",
        "icon": "🔥",
        "requirement": "30-day streak",
        "xp_reward": 500,
        "condition": {"streak_days": 30},
        "created_at": datetime.now()
    },
    
    # Category achievements
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Category Explorer",
        "description": "Complete quizzes in 3 different categories",
        "icon": "🧠",
        "requirement": "3 different categories",
        "xp_reward": 100,
        "condition": {"unique_categories": 3},
        "created_at": datetime.now()
    },
    
    # Level achievements
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Level 5 Scholar",
        "description": "Reach level 5",
        "icon": "📚",
        "requirement": "Reach level 5",
        "xp_reward": 150,
        "condition": {"level": 5},
        "created_at": datetime.now()
    },
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Level 10 Expert",
        "description": "Reach level 10",
        "icon": "📚",
        "requirement": "Reach level 10",
        "xp_reward": 300,
        "condition": {"level": 10},
        "created_at": datetime.now()
    },
    
    # Time-based achievements
    {
        "achievement_id": str(uuid.uuid4()),
        "title": "Speed Demon",
        "description": "Complete a quiz in under 2 minutes",
        "icon": "⚡",
        "requirement": "Under 2 minutes",
        "xp_reward": 100,
        "condition": {"time_under": 120},
        "created_at": datetime.now()
    }
]

def seed_achievements():
    """Seed achievements into the database"""
    try:
        # Check if we have any achievements already
        existing_count = db.gamificationdb.achievements.count_documents({})
        
        # Only seed if we don't have any achievements
        if existing_count == 0:
            print("Seeding achievements into database...")
            db.gamificationdb.achievements.insert_many(achievements)
            print(f"Successfully added {len(achievements)} achievements")
        else:
            print(f"Database already contains {existing_count} achievements. Skipping seeding.")
            
            # Optional: Update achievements that may be missing
            for achievement in achievements:
                db.gamificationdb.achievements.update_one(
                    {'title': achievement['title']},
                    {'$setOnInsert': achievement},
                    upsert=True
                )
            print("Updated any missing achievements")
            
    except Exception as e:
        print(f"Error seeding achievements: {str(e)}")

if __name__ == "__main__":
    seed_achievements()