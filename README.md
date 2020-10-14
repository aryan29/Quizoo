# Quizoo :green_book::closed_book:
Free Online Quiz Platform for conducting quizes with lots of security features to avoid cheating and completely free   

<img src="ReadmeAssets/1.png">
</img>    
      

### Detailed List of Features it should have 
* Allow Creation of Quiz
* Allow People to give quiz by simple google sign in
* Proper Statistical Analysis of the Quiz to the admin after that Quiz
* Allow Admin to Re-schedule timing of quiz
* Allow addition and deletion of questions on admin panel
* Users to get questions in random order only one question visible at a time
* Show timer to user in which quiz is about to over
* Immediate test end in case of tab change or exiting full window
* List of Settings on Admin side
  * Auto email students there score after test got over
  * Show questions in random order or not
  * Shuffle options or not
  * Show students their score during the test itself
  * Can a student reattempt test after its end time
  * Allow admin to retake a previous quiz
  * Allowing multiple admins for a quiz
  * Camera On mode or not
  * Generating a Random Quiz from Previously owned question set 
  * Give x amount of questions to each user from a pool of n questions

 * A nice good looking and user friendly frontend is must
 
### :camera: Screenshots
<table>
<tr>
<td>
<kbd>
<img src="ReadmeAssets/1.png">
</kbd>
</td>
<td>
<kbd>
<img src="ReadmeAssets/2.png">
</kbd>
</td>
</tr>
<tr>
<td>
<kbd>
<img src="ReadmeAssets/3.png">
</kbd>
</td>
<td>
<kbd>
<img src="ReadmeAssets/4.png">
</kbd>
</td>
</tr>
<tr>
<td>
<kbd>
<img src="ReadmeAssets/5.png">
</kbd>
</td>
<td>
<kbd>
<img src="ReadmeAssets/6.png">
</kbd>
</td>
</tr>
<tr>
<td>
<kbd>
<img src="ReadmeAssets/7.png">
</kbd>
</td>
<td>
<kbd>
<img src="ReadmeAssets/8.png">
</kbd>
</td>
</tr>
<tr>
<td>
<kbd>
<img src="ReadmeAssets/9.png">
</kbd>
</td>
<td>
<kbd>
<img src="ReadmeAssets/10.png">
</kbd>
</td>
</tr>
</table>

### Get Started
##### Django Development Server
```
git clone https://github.com/aryan29/Quizoo.git    
cd Quizoo    
git checkout dev  
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cd quizoo
python manage.py runserver
```  
##### Nginx Deployment Server
```
git clone https://github.com/aryan29/Quizoo.git    
cd Quizoo    
git checkout dev    
sudo docker-compose -f docker-compose-deploy.yml up --build  
```  

### Contribution
Don't be lazy:smile: clone this repo and start contributing

<hr></hr>
Do leave a star :star: if you like this repo :blush:
