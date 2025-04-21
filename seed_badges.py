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
    ),
    Badge(
    name="Math Novice",
    description="Reach level 3 in Mathematics",
    icon="🧮",
    category="expertise", 
    category_type="math",
    rarity="common",
    level_requirement=3
    ),
    Badge(
        name="Math Scholar",
        description="Reach level 5 in Mathematics",
        icon="📐",
        category="expertise",
        category_type="math",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="Math Master",
        description="Reach level 10 in Mathematics",
        icon="➗",
        category="expertise",
        category_type="math",
        rarity="rare",
        level_requirement=10
    ),
    Badge(
        name="Science Explorer",
        description="Reach level 3 in Science",
        icon="🧪",
        category="expertise",
        category_type="science",
        rarity="common",
        level_requirement=3
    ),
    Badge(
        name="Science Researcher",
        description="Reach level 5 in Science",
        icon="🔬",
        category="expertise",
        category_type="science",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="Science Genius",
        description="Reach level 10 in Science",
        icon="🧬",
        category="expertise",
        category_type="science",
        rarity="rare",
        level_requirement=10
    ),
    Badge(
        name="History Buff",
        description="Reach level 3 in History",
        icon="📜",
        category="expertise",
        category_type="history",
        rarity="common",
        level_requirement=3
    ),
    Badge(
        name="History Scholar",
        description="Reach level 5 in History",
        icon="🏺",
        category="expertise",
        category_type="history",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="History Expert",
        description="Reach level 10 in History",
        icon="🏛️",
        category="expertise",
        category_type="history",
        rarity="rare",
        level_requirement=10
    ),
    Badge(
        name="Language Learner",
        description="Reach level 3 in Language",
        icon="📖",
        category="expertise",
        category_type="language",
        rarity="common",
        level_requirement=3
    ),
    Badge(
        name="Language Scholar",
        description="Reach level 5 in Language",
        icon="🗣️",
        category="expertise",
        category_type="language",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="Language Pro",
        description="Reach level 10 in Language",
        icon="📝",
        category="expertise",
        category_type="language",
        rarity="rare",
        level_requirement=10
    ),
    Badge(
        name="Art Enthusiast",
        description="Reach level 3 in Art",
        icon="🎨",
        category="expertise",
        category_type="art",
        rarity="common",
        level_requirement=3
    ),
    Badge(
        name="Art Scholar",
        description="Reach level 5 in Art",
        icon="🖌️",
        category="expertise",
        category_type="art",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="Art Master",
        description="Reach level 10 in Art",
        icon="🖼️",
        category="expertise",
        category_type="art",
        rarity="rare",
        level_requirement=10
    ),
    Badge(
        name="Music Aficionado",
        description="Reach level 3 in Music",
        icon="🎶",
        category="expertise",
        category_type="music",
        rarity="common",
        level_requirement=3
    ),
    Badge(
        name="Music Scholar",
        description="Reach level 5 in Music",
        icon="🎵",
        category="expertise",
        category_type="music",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="Music Virtuoso",
        description="Reach level 10 in Music",
        icon="🎼",
        category="expertise",
        category_type="music",
        rarity="rare",
        level_requirement=10
    ),
    Badge(
        name="Physical Fitness Buff",
        description="Reach level 3 in Physical Education",
        icon="🏋️‍♂️",
        category="expertise",
        category_type="physical_education",
        rarity="common",
        level_requirement=3
    ),
    Badge(
        name="Physical Education Scholar",
        description="Reach level 5 in Physical Education",
        icon="🏃‍♂️",
        category="expertise",
        category_type="physical_education",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="Physical Education Expert",
        description="Reach level 10 in Physical Education",
        icon="🏅",
        category="expertise",
        category_type="physical_education",
        rarity="rare",
        level_requirement=10
    ),
    Badge(
        name="Coding Novice",
        description="Reach level 3 in Computer Science",
        icon="💻",
        category="expertise",
        category_type="computer_science",
        rarity="common",
        level_requirement=3
    ),
    Badge(
        name="Coding Scholar",
        description="Reach level 5 in Computer Science",
        icon="🖥️",
        category="expertise",
        category_type="computer_science",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="Coding Master",
        description="Reach level 10 in Computer Science",
        icon="🖱️",
        category="expertise",
        category_type="computer_science",
        rarity="rare",
        level_requirement=10
    ),
    Badge(
        name="Social Studies Explorer",
        description="Reach level 3 in Social Studies",
        icon="🌍",
        category="expertise",
        category_type="social_studies",
        rarity="common",
        level_requirement=3
    ),
    Badge(
        name="Social Studies Scholar",
        description="Reach level 5 in Social Studies",
        icon="🗺️",
        category="expertise",
        category_type="social_studies",
        rarity="uncommon",
        level_requirement=5
    ),
    Badge(
        name="Social Studies Expert",
        description="Reach level 10 in Social Studies",
        icon="🌐",
        category="expertise",
        category_type="social_studies",
        rarity="rare",
        level_requirement=10
    ),

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