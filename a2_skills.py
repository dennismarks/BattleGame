"""
The Skill classes for A2.

See a2_characters.py for how these are used.
For any skills you make, you're responsible for making sure their style adheres
to PythonTA and that you include all documentation for it.
"""


class Skill:
    """
    An abstract superclass for all Skills.
    """

    def __init__(self, cost: int, damage: int) -> None:
        """
        Initialize this Skill such that it costs cost SP and deals damage
        damage.
        """
        self._cost = cost
        self._damage = damage

    def get_sp_cost(self) -> int:
        """
        Return the SP cost of this Skill.
        """
        return self._cost

    def get_damage(self) -> int:
        """
        Return the damage of this SKill.
        """
        return self._damage

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.
        """
        raise NotImplementedError

    def _deal_damage(self, caster: 'Character', target: 'Character') -> None:
        """
        Reduces the SP of caster and inflicts damage on target.
        """
        caster.reduce_sp(self._cost)
        target.apply_damage(self._damage)


class NormalAttack(Skill):
    """
    A class representing a NormalAttack.
    Not to be instantiated.
    """

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(caster)


class MageAttack(NormalAttack):
    """
    A class representing a Mage's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this MageAttack.

        >>> m = MageAttack()
        >>> m.get_sp_cost()
        5
        """
        super().__init__(5, 20)


class MageSpecial(Skill):
    """
    A class representing a Mage's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this MageAttack.

        >>> m = MageSpecial()
        >>> m.get_sp_cost()
        30
        """
        super().__init__(30, 40)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Mage's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> m.special_attack()
        >>> m.get_sp()
        70
        >>> r.get_hp()
        70
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(target)
        caster.battle_queue.add(caster)


class RogueAttack(NormalAttack):
    """
    A class representing a Rogue's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this RogueAttack.

        >>> r = RogueAttack()
        >>> r.get_sp_cost()
        3
        """
        super().__init__(3, 15)


class RogueSpecial(Skill):
    """
    A class representing a Rogue's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this RogueSpecial.

        >>> r = RogueSpecial()
        >>> r.get_sp_cost()
        10
        """
        super().__init__(10, 20)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Rogue's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> r.special_attack()
        >>> r.get_sp()
        90
        >>> m.get_hp()
        88
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(caster)
        caster.battle_queue.add(caster)


class VampireAttack(NormalAttack):
    """
    A class representing a Vampire's Attack. Inherits from the NormallAttack.
    """

    def __init__(self) -> None:
        """
        Initialize this VampireAttack.

        Inherits from the Super

        >>> v = VampireAttack()
        >>> v.get_sp_cost()
        15
        """
        super().__init__(15, 20)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.

        Extends the Super()

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_characters import Vampire
        >>> bq = BattleQueue()
        >>> c = Vampire("r", bq, ManualPlaystyle(bq))
        >>> c2 = Vampire("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c.get_defense()
        3
        >>> c.get_hp()
        100
        >>> c2.get_hp()
        100
        >>> c.attack()
        >>> c.get_hp()
        117
        >>> c2.get_hp()
        83
        >>> c2._hp = 3
        >>> c.attack()
        >>> c.get_hp()
        120
        """
        orig_target_hp = target.get_hp()
        super().use(caster, target)
        if target.get_hp() == 0:
            new_hp = caster.get_hp() + orig_target_hp
        else:
            new_hp = caster.get_hp() + (self._damage - target.get_defense())
        caster.set_hp(new_hp)


class VampireSpecial(Skill):
    """
    A class representing a Vampire's Special Attack. Inherits from the SKill.
    """

    def __init__(self) -> None:
        """
        Initialize this VampireSpecial.

        Inherits from the Super

        >>> v = VampireSpecial()
        >>> v.get_sp_cost()
        20
        """
        super().__init__(20, 30)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Vampire's SpecialAttack on target.

        Overrides the super

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Vampire, Mage
        >>> bq = BattleQueue()
        >>> v = Vampire("r", bq, ManualPlaystyle(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> v.enemy = m
        >>> m.enemy = v
        >>> bq.add(v)
        >>> bq.add(m)
        >>> bq
        r (Vampire): 100/100 -> m (Mage): 100/100
        >>> v.special_attack()
        >>> v.get_sp()
        80
        >>> m.get_hp()
        78
        """
        orig_target_hp = target.get_hp()
        self._deal_damage(caster, target)
        if target.get_hp() == 0:
            new_hp = caster.get_hp() + orig_target_hp
        else:
            new_hp = caster.get_hp() + (self._damage - target.get_defense())
        caster.set_hp(new_hp)
        caster.battle_queue.add(caster)
        caster.battle_queue.add(caster)
        caster.battle_queue.add(target)


class SorcererAttack(NormalAttack):
    """
    A class representing a Sorcerer's Attack. Inherits from the NormalAttack
    """

    def __init__(self) -> None:
        """
        Initialize this SorcererAttzck.

        Inherits from the Super

        >>> s = SorcererAttack()
        >>> s.get_sp_cost()
        15
        """
        super().__init__(15, 0)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.

        Overrides the Super

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_characters import Sorcerer
        >>> from a2_skill_decision_tree import create_default_tree
        >>> t = create_default_tree()
        >>> bq = BattleQueue()
        >>> c = Sorcerer("r", bq, ManualPlaystyle(bq))
        >>> c2 = Sorcerer("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c.set_skill_decision_tree(t)
        >>> c.get_defense()
        10
        >>> c2.get_hp()
        100
        >>> c.get_sp()
        100
        >>> c.attack()
        >>> c.get_sp()
        85
        >>> c2.get_hp()
        90
        """
        skill_to_use = caster.tree.pick_skill(caster, target)
        caster.reduce_sp(self.get_sp_cost())
        target.apply_damage(skill_to_use.get_damage())
        caster.battle_queue.add(caster)


class SorcererSpecial(Skill):
    """
    A class representing a Sorcerer's Special Attack. Inherits from the Skill.
    """

    def __init__(self) -> None:
        """
        Initialize this SorcererSpecial.

        Inherits from the Super

        >>> s = SorcererSpecial()
        >>> s.get_sp_cost()
        20
        """
        super().__init__(20, 25)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Sorcerer's SpecialAttack on target.

        Overrides the Super

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Sorcerer, Rogue
        >>> bq = BattleQueue()
        >>> s = Sorcerer("s", bq, ManualPlaystyle(bq))
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> s.enemy = r
        >>> r.enemy = s
        >>> bq.add(s)
        >>> bq.add(r)
        >>> bq.add(r)
        >>> bq.add(s)
        >>> bq.add(r)
        >>> bq
        s (Sorcerer): 100/100 -> r (Rogue): 100/100 -> r (Rogue): 100/100 -> s (Sorcerer): 100/100 -> r (Rogue): 100/100
        >>> s.special_attack()
        >>> bq
        s (Sorcerer): 100/80 -> r (Rogue): 85/100 -> s (Sorcerer): 100/80
        >>> s.get_sp()
        80
        >>> r.get_hp()
        85
        """
        self._deal_damage(caster, target)
        while not caster.battle_queue.is_empty():
            caster.battle_queue.remove()
        caster.battle_queue.add(caster)
        caster.battle_queue.add(target)
        caster.battle_queue.add(caster)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
