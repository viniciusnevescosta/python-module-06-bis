from ex3 import TransformCreatureFactory


def main() -> None:
    factory = TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing Creature with transform capability")
    print(" base:")
    print(base.describe())
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())
    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


if __name__ == "__main__":
    main()
