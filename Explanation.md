```bash
  for q in question: long hallway with 4 doors - start with the first door, and don't stop until you've gone through all of them.
   print(f"Question: {q['question']}"):  shows the specific question from the quiz bank
   for option in q['options']: print option - 4 buttons on the wall, prints out options of the question
  while True: once you are in front of the door, you find out that the door is locked. The only way to open this door
  and move on to the next one is to give the correct answer. If your answer is incorrect, you'll stay at this door.
  3 choices: Once you go inside the room, the computer looks at what you typed and follows these rules:
      a. If you ask for a hint: the guard gives you a clue but takes away 10 points. You are still stuck at the same door.
      b. If you give the wrong answer: the guard says "Try again" and takes away 10 points. You are still stuck at the same door.
      c. If you give the correct answer: The guard gives you 50 points, unlocks the door(break) and allows you to move to the next door

```
```bash
   if __name__ == "__main__":
    start_quiz()            --> starts the quiz in the terminal
