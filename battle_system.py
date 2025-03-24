import random
 
# TODO: Create a character class definition
'''
this is a character class definition. Each character will need the following attributes:
name
strength
max health
current health
speed
armor
self.attacks = attacks (this will be aDictionary of attack names and damage dice (e.g., {"Sword": "1d8", "Punch": "1d4"}))
self.magic_types = magic_types if magic_types else {} 
    (I don't know, but also some kind of Dictionary of magic types and damge dice (e.g. {"Fire": "2d6", "Ice": "1d4"}))
'''
# I might need something similar for enemies?

class Character:
    def __init__(self, name, strength, max_health, current_health, speed, armor, attacks, magic_types):
        self.name = name
        self.strength = strength
        self.max_health = max_health
        self.current_health = current_health
        self.speed = speed
        self.armor = armor
        self.attacks = attacks
        self.magic_types = magic_types = magic_types if magic_types else {
            "Fire" : "2d6",
            "Ice" : "1d4",
            "Lightning" : "1d8"
        }


'''
I'll need some sort of game mechanic for the dice roll (a def function?)
a quick Google tells me that you can imitate a dice roll in python by using the random.randint(1, 8) function
something sort of like this?
def roll_1d8():
  """Simulates rolling a single 8-sided die."""
  return random.randint(1, 8)

# Example usage
result = roll_1d8()
print(f"You rolled: {result}")
'''

  
def roll_dice(self, dice_notation):
    #rolls dice based on the given notation (i.e., "1d8", "2d6", etc.)
    num_dice, die_size = map(int, dice_notation.split('d'))
    return sum(random.randint(1, die_size) for _ in range(num_dice))





'''
At the start of each turn, I'd want to print out the state of all the characters stats (health remaining, strength, remaining magic, etc.)
I want to make good use of the random module. it's like dice rolls. high numbers hit harder. randomized strength/health against randomized damage done by baddies, that sort of thing.
Take enough hits and you die. Hit them enough times and they die. Turn based. Decide if you wanna heal or attack or dodge or whatever. 
Magic does more damage against certain enemies. Swords against others. 
'''

# TODO: Create a character instance

# TODO: Create a battle function definition
# like def battle(player, enemy):

def attack(self, target, attack_name, magic_type=None):
    #this will be the attack function (whatever type of attack it is, physical or magical)
    if magic_type and magic_type in self.magic_types: #this line checks to see if the attack is magical in nature, and if the magic type is known
        damage = self.roll_dice(self.magic_types[magic_type]) #this will be the roll damage based on the magic type        
        print(f"{self.name} cast {magic_type} and dealt {damage} damage to {target.name}!") # this will print the magic type and the damage done to the target
    elif attack_name in self.attacks:
        damage = self.roll_dice(self.attacks[attack_name]) #this will be the roll damage based on the attack name's damage
        damage -= target.armor #this will subtract the target's armor from the damage. Better armor = less damage. Duh.
        damage = max(0, damage) #this will make sure the damage is at least 0. Can't have negative damage. Duh.
        print(f"{self.name} used {attack_name} and dealt {damage} damage to {target.name}!") # this will print the attack name and the damage done to the target
    else:
        print(f"{self.name} doesn't know how to attack with {attack_name}. No damage!") # this will print that the character doesn't know how to attack with the attack name
        return #this will exit the function if the attack is invalid
    target.take_damage(damage) #this will subtract the damage from the target's health

# how is a character's health damaged?
def take_damage(self, damage):
    self.current_health -= damage #this reduces the character's health by the damage amount rolled
    if self.current_health <= 0: #this checks to see if the character's health is less than or equal to 0
        self.current_health = 0 # this sets the character's health to 0
        print(f"{self.name} is dead!") # this makes it official

# how can characters be healed?
def heal(self, amount):
    self.current_health = min(self.max_health, self.current_health + amount) # this increases the character's health, but not beyond their max health
    print(f"{self.name} healed for {amount} health. Current health: {self.current_health}.")
    
# not sure if I'd need this, but I probably should be able to check if a character is alive
def is_alive(self):
    if self.current_health > 0:
        print(f"{self.name} is not dead yet!")
        return True
    else:
        print(f"{self.name} is dead!")
        return False

# how can characters display their stats?
def display_stats(self):
        # Displays the character's stats.
        print(f"{self.name}: Health: {self.current_health}/{self.max_health}, Strength: {self.strength}, Armor: {self.armor}, Speed: {self.speed}")  # Print character stats

