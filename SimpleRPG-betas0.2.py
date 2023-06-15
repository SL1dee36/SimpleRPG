import tkinter as tk
import random
from tkinter import ttk


class Player:
    def __init__(self):
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
    Enemy("Bruce", 30, 15)
]

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
    
    update_stats()

def attack():
    player.attack(enemy)
    update_stats()
    if enemy.hp > 0:
        enemy.attack(player)
    if player.hp <= 0:
        text.insert(tk.END, "GAME OVER\n")
        button_attack.config(state=tk.DISABLED)
        button_flee.config(state=tk.DISABLED)
        button_heal.config(state=tk.DISABLED)
    elif enemy.hp <= 0:
        button_attack.config(state=tk.DISABLED)
        button_flee.config(state=tk.DISABLED)
        button_heal.config(state=tk.DISABLED)
        button_start.config(state=tk.NORMAL)

def flee():
    if player.flee(enemy):
        button_attack.config(state=tk.DISABLED)
        button_flee.config(state=tk.DISABLED)
        button_heal.config(state=tk.DISABLED)
        button_start.config(state=tk.NORMAL)
    else:
        enemy.attack(player)
        if player.hp <= 0:
            text.insert(tk.END, "GAME OVER\n")
            button_attack.config(state=tk.DISABLED)
            button_flee.config(state=tk.DISABLED)
            button_heal.config(state=tk.DISABLED)

def heal():
    player.heal()
    update_stats()
    if player.available_heals == 0:
        button_heal.config(state=tk.DISABLED)

def update_stats():
    hp_text.set(f"HP: {player.hp}/{player.max_hp}")
    xp_text.set(f"XP: {player.xp}")
    level_text.set(f"Level: {player.level}")
#Create an instance of the player

player = Player()
#Create the application window

window = tk.Tk()
window.title("SimpleRPG")
window.geometry("400x640")
window.resizable(False, False)
window.configure(background="#2F4F4F")
#Add styles

COLOR_TEXT = "#DCDCDC"
COLOR_BUTTON_ATTACK = "#008080"
COLOR_BUTTON_HEAL = "#32CD32"
COLOR_BUTTON_OTHER = "#008080"
COLOR_BUTTON_START = "#20B2AA"

style = ttk.Style()
style.theme_use('clam')
style.configure('.', background="#2F4F4F", foreground=COLOR_TEXT, font=('Arial', 14))
style.configure('TButton', padding=6, relief='flat', background=COLOR_BUTTON_OTHER)
style.map('TButton', foreground=[('active', COLOR_TEXT), ('pressed', COLOR_TEXT)], background=[('active', "#2F4F4F"),('disabled','#708090'), ('pressed', "#66CDAA")])
style.configure('Start.TButton', padding=6, relief='flat', background=COLOR_BUTTON_START)
style.map('Start.TButton', foreground=[('active', COLOR_TEXT), ('pressed', COLOR_TEXT)], background=[('active', "#20B2AA"),('disabled','#708090'), ('pressed', "#66CDAA")])
style.configure('Attack.TButton', background=COLOR_BUTTON_ATTACK)
style.map('Attack.TButton', foreground=[('active', COLOR_TEXT), ('pressed', COLOR_TEXT)], background=[('active', "#2F4F4F"),('disabled','#708090'), ('pressed', "#66CDAA")])
style.configure('Heal.TButton', background=COLOR_BUTTON_HEAL)
style.map('Heal.TButton', foreground=[('active', COLOR_TEXT), ('pressed', COLOR_TEXT)], background=[('active', "#2F4F4F"),('disabled','#708090'), ('pressed', "#66CDAA")])
style.configure('TLabel', background="#2F4F4F", foreground=COLOR_TEXT)
#Create widgets

hp_text = tk.StringVar()
hp_text.set(f"HP: {player.hp}/{player.max_hp}")
xp_text = tk.StringVar()
xp_text.set(f"XP: {player.xp}")
level_text = tk.StringVar()
level_text.set(f"Level: {player.level}")

label_hp = ttk.Label(window, textvariable=hp_text)
label_hp.pack()

label_xp = ttk.Label(window, textvariable=xp_text)
label_xp.pack()

label_level = ttk.Label(window, textvariable=level_text)
label_level.pack()

button_start = ttk.Button(window, text="Start Battle", style='Start.TButton', command=start_battle)
button_start.pack()

button_attack = ttk.Button(window, text="Attack", style='Attack.TButton', command=attack, state=tk.DISABLED)
button_attack.pack()

button_flee = ttk.Button(window, text="Flee", command=flee, state=tk.DISABLED)
button_flee.pack()

button_heal = ttk.Button(window, text="Heal", style='Heal.TButton', command=heal)
if player.available_heals == 0:
    button_heal.config(state=tk.DISABLED)
button_heal.pack()


text = tk.Text(window, height=12, background="#2F4F4F", foreground=COLOR_TEXT, font=('Arial', 14))
text.pack(fill=tk.BOTH, expand=True)
#Add language selection dropdown

def change_language(event):
    language = combobox_language.get()
    if language == "Russian":
        button_start.config(text="Начать битву")
        button_attack.config(text="Атаковать")
        button_flee.config(text="Сбежать")
        button_heal.config(text="Исцелиться")
        text.insert(tk.END, "Выбран русский язык!\n")
    else:
        button_start.config(text="Start Battle")
        button_attack.config(text="Attack")
        button_flee.config(text="Flee")
        button_heal.config(text="Heal")
        text.insert(tk.END, "English language selected.\n")

combobox_language = ttk.Combobox(window, values=["English", "Russian"], state="readonly", background="#008B8B", foreground="#2F4F4F")
combobox_language.current(0)
combobox_language.bind("<<ComboboxSelected>>", change_language)
combobox_language.pack()
#Start the main event loop

window.mainloop()