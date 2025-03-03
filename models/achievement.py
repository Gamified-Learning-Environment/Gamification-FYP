import uuid
from datetime import datetime

# Achievement model is a class that represents an achievement in the gamification service.

# Initialize the Achievement class with the following attributes:
class Achievement: 
    def __init__(self, achievement_id=None, title="", description="", icon="", category="", xp_reward=0, conditions=None, hidden=False): 
        self.achievement_id = achievement_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.icon = icon
        self.category = category
        self.xp_reward = xp_reward
        self.conditions = conditions or []
        self.hidden = hidden
        self.created_at = datetime.now()

    def to_dict(self): # Convert the achievement object to a dictionary
        return {
            'achievement_id': self.achievement_id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'xp_reward': self.xp_reward,
            'conditions': self.conditions,
            'hidden': self.hidden,
            'created_at': self.created_at
        }