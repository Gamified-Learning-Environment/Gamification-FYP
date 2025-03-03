# Badge model is a class that represents a badge in the gamification service.

import uuid

# Initialize the Badge class with the following attributes:

class Badge:
    def __init__(self, badge_id=None, name="", description="", icon="", category="", rarity="common"):
        self.badge_id = badge_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category
        self.rarity = rarity # Common, Uncommon, Rare, Epic, Legendary

    def to_dict(self):
        return {
            'badge_id': self.badge_id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'rarity': self.rarity
        }