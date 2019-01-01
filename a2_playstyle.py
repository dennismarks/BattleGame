"""
The Playstyle classes for A2.
Docstring examples are not required for Playstyles.

You are responsible for implementing the get_state_score function, as well as
creating classes for both Iterative Minimax and Recursive Minimax.
"""
import random
from typing import Any, Union, List
from adts import Stack


class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        raise NotImplementedError


class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)


class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)


def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> print(bq)
    m (Mage): 3/100 -> r (Rogue): 40/100
    >>> get_state_score(bq)
    -10
    >>> bq._content = []
    >>> bq.add(r)
    >>> bq.add(m)
    >>> r.set_hp(100)
    >>> r.set_sp(12)
    >>> m.set_hp(28)
    >>> m.set_sp(100)
    >>> get_state_score(bq)
    40
    >>> bq._content = []
    >>> bq.add(m)
    >>> bq.add(r)
    >>> r.set_hp(50)
    >>> r.set_sp(100)
    >>> m.set_hp(50)
    >>> m.set_sp(100)
    >>> get_state_score(bq)
    26
    """
    bq_c = battle_queue.copy()
    first_player = bq_c.peek()
    curr_p = bq_c.peek()
    list_ = []
    if bq_c.is_over():
        if bq_c.get_winner() is None:
            return 0
        if bq_c.get_winner() == first_player:
            return bq_c.get_winner().get_hp()
        elif bq_c.get_winner() != first_player:
            return bq_c.get_winner().get_hp() * -1
    else:
        if len(curr_p.get_available_actions()) == 2:
            bq_1, bq_2 = bq_c.copy(), bq_c.copy()
            cur_1, cur_2 = bq_1.peek(), bq_2.peek()
            bq_1.remove().attack()
            bq_2.remove().special_attack()
            next_1, next_2 = bq_1.peek(), bq_2.peek()
            if cur_1 == next_1:
                list_.append(get_state_score(bq_1))
            else:
                list_.append(get_state_score(bq_1) * -1)
            if cur_2 == next_2:
                list_.append(get_state_score(bq_2))
            else:
                list_.append(get_state_score(bq_2) * -1)
        elif len(curr_p.get_available_actions()) == 1:
            cur = bq_c.peek()
            bq_c.remove().attack()
            next_ = bq_c.peek()
            if cur == next_:
                list_.append(get_state_score(bq_c))
            else:
                list_.append(get_state_score(bq_c) * -1)
    return max(list_)


class RecursiveMinimax(Playstyle):
    """
    The RecursiveMinimax superclass. Inherits from Playstyle
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RecursiveMinimax with BattleQueue as its battle queue.

        Extends the super
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this RecursiveMinimax's
        battle_queue to perform.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, RecursiveMinimax(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(m)
        >>> bq.add(r)
        >>> r.set_hp(40)
        >>> r.set_sp(6)
        >>> m.set_hp(14)
        >>> m.set_sp(35)
        >>> RecursiveMinimax(bq).select_attack()
        'A'
        >>> bq._content = []
        >>> bq.add(r)
        >>> bq.add(m)
        >>> r.set_hp(100)
        >>> r.set_sp(12)
        >>> m.set_hp(28)
        >>> m.set_sp(100)
        >>> RecursiveMinimax(bq).select_attack()
        'A'
        >>> bq._content = []
        >>> bq.add(m)
        >>> bq.add(r)
        >>> r.set_hp(30)
        >>> r.set_sp(100)
        >>> m.set_hp(5)
        >>> m.set_sp(30)
        >>> print(bq)
        m (Mage): 5/30 -> r (Rogue): 30/100
        >>> RecursiveMinimax(bq).select_attack()
        'S'
        """
        bq_a = self.battle_queue.copy()
        bq_s = self.battle_queue.copy()
        char = self.battle_queue.peek()
        moves = char.get_available_actions()
        d = {}
        if 'A' in moves:
            char = bq_a.peek()
            bq_a.remove().attack()
            new_char = bq_a.peek()
            score = get_state_score(bq_a)
            if char == new_char:
                d[score] = 'A'
            else:
                d[score * -1] = 'A'
        if 'S' in moves:
            char = bq_s.peek()
            bq_s.remove().special_attack()
            new_char = bq_s.peek()
            score = get_state_score(bq_s)
            if char == new_char:
                d[score] = 'S'
            else:
                d[score * -1] = 'S'
        if d == {}:
            return ''
        max_score = max(d.keys())
        return d[max_score]

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RecursiveMinimax which uses the BattleQueue
        new_battle_queue.
        """
        return RecursiveMinimax(new_battle_queue)


class StateTree:
    """
    A class representing a StateTree

    bq - the BattleQueue that this StateTree will use
    children - the children that this StateTree will have
    score - the score that this StateTree will have
    need_to_mult - an atribute containing a boolean whether a state needs to
                   be multiplied by * -1
    """
    bq: 'BattleQueue'
    children: Union[None, List['StateTree']]
    score: Union[None, int]
    need_to_mult: bool

    def __init__(self, bq: 'BattleQueue') -> None:
        """
        Initialize this StateTree with the battle_queue bq.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, RecursiveMinimax(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(m)
        >>> bq.add(r)
        >>> r.set_hp(40)
        >>> state = StateTree(bq)
        >>> state.bq
        m (Mage): 100/100 -> r (Rogue): 40/100
        >>> print(state.children)
        None
        >>> state.bq.is_over()
        False
        """
        self.bq = bq
        self.children = None
        self.score = None
        self.need_to_mult = False


def get_state_score_iterative(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score_iterative(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score_iterative(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> bq
    m (Mage): 3/100 -> r (Rogue): 40/100
    >>> get_state_score_iterative(bq)
    -10
    >>> bq._content = []
    >>> bq.add(r)
    >>> bq.add(m)
    >>> r.set_hp(100)
    >>> r.set_sp(12)
    >>> m.set_hp(28)
    >>> m.set_sp(100)
    >>> get_state_score_iterative(bq)
    40
    >>> bq._content = []
    >>> bq.add(r)
    >>> bq.add(m)
    >>> r.set_hp(30)
    >>> r.set_sp(100)
    >>> m.set_hp(5)
    >>> m.set_sp(30)
    >>> get_state_score_iterative(bq)
    30
    >>> bq._content = []
    >>> bq.add(m)
    >>> bq.add(r)
    >>> r.set_hp(50)
    >>> r.set_sp(100)
    >>> m.set_hp(50)
    >>> m.set_sp(100)
    >>> get_state_score_iterative(bq)
    26
    """
    bq_c = battle_queue.copy()
    first_state = StateTree(bq_c)
    s = Stack()
    s.add(first_state)
    list_ = []
    while not s.is_empty():
        state = s.remove()
        first_player = state.bq.peek()
        if state.bq.is_over():
            if state.bq.get_winner() is None:
                state.score = 0
            elif state.bq.get_winner() == first_player:
                state.score = state.bq.get_winner().get_hp()
            elif state.bq.get_winner() != first_player:
                state.score = state.bq.get_winner().get_hp() * -1
        else:
            if state.children is None:
                moves = first_player.get_available_actions()
                if 'A' in moves:
                    bq_a = state.bq.copy()
                    cur = bq_a.peek()
                    bq_a.remove().attack()
                    next_ = bq_a.peek()
                    attack_state = StateTree(bq_a)
                    if cur != next_:
                        attack_state.need_to_mult = True
                    if state.children is None:
                        state.children = [attack_state]
                    else:
                        state.children.append(attack_state)
                if 'S' in moves:
                    bq_s = state.bq.copy()
                    cur = bq_s.peek()
                    bq_s.remove().special_attack()
                    next_ = bq_s.peek()
                    special_state = StateTree(bq_s)
                    if cur != next_:
                        special_state.need_to_mult = True
                    if state.children is None:
                        state.children = [special_state]
                    else:
                        state.children.append(special_state)
                s.add(state)
                for child in state.children:
                    s.add(child)
            elif state.children is not None:
                child_scores = []
                for child in state.children:
                    if child.need_to_mult and child.score is not None:
                        child_scores.append(child.score * -1)
                    else:
                        child_scores.append(child.score)
                state.score = max(child_scores)
                if state.need_to_mult:
                    list_.append(state.score * -1)
                else:
                    list_.append(state.score)
    return list_[-1]


class IterativeMinimax(Playstyle):
    """
    The IterativeMinimax superclass. Inherits from Playstyle
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this IterativeMinimax with BattleQueue as its battle queue.

        Extends the superclass
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this IterativeMinimax's
        battle_queue to perform.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(m)
        >>> bq.add(r)
        >>> r.set_hp(40)
        >>> r.set_sp(6)
        >>> m.set_hp(14)
        >>> m.set_sp(35)
        >>> IterativeMinimax(bq).select_attack()
        'A'
        >>> bq._content = []
        >>> bq.add(r)
        >>> bq.add(m)
        >>> r.set_hp(100)
        >>> r.set_sp(12)
        >>> m.set_hp(28)
        >>> m.set_sp(100)
        >>> bq
        r (Rogue): 100/12 -> m (Mage): 28/100
        >>> IterativeMinimax(bq).select_attack()
        'A'
        >>> bq._content = []
        >>> bq.add(m)
        >>> bq.add(r)
        >>> r.set_hp(30)
        >>> r.set_sp(100)
        >>> m.set_hp(5)
        >>> m.set_sp(30)
        >>> bq
        m (Mage): 5/30 -> r (Rogue): 30/100
        >>> IterativeMinimax(bq).select_attack()
        'S'
        """
        bq_a = self.battle_queue.copy()
        bq_s = self.battle_queue.copy()
        char = self.battle_queue.peek()
        moves = char.get_available_actions()
        d = {}
        if 'A' in moves:
            char = bq_a.peek()
            score_to_return = char.get_hp()
            bq_a.remove().attack()
            new_char = bq_a.peek()
            if bq_a.is_over():
                score = score_to_return
            else:
                score = get_state_score_iterative(bq_a)
            if char == new_char:
                d[score] = 'A'
            else:
                d[score * -1] = 'A'
        if 'S' in moves:
            char = bq_s.peek()
            score_to_return = char.get_hp()
            bq_s.remove().special_attack()
            new_char = bq_s.peek()
            if bq_s.is_over():
                score = score_to_return
            else:
                score = get_state_score_iterative(bq_s)
            if char == new_char:
                d[score] = 'S'
            else:
                d[score * -1] = 'S'
        max_score = max(d.keys())
        return d[max_score]

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this IterativeMinimax which uses the BattleQueue
        new_battle_queue.
        """
        return IterativeMinimax(new_battle_queue)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
