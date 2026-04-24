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
       print(f"[문제 {number}]")
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
               menu_choice = self.read_number("선택: ", 1, 5)
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
       print("        나만의 파이썬 퀴즈 게임")
       print("=" * 40)


       if self.startup_message:
           print(self.startup_message)
           print("=" * 40)


   def show_menu(self):
       """Display the main menu."""
       print("1. 퀴즈 풀기")
       print("2. 퀴즈 추가")
       print("3. 퀴즈 목록")
       print("4. 점수 확인")
       print("5. 종료")
       print("=" * 40)


   def play_quiz(self):
       """Run every saved quiz and update the best score."""
       if not self.quizzes:
           print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.\n")
           return


       total_questions = len(self.quizzes)
       correct_count = 0


       print(f"총 {total_questions}문제를 시작합니다.\n")


       for index, quiz in enumerate(self.quizzes, start=1):
           quiz.display(index)
           answer = self.read_number("정답 번호 (1-4): ", 1, 4)


           if quiz.is_correct(answer):
               correct_count += 1
               print("정답입니다!\n")
           else:
               print(f"오답입니다. 정답은 {quiz.answer}번입니다.\n")


       score = int((correct_count / total_questions) * 100)
       print("=" * 40)
       print(f"결과: {total_questions}문제 중 {correct_count}문제 정답")
       print(f"점수: {score}점")


       if score > self.best_score:
           self.best_score = score
           self.best_correct_count = correct_count
           self.best_total_questions = total_questions
           self.save_state()
           print("새로운 최고 점수입니다!")
       else:
           print("최고 점수는 유지됩니다.")


       print("=" * 40)
       print()


   def add_quiz(self):
       """Collect quiz data from the user and save it."""
       print("새로운 퀴즈를 추가합니다.")
       question = self.read_text("문제를 입력하세요: ")


       choices = []
       for index in range(1, 5):
           choice = self.read_text(f"선택지 {index}: ")
           choices.append(choice)


       answer = self.read_number("정답 번호 (1-4): ", 1, 4)


       new_quiz = Quiz(question, choices, answer)
       self.quizzes.append(new_quiz)
       self.save_state()


       print("퀴즈가 추가되었습니다.\n")


   def list_quizzes(self):
       """Show the saved quiz list."""
       if not self.quizzes:
           print("등록된 퀴즈가 없습니다.\n")
           return


       print(f"등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
       print("-" * 40)


       for index, quiz in enumerate(self.quizzes, start=1):
           print(f"[{index}] {quiz.question}")


       print("-" * 40)
       print()


   def show_best_score(self):
       """Print the best score information."""
       if self.best_total_questions == 0:
           print("아직 퀴즈를 푼 기록이 없습니다.\n")
           return


       print(f"최고 점수: {self.best_score}점")
       print(
           f"기록: {self.best_total_questions}문제 중 "
           f"{self.best_correct_count}문제 정답\n"
       )


   def load_state(self):
       """Load quizzes and score data from the JSON file."""
       if not self.STATE_FILE.exists():
           self.quizzes = self.create_default_quizzes()
           self.startup_message = (
               f"state.json 파일이 없어 기본 퀴즈 {len(self.quizzes)}개를 불러왔습니다."
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
               f"저장된 데이터를 불러왔습니다. "
               f"(퀴즈 {len(self.quizzes)}개, 최고 점수 {self.best_score}점)"
           )
       except (OSError, json.JSONDecodeError, TypeError, ValueError):
           self.quizzes = self.create_default_quizzes()
           self.best_score = 0
           self.best_correct_count = 0
           self.best_total_questions = 0
           self.startup_message = (
               "state.json 파일이 손상되어 기본 퀴즈 데이터로 복구했습니다."
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
           print("파일 저장 중 오류가 발생했습니다. 다시 시도해 주세요.")


   def exit_game(self):
       """Save data and close the program from the menu."""
       self.save_state()
       print("데이터를 저장하고 프로그램을 종료합니다.")


   def handle_safe_exit(self):
       """Save data and close the program after Ctrl+C or EOF."""
       print("\n입력이 중단되어 저장 후 안전하게 종료합니다.")
       self.save_state()


   def read_text(self, prompt):
       """Read a non-empty line of text from the user."""
       while True:
           try:
               value = input(prompt).strip()
           except (KeyboardInterrupt, EOFError):
               raise SafeExitSignal from None


           if not value:
               print("빈 입력은 사용할 수 없습니다. 다시 입력해 주세요.")
               continue


           return value


   def read_number(self, prompt, min_value, max_value):
       """Read a number in a specific range from the user."""
       while True:
           text = self.read_text(prompt)


           if not text.isdigit():
               print(
                   f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력해 주세요."
               )
               continue


           number = int(text)
           if not min_value <= number <= max_value:
               print(
                   f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력해 주세요."
               )
               continue


           return number


   def create_default_quizzes(self):
       """Build the default quiz set used on first launch or recovery."""
       return [
           Quiz(
               "Python에서 문자열을 나타낼 때 사용하는 자료형은 무엇인가요?",
               ["int", "str", "bool", "list"],
               2,
           ),
           Quiz(
               "조건에 따라 다른 코드를 실행할 때 가장 알맞은 문장은 무엇인가요?",
               ["for", "if", "while", "import"],
               2,
           ),
           Quiz(
               "여러 개의 값을 순서대로 저장하는 자료형은 무엇인가요?",
               ["dict", "list", "bool", "float"],
               2,
           ),
           Quiz(
               "함수의 결과를 호출한 곳으로 돌려줄 때 사용하는 키워드는 무엇인가요?",
               ["break", "pass", "return", "continue"],
               3,
           ),
           Quiz(
               "JSON 파일을 다룰 때 파이썬 표준 라이브러리로 주로 사용하는 모듈은 무엇인가요?",
               ["random", "json", "math", "time"],
               2,
           ),
           Quiz(
               "클래스에서 인스턴스 자신을 가리킬 때 사용하는 첫 번째 매개변수 이름은 보통 무엇인가요?",
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