# Badge model is a class that represents a badge in the gamification service.

import uuid

# Initialize the Badge class with the following attributes:

class Badge:
    def __init__(self, badge_id=None, name="", description="", icon="", category="", rarity="common", level_requirement=None, category_type=None):
        self.badge_id = badge_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category  # Badge category like "achievement", "streak", etc
        self.category_type = category_type  # The specific subject category like "math", "science"
        self.rarity = rarity # Common, Uncommon, Rare, Epic, Legendary
        self.level_requirement = level_requirement  # For category level badges

    def to_dict(self):
        return {
            'badge_id': self.badge_id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'category_type': self.category_type,
            'rarity': self.rarity,
            'level_requirement': self.level_requirement
        }