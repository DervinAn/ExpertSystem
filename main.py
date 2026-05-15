from expert_system.engine import LaptopExpertSystem
from expert_system.domain import DEMO_CASES


def run_interactive() -> None:
    system = LaptopExpertSystem()
    system.run_interactive()


def run_demo() -> None:
    system = LaptopExpertSystem()
    system.run_demo(DEMO_CASES)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Laptop Recommendation Expert System")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run two predefined tests that are useful for screenshots and PDF submission.",
    )
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
