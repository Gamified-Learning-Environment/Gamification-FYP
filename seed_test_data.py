import pymongo
from bson import ObjectId
import random
import uuid
from datetime import datetime, timedelta
from config import MONGODB_URI

# Connect to MongoDB
client = pymongo.MongoClient(MONGODB_URI)
user_db = client["userdatabase"]
gamification_db = client["Gamificationdatabase"]

# Get collections
user_collection = user_db["usercollection"]
player_collection = gamification_db["players"]

# Achievement IDs
achievement_ids = [
    "0df5e304-c5b2-4e5f-879d-4c883b0ed75c",
    "b369df5d-abea-4634-805e-7e56234da7dc",
    "012bf02f-a68c-44bc-8bc5-f1d793ce18b7",
    "8c6c0b0e-0f8f-4b55-bc00-ac33dcc64666",
    "d12dd9b1-1e96-48d7-adbe-da6a92228b9f",
    "009ce924-5698-47bb-99a3-781a731fad61",
    "c4f7e25a-7b3d-4982-b8d5-e9a6b1f2d4c3",
    "a3b7c8d9-e0f1-4a5b-9c8d-7e6f5a4b3c2d"
]

# Badge IDs
badge_ids = [
    "4d64166c-b0e3-4f74-b7e0-e2978c322b66",
    "5e75277d-c1f4-4f85-c8f1-f3d87b3e5c6d",
    "6f86388e-d2g5-5g96-d9g2-g4e98c4f6d7e"
]

# Categories
categories = ["Science", "Math", "History", "Geography", "Programming", "Languages", "Arts", "Music", "Sports", "Animals"]

# Generate fake password hash
def generate_fake_hash(password):
    import hashlib
    import os
    salt = os.urandom(8).hex()
    return f"scrypt:32768:8:1${salt}${hashlib.sha256((password + salt).encode()).hexdigest()}"

# Create test users
test_users = []
test_players = []

for i in range(1, 11):
    # Create user
    user_id = ObjectId()
    username = f"TestUser{i}"
    
    user = {
        "_id": user_id,
        "email": f"test{i}@example.com",
        "password": generate_fake_hash(f"password{i}"),
        "username": username,
        "firstName": f"Test{i}",
        "lastName": f"User{i}",
        "imageUrl": f"https://randomuser.me/api/portraits/{'men' if i % 2 else 'women'}/{i}.jpg" if i % 3 == 0 else None
    }
    
    test_users.append(user)
    
    # Create varied stats for players
    level = random.randint(1, 15)
    xp = random.randint(0, 1000) + level * 100
    quizzes_completed = random.randint(5, 55)
    perfect_scores = int(quizzes_completed * (random.random() * 0.6 + 0.1))
    
    # Randomly select achievements
    num_achievements = random.randint(0, len(achievement_ids))
    user_achievements = random.sample(achievement_ids, num_achievements)
    
    # Randomly select badges
    num_badges = random.randint(0, len(badge_ids))
    user_badges = random.sample(badge_ids, num_badges)
    
    # Generate category progress
    category_levels = {}
    completed_categories = []
    num_categories = random.randint(1, 6)
    
    for j in range(num_categories):
        category = categories[j]
        completed_categories.append(category)
        
        category_level = random.randint(1, 8)
        category_xp = random.randint(0, 400)
        
        category_levels[category] = {
            "level": category_level,
            "xp": category_xp
        }
    
    # Create player
    player = {
        "_id": ObjectId(),
        "user_id": str(user_id),
        "username": username,
        "current_level": level,
        "xp": xp,
        "achievements": user_achievements,
        "badges": user_badges,
        "streaks": [],
        "category_levels": category_levels,
        "completed_categories": completed_categories,
        "quizzes_completed": quizzes_completed,
        "perfect_scores": perfect_scores
    }
    
    test_players.append(player)

# Insert data into database
if test_users:
    user_result = user_collection.insert_many(test_users)
    print(f"{len(user_result.inserted_ids)} users inserted")
    
    player_result = player_collection.insert_many(test_players)
    print(f"{len(player_result.inserted_ids)} players inserted")
    
print("Seed completed successfully")