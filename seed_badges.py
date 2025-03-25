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
    Badge(
        name="Accuracy Expert",
        description="Score 5 perfect quizzes",
        icon="🎯",
        category="achievement",
        rarity="rare"
    ),
    Badge(
        name="Getting Started",
        description="Maintain a 3-day streak",
        icon="🔥",
        category="streak",
        rarity="common"
    ),
    Badge(
        name="Commitment",
        description="Maintain a 7-day streak",
        icon="🔥🔥",
        category="streak",
        rarity="uncommon"
    ),
    Badge(
        name="Dedication",
        description="Maintain a 30-day streak",
        icon="🔥🔥🔥",
        category="streak",
        rarity="rare"
    ),
    Badge(
        name="Category Explorer",
        description="Complete quizzes in 3 different categories",
        icon="🧭",
        category="exploration",
        rarity="uncommon"
    ),
    Badge(
        name="Category Specialist",
        description="Reach level 5 in any category",
        icon="🔍",
        category="expertise",
        rarity="rare"
    ),
    Badge(
        name="Jack of All Trades",
        description="Reach level 3 in 5 different categories",
        icon="🌟",
        category="expertise",
        rarity="epic"
    ),
    Badge(
        name="Level 5 Scholar",
        description="Reach level 5 in the system",
        icon="📚",
        category="progression",
        rarity="uncommon"
    ),
    Badge(
        name="Level 10 Scholar",
        description="Reach level 10 in the system",
        icon="📚📚",
        category="progression",
        rarity="rare"
    ),
    Badge(
        name="Speed Demon",
        description="Complete a quiz in under 2 minutes",
        icon="⚡",
        category="speed",
        rarity="uncommon"
    )
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