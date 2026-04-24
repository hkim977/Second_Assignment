import json
from pathlib import Path




# Section: Custom exception
class SafeExitSignal(Exception):
   """Stop the program safely when the user interrupts input."""




# Section: Quiz model
class Quiz:
   """Represent one quiz question with four choices and one correct answer."""


   def __init__(self, question, choices, answer):
       self.question = question.strip()
       self.choices = [choice.strip() for choice in choices]
       self.answer = answer
       self.validate()


   def validate(self):
       """Validate quiz data before using or saving it."""
       if not self.question:
           raise ValueError("Question cannot be empty.")


       if len(self.choices) != 4:
           raise ValueError("Each quiz must have exactly 4 choices.")


       if any(not choice for choice in self.choices):
           raise ValueError("Choices cannot be empty.")


       if not isinstance(self.answer, int) or not 1 <= self.answer <= 4:
           raise ValueError("Answer must be a number between 1 and 4.")


   def display(self, number):
       """Print the quiz to the console."""
       print("-" * 40)
       print(f"[Question {number}]")
       print(self.question)
       print()


       for index, choice in enumerate(self.choices, start=1):
           print(f"{index}. {choice}")


       print()


   def is_correct(self, user_answer):
       """Return True when the user's answer matches the correct answer."""
       return user_answer == self.answer


   def to_dict(self):
       """Convert the quiz object into a JSON-friendly dictionary."""
       return {
           "question": self.question,
           "choices": self.choices,
           "answer": self.answer,
       }


   @classmethod
   def from_dict(cls, data):
       """Create a quiz object from loaded JSON data."""
       question = str(data.get("question", "")).strip()
       raw_choices = data.get("choices", data.get("options", []))
       answer = data.get("answer")


       if not isinstance(raw_choices, list):
           raise ValueError("Choices must be stored as a list.")


       cleaned_choices = []
       for choice in raw_choices[:4]:
           cleaned_choices.append(cls._remove_number_prefix(str(choice).strip()))


       return cls(question, cleaned_choices, int(answer))


   @staticmethod
   def _remove_number_prefix(choice_text):
       """Remove an old number prefix such as '1. ' from a choice."""
       if len(choice_text) >= 2 and choice_text[0] in "1234" and choice_text[1] == ".":
           return choice_text[2:].strip()
       return choice_text




