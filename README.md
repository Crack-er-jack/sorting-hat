# sorting-hat quiz
If you're unfamiliar with Harry Potter series by J.K.Rowling, when you get accepted into the magic school "Hogwarts" the sorting hat assigns you a house. There are a total of 4 houses, Gryffindor for the Brave, Slytherin for the Cunning, Ravenclaw for the Wit and Hufflepuff for the Loyal.

# Soft Skills assessed
There are a total of 5 questions in the quiz. Each question assesses the following soft skils:
- Creativity
- Problem Solving
- Eye for Detail
- Adaptability
- Flexibility

## Quiz pathways
1. When 2nd question is answered wrong, a 2nd chance is given to the user. A puzzle is given as the second chance but failing to solve it will lead to Deadend1
2. Similary to 2nd question, when 4th question is answered wrong, a 2nd chance is given to the user. A puzzle is given as the second chance but failing to solve it will lead to Deadend2
3. The questions must be attempted in order and a question can only be answered once. (Except 2 and 4)
4. Upon attempting all 5 questions, the ending is reached where the sorted house, scores of various soft skills are displayed.

## Set up the project:
- Download the zip file from github
- Navigate to the project folder using cd on a linux terminal
- Run "python -m venv my-env" to create a virtual environment
- Run "source my-env/bin/activate" to activate the virtual environment
- Run "pip install -r requirements.txt" to install required libraries
- Finally run, "flask run" on the terminal. Copy paste the link shown in the output to access the website.
- Alternatively you can also access the website at, [https://sorting-hat.onrender.com](https://sorting-hat.onrender.com)

# Feature Checklist:
- Anyone with an email address can create an Id and password to participate in the game :white_check_mark:
- 5 clues :white_check_mark:
- 2 deadends :white_check_mark:
- 1 solution :white_check_mark:
- user score for each question based on the softskill is stored :white_check_mark:
- browser retains user progress on refresh :white_check_mark:
- Admin dashboard :white_check_mark:
- Hosted on cloud platform :white_check_mark:

## Additional Features:
- Spider chart showing score in each soft skill is plotted for easily drawing insights about a user

# Tech Stack:
- Backend: Flask
- Database: MySQL
- Frontend: jinja html templates

Thank you for this interesting task eLitmus!



