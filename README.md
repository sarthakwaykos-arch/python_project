1. Project Overview
This is a Rock Paper Scissors game played against a computer. The game has been developed using Python, a widely used and beginner-friendly programming language, with a graphical user interface built using the tkinter and Pillow libraries.
Upon launching the game, the player is presented with a full-screen dark-themed interface displaying three choices: Rock, Paper, and Scissors, represented by clickable image buttons. The player must select their weapon within a 7-second countdown timer. The computer then simulates a thinking animation before revealing its choice. The winner of each round is determined by classic game rules, the scores are updated in real time, and the result is displayed with a flash animation.
The game tracks the cumulative scores of both the player and the computer. Players can check the current standings at any time using the Result button, reset the game using Play Again, or exit the application cleanly.

2. Problem Statement
Rock Paper Scissors is one of the most popular and universally known hand games. However, most digital implementations of this game are either web-based and require an internet connection, or use external game frameworks that are complex for a beginner to understand and set up.
This project was created to address that gap. The main goals were:
1.	Build a fully offline Rock Paper Scissors game that runs directly on any computer without needing an internet connection.
2.	Use Python's standard library (tkinter) along with the lightweight Pillow module so setup is minimal and straightforward.
3.	Add a countdown timer to make gameplay more challenging and engaging.
4.	Include smooth animations (computer thinking animation, bounce effect, result flashing) to improve the visual experience.
5.	Handle errors gracefully, such as missing image files, so the game falls back to text-based buttons without crashing.
6.	Write the code in a clean, object-oriented, and well-structured way so both contributors can understand and extend it easily.

3. Technology Stack
•	Programming Language: Python 3.x
•	GUI Module: tkinter (Python's built-in windowing toolkit)
•	Image Processing: Pillow / PIL (PIL.Image, PIL.ImageTk) — for loading and resizing PNG images
•	Randomization: random module — for generating the computer's choice
•	Threading / Timing: root.after() (tkinter's non-blocking delay) — for the countdown timer and animations
•	IDE / Editor: Python IDLE / VS Code
•	Version Control: GitHub

4. Implementation
The implementation follows a clear, step-by-step logical flow:
Step 1: Open the Window
When the program is run, a full-screen window opens using tkinter. The window is configured with a dark navy background color and the escape key is bound to exit full-screen mode for convenience.
Step 2: Load Images
The program attempts to open rock.png, paper.png, and scissors.png from the same directory. Each image is resized to 80x80 pixels using Pillow's LANCZOS resampling. If any image file is missing, the game prints a warning and falls back to text labels for the buttons so the application does not crash.
Step 3: Build the User Interface
The setup_ui() method builds the entire screen layout using a centered wrapper frame. It creates the title label at the top, a score display frame showing the player's score (green) and computer's score (red), three clickable choice buttons in the middle, a status message label, a countdown timer label, and three control buttons at the bottom (Result, Play Again, Exit).
Step 4: Start the Countdown Timer
As soon as the UI is ready, start_timer() is called. It resets time_left to 7 and calls update_timer() repeatedly using root.after(1000, ...) every second. If the timer reaches zero before the player clicks, the game displays 'Time's up!' and locks further input.
Step 5: Player Makes a Choice
When the player clicks one of the three image buttons (Rock, Paper, or Scissors), the play() method is triggered. The timer is cancelled immediately, is_playing is set to True to prevent further clicks, and a bounce animation is applied to the selected button.
Step 6: Computer Thinking Animation
The animate_computer_choice() method runs 10 iterations using root.after(100, ...), displaying a randomly cycling choice name in the timer label to simulate the computer 'thinking'. After the animation completes, a final random choice is locked in.
Step 7: Determine the Winner
The determine_winner() method compares the player's choice and the computer's choice using the standard Rock-Paper-Scissors rules. The appropriate score is incremented, the result text is updated in the status label, and the scores on-screen are refreshed.
Step 8: Flash the Result
The flash_result() method toggles the status label color between the result color and the default text color four times using root.after(300, ...) to create a blinking effect that draws the player's attention to the outcome.
Step 9: Play Again or View Result
The player can click Play Again at any time to reset is_playing to False, restore the status message, and restart the countdown timer. The Result button opens a messagebox popup showing the current score standings and who is winning.


6. Sample Test Cases
#	Action / Input	Expected Output
1	Launch the game	Full-screen window opens with Rock, Paper, Scissors buttons and 7-second countdown
2	Click Rock within 7 seconds	Bounce animation plays, computer thinking animation runs, result is displayed
3	Player wins a round	Score updates: Player +1, flash animation on result label, 'You Win! 🎉' shown
4	Computer wins a round	Score updates: Computer +1, 'Computer Wins! 😔' shown
5	Both choose same option	'It's a Tie!' displayed, no score change
6	Timer reaches 0 without click	'Time's up!' and 'Too slow!' shown, input locked until Play Again
7	Click Result button	Popup displays current scores and who is winning
8	Click Play Again button	Timer resets to 7s, status resets, ready for new round
9	Image files missing	Game starts with text fallback buttons instead of images, no crash
10	Press Escape key	Exits full-screen mode to windowed mode

7. Challenges Faced
During the development of this game, our team encountered several challenges that required careful problem-solving:
Image Garbage Collection: Initially, the images loaded using Pillow were not appearing on the buttons. This happened because Python's garbage collector was removing the PhotoImage objects from memory. The issue was resolved by storing references to all loaded images inside the class instance (self.images) so they persist throughout the application's lifetime.
Preventing Multiple Clicks: During the computer's thinking animation, there was a risk that the player could click additional buttons, causing the game logic to break. This was solved by setting the is_playing flag to True as soon as the player makes a choice, which disables all input until the round is fully resolved and Play Again is clicked.
Timer and Animation Coordination: Coordinating the countdown timer with the choice animation was tricky. If the timer expired at the same moment the player clicked, conflicting states could arise. This was handled by cancelling the timer immediately in the play() method using root.after_cancel(self.timer_id) before starting the animation.
Pillow Dependency: The tkinter PhotoImage function only supports PNG and GIF formats natively. Since we wanted to use LANCZOS resampling for better image quality, we integrated the Pillow library. A try-except block handles the case where Pillow is unavailable or image files are missing, falling back to text labels gracefully.
Fullscreen Compatibility: The -fullscreen attribute behaves differently across operating systems. On Windows it works as expected, but on Linux or macOS the behavior may differ. We added the Escape key binding as an override so users can exit full-screen on any platform.

8. Results and Observations
The game was tested on Windows 11 using Python 3.11 with Pillow 10.x installed. The following observations were made during testing:
•	The 7-second countdown timer works consistently and creates a sense of urgency that makes the gameplay more exciting.
•	The computer thinking animation (10 rapid random cycles at 100ms intervals) feels realistic and avoids the game feeling instant or mechanical.
•	The bounce animation on the selected button and the flashing result label provide clear visual feedback without requiring any external animation library.
•	Score tracking works correctly across multiple rounds, including ties where neither score changes.
•	The fallback to text buttons when images are missing was tested by removing the PNG files — the game launched and functioned correctly without any crash.
•	The Result popup accurately reports the current game state: win, loss, tie, or no games played yet.
•	The game uses minimal system resources and runs smoothly on any standard computer running Python 3.x.
