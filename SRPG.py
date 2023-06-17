import tkinter as tk
import random
from tkinter import ttk
import os

class Player:
    def __init__(self):
        if os.path.exists(SAVE_FILE_PATH):
            self.load()
        else:
            self.max_hp = 20
            self.hp = self.max_hp
            self.xp = 0
            self.level = 1
            self.damage = 3
            self.heal_amount = 5
            self.available_heals = 3
            
    def attack(self, enemy):
        damage = random.randint(1, self.damage)
        enemy.hp -= damage
        text.insert(tk.END, f"You attacked the {enemy.name} for {damage} damage!\n")
        if enemy.hp <= 0:
            self.xp += enemy.xp_reward
            text.insert(tk.END, f"\nYou defeated the {enemy.name} and gained {enemy.xp_reward} XP!\n\n")
            
            if self.xp >= 10:
                self.level += 1
                self.max_hp += 5
                self.hp = self.max_hp
                self.damage += 1
                self.available_heals += 1
                self.xp -= 10
                text.insert(tk.END, "Congratulations! You leveled up!\n\n")

    def heal(self):
        if self.hp == self.max_hp:
            text.insert(tk.END, "Your HP is already at maximum.\n\n")
        elif self.available_heals == 0:
            text.insert(tk.END, "You have no more heals left.\n\n")
        else:
            healed_amount = min(self.max_hp - self.hp, self.heal_amount)
            self.hp += healed_amount
            self.available_heals -= 1
            text.insert(tk.END, f"You healed yourself for {healed_amount} HP. You have {self.available_heals} heals left.\n\n")
            if self.available_heals == 0:
                button_heal.config(state=tk.DISABLED)
        
    def flee(self, enemy):
        chance = random.randint(1, 2)
        if chance == 1:
            text.insert(tk.END, f"You successfully fled from the {enemy.name}.\n\n")
            return True
        else:
            text.insert(tk.END, f"You failed to flee from the {enemy.name}.\n\n")
            return False
        
    def save(self):
        with open(SAVE_FILE_PATH, "w") as f:
            f.write(f"{self.max_hp}\n{self.hp}\n{self.xp}\n{self.level}\n{self.damage}\n{self.heal_amount}\n{self.available_heals}")
        text.insert(tk.END, "Your progress has been saved.\n\n")
        
    def load(self):
        with open(SAVE_FILE_PATH, "r") as f:
            lines = f.readlines()
            self.max_hp = int(lines[0])
            self.hp = int(lines[1])
            self.xp = int(lines[2])
            self.level = int(lines[3])
            self.damage = int(lines[4])
            self.heal_amount = int(lines[5])
            self.available_heals = int(lines[6])
        text.insert(tk.END, "Your progress has been loaded.\n\n")

class Enemy:
    def __init__(self, name, hp, xp_reward):
        self.name = name
        self.hp = hp
        self.xp_reward = xp_reward

    def attack(self, player):
        damage = random.randint(1, 3)
        player.hp -= damage
        text.insert(tk.END, f"The {self.name} attacked you for {damage} damage!\n")
        if player.hp <= 0:
            text.insert(tk.END, "GAME OVER\n")
            button_attack.config(state=tk.DISABLED)
            button_flee.config(state=tk.DISABLED)
            button_heal.config(state=tk.DISABLED)

enemies = [
Enemy("Goblin", 10, 5),
Enemy("Orc", 12, 7),
Enemy("Troll", 15, 10),
Enemy("Dragon", 20, 15),
Enemy("Ciclop", 30, 30),
Enemy("Admin", 70, 40),
Enemy("Shark", 29, 71),
Enemy("Watermelon", 91, 88),
Enemy("RED Dragon", 120, 130),
Enemy("Bruce", 90, 124)
]

SAVE_FILE_PATH = "save.txt"

def start_battle():
    global player, enemy

    enemy = random.choice(enemies)
    enemy.hp += 2 * player.level
    enemy.xp_reward += player.level

    text.insert(tk.END, f"A {enemy.name} has appeared!\n\n")

    button_start.config(state=tk.DISABLED)
    button_attack.config(state=tk.NORMAL)
    button_flee.config(state=tk.NORMAL)
    button_heal.config(state=tk.NORMAL)

