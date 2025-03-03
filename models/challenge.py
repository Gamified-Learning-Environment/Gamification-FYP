# Challenge model is a class that represents a challenge in the gamification service.
from datetime import datetime, timedelta
import uuid

# Initialize the Challenge class with the following attributes:
class Challenge:
    def __init__(self, challenge_id=None, title="", description="", category="", start_date=None, end_date=None, reward_xp=0, reward_badges=None, requirements=None):
        self.challenge_id = challenge_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.category = category
        self.start_date = start_date or datetime.now()
        self.end_date = end_date or (self.start_date + timedelta(days=7)) # Default end date is 7 days from start date
        self.reward_xp = reward_xp
        self.reward_badges = reward_badges or []
        self.requirements = requirements or []

    def to_dict(self):
        return {
            'challenge_id': self.challenge_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'reward_xp': self.reward_xp,
            'reward_badges': self.reward_badges,
            'requirements': self.requirements,
            'is_active': self.is_active()
        }

    def is_active(self):
        current_time = datetime.now()
        return self.start_date <= current_time <= self.end_date