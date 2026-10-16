from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    NormalStrategy,
    StrategyError,
)


Opponent = tuple[CreatureFactory, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for first_index in range(len(opponents)):
            for second_index in range(first_index + 1, len(opponents)):
                first_factory, first_strategy = opponents[first_index]
                second_factory, second_strategy = opponents[second_index]
                first = first_factory.create_base()
                second = second_factory.create_base()
                print("\n* Battle *")
                print(first.describe())
                print(" vs.")
                print(second.describe())
                print(" now fight!")
                for action in first_strategy.act(first):
                    print(action)
                for action in second_strategy.act(second):
                    print(action)
    except StrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def tournament(opponents: list[Opponent]) -> None:
    battle(opponents)


def main() -> None:
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Shiftling+Aggressive) ]")
    battle([
        (flame, NormalStrategy()),
        (transform, AggressiveStrategy()),
    ])
    print("\nTournament 1 (error)")
    print(" [ (Shiftling+Aggressive), (Flameling+Aggressive) ]")
    battle([
        (transform, AggressiveStrategy()),
        (flame, AggressiveStrategy()),
    ])


if __name__ == "__main__":
    main()
