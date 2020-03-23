import os

class Tab():
    def __init__(self):
        self.history = []
        self.cwd = os.getcwd()
        self.cursor = 0
        self.subcursor = -1

    def changeDir(self, newdir):
        self.history.append(self.cwd)
        self.cwd = newdir
        self.cursor = 0

    def popHistory(self):
        if len(self.history) > 0:
            self.cwd = self.history.pop()
            self.cursor = 0