# I need a function that makes it so that the more armor a character has, the less speed they have.
# TODO figure out if this requires a max speed. Probably does.
def calculate_speed(self):
    return self.speed - self.armor


# TODO: figure out the dodge function

# TODO: figure out the list of attack names

# TODO: figure out the list of magic attacks

# TODO: figure out the list of enemy attack choices

# what does a battle look like?
def battle(player, enemies):
    # This will handle the battle between the player and enemies
    characters = [player] + enemies  # TODO Create a list of all characters (player and enemies)
    turn = 1  # Initializes the turn counter

    while player.is_alive() and any(enemy.is_alive() for enemy in enemies):  # Continue the battle while the player and any enemy is alive
        print(f"\n--- Turn {turn} ---")  # Print the turn number

        for character in characters:  # This will loop through each character
            if not character.is_alive():  # Skip the dead characters
                continue

            character.display_stats()  # Display the character's stats

            if character == player:  # Player's turn
                action = input("Choose action (attack, heal, magic, dodge): ").lower()  # Get player's action input
                # if they choose violence...
                if action == "attack":
                    enemy_names = [enemy.name for enemy in enemies if enemy.is_alive()] #Create a list of alive enemy names.
                    if not enemy_names: # If there are no alive enemies.
                        print("No enemies left to attack!")
                        continue # Skip rest of turn.
                    print("Enemies:", ", ".join(enemy_names)) #Prints the alive enemy names.
                    target_name = input("Who will you attack? ") #Gets the target enemy name.
                    target = next((enemy for enemy in enemies if enemy.name == target_name and enemy.is_alive()), None) #Find the target enemy object.
                    if not target: # If the target enemy is invalid.
                        print("Invalid target.")
                        continue # Skip rest of turn.
                    attack_names = list(character.attacks.keys()) # Gets the list of attack names.
                    print("Attacks:", ", ".join(attack_names)) # Prints the attack names.
                    attack_choice = input("Choose attack: ") # Gets the attack choice.
                    character.attack(target, attack_choice) # Actually performs the attack.
                # if they choose to heal...
                elif action == "heal":
                    heal_amount = random.randint(10, 20)  # Generate a random heal amount
                    player.heal(heal_amount)  # Heal the player
                # if they choose to be REALLY awesome...
                elif action == "magic":
                    enemy_names = [enemy.name for enemy in enemies if enemy.is_alive()] # Creates list of alive enemy names.
                    if not enemy_names: # If there are no alive enemies.
                        print("No enemies alive to attack!")
                        continue # Skips rest of turn.
                    print("Enemies:", ", ".join(enemy_names)) # Prints the alive enemy names.
                    target_name = input("Who to attack? ") # Gets the target enemy name.
                    target = next((enemy for enemy in enemies if enemy.name == target_name and enemy.is_alive()), None) #Find the target enemy object.
                    if not target: # If the target enemy is invalid.
                        print("Invalid target.")
                        continue # Skips rest of turn.
                    magic_names = list(character.magic_types.keys()) # Gets the list of magic spell names.
                    print("Magic:", ", ".join(magic_names)) # Prints magic spell names.
                    magic_choice = input("Choose magic: ") # Gets the magic spell choice.
                    character.attack(target, "magic attack", magic_choice) #Perform the magic attack.
                # if they are a little bit chicken...
                elif action == "dodge":
                    print(f"{player.name} attempts to dodge!")  # Prints a dodge message
                    # TODO I need to figure out the dodge mechanics here (so that it reduces incoming damage for the next turn).
                else:
                    print("Invalid action.")  # Prints an error message for invalid actions

            else:  # Enemy's turn (basic AI)
                player_alive = player.is_alive()
                if player_alive:
                    character.attack(player, random.choice(list(character.attacks.keys())))  # Enemy attacks the player with a random attack

        turn += 1  # Increment the turn counter

    if player.is_alive():  # Checks if the player is alive after the battle
        print("You won the battle!")
    else:
        print("You were defeated!")






# # Example Usage:
# player = Character("Hero", strength=15, health=100, armor=2, attacks={"Sword": "1d10", "Kick": "1d6"}, magic_types={"Fire": "2d6"})  # Create a player character
# enemy1 = Character("Goblin", strength=8, health=50, armor=1, attacks={"Club": "1d6"})  # Create an enemy character
# enemy2 = Character("Orc", strength=12, health=75, armor=3, attacks={"Axe": "1d8"})  #Create another enemy character

# battle(player, [enemy1, enemy2]) #Start the battle







