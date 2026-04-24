
1. 프로젝트 개요
   ```bash
   a. This project is about implementing a quiz game using Python. Users can take quizzes, add new questions, and save their scores.
   ```

2. Why I chose this quiz for this project:
   ```bash
   a. I chose trivia as the theme for the quiz. The reasons are as follows:
        i. focus on logic: By using a content that is familiar to me, I could focus more on the technical                   implementation of the program. 
   ```
3. how to run the file: open vs code by using a terminal(code .) and run the python file
4. Structure of the file:
   ```bash
   a. Quiz class: represents the structure of the quiz
   b. QuizGame class: sets up the quiz
       i. init function: question bank, shows menu
       ii. show menu function: shows menu and lets the user to choose the option
           if user selects option 1: start quiz
           if user selects option 2: add question
           if user selects option 3: print highest score
           if user selects option 4: quit the program
       iii. start quiz function: starts the quiz
            Step 1: go through each question - show the question and answers to the user
            Step 2: user types his answer
            Step 3: do one of the following
               If user types 'hint': give hint and take 10 points away(If user used 2 hints, let him                   know that he ran out of hints.)
               If user types an answer and gets the question right: give 50 points to user
               If user types an answer and doesn't get the question right: take 10 points away from the                user
               If the input is not a number: tell the user to type his answer again.
            Step 4: Update the user's score(if it's necessary to do so) & save it to user's account
        iv. add quiz function: adds question to the quiz
            Step 1: make the user create a question
            Step 2: make the user create 4 options (answer choices)
            Step 3: make the user type answer for the question
            Step 4: make the user create a hint for the question
            Step 5: add the user's inputs from step 1,2,3,and 4 to the question bank
            Step 6: save data
   ```
