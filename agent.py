from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)
        self.collision_distance = 0.25  # Distância mínima para troca de alvo, baseada no raio+0.02

    def is_too_close(self, teammate):
        #Verifica se o agente está muito próximo de outro agente
        distance = self.pos.dist_to(Point(teammate.x, teammate.y))
        return distance < self.collision_distance

    def manage_targets(self):
        if len(self.targets) == 0:
            return None
        """"
        # Verifica se há agentes próximos
        for teammate in self.teammates.values():
            if teammate.id != self.id and self.is_too_close(teammate):
                # Se estiver muito próximo, escolhe um alvo diferente
                alternative_targets = [t for t in self.targets if t != self.targets[0]]
                if alternative_targets:
                    return alternative_targets[0]
        
        return self.targets[0]
        """
        
         # Distribuição inteligente de alvos: evita múltiplos agentes no mesmo alvo
        target_scores = {}
        for target in self.targets:
            agents_near_target = sum(
                1 for teammate in self.teammates.values()
                if Point(teammate.x, teammate.y).dist_to(target) < self.pos.dist_to(target)
            )
            # Penaliza alvos com muitos agentes próximos
            target_scores[target] = self.pos.dist_to(target) + agents_near_target * 2.0

        # Escolhe o alvo com menor pontuação (distância + penalidade)
        best_target = min(target_scores, key=target_scores.get)
        return best_target
        
    def navigate_to_target(self, target):
        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, target)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

    def decision(self):
        target = self.manage_targets()
        if target:
            self.navigate_to_target(target)

    def post_decision(self):
        pass
