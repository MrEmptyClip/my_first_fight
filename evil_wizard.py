import random

#Create the ability to have damage over time
class DoT:
    def __init__(self, damage_per_turn, duration):
        self.damage_per_turn = damage_per_turn
        self.duration = duration
        self.turns_remaining = duration

    def apply_effect(self, opponent):
        if self.turns_remaining > 0:
            opponent.take_damage(self.damage_per_turn)
            self.turns_remaining -= 1
            print(f"{opponent.name} took {int(self.damage_per_turn)} DoT damage. Turns remaining: {self.turns_remaining}")
        else:
            print(f"The DoT effect on {opponent.name} has expired.")

#Turn counter
class CountedInput(object):
    def __init__(self):
        self.counter = 0
    def input(self, *args):
        self.counter += 1
        return input(*args)

counted_input = CountedInput()

# Base Character class
class Character:
    def __init__(self, name, health, min_att, max_att):
        self.name = name
        self.health = health
        self.min_att = min_att
        self.max_att = max_att
        self.max_health = health
        self.active_effects = []

    def attack(self, opponent):
        attack_power = random.randint(self.min_att, self.max_att)
        opponent.health -= attack_power
        print(f"{self.name} attacks {opponent.name} for {int(attack_power)} damage!")
        

    def heal(self):
        if self.health <= self.max_health - 30:
            self.health += 30
            print(f"{self.name} drinks a health potion to recover to {int(self.health)} health!")
        else:
            print("Turn lost as you vomit the potion because you have not lost enouigh health to heal yourself!")
    
    #applies DoTs
    def apply_effects(self):
        for effect in self.active_effects[:]:
            effect.apply_effect(self)
            if effect.turns_remaining <= 0:
                self.active_effects.remove(effect)
    #applies DoT damage
    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name} has {int(self.health)} health remaining.")
        if self.health <= 0:
            print(f"{self.name} has been defeated!")

#takes a turn to view current player stats
    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {int(self.health)}/{self.max_health}, Attack Power: {self.min_att}-{self.max_att}")

# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, min_att=20, max_att=30)
    def special(self, opponent):
        attack_power = random.randint(self.min_att, self.max_att) * .6
        opponent.health -= attack_power
        dot_effect = DoT(damage_per_turn=attack_power, duration=3)
        opponent.active_effects.append(dot_effect)
        print(f"{self.name} disembowels {opponent.name}, dealing {int(attack_power)} damage until he picks up his intestines in 3 turns!")

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, min_att=30, max_att=40)
    def special(self, opponent):
        attack_power = random.randint(self.min_att, self.max_att) * 1.6
        opponent.health -= attack_power
        print(f"{self.name} drops a meteorite on {opponent.name} for {int(attack_power)} damage!")

# Create Archer class
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=90, min_att=30, max_att=40)
    def special(self, opponent):
        attack_power = random.randint(self.min_att, self.max_att) * 2
        opponent.health -= attack_power
        print(f"{self.name} launches two arrows at once for {int(attack_power)} damage!")

# Create Paladin class 
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=140, min_att=25, max_att=35)
    def special(self, opponent):
        attack_power = random.randint(self.min_att, self.max_att) * .7
        #uses DoT class method to apply a heal over time to player with a negative integer based on attack power
        heal = random.randint(self.min_att, self.max_att) / 5 * -1
        dot_effect = DoT(damage_per_turn=heal, duration=3)
        #applies DoT class method to opponent
        self.active_effects.append(dot_effect)
        dot_effect = DoT(damage_per_turn=attack_power, duration=3)
        opponent.active_effects.append(dot_effect)
        print(f"{self.name} consecrates the ground for {int(attack_power)} damage and healing themselves for {heal} over 3 turns!")
        
class Technician(Character):
    def __init__(self, name):
        super().__init__(name, health=70, min_att=15, max_att=40)
    def special(self, opponent):
        attack_power = random.randint(self.min_att, self.max_att) * 2 / 3
        dot_effect = DoT(damage_per_turn=attack_power, duration=5)
        opponent.active_effects.append(dot_effect)
        print(f"{self.name} shoots a dart with nanobots that attack {opponent.name} from the inside for {int(attack_power)} over 5 turns!")
        
# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=250, min_att=10, max_att=60)
        self.attacks = {
            "Staff Whack": 10,
            "Cat Throw": 30,
            "Acid Pour": 13,
            "Magic Flatulence": 50,
        }
        
    def select_random_attack(self):
        attack = random.choice(list(self.attacks.keys()))
        damage = self.attacks[attack]
        return attack, damage

    def regenerate(self):
        if self.health < self.max_health:
            self.health += random.randint(5, 16)
            print(f"{self.name} regenerates health! Current health: {int(self.health)}")

def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer") 
    print("4. Paladin")
    print("5. Technician")  

    class_choice = input("Enter the number of your class choice: ")
    name = input("Enter your character's name: ")

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Archer(name)
    elif class_choice == '4':
        return Paladin(name)
    elif class_choice == '5':
        return Technician(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)

def battle(player, wizard):
    while wizard.health > 0.0 and player.health > 0.0:
        player.apply_effects()
        wizard.apply_effects()
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Heal")
        print("4. View Stats")
        print(f"Current Health: {int(player.health)}")
        choice = counted_input.input("Choose an action: ")

        if choice == '1':
            player.attack(wizard)
        elif choice == '2':
            player.special(wizard)
        elif choice == '3':
            player.heal()
        elif choice == '4':
            player.display_stats()
        else:
            print("Did you really just give up a turn?")
        
        if wizard.health > 0:
            wizard.regenerate()
            attack, damage = wizard.select_random_attack()
            player.health -= damage
            print(f"{wizard.name} used {attack}! It dealt {damage} damage.")

        if player.health <= 0:
            print(f"{player.name} has been defeated in {counted_input.counter} turns!")
            break

    if wizard.health <= 0.0:
        print(f"{wizard.name} has been defeated by {player.name} in {counted_input.counter} turns with {player.health} health remaining!")

def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)

if __name__ == "__main__":
    main()
    
    
    