from singleton import singleton
from model import World
from view import View
from time import time, sleep

@singleton
class Controller:
    def __init__(self, sim_rate, fps):
        self.world = World(self, 1.0/sim_rate)
        self.view = View(sim_rate = sim_rate, fps = fps, sound = True)
        self.input_accept = ["human", "ai"]
        self.callbacks = []

    def mainloop(self):
        self.running = True
        while (self.running):
            self.view.handle_events(self, self.world)

    def input(self, player, action):
        if (player in self.input_accept):
            switch = {"shoot": self.world.get_spaceship().shoot,
                      "hyperspace": self.world.get_spaceship().hyperspace,
                      "accelerate": self.world.get_spaceship().accelerate,
                      "turn_left": (self.world.get_spaceship().turn, 1),
                      "turn_right": (self.world.get_spaceship().turn, -1)}
            try:
                if (type(switch[action])==tuple):
                    func = switch[action][0]
                    args = switch[action][1:]
                else:
                    func = switch[action]
                    args = []
                func(*args)
                return True
            except KeyError:
                return False
        else:
            return True

    def callback_model_step(self):
        for c in self.callbacks:
            c(self, self.world)
        self.world.collision_detection()
        self.world.integrate()

    def gameover(self, score):
        self.quit()

    def quit(self):
        self.running = False

if (__name__=="__main__"):
    controller = Controller(50, 25)
    
    try:
        controller.mainloop()
    except KeyboardInterrupt:
        pass
