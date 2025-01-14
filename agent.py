from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)

    def manage_targets(self):
       #Prioriza ou seleciona o próximo alvo
        if len(self.targets) == 0:
            return None
        return self.targets[0]

    def navigate_to_target(self, target):
        #Navega até o alvo especificado
        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, target)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

    def decision(self):
        target = self.manage_targets()
        if not target:
            return

        self.navigate_to_target(target)

    def post_decision(self):
        pass
