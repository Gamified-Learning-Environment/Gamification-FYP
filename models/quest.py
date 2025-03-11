# Quest model is a class that represents a quest in the gamification service.
from datetime import datetime
from bson import ObjectId

class Quest: # Initialize the Quest class with the following attributes:
    def __init__(self,
                 campaign_id,
                 title,
                 description,
                 objectives,
                 xp_reward=50,
                 customization_rewards=None,
                 order=0,
                 quest_id=None):
        self.quest_id = quest_id or str(ObjectId())
        self.campaign_id = campaign_id
        self.title = title
        self.description = description
        self.objectives = objectives  # List of {type, target, current, required}
        self.order = order
        self.xp_reward = xp_reward
        self.customization_rewards = customization_rewards or []
        self.created_at = datetime.now().isoformat()

    
    def to_dict(self): # Convert the quest object to a dictionary
        return {
            "quest_id": self.quest_id,
            "campaign_id": self.campaign_id,
            "title": self.title,
            "description": self.description,
            "objectives": self.objectives,
            "order": self.order,
            "xp_reward": self.xp_reward,
            "customization_rewards": self.customization_rewards,
            "created_at": self.created_at
        }