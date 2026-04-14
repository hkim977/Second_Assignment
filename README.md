============================================================
1. 프로젝트 개요
   a. 이 프로젝트는 Python과 Git을 활용하여 터미널에서 실행되는 퀴즈 게임을 구현하는 과제입니다. 사용자는 퀴즈를 풀고, 새로운 퀴즈를 추가하며, 점수를 기록할 수 있습니다.
   b. 또한 JSON 파일을 활용하여 프로그램 종료 후에도 퀴즈 데이터와 점수, 플레이 기록이 유지되는 데이터 영속성을 구현했습니다.
   =======================================================

3. 퀴즈 주제 선정 이유
   a. 본 프로젝트에서는 개인적인 질문 기반의 퀴즈를 주제로 선택했습니다. 이유는 다음과 같습니다:

        직접 문제를 만들기 쉽고 확장성이 높음
        프로그램 기능 구현에 집중할 수 있음
        데이터 저장 및 관리 구조를 이해하기에 적합
   
4. how to run the file: open vs code by using a terminal(code .) and run the python file
5. list of contents:
    a. Take the quiz
       1) Randomly select questions from the quiz data
       2) Check whether the answer is correct or incorrect
       3) Scoring system:
          Correct answer: 100 points
          Wrong answer: -15 points
       4) Hint: Each round allows 2 hints in total
    b. add questions
       1) Allow user to add a new question with: question, 4 multiple-choice options, correct answer and a hint
       2) input validation: No empty inputs, must be 4 choices
    c. Save data to a JSON file
6. View the quiz
   a. Display all the quizzes
   b. If the quizzes don't exist: handle the case in a professional maanner ("No quizzes available")
7. View Score
   a. Reveal the highest score
8. 
   
