class Agent:

    def __init__(self):
        self.done: bool = False

    def observe(self):
        print("Observing")

    def plan(self):
        print("Planning")

    def act(self):
        print("Acting")

    def reflect(self):
        print("Reflecting")

    def run(self, prompt: str):
        self.done = False
        while not self.done:
            self.observe()
            self.plan()
            self.act()
            self.reflect()
            self.done = True
