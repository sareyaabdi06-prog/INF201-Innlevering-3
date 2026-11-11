
#DELIVERABLE 3 - INF201

import random
import time

#TASK 1 CHARACTER

class Character:
    """Represents a character in the RPG."""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon=None
    ) -> None:
        """Initialize a character with HP, damage and an optional weapon."""
        self.name = name
        self._hp = hp_max
        self.hp_max = hp_max
        self.damage = damage
        self.weapon = weapon

    def take_damage(self, amount: int) -> None:
        """Reduce the character's HP when taking damage."""
        self._hp = max(0, self._hp - amount)

    def heal(self, amount: int) -> None:
        """Heal the character without exceeding maximum HP."""
        self._hp = min(self.hp_max, self._hp + amount)

    def attack(self, target) -> None:
        """Attack with a weapon if equipped, otherwise use base damage."""
        if self.weapon is not None:
            damage = self.weapon.roll_damage()
        else:
            damage = self.damage

        target.take_damage(damage)

    def introduce(self) -> None:
        """Introduce the character."""
        print(f"Hi, my name is {self.name}!")

    def __repr__(self) -> str:
        """Representation of character object."""
        return f"<Character name={self.name} hp={self.hp} damage={self.damage}>"

    def __str__(self) -> str:
        """String representation of character object."""
        return f"Character: {self.name} with {self.hp} HP and {self.damage} damage"

    @property
    def hp(self) -> int:
        """Public read-only property to inspect HP."""
        return self._hp

    @property
    def is_alive(self) -> bool:
        """Return True if the character is alive."""
        return self._hp > 0

#TASK 2 DICE

import random

class Dice:

  """A class representing a customizable die for the RPG game simulator."""

  def __init__(self, sides: int = 6) -> None:
    """Initializes a die with at least 2 sides."""
    
    if sides < 2:
        raise ValueError("A die must have at least 2 sides.")
    self.sides = sides

  def roll(self) -> int:

    """Rolls the die and returns a random integer between 1 and the number of sides."""

    return random.randint(1, self.sides)

  def __repr__(self) -> str:

    """Returns a string representation of the Dice object."""

    return f"Dice(sides={self.sides})"

  def __call__(self) -> int:

    """Allows the dice instance to be called directly like a function to roll it."""



#Task 3 Weapon

class Weapon:
  """A class representing a weapon that uses a Dice object for damage calculation."""

  def __init__(self, name: str, damage_dice: Dice) -> None:

    """Initializes a weapon with a name and a damage-dealing Dice object."""

    self.name = name

    self.damage_dice = damage_dice

  def roll_damage(self) -> int:

    """Rolls the weapon's damage dice and returns the resulting damage."""

    return self.damage_dice.roll()

  def __repr__(self) -> str:

    """Returns a string representation of the Weapon object."""

    return f"Weapon(name='{self.name}', damage_dice={self.damage_dice})"


#Task 4
from typing import Optional


class Warrior(Character):
    """A defensive specialist with armor protection."""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        armor: int = 5,
        weapon: Optional[Weapon] = None
    ) -> None:
        """Initialize a warrior with armor and an optional weapon."""

        super().__init__(name=name, hp_max=hp_max)
        self.armor = armor
        self.weapon = weapon

    def take_damage(self, amount: int) -> None:
        """Reduce incoming damage by armor before applying it to HP."""

        actual_damage = max(0, amount - self.armor)
        super().take_damage(actual_damage)


class Mage(Character):
    """A magic attacker that uses mana to cast spells."""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        mana: int = 30,
        mana_max: int = 30,
        weapon: Optional[Weapon] = None
    ) -> None:
        """Initialize a mage with mana and an optional weapon."""

        super().__init__(name=name, hp_max=hp_max)

        self.weapon = weapon
        self.mana_max = mana_max
        self.mana = min(max(0, mana), self.mana_max)

    def attack(self, target: Character) -> None:
        """Use magic if enough mana is available, otherwise attack normally."""

        if self.mana >= 10:
            self.mana -= 10

            # Magic deals double base damage without using a weapon
            magic_damage = self.damage * 2
            target.take_damage(magic_damage)

            print(f"{self.name} casts a spell for {magic_damage} damage!")

        else:
            # Normal attack uses a weapon if equipped
            if self.weapon is not None:
                damage = self.weapon.roll_damage()
                target.take_damage(damage)
            else:
                super().attack(target)

            # Restore 5 mana without exceeding maximum mana
            self.mana = min(self.mana_max, self.mana + 5)

            print(f"{self.name} uses a normal attack and recovers 5 mana.")


#TASK 5

class Battle:
    """A class to manage turn-based combat between two Character objects."""

    def __init__(self, hero: Character, enemy: Character) -> None:
        """Initialize the battle with a hero and an enemy."""
        self.hero = hero
        self.enemy = enemy

    def play_round(self) -> None:
        """Play one round where the hero attacks first."""

        if self.hero.is_alive and self.enemy.is_alive:
            print(f"\n--- {self.hero.name}'s turn ---")
            self.hero.attack(self.enemy)

        # Enemy attacks only if still alive
        if self.enemy.is_alive and self.hero.is_alive:
            print(f"\n--- {self.enemy.name}'s turn ---")
            self.enemy.attack(self.hero)

        # Display HP after the round
        print(
            f"Status -> {self.hero.name}: {self.hero.hp} HP | "
            f"{self.enemy.name}: {self.enemy.hp} HP"
        )

    def simulate_battle(self) -> Character:
        """Simulate rounds until one character dies and return the winner."""

        print(
            f"=== BATTLE START: {self.hero.name} vs {self.enemy.name} ==="
        )

        # Continue until one character dies
        while self.hero.is_alive and self.enemy.is_alive:
            self.play_round()
            time.sleep(0.5)

        print("\n=== BATTLE OVER ===")

        if self.hero.is_alive:
            print(f"{self.hero.name} wins the battle!")
            return self.hero
        else:
            print(f"{self.enemy.name} wins the battle!")
            return self.enemy


