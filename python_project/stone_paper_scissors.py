import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import random
import sys
import threading
import time
import os

BG_COLOR = "#0F172A"
FRAME_BG = "#1E293B"
ACCENT_COLOR = "#6366F1"
TEXT_COLOR = "#F8FAFC"
SUCCESS_COLOR = "#10B981"
DANGER_COLOR = "#EF4444"
INFO_COLOR = "#3B82F6"

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.configure(bg=BG_COLOR)
        
        self.user_score = 0
        self.computer_score = 0
        self.time_left = 7
        self.timer_id = None
        self.is_playing = False
        
        self.images = {}
        try:
            for item in ["rock", "paper", "scissors"]:
                img = Image.open(f"{item}.png").resize((80, 80), Image.LANCZOS)
                self.images[item] = ImageTk.PhotoImage(img)
        except Exception as e:
            print("Could not load images. Using text fallbacks.")
            self.images = {"rock": None, "paper": None, "scissors": None}

        self.setup_ui()
        self.start_timer()

    def setup_ui(self):
        self.center_wrapper = tk.Frame(self.root, bg=BG_COLOR)
        self.center_wrapper.place(relx=0.5, rely=0.5, anchor="center")
        
        title_font = font.Font(family="Segoe UI", size=30, weight="bold")
        title_lbl = tk.Label(self.center_wrapper, text="Rock Paper Scissors", bg=BG_COLOR, fg=TEXT_COLOR, font=title_font)
        title_lbl.pack(pady=(40, 20))
        
        self.main_frame = tk.Frame(self.center_wrapper, bg=FRAME_BG, highlightbackground=ACCENT_COLOR, highlightcolor=ACCENT_COLOR, highlightthickness=3)
        self.main_frame.pack(pady=20, padx=50, fill="x")
        
        score_frame = tk.Frame(self.main_frame, bg=FRAME_BG)
        score_frame.pack(pady=30)
        
        score_font = font.Font(family="Segoe UI", size=14, weight="bold")
        
        self.player_score_lbl = tk.Label(score_frame, text=f"Player: {self.user_score}", bg=FRAME_BG, fg=SUCCESS_COLOR, 
                                         font=score_font, highlightbackground=SUCCESS_COLOR, highlightthickness=2, padx=15, pady=5, borderwidth=0)
        self.player_score_lbl.pack(side="left", padx=15)
        
        self.comp_score_lbl = tk.Label(score_frame, text=f"Computer: {self.computer_score}", bg=FRAME_BG, fg=DANGER_COLOR, 
                                       font=score_font, highlightbackground=DANGER_COLOR, highlightthickness=2, padx=15, pady=5, borderwidth=0)
        self.comp_score_lbl.pack(side="left", padx=15)
        
        btn_frame = tk.Frame(self.main_frame, bg=FRAME_BG)
        btn_frame.pack(pady=20)
        
        self.rock_lbl = self.create_choice_btn(btn_frame, "rock")
        self.rock_lbl.pack(side="left", padx=15)
        
        self.paper_lbl = self.create_choice_btn(btn_frame, "paper")
        self.paper_lbl.pack(side="left", padx=15)
        
        self.scissors_lbl = self.create_choice_btn(btn_frame, "scissors")
        self.scissors_lbl.pack(side="left", padx=15)
        
        self.status_font = font.Font(family="Segoe UI", size=20, weight="bold")
        self.status_lbl = tk.Label(self.main_frame, text="Choose your weapon!", bg=FRAME_BG, fg=TEXT_COLOR, font=self.status_font)
        self.status_lbl.pack(pady=(20, 5))
        
        self.timer_font = font.Font(family="Segoe UI", size=16)
        self.timer_lbl = tk.Label(self.main_frame, text=f"Time left: {self.time_left}s", bg=FRAME_BG, fg=ACCENT_COLOR, font=self.timer_font)
        self.timer_lbl.pack(pady=(0, 30))
        
        control_frame = tk.Frame(self.main_frame, bg=FRAME_BG)
        control_frame.pack(pady=(0, 40))
        
        btn_font = font.Font(family="Segoe UI", size=12, weight="bold")
        
        self.result_btn = tk.Button(control_frame, text="Result", bg=INFO_COLOR, fg="#FFFFFF", font=btn_font, 
                                    relief=tk.FLAT, activebackground="#2563EB", activeforeground="#FFFFFF",
                                    command=self.show_result, width=10, pady=8, cursor="hand2")
        self.result_btn.pack(side="left", padx=10)
        
        self.play_again_btn = tk.Button(control_frame, text="Play Again", bg=ACCENT_COLOR, fg="#FFFFFF", font=btn_font, 
                                        relief=tk.FLAT, activebackground="#4F46E5", activeforeground="#FFFFFF",
                                        command=self.reset_game, width=12, pady=8, cursor="hand2")
        self.play_again_btn.pack(side="left", padx=10)
        
        self.exit_btn = tk.Button(control_frame, text="Exit", bg=DANGER_COLOR, fg="#FFFFFF", font=btn_font, 
                                  relief=tk.FLAT, activebackground="#DC2626", activeforeground="#FFFFFF",
                                  command=self.root.destroy, width=10, pady=8, cursor="hand2")
        self.exit_btn.pack(side="left", padx=10)

    def create_choice_btn(self, parent, choice):
        lbl = tk.Label(parent, bg="#FFFFFF", highlightbackground=ACCENT_COLOR, highlightthickness=3, cursor="hand2")
        img = self.images.get(choice)
        if img:
            lbl.config(image=img)
        else:
            lbl.config(text=choice.capitalize(), font=("Segoe UI", 16), padx=20, pady=20)
            
        lbl.bind("<Button-1>", lambda e: self.play(choice))
        lbl.bind("<Enter>", lambda e: lbl.config(highlightthickness=3))
        lbl.bind("<Leave>", lambda e: lbl.config(highlightthickness=1))
        return lbl

    def start_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.time_left = 7
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0 and not self.is_playing:
            self.timer_lbl.config(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and not self.is_playing:
            self.timer_lbl.config(text="Time's up!")
            self.status_lbl.config(text="Too slow!")
            self.is_playing = True

    def play(self, user_choice):
        if self.is_playing:
            return
        
        self.is_playing = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        self.status_lbl.config(text="Computer is thinking...")
        
        chosen_lbl = getattr(self, f"{user_choice}_lbl")
        self.animate_bounce(chosen_lbl, 0)
        
        self.animation_step = 0
        self.animate_computer_choice(user_choice)

    def animate_bounce(self, widget, step):
        if step < 3:
            widget.pack_configure(pady=(0, 10))
            self.root.after(50, lambda: self.animate_bounce_down(widget, step))
            
    def animate_bounce_down(self, widget, step):
        widget.pack_configure(pady=(0, 0))
        self.root.after(50, lambda: self.animate_bounce(widget, step + 1))

    def animate_computer_choice(self, user_choice):
        options = ["rock", "paper", "scissors"]
        if self.animation_step < 10:
            random_choice = random.choice(options)
            self.timer_lbl.config(text=f"Computer rolls: {random_choice.capitalize()}")
            self.animation_step += 1
            self.root.after(100, lambda: self.animate_computer_choice(user_choice))
        else:
            computer_choice = random.choice(options)
            self.timer_lbl.config(text=f"Computer chose: {computer_choice.capitalize()}!")
            self.determine_winner(user_choice, computer_choice)

    def determine_winner(self, user, comp):
        if user == comp:
            result = "It's a Tie!"
        elif (user == "rock" and comp == "scissors") or \
             (user == "paper" and comp == "rock") or \
             (user == "scissors" and comp == "paper"):
            result = "You Win! 🎉"
            self.user_score += 1
        else:
            result = "Computer Wins! 😔"
            self.computer_score += 1

        self.status_lbl.config(text=result)
        self.update_scores()
        self.flash_result(0)

    def flash_result(self, count):
        if count < 4:
            current_color = self.status_lbl.cget("fg")
            new_color = SUCCESS_COLOR if current_color == TEXT_COLOR else TEXT_COLOR
            self.status_lbl.config(fg=new_color)
            self.root.after(300, lambda: self.flash_result(count + 1))
        else:
            self.status_lbl.config(fg=TEXT_COLOR)

    def update_scores(self):
        self.player_score_lbl.config(text=f"Player: {self.user_score}")
        self.comp_score_lbl.config(text=f"Computer: {self.computer_score}")

    def reset_game(self):
        self.is_playing = False
        self.status_lbl.config(text="Choose your weapon!", fg=TEXT_COLOR)
        self.start_timer()

    def show_result(self):
        if self.user_score == 0 and self.computer_score == 0:
            msg = "No games have been scored yet!\nStart playing to see results."
        elif self.user_score > self.computer_score:
            msg = f"🏆 You are winning!\n\nCurrent Score:\nYou: {self.user_score}\nComputer: {self.computer_score}"
        elif self.computer_score > self.user_score:
            msg = f"🤖 Computer is winning!\n\nCurrent Score:\nYou: {self.user_score}\nComputer: {self.computer_score}"
        else:
            msg = f"⚖️ It's a dead heat tie!\n\nCurrent Score:\nYou: {self.user_score}\nComputer: {self.computer_score}"
            
        messagebox.showinfo("Game Result", msg)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = RockPaperScissorsGame(root)
        root.mainloop()
    except Exception as e:
        print("Application Error:", e)

