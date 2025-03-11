# This script seeds the database with campaign definitions
# It is intended to be run once to populate the database with campaigns and quests

import db
import uuid
from datetime import datetime

# Helper function to generate UUIDs for campaigns and quests
def gen_id():
    return str(uuid.uuid4())

# Campaign definitions with their associated quests
campaigns = [
    # Campaign 1: Quiz Creator
    {
        "campaign_id": gen_id(),
        "title": "Quiz Master Creator",
        "description": "Learn to create engaging and effective quizzes",
        "theme": {
            "primaryColor": "#9333ea",  # Purple
            "secondaryColor": "#c4b5fd",
            "backgroundImage": "https://images.unsplash.com/photo-1546776310-eef45dd6d63c?q=80&w=2069&auto=format&fit=crop"
        },
        "category": "creation",
        "required_level": 1,
        "xp_reward": 200,
        "customization_rewards": [
            {"type": "avatar_frame", "id": "quiz_master_frame", "name": "Quiz Master Frame"}
        ],
        "created_at": datetime.now(),
        "quests": [
            {
                "quest_id": gen_id(),
                "title": "First Steps",
                "description": "Create your first quiz",
                "order": 0,
                "xp_reward": 50,
                "objectives": [
                    {
                        "type": "create_quiz",
                        "description": "Create your first quiz",
                        "current": 0,
                        "required": 1
                    }
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "Add Some Images",
                "description": "Create a quiz with at least 3 images",
                "order": 1,
                "xp_reward": 75,
                "objectives": [
                    {
                        "type": "quiz_with_images",
                        "description": "Add at least 3 images to a quiz",
                        "current": 0,
                        "required": 1
                    }
                ],
                "customization_rewards": [
                    {"type": "avatar_background", "id": "quiz_creator_bg", "name": "Quiz Creator Background"}
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "AI Assistant",
                "description": "Create a quiz using AI generation",
                "order": 2,
                "xp_reward": 100,
                "objectives": [
                    {
                        "type": "create_ai_quiz",
                        "description": "Create a quiz using AI generation",
                        "current": 0,
                        "required": 1
                    }
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "Quiz Portfolio",
                "description": "Create 5 quizzes in total",
                "order": 3,
                "xp_reward": 150,
                "objectives": [
                    {
                        "type": "create_quiz",
                        "description": "Create quizzes",
                        "current": 0,
                        "required": 5
                    }
                ],
                "customization_rewards": [
                    {"type": "title", "id": "quiz_creator", "name": "Quiz Creator"}
                ]
            }
        ]
    },
    
    # Campaign 2: Science Explorer
    {
        "campaign_id": gen_id(),
        "title": "Science Explorer",
        "description": "Master scientific knowledge through quizzes",
        "theme": {
            "primaryColor": "#2563eb",  # Blue
            "secondaryColor": "#93c5fd",
            "backgroundImage": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?q=80&w=2070&auto=format&fit=crop"
        },
        "category": "science",
        "required_level": 2,
        "xp_reward": 250,
        "customization_rewards": [
            {"type": "avatar", "id": "scientist_avatar", "name": "Scientist Avatar"}
        ],
        "created_at": datetime.now(),
        "quests": [
            {
                "quest_id": gen_id(),
                "title": "Beginner Scientist",
                "description": "Complete 3 science quizzes",
                "order": 0,
                "xp_reward": 50,
                "objectives": [
                    {
                        "type": "complete_category_quiz",
                        "category": "science",
                        "description": "Complete science quizzes",
                        "current": 0,
                        "required": 3
                    }
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "Perfect Score",
                "description": "Get a perfect score on a science quiz",
                "order": 1,
                "xp_reward": 100,
                "objectives": [
                    {
                        "type": "perfect_category_quiz",
                        "category": "science",
                        "description": "Get 100% on a science quiz",
                        "current": 0,
                        "required": 1
                    }
                ],
                "customization_rewards": [
                    {"type": "badge", "id": "science_perfect", "name": "Science Perfect"}
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "Science Expert",
                "description": "Complete 10 science quizzes with an average score of 80% or higher",
                "order": 2,
                "xp_reward": 150,
                "objectives": [
                    {
                        "type": "complete_category_quiz_with_score",
                        "category": "science",
                        "min_score": 80,
                        "description": "Complete science quizzes with high scores",
                        "current": 0,
                        "required": 10
                    }
                ]
            }
        ]
    },
    
    # Campaign 3: Streak Master
    {
        "campaign_id": gen_id(),
        "title": "Streak Master",
        "description": "Build your consistency and daily learning habit",
        "theme": {
            "primaryColor": "#dc2626",  # Red
            "secondaryColor": "#fca5a5",
            "backgroundImage": "https://images.unsplash.com/photo-1563089145-599997674d42?q=80&w=2070&auto=format&fit=crop"
        },
        "category": "consistency",
        "required_level": 1,
        "xp_reward": 300,
        "customization_rewards": [
            {"type": "profile_effect", "id": "flame_aura", "name": "Flame Aura"}
        ],
        "created_at": datetime.now(),
        "quests": [
            {
                "quest_id": gen_id(),
                "title": "First Week",
                "description": "Maintain a 7-day streak",
                "order": 0,
                "xp_reward": 75,
                "objectives": [
                    {
                        "type": "maintain_streak",
                        "description": "Log in and complete at least one quiz every day",
                        "current": 0,
                        "required": 7
                    }
                ],
                "customization_rewards": [
                    {"type": "badge", "id": "weekly_streak", "name": "Weekly Streak"}
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "Two Week Challenge",
                "description": "Maintain a 14-day streak",
                "order": 1,
                "xp_reward": 150,
                "objectives": [
                    {
                        "type": "maintain_streak",
                        "description": "Log in and complete at least one quiz every day",
                        "current": 0,
                        "required": 14
                    }
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "Month Master",
                "description": "Maintain a 30-day streak",
                "order": 2,
                "xp_reward": 300,
                "objectives": [
                    {
                        "type": "maintain_streak",
                        "description": "Log in and complete at least one quiz every day",
                        "current": 0,
                        "required": 30
                    }
                ],
                "customization_rewards": [
                    {"type": "title", "id": "streak_master", "name": "Streak Master"}
                ]
            }
        ]
    },
    
    # Campaign 4: Trivia Champion (new campaign)
    {
        "campaign_id": gen_id(),
        "title": "Trivia Champion",
        "description": "Test your knowledge across various trivia categories",
        "theme": {
            "primaryColor": "#047857",  # Emerald
            "secondaryColor": "#6ee7b7",
            "backgroundImage": "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?q=80&w=2070&auto=format&fit=crop"
        },
        "category": "trivia",
        "required_level": 3,
        "xp_reward": 350,
        "customization_rewards": [
            {"type": "avatar_accessory", "id": "knowledge_crown", "name": "Crown of Knowledge"}
        ],
        "created_at": datetime.now(),
        "quests": [
            {
                "quest_id": gen_id(),
                "title": "Trivia Beginner",
                "description": "Complete 5 different category quizzes",
                "order": 0,
                "xp_reward": 100,
                "objectives": [
                    {
                        "type": "unique_categories",
                        "description": "Complete quizzes from different categories",
                        "current": 0,
                        "required": 5
                    }
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "Quick Thinker",
                "description": "Complete a quiz in under 3 minutes with a score of at least 70%",
                "order": 1,
                "xp_reward": 150,
                "objectives": [
                    {
                        "type": "timed_quiz",
                        "description": "Complete quiz quickly with good score",
                        "current": 0,
                        "required": 1,
                        "time_limit": 180,
                        "min_score": 70
                    }
                ],
                "customization_rewards": [
                    {"type": "badge", "id": "quick_thinker", "name": "Quick Thinker"}
                ]
            },
            {
                "quest_id": gen_id(),
                "title": "Knowledge Master",
                "description": "Score 90% or higher on 3 different category quizzes",
                "order": 2,
                "xp_reward": 200,
                "objectives": [
                    {
                        "type": "high_score_different_categories",
                        "description": "High scores across different categories",
                        "current": 0,
                        "required": 3,
                        "min_score": 90
                    }
                ],
                "customization_rewards": [
                    {"type": "title", "id": "trivia_master", "name": "Trivia Master"}
                ]
            }
        ]
    }
]

def seed_campaigns():
    """Seed campaigns into the database"""
    try:
        # Check if we have any campaigns already
        existing_count = db.gamificationdb.campaigns.count_documents({})
        
        if existing_count == 0:
            print("Seeding campaigns into database...")
            
            # Insert each campaign and its quests
            for campaign in campaigns:
                # Extract quests from the campaign
                quests = campaign.pop("quests", [])
                
                # Insert campaign
                db.gamificationdb.campaigns.insert_one(campaign)
                
                # Insert quests with campaign_id reference
                for quest in quests:
                    quest["campaign_id"] = campaign["campaign_id"]
                    db.gamificationdb.quests.insert_one(quest)
                
            print(f"Successfully added {len(campaigns)} campaigns with their quests")
        else:
            print(f"Database already contains {existing_count} campaigns. Skipping seeding.")
            
            # Optional: Update campaigns that may be missing
            for campaign in campaigns:
                quests = campaign.pop("quests", [])
                
                # Upsert campaign
                db.gamificationdb.campaigns.update_one(
                    {'title': campaign['title']},
                    {'$setOnInsert': campaign},
                    upsert=True
                )
                
                # Find the inserted/existing campaign
                existing_campaign = db.gamificationdb.campaigns.find_one({'title': campaign['title']})
                
                # Update quests for this campaign
                for quest in quests:
                    quest["campaign_id"] = existing_campaign["campaign_id"]
                    db.gamificationdb.quests.update_one(
                        {'title': quest['title'], 'campaign_id': quest['campaign_id']},
                        {'$setOnInsert': quest},
                        upsert=True
                    )
                    
            print("Updated any missing campaigns and quests")
            
    except Exception as e:
        print(f"Error seeding campaigns: {str(e)}")
        
if __name__ == "__main__":
    seed_campaigns()