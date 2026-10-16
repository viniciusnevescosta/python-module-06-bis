from ex3 import TransformCreatureFactory


def main() -> None:
    factory = TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing Creature with transform capability")
    for label, creature in (("base", base), ("evolved", evolved)):
        print(f" {label}:")
        print(creature.describe())
        print(creature.attack())
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


if __name__ == "__main__":
    main()
