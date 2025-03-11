# Campaign model is a class that represents a campaign in the gamification service.

from datetime import datetime
from bson import ObjectId

# Initialize the Campaign class with the following attributes:
class Campaign:
    def __init__(self, 
                 title, 
                 description, 
                 theme,
                 category,
                 quests=None,
                 required_level=1,
                 xp_reward=100,
                 customization_rewards=None,
                 campaign_id=None):
        self.campaign_id = campaign_id or str(ObjectId())
        self.title = title
        self.description = description
        self.theme = theme  # {primaryColor, secondaryColor}
        self.category = category
        self.quests = quests or []
        self.required_level = required_level
        self.xp_reward = xp_reward
        self.customization_rewards = customization_rewards or []
        self.created_at = datetime.now().isoformat()

    def to_dict(self): # Convert the campaign object to a dictionary
        return {
            "campaign_id": self.campaign_id,
            "title": self.title,
            "description": self.description,
            "theme": self.theme,
            "category": self.category,
            "quests": self.quests,
            "required_level": self.required_level,
            "xp_reward": self.xp_reward,
            "customization_rewards": self.customization_rewards,
            "created_at": self.created_at
        }