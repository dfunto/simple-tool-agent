import sys
import signal
from agent import Agent
from logs import init_logger


def main():
    agent = Agent()
    agent.run()


def signal_handler(_sig, _frame):
    print("\nGoodbye!")
    sys.exit(0)


if __name__ == "__main__":
    init_logger()
    signal.signal(signal.SIGINT, signal_handler)
    main()
