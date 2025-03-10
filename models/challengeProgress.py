from datetime import datetime

# ChallengeProgress model is a class that represents the progress of a user in a challenge.
class ChallengeProgress:
    def __init__(self, user_id, challenge_id, progress=0, last_updated=None):
        self.user_id = user_id
        self.challenge_id = challenge_id
        self.progress = progress
        self.last_updated = last_updated or datetime.now()
        
    def to_dict(self): # Convert the challenge progress object to a dictionary
        return {
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'progress': self.progress, 
            'last_updated': self.last_updated
        }
        
    @classmethod # Convert a dictionary to a Challenge
    def from_dict(cls, data):
        return cls(
            user_id=data.get('user_id'),
            challenge_id=data.get('challenge_id'),
            progress=data.get('progress', 0),
            last_updated=data.get('last_updated')
        )