import sys
import signal
from agent import Agent


def main():
    agent = Agent()
    while True:
        print("How can I help you today? (Hit CTRL + C to exit)")
        prompt = input()
        agent.run(prompt=prompt)


def signal_handler(_sig, _frame):
    print("\nGoodbye!")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
