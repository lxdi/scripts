import os

class Tab():
    def __init__(self):
        self.history = []
        self.cwd = os.getcwd()
