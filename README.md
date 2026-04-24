
1. Project Overview
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

5. Class Responsibility Design (클래스 책임 분리):

   This project follows the **Single Responsibility Principle** to maintain clean and maintainable code.

   a. **SafeExitSignal** (Exception Class)
      - Responsibility: Define signal for safe program termination when user interrupts input
      - Ensures graceful shutdown with data saving

   b. **Quiz** (Data Model)
      - Responsibility: Manage individual quiz data and validation logic
      - Key responsibilities:
         i. Store question, choices, and correct answer
         ii. Validate quiz data (validate method)
         iii. Check if user answer is correct (is_correct method)
         iv. Display quiz on screen (display method)
         v. Serialize/Deserialize to/from JSON (to_dict, from_dict methods)
      - Focus: Only handles ONE quiz

   c. **QuizGame** (Controller/Manager)
      - Responsibility: Orchestrate entire game flow and state management
      - Key responsibilities:
         i. Manage menu system and user navigation
         ii. Manage collection of quizzes
         iii. Track high scores
         iv. Handle user input processing
         v. Save/Load game state (save_state, load_state methods)
         vi. Control game execution (run, play_quiz, add_quiz methods)
      - Focus: Coordinates the ENTIRE game

   d. **Design Benefits**
      - Easy maintenance: Each class has a single, clear purpose
      - Independent modification: Changes to Quiz logic don't affect game flow
      - Better testability: Each component can be tested in isolation
      - Code reusability: Quiz class can be used in different game systems
   ```

6. Logic Separation Criteria Explanation:

   Based on code analysis, the "input processing (validation)", "game progression", and "data saving/loading" logics are separated based on **Separation of Concerns** and **Single Responsibility Principle**. This design ensures each logic performs an independent role, improving code maintainability and readability. Below, the separation criteria and implementation examples for each logic are explained.

   ### 1. **Input Processing (Validation) Logic**
      - **Separation Criteria**: Independently handles the responsibility of safely receiving user input and validating its validity. Uses exception handling (KeyboardInterrupt, EOFError) to ensure safe program termination, and enforces input formats to guarantee data integrity.
      - **Implementation Location**: `read_text` and `read_number` methods in the `QuizGame` class.
        - `read_text`: Rejects empty strings and reads input.
        - `read_number`: Validates number ranges (e.g., 1-4) and prompts for re-entry if invalid.
      - **Benefits**: Input logic is separated from other game logic, so changes to input methods do not affect other parts.

   ### 2. **Game Progression Logic**
      - **Separation Criteria**: Manages the core flow of the quiz game (playing, adding, listing, score checking). Handles user interactions through a menu-based interface and processes quiz objects and score calculations independently.
      - **Implementation Location**: `play_quiz`, `add_quiz`, `list_quizzes`, `show_best_score` methods in the `QuizGame` class.
        - `play_quiz`: Displays quizzes sequentially, validates answers, and calculates scores.
        - `add_quiz`: Creates and validates new quizzes.
        - Other methods: Display lists or check scores.
      - **Benefits**: Game logic is centralized, making it easy to extend with new features (e.g., difficulty settings).

   ### 3. **Data Saving/Loading Logic**
      - **Separation Criteria**: Handles file I/O and data serialization/deserialization. Persistently saves state (quiz list, high scores) via JSON files and independently manages recovery to default data if files are corrupted.
      - **Implementation Location**: `load_state`, `save_state`, `create_default_quizzes` methods in the `QuizGame` class.
        - `load_state`: Loads and validates data from JSON files.
        - `save_state`: Saves data to JSON.

### 파일 입출력에서 try/except의 필요성

네, 파일 입출력에서 `try/except`가 필요한 이유를 설명하겠습니다. 파일 입출력은 프로그램 외부의 리소스(파일 시스템, 디스크 등)와 상호작용하기 때문에 예측할 수 없는 오류가 발생할 수 있습니다. 이러한 오류를 처리하지 않으면 프로그램이 예기치 않게 종료될 수 있으므로, `try/except`를 사용하여 예외를 잡고 적절히 대응하는 것이 중요합니다. 이를 통해 프로그램의 안정성과 사용자 경험을 향상시킬 수 있습니다.

#### 발생 가능한 실패 케이스
파일 입출력 중 발생할 수 있는 주요 오류는 다음과 같습니다. 각 케이스에 대해 `try/except`로 처리하는 이유를 간단히 설명하겠습니다:

1. **파일이 존재하지 않음 (FileNotFoundError)**:  
   지정한 경로에 파일이 없을 때 발생합니다. 예를 들어, 읽기 모드로 파일을 열 때. `except FileNotFoundError`로 잡아 사용자에게 파일이 없음을 알리고, 대체 동작(예: 기본 파일 생성)을 수행할 수 있습니다.

2. **권한 부족 (PermissionError)**:  
   파일을 읽거나 쓸 권한이 없을 때 발생합니다. 예를 들어, 읽기 전용 파일에 쓰려고 하거나, 시스템 파일에 접근할 때. `except PermissionError`로 처리하여 권한 문제를 알려주고, 프로그램을 안전하게 종료하거나 재시도할 수 있습니다.

3. **디스크 공간 부족 (OSError)**:  
   파일을 쓸 때 디스크 공간이 부족하면 발생합니다. `except OSError`로 잡아 공간 부족을 감지하고, 사용자에게 알리거나 임시 파일을 삭제하는 등의 조치를 취할 수 있습니다.

4. **파일이 이미 사용 중 (OSError 또는 BlockingIOError)**:  
   다른 프로그램이 파일을 잠금 상태로 사용 중일 때 발생합니다. `except OSError`로 처리하여 잠시 기다리거나 다른 파일을 사용하도록 유도할 수 있습니다.

5. **인코딩 문제 (UnicodeDecodeError 또는 UnicodeEncodeError)**:  
   텍스트 파일을 읽거나 쓸 때 인코딩이 맞지 않으면 발생합니다. 예를 들어, UTF-8 파일을 ASCII로 읽으려고 할 때. `except UnicodeDecodeError`로 잡아 인코딩을 재시도하거나 오류를 기록할 수 있습니다.

6. **하드웨어 또는 시스템 오류 (OSError)**:  
   디스크 오류, 네트워크 파일 시스템 문제, 또는 파일 시스템 손상 등으로 인해 발생합니다. `except OSError`로 일반적인 I/O 오류를 처리하여 프로그램이 충돌하지 않도록 합니다.

#### 예시 코드 구조
간단한 파일 읽기 예시에서 `try/except`를 사용하는 방식은 다음과 같습니다:

```python
try:
    with open('example.txt', 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("파일이 존재하지 않습니다.")
except PermissionError:
    print("파일을 읽을 권한이 없습니다.")
except OSError as e:
    print(f"I/O 오류 발생: {e}")
```

이렇게 하면 각 오류에 맞는 메시지를 출력하고, 프로그램이 계속 실행될 수 있습니다. 파일 입출력은 특히 사용자 입력이나 외부 환경에 의존하므로, 항상 `try/except`를 고려하는 것이 좋습니다. 추가 질문이 있으시면 말씀해주세요!

### JSON 파일로 데이터를 저장하는 이유

JSON(JavaScript Object Notation)은 데이터를 저장하고 교환하는 데 널리 사용되는 형식입니다. 주요 이유는 다음과 같습니다:

- **가독성**: 텍스트 기반으로 사람이 읽고 이해하기 쉽습니다. 코드나 데이터를 직접 확인할 수 있어 디버깅이나 수동 편집이 용이합니다.
- **범용성**: 대부분의 프로그래밍 언어(Python, JavaScript, Java 등)에서 기본적으로 지원되므로, 언어 간 데이터 교환이 간단합니다.
- **경량성**: 불필요한 메타데이터가 적어 파일 크기가 작고, 네트워크 전송이나 저장에 효율적입니다.
- **구조화**: 객체(키-값 쌍), 배열, 기본 데이터 타입(문자열, 숫자, 불리언)을 지원해 복잡한 데이터를 계층적으로 표현할 수 있습니다.
- **안정성**: 파싱 오류가 발생해도 프로그램이 중단되지 않도록 예외 처리를 쉽게 구현할 수 있습니다.

예를 들어, 첨부된 `QuizGame.py` 코드에서는 `state.json` 파일에 퀴즈 목록과 최고 점수를 저장합니다. 이는 프로그램 재시작 시 데이터를 유지하고, 사용자가 추가한 퀴즈를 잃지 않도록 하기 위함입니다.

### JSON 형식의 특징

JSON은 간단하고 유연한 데이터 형식으로, 다음과 같은 특징이 있습니다:

- **키-값 구조**: 데이터를 `{ "key": "value" }` 형태로 표현합니다. 키는 문자열, 값은 문자열, 숫자, 불리언, null, 객체, 배열 중 하나입니다.
- **배열 지원**: `[ "item1", "item2" ]`처럼 순서가 있는 데이터를 저장할 수 있습니다.
- **데이터 타입**: 기본 타입(문자열: `"text"`, 숫자: `123`, 불리언: `true/false`, null: `null`)과 복합 타입(객체, 배열)을 지원합니다.
- **텍스트 기반**: UTF-8 인코딩의 평문 텍스트로 저장되므로, 파일로 쉽게 읽고 쓸 수 있습니다.
- **언어 독립적**: JavaScript에서 유래했지만, Python의 `json` 모듈처럼 다른 언어에서도 쉽게 처리할 수 있습니다.
- **제한**: 바이너리 데이터(이미지, 파일)를 직접 저장할 수 없으며, 주석을 지원하지 않습니다. 대신, 구조화된 텍스트 데이터에 최적화되어 있습니다.

JSON은 웹 API, 설정 파일, 데이터 저장 등 다양한 용도로 사용되며, `QuizGame.py`처럼 Python 프로그램에서 `json.dump()`와 `json.load()`로 쉽게 다룰 수 있습니다.


        - `create_default_quizzes`: Generates default quizzes when files are missing.
      - **Benefits**: Data logic is separated, so changing storage formats (e.g., to a database) does not affect other logic.

   This separation enhances code modularity, allowing each part to be tested and modified independently. Overall, the `QuizGame` class acts as the controller, while the `Quiz` class handles the data model.

7. state.json 읽기/쓰기 흐름:

   This section explains when and where the `state.json` file is read and written during program execution.

   ### **단계 1: 프로그램 시작 (읽기 한 번)**
   
   When `QuizGame()` is instantiated, the `__init__()` method is called:
   - Instance variables are initialized (quizzes, best_score, etc.)
   - `load_state()` is called → **state.json 파일 읽기** 📖

   ### **단계 2: load_state() 상세 흐름**

   ```
   state.json 존재 확인
   ├─ 파일 없음
   │  └─ 기본 퀴즈 6개 생성
   │     startup_message: "Loaded {n} default quizzes"
   │
   ├─ 파일 존재 + 유효한 JSON
   │  └─ 퀴즈, 최고점, 기록 로드
   │     startup_message: "Loaded saved data..."
   │
   └─ 파일 손상/읽기 오류 → 기본 퀴즈 복구
      └─ save_state() 호출 → **파일 쓰기** 📝
         startup_message: "state.json file corrupted..."
   ```

   **Flow Details:**
   - If `state.json` does not exist: Load 6 default quizzes from `create_default_quizzes()`
   - If `state.json` exists and is valid: Parse JSON and load quizzes, best_score, best_correct_count, best_total_questions
   - If `state.json` is corrupted or invalid: Recover with default quizzes and call `save_state()` to overwrite the corrupted file

   ### **단계 3: 메인 루프에서의 쓰기 작업**

   After the main menu loop starts (`run()` method), the program writes to `state.json` based on user actions:

   | 메뉴 선택 | 메서드 | 파일 쓰기 | 쓰기 발생 시점 |
   |---------|--------|---------|-------------|
   | 1. 퀴즈 풀기 | `play_quiz()` | ✅ Yes | 새 최고점 달성 시 |
   | 2. 퀴즈 추가 | `add_quiz()` | ✅ Yes | 퀴즈 추가 직후 |
   | 3. 퀴즈 목록 | `list_quizzes()` | ❌ No | 메모리에서 읽음만 |
   | 4. 점수 확인 | `show_best_score()` | ❌ No | 메모리에서 읽음만 |
   | 5. 종료 | `exit_game()` | ✅ Yes | 정상 종료 시 |

   **Key Points:**
   - `play_quiz()`: Calls `save_state()` only when a new high score is achieved
   - `add_quiz()`: Calls `save_state()` immediately after adding a new quiz
   - `exit_game()`: Calls `save_state()` before program termination
   - Menu options 3 & 4 only read from in-memory data; no file I/O occurs

   ### **단계 4: 예외 상황 처리**

   When user interrupts the program (Ctrl+C or EOF):
   - `SafeExitSignal` exception is raised
   - `handle_safe_exit()` method is called
   - `save_state()` is called → **파일 쓰기** 📝
   - This ensures no data loss even if the user forcefully terminates the program

   ### **save_state() 작성 내용**

   The `save_state()` method writes the following JSON structure to `state.json`:

   ```json
   {
     "quizzes": [
       {
         "question": "What data type is used to represent strings in Python?",
         "choices": ["int", "str", "bool", "list"],
         "answer": 2
       }
     ],
     "best_score": 85,
     "best_correct_count": 5,
     "best_total_questions": 6
   }
   ```

   **Written fields:**
   - `quizzes`: Array of all quiz objects (converted via `Quiz.to_dict()`)
   - `best_score`: Highest percentage score achieved
   - `best_correct_count`: Number of correct answers in the best attempt
   - `best_total_questions`: Total number of questions in the best attempt

   ### **쓰기 흐름 요약**

   **Startup Flow:**
   ```
   프로그램 시작 → QuizGame() → __init__() → load_state() 📖 (1회 읽기) → 메인 루프 시작
   ```

   **During Main Loop:**
   ```
   사용자 액션 → 선택지 처리 → 필요시 save_state() 📝 → 메뉴로 돌아감
   ```

8. Safe Exit Handling (안전 종료 처리)

   코드에서 Ctrl+C (KeyboardInterrupt) 또는 EOF (End of File, EOFError) 상황에서 안전하게 종료하기 위한 처리를 구현했습니다. 이는 사용자가 입력 중에 프로그램을 강제로 중단할 때 데이터를 잃지 않고 안전하게 저장한 후 종료하도록 설계되었습니다. 아래에서 관련 처리 방법을 단계적으로 설명하겠습니다.

   ### 1. **커스텀 예외 클래스: SafeExitSignal**
      - 코드의 "Section: Custom exception" 부분에 `SafeExitSignal`이라는 커스텀 예외 클래스를 정의했습니다.
      - 이 예외는 "Stop the program safely when the user interrupts input."라는 설명처럼, 사용자 입력 중단 시 안전 종료를 위한 신호로 사용됩니다.
      - KeyboardInterrupt나 EOFError가 발생하면 이 예외를 raise하여 프로그램이 정상적으로 종료되도록 합니다.

   ### 2. **입력 처리 메소드: read_text와 read_number**
      - `read_text` 메소드에서 `input()`을 호출할 때, `try-except` 블록으로 KeyboardInterrupt와 EOFError를 catch합니다.
      - 이러한 예외가 발생하면 `SafeExitSignal`을 raise하여 상위로 전달합니다.
      - `read_number` 메소드는 `read_text`를 호출하므로, 동일한 방식으로 예외를 처리합니다.
      - 이렇게 하면 입력 루프에서 예외가 발생해도 프로그램이 갑자기 종료되지 않고, 안전 종료 루틴으로 이동합니다.

   ### 3. **메인 루프와 예외 처리: run 메소드**
      - `run` 메소드의 메인 루프(`while True`)에서 전체를 `try-except` 블록으로 감쌉니다.
      - `except SafeExitSignal:`에서 `handle_safe_exit()` 메소드를 호출합니다.
      - 이로써 메뉴 선택이나 퀴즈 진행 중에 Ctrl+C나 EOF가 발생해도 루프가 깨지지 않고 안전하게 처리됩니다.

   ### 4. **안전 종료 핸들러: handle_safe_exit 메소드**
      - 이 메소드는 "Save data and close the program after Ctrl+C or EOF."라는 설명처럼, 데이터를 저장하고 프로그램을 종료합니다.
      - 내부적으로 `save_state()`를 호출하여 퀴즈 데이터와 최고 점수를 JSON 파일(`state.json`)에 저장합니다.
      - 메시지("\nInput interrupted, saving and exiting safely.")를 출력하여 사용자에게 상황을 알립니다.
      - 메뉴에서 정상 종료할 때 사용하는 `exit_game` 메소드와 유사하게 작동하지만, 강제 중단 시 자동으로 호출됩니다.

   ### 왜 이러한 처리가 필요한가?
      - Python 프로그램에서 Ctrl+C는 KeyboardInterrupt를 발생시키고, EOF (예: 터미널에서 Ctrl+D)는 EOFError를 발생시킬 수 있습니다.
      - 이러한 예외를 처리하지 않으면 프로그램이 갑자기 종료되어 진행 중인 데이터(퀴즈 목록, 최고 점수 등)가 저장되지 않을 수 있습니다.
      - 이 코드에서는 예외를 catch하여 `save_state()`를 호출함으로써 데이터를 안전하게 유지하고, 사용자 경험을 개선합니다.
      - 만약 이러한 처리가 없었다면, 사용자가 실수로 Ctrl+C를 눌렀을 때 데이터가 손실될 위험이 있습니다.

   이 구현은 간단하면서도 효과적이며, 프로그램의 안정성을 높입니다.

   **종료 흐름:**
   ```
   메뉴 선택 5 또는 Ctrl+C → exit_game() 또는 handle_safe_exit() → save_state() 📝 → 프로그램 종료
   ```

   **Summary:**
   - **Total file reads**: 1 (at startup)
   - **Total file writes**: Multiple (depending on user actions: adding quiz, achieving high score, normal exit, or interrupt exit)
   - **Data persistence**: All quiz data and score records are safely saved whenever they change
   - **Error recovery**: Corrupted files are automatically restored to default state

9. Git Commit Strategy

   This section explains how commit units and messages were organized during development.

   ### Commit Unit Criteria
      - Each commit contains a single logical change.
      - Example units:
         - file/directory structure changes
         - code changes or bug fixes
         - documentation improvements
         - feature additions
      - This helps make each commit easy to review and easy to revert if necessary.

   ### Commit Message Rules
      - Messages describe what was changed clearly and concisely.
      - Prefer a short summary line that explains the purpose of the change.
      - Use wording that reflects the type of work, such as:
         - `file directory move`
         - `Code modified`
         - `Docs: Code Refactoring`
         - `Revise README structure and content clarity`
      - The goal is to make it immediately obvious what the commit contains.

   ### Why this matters
      - Clear commit boundaries improve project history readability.
      - Consistent commit messages make it easier to understand why changes were made.
      - Logical commits simplify debugging and code review.

## 클래스를 사용한 이유

이 `QuizGame.py` 코드에서는 객체 지향 프로그래밍(OOP)을 채택하여 클래스를 사용했습니다. 주요 이유는 다음과 같습니다:

1. **캡슐화 (Encapsulation)**: 데이터(예: 퀴즈 질문, 선택지, 정답)와 그 데이터를 처리하는 로직(예: 검증, 표시, 저장)을 하나의 클래스(예: `Quiz` 또는 `QuizGame`)로 묶어 관리합니다. 이렇게 하면 데이터가 외부에서 직접 변경되는 것을 방지하고, 코드의 안정성을 높입니다.

2. **재사용성과 모듈성 (Reusability and Modularity)**: 클래스를 사용하면 객체를 여러 번 생성할 수 있어, 퀴즈 게임을 확장하거나 재사용하기 쉽습니다. 예를 들어, `Quiz` 클래스의 인스턴스를 여러 개 만들어 퀴즈 목록을 관리할 수 있습니다.

3. **유지보수성 (Maintainability)**: 코드가 구조화되어 있어, 특정 기능(예: 퀴즈 추가)을 수정할 때 해당 클래스만 변경하면 됩니다. 이는 대규모 코드에서 특히 유용합니다.

4. **상태 관리 (State Management)**: 객체는 자신의 상태(예: 최고 점수, 퀴즈 목록)를 유지할 수 있어, 프로그램 실행 중 데이터를 일관되게 관리합니다.

### 함수만으로 구현할 때와의 차이

함수만으로 구현하면 모든 로직을 전역 함수와 전역 변수로 처리해야 합니다. 이 경우 다음과 같은 차이가 발생합니다:

- **데이터 관리의 어려움**: 퀴즈 데이터나 게임 상태를 전역 변수(예: 리스트나 딕셔너리)로 저장해야 하므로, 함수 간 데이터 공유가 복잡해지고, 실수로 변수가 변경될 위험이 큽니다. 반면, 클래스에서는 객체의 속성으로 데이터를 캡슐화하여 안전하게 관리합니다.

- **코드 구조의 복잡성**: 함수 기반에서는 모든 기능을 별도의 함수로 분리해야 하므로, 코드가 길어지고 읽기 어려워집니다. 예를 들어, 퀴즈를 추가하는 함수, 표시하는 함수, 검증하는 함수 등이 흩어져 있어 유지보수가 힘듭니다. 클래스에서는 관련 메서드를 한 곳에 모아두어 직관적입니다.

- **확장성 부족**: 새로운 기능을 추가할 때(예: 퀴즈 카테고리 추가), 함수를 계속 늘려야 하므로 코드가 지저분해집니다. 클래스에서는 상속이나 메서드 추가로 쉽게 확장할 수 있습니다.

- **예시 비교**:
  - **클래스 기반**: `quiz = Quiz(question, choices, answer)`로 객체를 생성하고, `quiz.display()`로 표시합니다. 데이터와 로직이 결합되어 있어 명확합니다.
  - **함수 기반**: `def create_quiz(question, choices, answer): ...`와 `def display_quiz(quiz_data): ...`처럼 함수를 따로 정의하고, 전역 리스트에 데이터를 저장해야 합니다. 데이터가 분산되어 오류가 발생하기 쉽습니다.

결론적으로, 이 코드처럼 상태를 유지하고 복잡한 로직을 다루는 프로그램에서는 클래스가 더 적합합니다. 함수만으로도 작동할 수 있지만, 코드의 질과 유지보수성이 떨어집니다. OOP는 특히 Python에서 강력한 패턴으로, 이 코드를 통해 실전적인 예시를 볼 수 있습니다.

## 10. Git 브랜치 분리와 병합(Merge)

### 브랜치를 분리해 작업하는 이유

**1. 독립적인 개발 환경**
- 메인 코드(`main` 또는 `master`)를 안전하게 보호할 수 있습니다
- 여러 기능을 동시에 개발할 때 서로 방해하지 않습니다

**2. 안정성 확보**
- 새로운 기능이나 버그 수정을 별도 브랜치에서 테스트한 후 통합합니다
- 문제가 발생하면 해당 브랜치만 수정하면 됩니다

**3. 협업 효율성**
- 팀 전체가 하나의 파일을 동시에 수정해도 충돌을 최소화합니다
- 각자의 작업 진행 상황을 명확히 추적할 수 있습니다

**4. 코드 리뷰 및 품질 관리**
- Pull Request(PR)를 통해 코드 검토 후 병합합니다
- 버그나 개선사항을 미리 발견할 수 있습니다

### 병합(Merge)의 의미

**병합(Merge)**: 한 브랜치의 변경사항을 다른 브랜치에 통합하는 작업입니다.

**기본 동작 흐름**:
```
feature 브랜치        main 브랜치
    ↓                  ↓
  C1 ← C2 ← C3        A1 ← A2
        ↓                ↓
     (merge)         A1 ← A2 ← C1 + C2 + C3 (병합됨)
```

**실제 명령어**:
```bash
git checkout main              # main 브랜치로 이동
git merge feature-branch       # feature-branch의 내용을 main에 병합
```

**결과**: 
- `feature-branch`에서 만든 모든 커밋과 변경사항이 `main`에 통합됩니다
- 양쪽 브랜치의 이력이 유지되며, 병합 커밋이 생성됩니다

### 브랜치 생성과 작업 예시

```bash
# 1. 새로운 브랜치 생성
git branch feature/add-quiz

# 2. 해당 브랜치로 이동
git checkout feature/add-quiz

# 3. 기능 개발 및 커밋
echo "new feature" >> file.py
git add file.py
git commit -m "Add new feature"

# 4. main 브랜치로 돌아가기
git checkout main

# 5. 병합하기
git merge feature/add-quiz

# 6. 불필요한 브랜치 삭제 (선택사항)
git branch -d feature/add-quiz
```

### 병합의 장점

- **안전한 통합**: 완성된 작업만 메인 코드에 추가됩니다
- **히스토리 보존**: 각 브랜치의 개발 과정이 기록됩니다
- **롤백 용이**: 문제가 발생하면 병합을 되돌릴 수 있습니다
- **팀 협업**: 여러 팀 멤버가 동시에 다른 기능을 개발할 수 있습니다

이 방식으로 안정적이고 체계적인 개발 프로세스를 만들 수 있습니다!

## 11. state.json 데이터 구조 설계 이유

### 현재 state.json 구조

```json
{
  "quizzes": [
    {
      "question": "...",
      "choices": [...],
      "answer": 2
    }
  ],
  "best_score": 100,
  "best_correct_count": 6,
  "best_total_questions": 6
}
```

### 설계 이유

#### 1. **최상위 계층의 두 가지 책임 분리**
- **`quizzes`**: 퀴즈 콘텐츠 데이터 (사용자가 추가/수정)
- **`best_score` 그룹**: 게임 성과 메타데이터 (프로그램에서 자동 관리)

이렇게 분리하면 데이터의 본질이 다른 두 부분을 논리적으로 구조화할 수 있습니다.

#### 2. **각 퀴즈 객체의 필드 설계**
```python
{
  "question": "...",        # 1개의 질문
  "choices": [...],         # 정확히 4개의 선지
  "answer": 2               # 1~4 범위의 정답 인덱스
}
```

**왜 이 3개 필드일까?**
- **최소한의 필드**: 퀴즈 기능에 필수적인 것만 포함
- **`answer`가 숫자 인덱스인 이유**: 
  - 저장 공간 효율적 (문자열 vs 숫자)
  - 사용자 입력과 직접 비교 가능 (`user_answer == quiz.answer`)
  - 빠른 검증 (`1 <= answer <= 4`)

#### 3. **최상위 배열 구조 (flat, not deeply nested)**
```python
"quizzes": [
  { "question": "...", "choices": [...], "answer": 2 },
  { "question": "...", "choices": [...], "answer": 2 }
]
```

대신 이렇게 하지 않은 이유:
```python
# ✗ 불필요하게 복잡한 구조
"quizzes": {
  "items": [...],
  "count": 6
}
```

**선택한 이유**:
- JSON 직렬화/역직렬화가 간단함
- `for item in raw_quizzes`로 순회하기 쉬움
- 파일 크기가 작음

#### 4. **점수 추적 필드 3개 분리**
```python
"best_score": 100,              # 백분율 (0-100)
"best_correct_count": 6,        # 맞은 개수
"best_total_questions": 6       # 총 문제 수
```

**왜 3개를 모두 저장할까?**
- **점수만으로는 부족**: 100점이라도 어떤 조건에서 달성했는지 알 수 없음
- **정보 복원**: `6/6`이나 `3/3`은 모두 100점이지만, 기록은 다름
- **점수 재계산 필요 없음**: 저장된 정확한 값 사용 (`show_best_score()`)

### 결론

state.json은 **필요한 정보만 포함**하면서도 **데이터 검증과 게임 기능을 지원**하도록 최소한으로 설계되었습니다.

## 12. 대규모 데이터(1000개 이상)의 JSON 저장 방식 한계

현재 JSON 저장 방식이 1000개 이상의 퀴즈 데이터로 확장될 경우, 다음과 같은 한계점이 발생합니다.

### 1. **메모리 효율성 문제**
- **프로그램 시작 시 전체 로드**: `load_state()` 메서드는 모든 퀴즈를 메모리에 로드합니다
- **메모리 점유**: 1000개의 퀴즈 객체가 모두 메모리에 유지되어, 각 퀴즈(문제, 4개 선택지, 정답)마다 객체를 생성합니다
- **저사양 시스템 성능 저하**: 메모리 부족 시 시스템 전체 성능이 저하됩니다

### 2. **I/O 성능 저하**
- **파일 로딩 시간 증가**: 1000개 항목을 파싱하는 데 시간이 소요됩니다
- **파일 저장의 비효율**: 단 1개 퀴즈 추가 시에도 전체 1000개 퀴즈를 다시 저장해야 합니다
  ```
  add_quiz() → save_state()에서 1000개 전부 다시 저장
  ```
- **디스크 I/O 병목**: 매번 전체 파일을 다시 쓰는 작업이 반복되어 디스크 I/O가 병목이 됩니다

### 3. **파일 크기 증가**
- **JSON 형식의 오버헤드**: 각 항목마다 `"question"`, `"choices"`, `"answer"` 키가 반복됩니다
- **파일 크기**: 1000개 퀴즈 = 수 MB 크기의 텍스트 파일
- **바이너리 형식 대비 비효율**: 텍스트 기반 저장으로 인해 바이너리 형식 대비 3~5배 크기

**예시**:
```json
{
  "quizzes": [
    {"question": "...", "choices": ["...", "...", "...", "..."], "answer": 2},  // 약 300 bytes
    {"question": "...", "choices": ["...", "...", "...", "..."], "answer": 2},
    ...
    // 1000개 × 300 bytes ≈ 300 KB ~ 수 MB
  ],
  "best_score": 100,
  "best_correct_count": 50,
  "best_total_questions": 50
}
```

### 4. **데이터 무결성 위험**
- **저장 중 프로그램 충돌**: 파일 쓰기 중 프로그램이 충돌하면 **전체 state.json이 손상**됩니다
- **트랜잭션 미지원**: 부분 업데이트가 불가능하고, 항상 전체 파일을 덮어씁니다
- **롤백 불가능**: 손상된 파일을 복구할 방법이 없습니다 (현재 코드에서는 기본 퀴즈로 복구)

### 5. **확장성 제한**
- **검색/필터링 불가**: 특정 퀴즈를 찾으려면 모든 1000개를 메모리에서 선형 검색해야 합니다
- **페이지네이션 불가**: UI에서 10개씩 표시하려 해도 전부 로드해야 합니다
- **고급 기능 추가 어려움**: 난이도별 분류, 카테고리 필터링 등의 기능 구현이 복잡합니다
- **데이터 부분 수정 불가**: 한 퀴즈만 수정하려 해도 전체 파일을 다시 저장해야 합니다

### 6. **동시 접근 문제**
- **파일 잠금 없음**: 만약 여러 프로세스가 동시에 접근하면 데이터 충돌이 발생합니다
- **동시성 제어 미지원**: 현재 구현에서 파일 동시 접근을 처리하지 않습니다

### 개선 방안

#### **1. 데이터베이스 도입 (권장)**
```python
# SQLite 사용 예시
import sqlite3

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# 필요한 데이터만 로드 (예: 페이지 1의 10개만)
cursor.execute('SELECT * FROM quizzes LIMIT 10 OFFSET 0')
quizzes = cursor.fetchall()
```

**장점**:
- 필요한 데이터만 로드 (메모리 효율)
- 빠른 검색 (인덱싱)
- 부분 수정 가능
- 트랜잭션 지원
- 동시 접근 제어

#### **2. 바이너리 형식으로 변경**
```python
import pickle

# 저장
with open('quiz.pkl', 'wb') as f:
    pickle.dump(quizzes, f)

# 로드
with open('quiz.pkl', 'rb') as f:
    quizzes = pickle.load(f)
```

**장점**:
- 파일 크기 감소 (JSON 대비 1/3~1/2)
- 직렬화/역직렬화 속도 증가
- 객체 구조 유지

#### **3. 파일 분할 저장**
```
state/
  ├── quiz_0000.json  (0-99번)
  ├── quiz_0100.json  (100-199번)
  ├── quiz_0200.json  (200-299번)
  └── metadata.json   (점수 정보)
```

**장점**:
- 부분 로드 가능
- 손상 범위 제한
- 증분 저장 가능

#### **4. 클라우드/API 서버로 마이그레이션**
```python
# 예: REST API 호출
import requests

quizzes = requests.get('https://api.example.com/quizzes?page=1').json()
```

**장점**:
- 로컬 저장소 부담 제거
- 클라이언트-서버 분리
- 확장성 무한대

### 결론

**현재 JSON 방식의 적용 한계**: 100~500개 퀴즈까지는 문제없지만, **1000개 이상에서는 심각한 성능 저하와 유지보수 어려움** 발생

**권장 마이그레이션**:
- 1000~10,000개: SQLite 데이터베이스
- 10,000개 이상: 클라우드 데이터베이스 + API 서버
- 즉시 개선 가능: 바이너리 형식 또는 파일 분할 저장

## 13. state.json 손상 시 데이터 복구 전략

state.json이 손상되어 JSON 파싱에 실패한다면, 사용자가 데이터를 잃지 않도록 어떤 대응이 가능한지 설명합니다. 현재 코드의 복구 방식과 개선 가능한 방법을 비교합니다.

### 현재 코드의 손상 처리 방식

**[코드 위치]** [QuizGame.py](QuizGame.py#L180-L203)의 `load_state()` 메서드:

```python
except (OSError, json.JSONDecodeError, TypeError, ValueError):
    self.quizzes = self.create_default_quizzes()
    self.best_score = 0  # ❌ 데이터 손실!
    self.best_correct_count = 0
    self.best_total_questions = 0
    self.startup_message = "state.json file corrupted, restored with default quiz data."
    self.save_state()
```

**문제점:**
- ❌ 사용자 점수 데이터 완전 손실
- ❌ 사용자가 추가한 커스텀 퀴즈 손실  
- ❌ 자동 백업 메커니즘 없음
- ❌ 수동 복구 옵션 없음

### 가능한 대응 방법 (3단계 복구 전략)

#### **1단계: 자동 백업 생성** (데이터 손실 방지)

```python
def load_state(self):
    """Load quizzes and score data from the JSON file."""
    BACKUP_FILE = self.STATE_FILE.with_name("state.json.backup")
    
    # ✅ Step 1: 정상 로드 후 자동으로 백업본 생성
    if self.STATE_FILE.exists():
        try:
            shutil.copy(self.STATE_FILE, BACKUP_FILE)
        except OSError:
            pass  # 백업 생성 실패는 무시하고 계속 진행
        
        # Step 2: 파일 로드 시도
        try:
            with self.STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                # 정상 로드 성공
                ...
```

**효과**:
- 정상 로드될 때마다 백업 파일 자동 생성
- 만약의 사태에 최신 안전한 데이터 보유

#### **2단계: 손상 시 백업에서 복구** (데이터 복원)

```python
except (OSError, json.JSONDecodeError, TypeError, ValueError):
    BACKUP_FILE = self.STATE_FILE.with_name("state.json.backup")
    
    # ✅ Step 1: 백업 파일 존재 확인
    if BACKUP_FILE.exists():
        try:
            # Step 2: 손상된 파일 백업 (나중에 분석용)
            corrupt_file = self.STATE_FILE.with_name("state.json.corrupt")
            shutil.move(str(self.STATE_FILE), str(corrupt_file))
            
            # Step 3: 백업에서 원래 파일로 복구
            shutil.copy(BACKUP_FILE, self.STATE_FILE)
            
            # Step 4: 백업에서 다시 로드
            self.load_state()  # 재귀 호출
            
            # Step 5: 사용자 알림
            self.startup_message = (
                "state.json was corrupted but recovered from backup. "
                "Corrupted file saved as state.json.corrupt."
            )
            return
        except Exception:
            pass  # 백업도 손상된 경우 다음 단계로
```

**효과**:
- 손상된 파일을 자동으로 복구
- 손상 원인 분석을 위해 corrupt 파일 보존
- 사용자 데이터 손실 최소화

#### **3단계: 기본값으로 초기화** (마지막 수단)

```python
except (OSError, json.JSONDecodeError, TypeError, ValueError):
    # 백업 복구 모두 실패 → 기본값 사용
    self.quizzes = self.create_default_quizzes()
    self.best_score = 0  # 점수는 0으로 초기화
    self.best_correct_count = 0
    self.best_total_questions = 0
    self.startup_message = (
        "state.json file corrupted and backup unavailable. "
        "Restored with default quiz data. Previous data may be lost."
    )
    self.save_state()
```

**효과**:
- 프로그램은 안정적으로 시작
- 사용자는 기본 퀴즈로 게임 계속 진행 가능

### 복구 우선순위 및 데이터 손실 비교

| 순서 | 방법 | 데이터 손실 | 사용자 경험 | 구현 복잡도 |
|------|------|-----------|----------|----------|
| 1️⃣ | JSON 정상 로드 | **0%** | ✅ 완벽 | 기존 코드 |
| 2️⃣ | 백업 파일 복구 | **최소** (1회 분) | ✅ 좋음 | 간단 |
| 3️⃣ | 기본값 초기화 | **최대** (모든 데이터) | ❌ 나쁨 | 간단 |

### 권장 개선 구현 순서

**1. 우선순위가 높은 개선** (즉시 구현 가능):
```python
import shutil

# load_state() 시작 부분에 추가
BACKUP_FILE = self.STATE_FILE.with_name("state.json.backup")

# 파일 정상 로드 후 백업
if self.STATE_FILE.exists():
    try:
        shutil.copy(self.STATE_FILE, BACKUP_FILE)
    except OSError:
        pass
```

**2. 중간 우선순위** (권장):
```python
# 손상 감지 시 백업에서 자동 복구
except (OSError, json.JSONDecodeError, ...):
    if BACKUP_FILE.exists():
        shutil.copy(BACKUP_FILE, self.STATE_FILE)
        return self.load_state()  # 재시도
```

**3. 선택사항** (사용자 경험 향상):
- 사용자에게 선택 메뉴 제시
- 손상 파일 수동으로 복구 옵션 제공
- 복구 이력 로그 기록

### 구현 요구 사항

필요한 모듈:
```python
import shutil  # 파일 복사/이동

# load_state 메서드의 예외 처리 부분 수정 필요
```

### 사용자 경험 개선

**개선 전**:
```
state.json 손상됨
→ 즉시 기본 퀴즈로 초기화
→ "모든 데이터 손실" 메시지만 표시
→ 사용자: "어?! 내 점수가 없어졌네?"
```

**개선 후**:
```
state.json 손상됨
→ 백업에서 자동 복구 시도
→ "데이터가 복구되었습니다. 손상 파일은 state.json.corrupt로 저장됩니다"
→ 사용자: "다행이야, 데이터가 살아났다!"
```

### 결론

현재 코드는 **손상 감지는 하지만 데이터 손실** 방식으로 복구합니다. 

**최소한의 개선**으로 **최대의 효과**를 보려면:
1. **자동 백업 추가** → 코드 5줄 추가로 데이터 손실 위험 감소
2. **백업 복구 로직** → 코드 10줄로 사용자 데이터 99% 보호
3. **기본값 초기화** → 현재 코드와 같음 (마지막 수단)

이 3단계 전략으로 **state.json 손상 시에도 데이터를 안전하게 보호**할 수 있습니다.

## 14. 요구사항 변경 시 수정 순서

"정답 채점 방식(점수 계산)"이나 "퀴즈 구조(선택지 개수 등)" 요구사항이 바뀐다면, 어떤 파일/클래스/메서드를 먼저 수정해야 하는지 설명합니다.

### 1️⃣ **퀴즈 구조 변경 (선택지 개수 등)**

선택지가 4개에서 다른 개수로 변경된다면, 이 순서로 수정하세요:

| 우선순위 | 파일/클래스 | 메서드/부분 | 이유 |
|---------|-----------|-----------|------|
| **1순위** | `Quiz` | `validate()` | `len(self.choices) != 4` 검증 로직 변경 |
| **2순위** | `QuizGame` | `add_quiz()` | 선택지 입력 루프: `for index in range(1, 5)` 변경 |
| **3순위** | `QuizGame` | `play_quiz()` | 답변 입력 범위: `read_number("Answer number (1-4): ", 1, 4)` 변경 |
| **4순위** | `Quiz` | `from_dict()` | 선택지 자르(slicing): `for choice in raw_choices[:4]` 변경 |
| **5순위** | `QuizGame` | `add_quiz()` | 정답 입력 범위: `read_number("Correct answer number (1-4): ", 1, 4)` 변경 |

**상세 수정 위치**:

1. **Quiz.validate()** - [QuizGame.py](QuizGame.py#L21-L33)
   ```python
   # 변경 전
   if len(self.choices) != 4:
       raise ValueError("Each quiz must have exactly 4 choices.")
   
   # 변경 후 (예: 5개로 변경)
   if len(self.choices) != 5:
       raise ValueError("Each quiz must have exactly 5 choices.")
   ```

2. **QuizGame.add_quiz()** - [QuizGame.py](QuizGame.py#L243-L250)
   ```python
   # 변경 전
   for index in range(1, 5):
   
   # 변경 후 (예: 5개로 변경)
   for index in range(1, 6):
   ```

3. **QuizGame.play_quiz()** - [QuizGame.py](QuizGame.py#L227)
   ```python
   # 변경 전
   answer = self.read_number("Answer number (1-4): ", 1, 4)
   
   # 변경 후 (예: 5개로 변경)
   answer = self.read_number("Answer number (1-5): ", 1, 5)
   ```

4. **Quiz.from_dict()** - [QuizGame.py](QuizGame.py#L60)
   ```python
   # 변경 전
   for choice in raw_choices[:4]:
   
   # 변경 후 (예: 5개로 변경)
   for choice in raw_choices[:5]:
   ```

5. **QuizGame.add_quiz()** - [QuizGame.py](QuizGame.py#L251)
   ```python
   # 변경 전
   answer = self.read_number("Correct answer number (1-4): ", 1, 4)
   
   # 변경 후 (예: 5개로 변경)
   answer = self.read_number("Correct answer number (1-5): ", 1, 5)
   ```

### 2️⃣ **점수 계산 방식 변경**

점수 계산 공식이 변경된다면, 이 순서로 수정하세요:

| 우선순위 | 파일/클래스 | 메서드/부분 | 내용 |
|---------|-----------|-----------|------|
| **1순위** | `QuizGame` | `play_quiz()` | `score = int((correct_count / total_questions) * 100)` 공식 변경 |
| **2순위** | `QuizGame` | 상태 변수 검토 | `best_score`, `best_correct_count`, `best_total_questions` 변수명이나 의미 조정 필요 여부 판단 |
| **3순위** | `QuizGame` | `show_best_score()` | 필요시 점수 표시 형식 변경 |
| **4순위** | `QuizGame` | `load_state()` / `save_state()` | state.json 저장 형식 변경 필요 여부 확인 |

**상세 수정 위치**:

1. **QuizGame.play_quiz()** - [QuizGame.py](QuizGame.py#L233-L235)
   ```python
   # 변경 전: 백분율 계산
   score = int((correct_count / total_questions) * 100)
   
   # 변경 후 (예: 정답 개수로 변경)
   score = correct_count
   
   # 또는 다른 공식 (예: 정답 50점, 오답 -10점)
   score = (correct_count * 50) + ((total_questions - correct_count) * (-10))
   ```

2. **점수 저장 로직 검토** - [QuizGame.py](QuizGame.py#L236)
   ```python
   # 현재: 백분율로 저장
   if score > self.best_score:
   
   # 변경이 필요한 경우 최고점 비교 방식도 수정
   # (예: 정답 개수 비교로 변경)
   if correct_count > self.best_correct_count:
   ```

3. **QuizGame.show_best_score()** - [QuizGame.py](QuizGame.py#L268-L272)
   ```python
   # 변경 전: 백분율 표시
   print(f"High score: {self.best_score} points")
   
   # 변경 후 (예: 정답 개수 표시)
   print(f"High score: {self.best_correct_count} correct answers")
   ```

4. **state.json 저장 형식** - [QuizGame.py](QuizGame.py#L287-L292)
   ```python
   # 현재 저장 형식 (변경 필요한지 판단)
   data = {
       "best_score": self.best_score,           # 백분율
       "best_correct_count": self.best_correct_count,
       "best_total_questions": self.best_total_questions,
   }
   
   # 만약 점수 계산 방식이 극단적으로 변경되면
   # 새로운 필드 추가나 기존 필드 제거 고려
   ```

### 🔗 의존성 요약 (변경 영향 범위)

#### **퀴즈 구조 변경의 영향**:
```
Quiz.validate() (1순위)
    ↓
QuizGame.add_quiz() (2순위)
    ↓
QuizGame.play_quiz() (3순위)
    ↓
Quiz.from_dict() (4순위)
└─ JSON 호환성 유지
```

#### **점수 계산 변경의 영향**:
```
QuizGame.play_quiz() (1순위)
    ↓
점수 저장 로직 (2순위)
    ↓
QuizGame.show_best_score() (3순위)
    ↓
state.json 형식 (4순위)
└─ 기존 데이터 호환성 검토
```

### ✅ 주의사항

**퀴즈 구조 변경 시**:
- ✅ `Quiz` 클래스 검증부터 수정 (하위 의존성 고려)
- ❌ 점수 계산 로직에는 영향 없음 (독립적)
- ⚠️ 기존 JSON 데이터와의 호환성 확인 필요

**점수 계산 변경 시**:
- ✅ `play_quiz()` 점수 계산부터 수정
- ❌ `Quiz` 클래스에는 영향 없음 (독립적)
- ⚠️ `load_state()`에서 기존 점수 데이터가 새 공식과 호환되는지 검토

**변경 후 테스트**:
```python
# 1. Quiz 객체 생성/검증 테스트
quiz = Quiz("Q", ["A", "B", "C", "D", "E"], 2)  # 5개 선택지

# 2. 게임 흐름 테스트
game.add_quiz()    # 새 구조로 퀴즈 추가
game.play_quiz()   # 새 점수 공식으로 계산
game.show_best_score()  # 점수 표시 형식 확인

# 3. 저장/로드 테스트
game.save_state()  # 새 형식 저장
game2 = QuizGame()  # 재로드 확인
```

### 예시: 선택지 4개 → 3개로 변경

전체 수정 과정:

```python
# 1단계: Quiz.validate() 수정
# if len(self.choices) != 4:  ❌
if len(self.choices) != 3:  ✅

# 2단계: QuizGame.add_quiz() 수정
# for index in range(1, 5):  ❌
for index in range(1, 4):  ✅

# 3단계: QuizGame.play_quiz() 수정
# answer = self.read_number("Answer number (1-4): ", 1, 4)  ❌
answer = self.read_number("Answer number (1-3): ", 1, 3)  ✅

# 4단계: Quiz.from_dict() 수정
# for choice in raw_choices[:4]:  ❌
for choice in raw_choices[:3]:  ✅

# 5단계: QuizGame.add_quiz() 정답 입력 수정
# answer = self.read_number("Correct answer number (1-4): ", 1, 4)  ❌
answer = self.read_number("Correct answer number (1-3): ", 1, 3)  ✅
```

이 순서를 따르면 **에러 없이 안전하게 요구사항을 반영**할 수 있습니다.