def attack():
    player.attack(enemy)
    update_stats()
    if enemy.hp > 0:
        enemy.attack(player)
        update_stats()

def flee():
    if player.flee(enemy):
        end_battle()

def heal():
    player.heal()
    update_stats()

def save_game():
    player.save()

def load_game():
    player.load()
    update_stats()

def end_battle():
    button_start.config(state=tk.NORMAL)
    button_attack.config(state=tk.DISABLED)
    button_flee.config(state=tk.DISABLED)
    button_heal.config(state=tk.DISABLED)
    text.insert(tk.END, "The battle has ended.\n\n")
    player.available_heals = min(player.available_heals + 1, 3)
    player.xp += enemy.xp_reward
    if player.xp >= 10:
        player.level += 1
        player.max_hp += 5
        player.hp = player.max_hp
        player.damage += 1
        player.available_heals += 1
        player.xp -= 10
        text.insert(tk.END, "Congratulations! You leveled up!\n\n")
        update_stats()

def update_stats():
    label_hp.config(text=f"HP: {player.hp}/{player.max_hp}")
    label_level.config(text=f"Level: {player.level}")
    label_xp.config(text=f"XP: {player.xp}/10")
    label_heals.config(text=f"Heals: {player.available_heals}/3")

window = tk.Tk()
window.title("SimpleRPG V0.3")
window.geometry('800x560')
window.resizable(False, False)
window.configure(bg="white")
try:
    icon_path = "C:/Users/nazar/Downloads/swordsman.ico"
    window.iconbitmap(default=icon_path)
except: pass
font = ("Consolas", 14)
style = ttk.Style()

style.theme_use("alt")

style.configure("TLabel", background="#E0E0E0",font=font, foreground="#212121")
style.configure("TButton", background="#009688",font=font, foreground="white")
style.map("TButton",
          background=[("active", "#00897B")],
          foreground=[("active", "white")])

# ...


frame_top = ttk.Frame(window)
frame_top.pack(side=tk.TOP, padx=10, pady=10)

style = ttk.Style()
style.configure("My.TFrame", background="white")

frame_bottom = ttk.Frame(window, style="My.TFrame")
frame_bottom.pack(side=tk.BOTTOM, padx=10, pady=10)


text = tk.Text(frame_top, height=20, width=130, bg="black", fg="white")
text.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(frame_top, command=text.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

text.config(yscrollcommand=scrollbar.set)


style = ttk.Style()
style.configure("PurpleButton.TButton", foreground="white", background="black")

button_start = ttk.Button(frame_bottom, text="Start Battle", command=start_battle, style="PurpleButton.TButton")
button_start.pack(side=tk.LEFT)

button_attack = ttk.Button(frame_bottom, text="Attack", command=attack, state=tk.DISABLED, style="PurpleButton.TButton")
button_attack.pack(side=tk.LEFT, padx=10)

button_flee = ttk.Button(frame_bottom, text="Flee", command=flee, state=tk.DISABLED, style="PurpleButton.TButton")
button_flee.pack(side=tk.LEFT, padx=10)

button_heal = ttk.Button(frame_bottom, text="Heal", command=heal, state=tk.DISABLED, style="PurpleButton.TButton")
button_heal.pack(side=tk.LEFT, padx=10)

button_save = ttk.Button(frame_bottom, text="Save Game", command=save_game, style="PurpleButton.TButton")
button_save.pack(side=tk.BOTTOM)

button_load = ttk.Button(frame_bottom, text="Load Game", command=load_game, style="PurpleButton.TButton")
button_load.pack(side=tk.BOTTOM, padx=10)

label_hp = ttk.Label(window, text="HP: ", font=("Consolas", 12), foreground="black",background="white")
label_hp.pack(pady=5)

label_level = ttk.Label(window, text="Level: ", font=("Consolas", 12), foreground="black",background="white")
label_level.pack(pady=5)

label_xp = ttk.Label(window, text="XP: ", font=("Consolas", 12), foreground="black",background="white")
label_xp.pack(pady=5)

label_heals = ttk.Label(window, text="Heals: ", font=("Consolas", 12), foreground="black",background="white")
label_heals.pack(pady=5)

player = Player()
enemy = None

update_stats()

window.mainloop()
