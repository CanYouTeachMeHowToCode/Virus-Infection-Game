## Virus Infection Game 
from UI import UI

class Game(object):
    def __init__(self):
        self.GameUI = UI()

    def runVirusInfectionGame(self):
        self.GameUI.runGame(900, 900)

if __name__ == "__main__":
    Game().runVirusInfectionGame()