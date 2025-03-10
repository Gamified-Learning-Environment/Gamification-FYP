# Player model is a class that represents a player in the gamification service. 

# Initialize the Player class with the following attributes:
class Player: # Self is a reference to current instance, title and questions are parameter
    def __init__(self, user_id, username=None, current_level=1, xp=0, achievements=None, badges=None, completed_challenges=None, tracked_challenges=None, streaks=None, category_levels=None, quizzes_completed=0, perfect_scores=0): 
        self.user_id = user_id
        self.username = username or "Player"
        self.current_level = current_level
        self.xp = xp
        self.achievements = achievements or []
        self.badges = badges or []
        self.completed_challenges = completed_challenges or []
        self.tracked_challenges = tracked_challenges or []
        self.quizzes_completed = quizzes_completed
        self.perfect_scores = perfect_scores
        self.streaks = streaks or []
        self.category_levels = category_levels or {}

    def to_dict(self): # Convert the player object to a dictionary
        return {
            'user_id': self.user_id,
            'username': self.username,
            'current_level': self.current_level,
            'xp': self.xp,
            'achievements': self.achievements,
            'badges': self.badges,
            'completed_challenges': self.completed_challenges,
            'tracked_challenges': self.tracked_challenges,
            'quizzes_completed': self.quizzes_completed,
            'perfect_scores': self.perfect_scores,
            'streaks': self.streaks,
            'category_levels': self.category_levels,
            'next_level_xp': self.calculate_next_level_xp(),
            'level_progress': self.calculate_level_progress()
        }
    
    def calculate_next_level_xp(self): # Calculate the xp required to reach the next level
        # Formula: Each level requires more xp than previous
        return 1000 * (self.current_level * 0.5)
    
    def calculate_level_progress(self): # Calculate the progress towards the next level
        next_level_xp = self.calculate_next_level_xp()
        
        # Calculate the xp required to reach the previous level if the current level is greater than 1
        prev_level_xp = 1000 * ((self.current_level - 1) * 0.5) if self.current_level > 1 else 0 

        # Calculate progress percent
        current_level_xp_range = next_level_xp - prev_level_xp
        progress = self.xp - prev_level_xp

        # Return as percent
        # Return the progress as a percentage if the current level xp range is greater than 0
        return (progress / current_level_xp_range) * 100 if current_level_xp_range > 0 else 0 
    
    