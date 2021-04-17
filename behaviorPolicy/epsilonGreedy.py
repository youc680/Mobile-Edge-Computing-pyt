from behaviorPolicy.policy import Policy
import numpy as np

class EpsilonGreedy(Policy):
    
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon

    def getPolicy(self):
        def chooseAction(values_of_all_actions, exclude_indexs=[]):
            n_actions = len(values_of_all_actions)
            prob_taking_best_action_only = 1 - self.epsilon
            prob_taking_any_random_action = self.epsilon / (n_actions - len(exclude_indexs))
            action_prob_vertor = [prob_taking_any_random_action] * n_actions
            min_values = np.min(values_of_all_actions)
            for i in exclude_indexs:
                action_prob_vertor[i] = 0
                values_of_all_actions[i] = min_values - 1
            exploitation_action_index = np.argmax(values_of_all_actions)
            action_prob_vertor[exploitation_action_index] += prob_taking_best_action_only
            chosen_action = np.random.choice(np.arange(n_actions), p=action_prob_vertor)
            return chosen_action
        return chooseAction

# if __name__ == "__main__":
#     policy = EpsilonGreedy(epsilon=0.5).getPolicy()
#     print(policy([1, 2, 2, 1], exclude_indexs=[0]))