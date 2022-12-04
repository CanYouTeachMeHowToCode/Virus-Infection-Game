## Virus Infection Game 
from UI import UI

class Game(object):
    def __init__(self):
        self.GameUI = UI()

    def runVirusInfectionGame(self):
        self.GameUI.runGame(800, 800)

if __name__ == "__main__":
    Game().runVirusInfectionGame()