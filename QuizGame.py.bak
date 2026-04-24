
import json
#structure of the quiz
class Quiz: 
    def __init__(self, question, options, answer, hint):
        self.question = question
        self.options = options
        self.answer = answer
        self.hint = hint

#setting up for the quiz
class QuizGame: 
    def __init__(self):
        self.questions = [
            {
                "question": "What is my name?",
                "options": ["1. Sarah", "2. Sandy", "3. Sam", "4. Sophie"],
                "answer": "2",
                "hint": "It's a name often associated with the beach."
            },
            {
                "question": "Where am I from?",
                "options": ["1. USA", "2.UK", "3. Canada", "4. Australia"],
                "answer": "3",
                "hint": "It's the second-largest country in the world by land area."
            },
            {
                "question": "What's my hobby?",
                "options": [
                    "1. Playing sports", 
                    "2. Cooking and baking", 
                    "3. Watching movies and tv shows", 
                    "4. Reading books"
                ],
                "answer": "3",
                "hint": "It involves a screen, Netflix, or a cinema."
            },
            {
                "question": "What's my favorite food?",
                "options": ["1. Rice cake", "2. Pizza", "3. Poutine", "4. Cheese"],
                "answer": "3",
                "hint": "It is well-known in Canada!"
            }
            ,
            {
                "question": "What's the capital of South Korea?",
                "options": ["1. Busan", "2. Seoul", "3. Incheon", "4. Daegu"],
                "answer": "2",
                "hint": "It is the largest city in the country. "
            }
        ]
        self.high_score = 0
        self.show_menu()
    #shows menu for the game
    def show_menu(self):
        while True:
            print("-----Menu------")
            print("1. Take Quiz\n2. Add question\n3.Check highest score\n4.Quit")
            choice = input("Select: ")
            if choice == '1': self.start_quiz()
            elif choice == '2': self.add_quiz()
            elif choice == '3': print(f"High Score: {self.high_score}")
            elif choice == '4': break
    def start_quiz(self):
    # Starts the quiz
        current_score = 0
        print("--- Welcome to Sandy's MCQ Quiz! ---")
        print("Rules: Select 1, 2, 3, or 4. Correct (+50), Wrong/Hint (-10)\n")
        hint = 2

        for q in self.questions:
            print(f"Question: {q['question']}")
            for option in q['options']:
                print(option)
            
            while True:
                user_input = input("Your choice (1-4 or type 'hint'): ").strip().lower()

                if user_input == "hint":
                    if hint > 0:
                        hint-= 1
                        current_score -= 10
                        print(q['hint'])
                        continue
                    else:
                        print("Ran out of hints")
    
                if user_input == q['answer']:
                    current_score += 50
                    print(f"Correct! +50 points. (Current Score: {current_score})\n")
                    break
                elif user_input != q['answer']:
                    current_score -= 10
                    print(f"Incorrect. -10 points. (Current Score: {current_score})")
                    print("Try again!")
                else:
                    print("Invalid input. Please enter 1, 2, 3, 4, or 'hint'.")

        print("--- Quiz Over! ---")
        print(f"Your final score is: {current_score}")

        if current_score > self.high_score:
            self.high_score = current_score
            print(f"Score updated! Highest score is {self.high_score}")
            self.save_data()

    def add_quiz(self):
        print("----Adding a question")
        new_question = input("Enter the question: ").strip()
        options = []
        for i in range(1,5):
            opt = input(f"Enter option {i}: ").strip()
            options.append(f"{i}. {opt}")
        while True:
            new_answer = input("Enter the number(1-4): ").strip()
            if new_answer in ["1","2", "3","4"]:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 4.")
        
        new_hint = input("Enter a hint for this question: ").strip()

        new_quiz = {
            "question": new_question,
            "options": options,
            "answer": new_answer,
            "hint": new_hint}
        
        self.questions.append(new_quiz)
        self.save_data()
        print("Successfully saved the new quiz!!")
    
    def save_data(self):
        data_to_save = {
            "high_score": self.high_score,
            "questions": self.questions

        }
        with open('state.json', 'w', encoding = 'utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii = False, indent = 4)

if __name__ == "__main__":
    QuizGame()