# Section: Quiz game controller
class QuizGame:
   """Manage menu flow, quiz data, score tracking, and file persistence."""


   STATE_FILE = Path(__file__).resolve().parent / "state.json"


   def __init__(self):
       self.quizzes = []
       self.best_score = 0
       self.best_correct_count = 0
       self.best_total_questions = 0
       self.startup_message = ""
       self.load_state()


   def run(self):
       """Start the main menu loop."""
       self.print_banner()


       try:
           while True:
               self.show_menu()
               menu_choice = self.read_number("Choice: ", 1, 5)
               print()


               if menu_choice == 1:
                   self.play_quiz()
               elif menu_choice == 2:
                   self.add_quiz()
               elif menu_choice == 3:
                   self.list_quizzes()
               elif menu_choice == 4:
                   self.show_best_score()
               elif menu_choice == 5:
                   self.exit_game()
                   break
       except SafeExitSignal:
           self.handle_safe_exit()


   def print_banner(self):
       """Print the title and current load status."""
       print("=" * 40)
       print("        My Python Quiz Game")
       print("=" * 40)


       if self.startup_message:
           print(self.startup_message)
           print("=" * 40)


   def show_menu(self):
       """Display the main menu."""
       print("1. Take Quiz")
       print("2. Add Quiz")
       print("3. Quiz List")
       print("4. Check Score")
       print("5. Exit")
       print("=" * 40)


   def play_quiz(self):
       """Run every saved quiz and update the best score."""
       if not self.quizzes:
           print("No quizzes registered. Please add a quiz first.\n")
           return


       total_questions = len(self.quizzes)
       correct_count = 0


       print(f"Starting a total of {total_questions} questions.\n")


       for index, quiz in enumerate(self.quizzes, start=1):
           quiz.display(index)
           answer = self.read_number("Answer number (1-4): ", 1, 4)


           if quiz.is_correct(answer):
               correct_count += 1
               print("Correct!\n")
           else:
               print(f"Incorrect. The correct answer is {quiz.answer}.\n")


       score = int((correct_count / total_questions) * 100)
       print("=" * 40)
       print(f"Result: {correct_count} correct out of {total_questions} questions")
       print(f"Score: {score} points")


       if score > self.best_score:
           self.best_score = score
           self.best_correct_count = correct_count
           self.best_total_questions = total_questions
           self.save_state()
           print("New high score!")
       else:
           print("High score remains.")


       print("=" * 40)
       print()


   def add_quiz(self):
       """Collect quiz data from the user and save it."""
       print("Adding a new quiz.")
       question = self.read_text("Enter the question: ")


       choices = []
       for index in range(1, 5):
           choice = self.read_text(f"Choice {index}: ")
           choices.append(choice)


       answer = self.read_number("Correct answer number (1-4): ", 1, 4)


       new_quiz = Quiz(question, choices, answer)
       self.quizzes.append(new_quiz)
       self.save_state()


       print("Quiz added.\n")


   def list_quizzes(self):
       """Show the saved quiz list."""
       if not self.quizzes:
           print("No quizzes registered.\n")
           return


       print(f"Registered quiz list (Total {len(self.quizzes)})")
       print("-" * 40)


       for index, quiz in enumerate(self.quizzes, start=1):
           print(f"[{index}] {quiz.question}")


       print("-" * 40)
       print()


   def show_best_score(self):
       """Print the best score information."""
       if self.best_total_questions == 0:
           print("No quiz records yet.\n")
           return


       print(f"High score: {self.best_score} points")
       print(
           f"Record: {self.best_correct_count} correct out of {self.best_total_questions} questions\n"
       )


   def load_state(self):
       """Load quizzes and score data from the JSON file."""
       if not self.STATE_FILE.exists():
           self.quizzes = self.create_default_quizzes()
           self.startup_message = (
               f"state.json file not found, loaded {len(self.quizzes)} default quizzes."
           )
           return


       try:
           with self.STATE_FILE.open("r", encoding="utf-8") as file:
               data = json.load(file)


           raw_quizzes = data.get("quizzes", data.get("questions", []))
           if not isinstance(raw_quizzes, list):
               raise ValueError("Quiz list is missing or invalid.")


           self.quizzes = [Quiz.from_dict(item) for item in raw_quizzes]
           self.best_score = self.parse_non_negative_int(
               data.get("best_score", data.get("high_score", 0))
           )
           self.best_correct_count = self.parse_non_negative_int(
               data.get("best_correct_count", 0)
           )
           self.best_total_questions = self.parse_non_negative_int(
               data.get("best_total_questions", 0)
           )


           self.startup_message = (
               f"Loaded saved data. "
               f"({len(self.quizzes)} quizzes, high score {self.best_score} points)"
           )
       except (OSError, json.JSONDecodeError, TypeError, ValueError):
           self.quizzes = self.create_default_quizzes()
           self.best_score = 0
           self.best_correct_count = 0
           self.best_total_questions = 0
           self.startup_message = (
               "state.json file corrupted, restored with default quiz data."
           )
           self.save_state()


   def save_state(self):
       """Save quizzes and score data to the JSON file."""
       data = {
           "quizzes": [quiz.to_dict() for quiz in self.quizzes],
           "best_score": self.best_score,
           "best_correct_count": self.best_correct_count,
           "best_total_questions": self.best_total_questions,
       }


       try:
           with self.STATE_FILE.open("w", encoding="utf-8") as file:
               json.dump(data, file, ensure_ascii=False, indent=4)
       except OSError:
           print("An error occurred while saving the file. Please try again.")


   def exit_game(self):
       """Save data and close the program from the menu."""
       self.save_state()
       print("Saving data and exiting the program.")


   def handle_safe_exit(self):
       """Save data and close the program after Ctrl+C or EOF."""
       print("\nInput interrupted, saving and exiting safely.")
       self.save_state()


   def read_text(self, prompt):
       """Read a non-empty line of text from the user."""
       while True:
           try:
               value = input(prompt).strip()
           except (KeyboardInterrupt, EOFError):
               raise SafeExitSignal from None


           if not value:
               print("Empty input is not allowed. Please enter again.")
               continue


           return value


   def read_number(self, prompt, min_value, max_value):
       """Read a number in a specific range from the user."""
       while True:
           text = self.read_text(prompt)


           if not text.isdigit():
               print(
                   f"Invalid input. Please enter a number between {min_value} and {max_value}."
               )
               continue


           number = int(text)
           if not min_value <= number <= max_value:
               print(
                   f"Invalid input. Please enter a number between {min_value} and {max_value}."
               )
               continue


           return number


   def create_default_quizzes(self):
       """Build the default quiz set used on first launch or recovery."""
       return [
           Quiz(
               "What data type is used to represent strings in Python?",
               ["int", "str", "bool", "list"],
               2,
           ),
           Quiz(
               "What is the most appropriate statement to execute different code based on conditions?",
               ["for", "if", "while", "import"],
               2,
           ),
           Quiz(
               "What data type stores multiple values in order?",
               ["dict", "list", "bool", "float"],
               2,
           ),
           Quiz(
               "What keyword is used to return the result of a function to the caller?",
               ["break", "pass", "return", "continue"],
               3,
           ),
           Quiz(
               "What module from the Python standard library is mainly used to handle JSON files?",
               ["random", "json", "math", "time"],
               2,
           ),
           Quiz(
               "What is the usual name for the first parameter that refers to the instance itself in a class?",
               ["this", "me", "self", "current"],
               3,
           ),
       ]


   @staticmethod
   def parse_non_negative_int(value):
       """Convert a value into a non-negative integer."""
       number = int(value)
       if number < 0:
           raise ValueError("Negative numbers are not allowed.")
       return number




# Section: Program entry point
if __name__ == "__main__":
   game = QuizGame()
   game.run()