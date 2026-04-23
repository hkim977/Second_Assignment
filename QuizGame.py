def start_quiz():
    # MCQ Quiz Bank
    questions = [
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
            "options": ["1. Pizza", "2. Cheese curds", "3. Tacos", "4. Sushi"],
            "answer": "2",
            "hint": "They are squeaky and a key ingredient in poutine!"
        }
    ]

    score = 0
    print("--- Welcome to Sandy's MCQ Quiz! ---")
    print("Rules: Select 1, 2, 3, or 4. Correct (+50), Wrong/Hint (-10)\n")
    hint = 2

    for q in questions:
        print(f"Question: {q['question']}")
        for option in q['options']:
            print(option)
        
        while True:
            user_input = input("Your choice (1-4 or type 'hint'): ").strip().lower()

            if user_input == "hint":
                hint--
                score -= 10
                print(f"HINT: {q['hint']} (Score: {score})")
                continue 
 
            if user_input == q['answer']:
                score += 50
                print(f"Correct! +50 points. (Current Score: {score})\n")
                break
            elif user_input != q['answer']:
                score -= 10
                print(f"Incorrect. -10 points. (Current Score: {score})")
                print("Try again!")
            else:
                print("Invalid input. Please enter 1, 2, 3, 4, or 'hint'.")

    print("--- Quiz Over! ---")
    print(f"Your final score is: {score}")

if __name__ == "__main__":
    start_quiz()