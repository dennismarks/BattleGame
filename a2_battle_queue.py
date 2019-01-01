"""
The BattleQueue classes for A2.

A BattleQueue is a queue that lets our game know in what order various
characters are going to attack.

BattleQueue has been completed for you, and the class header for
RestrictedBattleQueue has been provided. You must implement
RestrictedBattleQueue and document it accordingly.
"""
from typing import Union, List


class BattleQueue:
    """
    A class representing a BattleQueue.
    """

    def __init__(self) -> None:
        """
        Initialize this BattleQueue.

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._content = []
        self._p1 = None
        self._p2 = None

    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq.is_empty()
        False
        """
        while self._content and self._content[0].get_available_actions() == []:
            self._content.pop(0)

    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_empty()
        False
        """
        self._content.append(character)

        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content.pop(0)

    def is_empty(self) -> bool:
        """
        Return whether this BattleQueue is empty (i.e. has no players or
        has no players that can perform any actions).

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content == []

    def peek(self) -> 'Character':
        """
        Return the character at the front of this BattleQueue but does not
        remove them.

        If this BattleQueue is empty, returns the first player who was added
        to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.peek()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        False
        """
        self._clean_queue()

        if self._content:
            return self._content[0]

        return self._p1

    def is_over(self) -> bool:
        """
        Return whether the game being carried out in this BattleQueue is over
        or not.

        A game is considered over if:
            - Both players have no skills that they can use.
            - One player has 0 HP
            or
            - The BattleQueue is empty.

        >>> bq = BattleQueue()
        >>> bq.is_over()
        True

        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_over()
        False
        """
        if self.is_empty():
            return True

        if self._p1.get_hp() == 0 or self._p2.get_hp() == 0:
            return True

        return False

    def get_winner(self) -> Union['Character', None]:
        """
        Return the winner of the game being carried out in this BattleQueue
        if the game is over. Otherwise, return None.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.get_winner()
        """
        if not self.is_over():
            return None

        if self._p1.get_hp() == 0:
            return self._p2
        elif self._p2.get_hp() == 0:
            return self._p1

        return None

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> new_bq = bq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_battle_queue = BattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_battle_queue.add(p1_copy)
        if not new_battle_queue.is_empty():
            new_battle_queue.remove()

        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)

        return new_battle_queue

    def __repr__(self) -> str:
        """
        Return a representation of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        return " -> ".join([repr(character) for character in self._content])


class RestrictedBattleQueue(BattleQueue):
    """
    A class representing a RestrictedBattleQueue.

    able_to_add - a list with information whther a character is able to add
                  himself or its enemy to a RestrictedBattleQueue

    Rules for a RestrictedBattleQueue:
    - The first time each character is added to the RestrictedBattleQueue,
      they're able to add.

    For the below, you may assume that the character at the front of the
    RestrictedBattleQueue is the one adding:
    - Characters that are added to the RestrictedBattleQueue by a character
      other than themselves cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> B
      Able to add:     Y    Y

      Then if A tried to add B to the RestrictedBattleQueue, it would look like:
      Character order: A -> B -> B
      Able to add:     Y    Y    N
    - Characters that have 2 copies of themselves in the RestrictedBattleQueue
      already that can add cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> A -> B
      Able to add:     Y    Y    Y

      Then if A tried to add themselves in, the RestrictedBattleQueue would
      look like:
      Character order: A -> A -> B -> A
      Able to add:     Y    Y    Y    N

      If we removed from the RestrictedBattleQueue and tried to add A in again,
      then it would look like:
      Character order: A -> B -> A -> A
      Able to add:     Y    Y    N    Y
    """
    able_to_add: List[bool]

    def __init__(self) -> None:
        """
        Initialize this RestrictedBattleQueue

        Extends the super

        >>> bq = RestrictedBattleQueue()
        >>> bq.is_empty()
        True
        >>> from a2_characters import Vampire, Sorcerer
        >>> from a2_playstyle import ManualPlaystyle
        >>> s = Sorcerer("S", bq, ManualPlaystyle(bq))
        >>> v = Vampire("V", bq, ManualPlaystyle(bq))
        >>> s.enemy = v
        >>> v.enemy = s
        >>> bq.add(v)
        >>> bq.add(s)
        >>> s.special_attack()
        >>> bq
        S (Sorcerer): 100/80 -> V (Vampire): 78/100 -> S (Sorcerer): 100/80
        >>> bq.able_to_add
        [True, True, True]
        >>> bq.add(s)
        >>> bq.able_to_add
        [True, True, True, False]
        >>> bq.remove()
        S (Sorcerer): 100/80
        >>> bq
        V (Vampire): 78/100 -> S (Sorcerer): 100/80 -> S (Sorcerer): 100/80
        >>> v.attack()
        >>> bq
        V (Vampire): 88/85 -> S (Sorcerer): 90/80 -> S (Sorcerer): 90/80 -> V (Vampire): 88/85
        >>> bq.able_to_add
        [True, True, False, True]
        """
        super().__init__()
        self.able_to_add = []

    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.

        Overrides the super

        >>> bq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq
        Sophia (Rogue): 100/100
        >>> bq.able_to_add
        [True]
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        >>> bq
        <BLANKLINE>
        >>> bq.able_to_add
        []
        """
        while self._content and self._content[0].get_available_actions() == []:
            self._content.pop(0)
            self.able_to_add.pop(0)

    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.

        Overrides the super

        >>> bq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue, Mage
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Mage("Alex", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq.add(c)
        >>> bq
        Sophia (Rogue): 100/100 -> Sophia (Rogue): 100/100 -> Alex (Mage): 100/100 -> Sophia (Rogue): 100/100
        >>> bq.able_to_add
        [True, True, True, False]
        >>> bq._content.pop(0)
        Sophia (Rogue): 100/100
        >>> bq.able_to_add.pop(0)
        True
        >>> bq
        Sophia (Rogue): 100/100 -> Alex (Mage): 100/100 -> Sophia (Rogue): 100/100
        >>> bq.able_to_add
        [True, True, False]
        >>> bq.add(c)
        >>> bq.add(c)
        >>> bq.able_to_add
        [True, True, False, True, False]
        """
        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

        # first time adding
        # if len(self.able_to_add) <= 1 and character not in self._content:
        if character not in self._content:
            self._content.append(character)
            self.able_to_add.append(True)
            return

        # character can't add
        if not self.able_to_add[0]:
            return

        # caster adding the enemy -- enemy will not be able to add
        if self._content[0] != character and self.able_to_add[0]:
            self._content.append(character)
            self.able_to_add.append(False)
            return

        # if count character is 2 and they can both add the next one can't
        if self._content[0] == character and self.able_to_add[0]:
            counter = 0
            for i in range(len(self._content)):
                if self._content[i] == character \
                        and self.able_to_add[i] is True:
                    counter += 1
            self._content.append(character)
            if counter < 2:
                self.able_to_add.append(True)
            else:
                self.able_to_add.append(False)
            return

    def get_winner(self) -> Union['Character', None]:
        """
        Return the winner of the game being carried out in this BattleQueue
        if the game is over. Otherwise, return None.

        Overrides the super

        >>> bq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.get_winner()
        """
        i_hp = 0
        i_sp = 0
        return_char = None
        if self._content == []:
            return None
        if not self.is_over():
            return None

        if self.is_over():
            for character in self._content:
                if character.get_hp() != 0:
                    return_char = character

        for character in self._content:
            # two players have 0 hp case
            if character.get_hp() == 0:
                i_hp += 1
            # two players have 0 sp case
            if character.get_available_actions() == []:
                i_sp += 1
        if i_hp == len(self._content):
            if return_char is not None:
                return return_char
            return None
        if i_sp == len(self._content):
            if return_char is not None:
                return return_char
            return None

        if return_char is not None:
            return return_char
        return None

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        Overrides the super

        >>> bq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq
        Sophia (Rogue): 100/100
        >>> bq.able_to_add
        [True]
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        >>> bq
        <BLANKLINE>
        >>> bq.able_to_add
        []
        """
        self._clean_queue()
        self.able_to_add.pop(0)
        return self._content.pop(0)

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        Overrides the super

        >>> bq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> new_bq = bq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_battle_queue = RestrictedBattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        able_to_add_copy = []
        for el in self.able_to_add:
            able_to_add_copy.append(el)

        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)
        new_battle_queue.able_to_add = able_to_add_copy

        return new_battle_queue


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
