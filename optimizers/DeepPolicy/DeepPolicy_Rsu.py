from optimizers.optimizer import Optimizer
from behaviorPolicy.DeepPolicy.PG_policy_Rsu import PG_policy_rsu


class DeepPolicy_Rsu(Optimizer):

    def __init__(self, agent_name=None):
        super().__init__(agent_name)
        self.agent_name = agent_name
        self.policy = PG_policy_rsu().getPolicy()