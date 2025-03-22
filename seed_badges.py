from models.badge import Badge
import db

# Define sample badges
# Update your existing badges to use Unicode emoji or other appropriate icons

badges = [
    Badge(
        name="Quiz Master",
        description="Complete 10 quizzes with a score of 80% or higher",
        icon="🏆",
        category="achievement",
        rarity="rare"
    ),
    Badge(
        name="First Steps",
        description="Complete your first quiz",
        icon="👣",
        category="achievement",
        rarity="common"
    ),
    Badge(
        name="Quiz Expert",
        description="Complete 50 quizzes with a score of 80% or higher",
        icon="🎓",
        category="achievement",
        rarity="epic"
    ),
    Badge( # First Perfect score
        name="Perfect Score",
        description="Achieve a perfect score in a quiz",
        icon="💯",
        category="achievement",
        rarity="uncommon",
    ),
    # Add more badges...
]

def seed_badges():
    # Clear existing badges
    db.gamificationdb.badges.delete_many({})
    
    # Insert badges
    badge_data = [badge.to_dict() for badge in badges]
    db.gamificationdb.badges.insert_many(badge_data)
    print(f"Seeded {len(badges)} badges")

if __name__ == "__main__":
    seed_badges()