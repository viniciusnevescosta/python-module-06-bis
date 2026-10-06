from abc import ABC, abstractmethod

from ex3.capabilities import TransformCapability
from ex3.creatures import Creature


class StrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise StrategyError(f"Invalid Creature '{creature.name}'")
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, TransformCapability):
            raise StrategyError(
                f"Invalid Creature '{creature.name}' for this "
                "aggressive strategy"
            )
        return [creature.transform(), creature.attack(), creature.revert()]
