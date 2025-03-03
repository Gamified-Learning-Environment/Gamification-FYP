# Streak model is a class that represents a streak in the gamification service.

from datetime import datetime, timedelta

class Streak: 
    def __init__(self, user_id, category=None, current_streak=0, highest_streak=0, last_activity_date=None):
        self.user_id = user_id
        self.category = category # None for overall streak
        self.current_streak = current_streak
        self.highest_streak = highest_streak
        self.last_activity_date = last_activity_date or datetime.now() # Default to current date if not provided

    def to_dict(self): # Convert the streak object to a dictionary
        return {
            'user_id': self.user_id,
            'category': self.category,
            'current_streak': self.current_streak,
            'highest_streak': self.highest_streak,
            'last_activity_date': self.last_activity_date
        }
    
    def update_streak(self):
        today = datetime.now().date()
        last_activity = self.last_activity_date.date()


        # If the last activity was today, return the current streak
        if today == last_activity: 
            return self.current_streak
        
        # If the last activity was yesterday, increment the current streak
        if today == last_activity + timedelta(days=1):
            self.current_streak += 1
            # Update the highest streak if the current streak is higher
            if self.current_streak > self.highest_streak:
                self.highest_streak = self.current_streak


        # If the last activity was more than 1 day ago, reset the current streak to 1
        elif today > last_activity + timedelta(days=1):
            self.current_streak = 1

        # Update the last activity date to today
        self.last_activity_date = datetime.now()
        return self.current_streak