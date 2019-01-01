"""
The SkillDecisionTree class for A2.

You are to implement the pick_skill() method in SkillDecisionTree, as well as
implement create_default_tree() such that it returns the example tree used in
a2.pdf.

This tree will be used during the gameplay of a2_game, but we may test your
SkillDecisionTree with other examples.
"""
from typing import Callable, List
from a2_skills import MageAttack, MageSpecial, RogueAttack, RogueSpecial


class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.

    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']

    def __init__(self, value: 'Skill',
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None):
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition  # self.comndition(caster, target)
        self.priority = priority
        self.children = children[:] if children else []

    # Implement a method called pick_skill which takes in a caster and target
    # and returns a skill.

    def find_skill_by_priority(self, priority_num: int) -> 'Skill':
        """
        Return a skill with a given pririty number priority_num.

        >>> t = create_default_tree()
        >>> t.find_skill_by_priority(1)[0].__class__.__name__
        'RogueAttack'
        >>> t.find_skill_by_priority(2)[0].__class__.__name__
        'MageSpecial'
        >>> t.find_skill_by_priority(3)[0].__class__.__name__
        'MageAttack'
        """
        if self.priority == priority_num:
            return [self.value]
        return sum([c.find_skill_by_priority(priority_num)
                    for c in self.children], [])

    def get_priorities(self, caster: 'Character', target: 'Character') \
            -> List[int]:
        """
        Return a list of priority numbers corresponding to caster's hp and sp,
        and target's hp and sp.

        >>> t = create_default_tree()
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_characters import Vampire
        >>> bq = BattleQueue()
        >>> c = Vampire("r", bq, ManualPlaystyle(bq))
        >>> c2 = Vampire("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c._hp = 50
        >>> c._sp = 50
        >>> c2._hp = 50
        >>> c2._sp = 50
        >>> t.get_priorities(c, c2)
        [5]
        >>> c._hp = 55
        >>> t.get_priorities(c, c2)
        [4, 8, 1]
        >>> c2._hp = 20
        >>> t.get_priorities(c, c2)
        [6, 8, 1]
        >>> c._sp = 20
        >>> t.get_priorities(c, c2)
        [3, 8, 1]
        >>> c2._sp = 40
        >>> t.get_priorities(c, c2)
        [3, 2, 1]
        >>> c._hp = 92
        >>> t.get_priorities(c, c2)
        [3, 2, 7]
        """
        if self.children == []:
            return [self.priority]
        else:
            if self.condition(caster, target):
                return sum([c.get_priorities(caster, target)
                            for c in self.children], [])
            return [self.priority]

    def pick_skill(self, caster: 'Character', target: 'Character') -> 'Skill':
        """
        Return a skill corresponding to caster's hp and sp,
        and target's hp and sp.

        >>> t = create_default_tree()
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_characters import Vampire
        >>> bq = BattleQueue()
        >>> c = Vampire("r", bq, ManualPlaystyle(bq))
        >>> c2 = Vampire("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c._hp = 50
        >>> c._sp = 50
        >>> c2._hp = 50
        >>> c2._sp = 50
        >>> t.pick_skill(c, c2).__class__.__name__
        'MageAttack'
        >>> c._hp = 91
        >>> t.pick_skill(c, c2).__class__.__name__
        'RogueSpecial'
        >>> c2._sp = 40
        >>> t.pick_skill(c, c2).__class__.__name__
        'MageSpecial'
        >>> c._hp = 49
        >>> t.pick_skill(c, c2).__class__.__name__
        'MageAttack'
        """
        priority = min(self.get_priorities(caster, target))
        skill = self.find_skill_by_priority(priority)
        return skill[0]


def create_default_tree() -> SkillDecisionTree:
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.

    >>> t = create_default_tree()
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Vampire
    >>> type(t.value) == MageAttack
    True
    >>> t.condition.__name__
    'f6'
    >>> t.priority
    5
    >>> type(t.children[1].value) == MageSpecial
    True
    >>> t.children[1].condition.__name__
    'f4'
    >>> t.children[1].priority
    2
    >>> bq = BattleQueue()
    >>> c = Vampire("r", bq, ManualPlaystyle(bq))
    >>> c2 = Vampire("r2", bq, ManualPlaystyle(bq))
    >>> c.enemy = c2
    >>> c2.enemy = c
    >>> c2._sp = 39
    >>> t.pick_skill(c, c2).__class__.__name__
    'MageSpecial'
    """
    def f1(caster, _) -> bool:
        """ Return whether caster's sp > 20 """
        return caster.get_sp() > 20

    def f2(_, target) -> bool:
        """ Return whether target's hp < 30 """
        return target.get_hp() < 30

    def f4(_, target) -> bool:
        """ Return whether target's sp > 40 """
        return target.get_sp() > 40

    def f5(caster, _) -> bool:
        """ Return whether caster's hp > 90 """
        return caster.get_hp() > 90

    def f6(caster, _) -> bool:
        """ Return whether caster's hp > 50 """
        return caster.get_hp() > 50

    def f_leaf(_, __) -> bool:
        """ Return True """
        return True

    t1 = SkillDecisionTree(MageAttack(), f1, 3,
                           [SkillDecisionTree(RogueSpecial(), f2, 4,
                                              [SkillDecisionTree(RogueAttack(),
                                                                 f_leaf, 6)])])
    t2 = SkillDecisionTree(MageSpecial(), f4, 2,
                           [SkillDecisionTree(RogueAttack(), f_leaf, 8)])
    t3 = SkillDecisionTree(RogueAttack(), f5, 1,
                           [SkillDecisionTree(RogueSpecial(), f_leaf, 7)])
    t = SkillDecisionTree(MageAttack(), f6, 5, [t1, t2, t3])
    return t


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
