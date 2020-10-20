# Quizoo :green_book::closed_book:
 

<img src="ReadmeAssets/7.png">
</img>     
Free Online Quiz Platform for conducting quizes with lots of security features to avoid cheating and completely free    
    


## Why Quizoo?
With Quizoo you can conduct mcqs test online too easily within matter of minutes without worrying about anything Quizoo will handle everything for you.     
It includes various features which makes it difficult to conduct cheating online and prevent it to the maximum level possible  
### LockDown Browser
It’s a custom browser window that adds more security to the exam environment by disabling those features that can be misused. When the lockdown browser is enabled during an exam, it restricts candidates from opening console, accessing other websites, switching applications, copying or printing questions, or even taking screenshots.     
### Resquencing Questions with NoBack Button
Most of the time participants tend to cheat because they can view all questions at once or move back to the previous questions , it becomes very difficult for the participants to cheat in limitted time if every person will get questions in different order and they are not allowed to move back to the previous question     
### Automated Image Poctoring(In Development)
This tool allows test creator to enable camera & microphone mode which sends audio-video and screen share feeds and makes use of advanced audio and video analytics to monitor any suspicious activities during the test

Beside all that Quizoo makes it easy to send results to each candidate's email address or downloading excel sheet of cadidate's responses  by just enabling few setting from the quiz panel  

## Architecture and Database
The app is hosted using uWSGI Server and make use of NGINX for hosting static files and as a reverse proxy      
        
Here is how the database design looks like for the Django App
<img src="ReadmeAssets/model.png">
</img>    
Database used is sqlite3 for current moment but will shift to postgresql in future      

##  Futures Coming
* Automated Image Poctoring 
* Live Anouncements during online test from admin panel
* View the candidate’s screen- live


## Contributors
[Aryan Khandelwal](https://github.com/aryan29)    
[Mukul Choudhury](https://github.com/Mukul-9)    
[Vibhu Bhatia](https://github.com/vibhubhatia007)    







