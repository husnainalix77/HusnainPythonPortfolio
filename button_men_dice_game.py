## Button Men Dice Game
## Developed by: Husnain Maroof
## Dated: Feb 25–28, 2026
## Description: A turn-based dice game featuring real-time dice rolling animations.
import random
import tkinter as tk
class Die:
    def __init__(self, side):
        self.side = side
        self.value = 0 
        
    def roll_die(self):
        self.value = random.randint(1, self.side)    

class Player:
    characters = {
        "Titanus": [12, 20], "Viper": [6, 18], "Rift": [10, 16],
        "Bauer": [4, 6, 8], "Hammer": [10, 12, 14], "Shore": [5, 7, 9], "Stark": [3, 11, 13],
        "Sentinel": [4, 6, 10, 14], "Tempest": [3, 8, 11, 15],
        "Legion": [2, 4, 6, 8, 10],
    }
    
    def __init__(self, name, sides):
        self.name = name
        self.sides = sides
        self.dice = [Die(s) for s in self.sides]
        
    def roll_all_die(self):
        for d in self.dice:
            d.roll_die()  
            
    def highest_die(self):
        if not self.dice: return 0
        return max(die.value for die in self.dice)   
                 
    @staticmethod
    def ai_choose_character():
        all_chars = list(Player.characters.keys())
        char_weights = [sum(Player.characters[char]) for char in all_chars]
        total = sum(char_weights)
        char_probs = [w / total for w in char_weights]
        return random.choices(all_chars, weights=char_probs, k=1)[0]       
                 
    def ai_choose_dice(self, opponent):
        best_score, best_attack, best_target = float('-inf'), None, None
        for attack_die in self.dice:
            for target_die in opponent.dice:
                prob = sum(1 for x in range(1, attack_die.side+1) for y in range(1, target_die.side+1) if x >= y) / (attack_die.side * target_die.side)
                expected_diff = sum(max(x - y, 0) for x in range(1, attack_die.side+1) for y in range(1, target_die.side+1)) / (attack_die.side * target_die.side)
                score = expected_diff * prob + (1 / target_die.side) 
                overkill_penalty = max(0, (attack_die.side - 2 * target_die.side) / attack_die.side)
                score -= overkill_penalty  
                big_target_bonus = target_die.side / max(d.side for d in opponent.dice)
                score += big_target_bonus

                if score > best_score:
                    best_score = score
                    best_attack = attack_die
                    best_target = target_die
        return best_attack, best_target    
                        
    def is_winner(self, other):
        return len(other.dice) == 0
    
    @staticmethod
    def is_captured(attack_die, target_die):
        return attack_die.value >= target_die.value   

class ButtonMenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("A Husnain Maroof Production • Est. Feb 2026")
        self.root.geometry("800x650")
        self.root.configure(bg="#2b2b2b")
        
        self.player1 = None
        self.ai_player = None
        self.current_player = None
        self.other_player = None
        self.selected_attack_die = None
        self.selected_target_die = None
        # Store button references to update them during animation
        self.dice_buttons = {} 
        self.show_splash_screen()
        
    def show_splash_screen(self):
        self.clear_screen()
        splash_frame = tk.Frame(self.root, bg="#1a1a1a")
        splash_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(splash_frame, text="Button Men", font=("Verdana", 36, "bold"), bg="#910B0B", fg="#FFFFFF").pack()
        tk.Label(splash_frame, text="DEVELOPED BY", font=("Helvetica", 12), bg="#1a1a1a", fg="#888888").pack()
        tk.Label(splash_frame, text="HUSNAIN MAROOF", font=("Times New Roman", 40, "bold italic"), bg="#1a1a1a", fg="#ffffff").pack(pady=10)
        tk.Label(splash_frame, text="Initializing Battle Systems...", font=("Courier", 15), bg="#1a1a1a", fg="#444444").pack(pady=20)

        self.root.after(5000, self.create_selection_screen)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_selection_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Select Your Character", font=("Helvetica", 24, "bold"), bg="#2b2b2b", fg="white").pack(pady=30)
        frame = tk.Frame(self.root, bg="#2b2b2b")
        frame.pack()
        row, col = 0, 0
        for char, dice in Player.characters.items():
            btn = tk.Button(frame, text=f"{char}\n{dice}", font=("Helvetica", 14), bg="#4a4a4a", fg="white",
                            width=15, height=3, command=lambda c=char: self.select_character(c))
            btn.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 2: col, row = 0, row + 1

    def select_character(self, choice):
        self.player1 = Player('Player 1', Player.characters[choice])
        self.ai_player = Player('AI', Player.characters[Player.ai_choose_character()])
        self.start_game()

    def start_game(self):
        self.player1.roll_all_die()
        self.ai_player.roll_all_die()

        while True:
            p1_high = self.player1.highest_die()
            ai_high = self.ai_player.highest_die()

            # If not tied → break loop
            if p1_high != ai_high:
                break

            # Tie detected → roll ONLY tied dice
            for d in self.player1.dice:
                if d.value == p1_high:
                    d.roll_die()

            for d in self.ai_player.dice:
                if d.value == ai_high:
                    d.roll_die()

        # Decide who starts
        if p1_high > ai_high:
            self.current_player, self.other_player = self.player1, self.ai_player
        else:
            self.current_player, self.other_player = self.ai_player, self.player1
        # Display whose turn it is
        start_message = f"{self.current_player.name} starts the battle!"
        self.create_battle_screen(start_message)

        if self.current_player == self.ai_player:
            self.root.after(1500, self.ai_turn)

    def create_battle_screen(self, status_message=""):
        self.clear_screen()
        self.dice_buttons = {}
        # AI Section
        ai_f = tk.Frame(self.root, bg="#2b2b2b")
        ai_f.pack(pady=20)
        tk.Label(ai_f, text="AI DICE", fg="#ff6666", bg="#2b2b2b", font=("Arial", 12, "bold")).pack()
        self.draw_dice(self.ai_player, ai_f, True)
        # Battle Log
        self.log_label = tk.Label(self.root, text=status_message, font=("Helvetica", 16, "bold"), 
                                 bg="#2b2b2b", fg="#ffff99", wraplength=600, height=3)
        self.log_label.pack(pady=30)
        # Player Section
        p_f = tk.Frame(self.root, bg="#2b2b2b")
        p_f.pack(pady=20, side=tk.BOTTOM)
        self.draw_dice(self.player1, p_f, False)
        tk.Label(p_f, text="YOUR DICE", fg="#66ccff", bg="#2b2b2b", font=("Arial", 12, "bold")).pack(side=tk.BOTTOM)

    def draw_dice(self, player, parent, is_opp):
        frame = tk.Frame(parent, bg="#2b2b2b")
        frame.pack()
        for die in player.dice:
            color = "#8b0000" if is_opp else "#00008b"
            state = tk.NORMAL if self.current_player == self.player1 else tk.DISABLED
            btn = tk.Button(frame, text=f"d{die.side}\n[{die.value}]", font=("Arial", 18, "bold"),
                            width=6, height=3, bg=color, fg="white", state=state,
                            command=lambda d=die, o=is_opp: self.on_die_click(d, o))
            btn.pack(side=tk.LEFT, padx=10)
            self.dice_buttons[die] = btn

    def on_die_click(self, die, is_opp):
        if not is_opp:
            self.selected_attack_die = die
            self.log_label.config(text=f"Selected d{die.side}. Click an AI die!")
        elif is_opp and self.selected_attack_die:
            self.selected_target_die = die
            self.animate_roll(10) # Start 10-step animation

    def animate_roll(self, steps):
        if steps > 0:
            # Show random numbers on the buttons being rolled
            temp_atk = random.randint(1, self.selected_attack_die.side)
            temp_tar = random.randint(1, self.selected_target_die.side)
            
            self.dice_buttons[self.selected_attack_die].config(text=f"d{self.selected_attack_die.side}\n[{temp_atk}]", bg="#ffcc00")
            self.dice_buttons[self.selected_target_die].config(text=f"d{self.selected_target_die.side}\n[{temp_tar}]", bg="#ffcc00")
            
            self.log_label.config(text="ROLLING...", fg="#ffcc00")
            
            # Recursive call to next step of animation
            self.root.after(80, lambda: self.animate_roll(steps - 1))
        else:
            self.resolve_attack()

    def resolve_attack(self):
        # Final real roll
        self.selected_attack_die.roll_die()
        self.selected_target_die.roll_die()

        atk_value = self.selected_attack_die.value
        tar_value = self.selected_target_die.value
        # Update buttons to show FINAL values
        self.dice_buttons[self.selected_attack_die].config(
            text=f"d{self.selected_attack_die.side}\n[{atk_value}]",
            bg="#ffaa00"
        )
        self.dice_buttons[self.selected_target_die].config(
            text=f"d{self.selected_target_die.side}\n[{tar_value}]",
            bg="#ffaa00"
        )
        # Show result text clearly
        self.log_label.config(
            text=f"{self.current_player.name} rolled {atk_value}  |  "
                f"{self.other_player.name} rolled {tar_value}",
            fg="#ffffff"
        )
        # Check capture
        captured = Player.is_captured(self.selected_attack_die, self.selected_target_die)

        if captured:
            result_text = "SUCCESS! Die Captured!"
            result_color = "#66ff66"
            self.other_player.dice.remove(self.selected_target_die)
        else:
            result_text = "FAILED! No capture."
            result_color = "#ff6666"
        # Delay before switching turn so player sees result
        self.root.after(1500, lambda: self.finish_turn(result_text, result_color))
        
    def finish_turn(self, result_text, result_color):
        # Check win condition
        if self.current_player.is_winner(self.other_player):
            self.game_over(self.current_player.name)
            return
        # Switch turns
        self.current_player, self.other_player = self.other_player, self.current_player

        self.create_battle_screen(f"{result_text}\n{self.current_player.name}'s turn.")
        self.log_label.config(fg=result_color)

        if self.current_player == self.ai_player:
            self.root.after(1500, self.ai_turn)
            
    def ai_turn(self):
        atk, tar = self.current_player.ai_choose_dice(self.other_player)
        self.selected_attack_die = atk
        self.selected_target_die = tar
        self.animate_roll(10)

    def game_over(self, winner):
        self.clear_screen()
        self.winner_name = winner
        self.anim_frame = tk.Frame(self.root, bg="#000000")
        self.anim_frame.pack(fill="both", expand=True)

        self.winner_label = tk.Label(
            self.anim_frame,
            text=f"{winner} WINS!",
            font=("Verdana", 40, "bold"),
            fg="#FFD700",
            bg="#000000"
        )
        self.winner_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.sub_label = tk.Label(
            self.anim_frame,
            text="🏆 VICTORY ACHIEVED 🏆",
            font=("Helvetica", 20, "bold"),
            fg="white",
            bg="#000000"
        )
        self.sub_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.animation_step = 0
        self.animate_victory()
        # Close game after 4 seconds
        self.root.after(4000, self.root.destroy)
    
    def animate_victory(self):
        colors = ["#000000", "#1a001a", "#330033", "#4d004d", "#660066"]
        # Background flashing
        bg_color = colors[self.animation_step % len(colors)]
        self.anim_frame.config(bg=bg_color)
        self.winner_label.config(bg=bg_color)
        self.sub_label.config(bg=bg_color)
        # Text pulsing effect
        size = 40 + (self.animation_step % 6) * 3
        self.winner_label.config(font=("Verdana", size, "bold"))
        self.animation_step += 1
        # Continue animation
        self.root.after(150, self.animate_victory)    

if __name__ == "__main__": 
    root = tk.Tk()
    app = ButtonMenGUI(root)
    root.mainloop()