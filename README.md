# FYP - Gamification Repository

This is the repository for managing the gamification elements of my Gamified Learning Environment where I plan to Implement an array of gamified features such as achievements, progress tracking, and leaderboards to enhance a student’s motivation to learn. See the Frontend and the Project Dissertation for greater details.

## Service Overview
The gamification microservice manages all the gaming elements that are developed within the platform to enhance a user's engagement and encourage their motivation to learn. These game mechanics help to reward users for study progress, give them a sense of achievement and maybe give them more consistent study habits.

Here is a full overview of each gamified element this system implemented: 
- Experience Points (XP) System: User progress in the app is tracked through an accumulative gain of experience points. This is where the app took its name from. Points are rewarded for completing quizzes, doing daily challenges, earning badges or completing achievements as well as other positive behaviour like maintaining daily streaks. XP gained is pool either into the player's overall XP gained on the platform or into the specific category being studied.
- Levelling System: Accumulated XP is converted into levels. This includes both global levels that indicate overall engagement with the platform and category-specific levels that show expertise in the respective category of study. Each level requires progressively more XP to achieve than the previous.
- Achievement System: A fully fledged achievement system is developed. This involves achievement objects that are stored in the database, and user's can unlock them by meeting their specified criteria. A variety of ways are used to check if a user has trigged an achievement milestone or not.
- Badge System: These are visual awards, sort of like stamps. They are earned when ever an achievement is complete or for select category levels reached. User's can display them on their profile to showcase what significant accomplishments they've made. They serve as a form of status symbol, a player's profile can be customised to showcase whichever ones they prefer.
- Leaderboard System: Maintains rankings across different metrics within the app. Whether that be total quizzes completed, achievements earned, total xp gained or more. This is a classic game mechanic that fosters some friendly competition amongst peers. 

## Deployment and Running
While you could download, compile and run each of the repositories for this Final Year Project and get a more in depth look into the code, it is also fully deployed on Railway at the following link : https://exper-frontend-production.up.railway.app

Alternatively, here's a QR Code: 

![ExperQRCode](https://github.com/user-attachments/assets/57795718-9c35-462c-b257-03cf354f5bd4)

Should this not be sufficient for grading, please see the instructions below: 

### Prerequisites
Node.js (v18+) and npm/yarn
Python (v3.9+)
MongoDB database
API keys for:
OpenAI
Anthropic Claude (optional)
Google Gemini (optional)

### Setup and Installation
1. Clone each repository for this project.
2. For each microservice repeat these steps
      1. 
         ```
         cd service-directory  # e.g., Quiz-Generation-FYP
         python -m venv venv
         source venv/bin/activate  # On Windows: venv\Scripts\activate
         pip install -r requirements.txt
         ```
         
      2. Environmental Variables
         Create a .env file in each microservice directory with appropriate values:
         ```
            MONGODB_URI=mongodb://localhost:27017/quizdb
            OPENAI_API_KEY=your_openai_key
            ANTHROPIC_API_KEY=your_anthropic_key  # Optional
            GOOGLE_API_KEY=your_gemini_key  # Optional
         ```
         User Management Service
         ```
         MONGODB_URI=mongodb://localhost:27017/userdb
         JWT_SECRET=your_jwt_secret
         ```

         Results Tracking Service
         ```
         MONGODB_URI=mongodb://localhost:27017/resultsdb
         ```
         Gamification Service
         ```
         MONGODB_URI=mongodb://localhost:27017/gamificationdb
         ```

3. Frontend Setup
      ```
      cd Exper-Frontend/experfrontend
      npm install
      ```
      Create a .env.local file with:
      ```
      NEXT_PUBLIC_USER_SERVICE_URL=http://localhost:8080
      NEXT_PUBLIC_QUIZ_SERVICE_URL=http://localhost:9090
      NEXT_PUBLIC_RESULTS_SERVICE_URL=http://localhost:8081
      NEXT_PUBLIC_GAMIFICATION_SERVICE_URL=http://localhost:8082
      ```

4. Running the Application
   1. Start the microservices, run each in a seperate terminal:
      ```
      # Quiz Generation Service
      cd Quiz-Generation-FYP
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      python app.py  # Will run on port 9090
      
      # User Management Service
      cd User-Management-Service
      source venv/bin/activate
      python app.py  # Will run on port 8080
      
      # Results Tracking Service
      cd Results-Tracking-FYP
      source venv/bin/activate
      python app.py  # Will run on port 8081
      
      # Gamification Service
      cd Gamification-FYP
      source venv/bin/activate
      python app.py  # Will run on port 8082
      ```
   2. Start the Frontend
      ```
      cd Exper-Frontend/experfrontend
      npm run dev
      ```
   Visit http://localhost:3000 to access the application.

