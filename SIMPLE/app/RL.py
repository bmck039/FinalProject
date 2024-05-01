from utils.files import load_model, write_results

from utils.register import get_environment

from utils.agents import Agent



from util import Card

from util import Suit

from players import PlayingClass

# import util



from spadesEnv import getCardFromIndex

# from stable_baselines import logger

# import config

# logger.configure(config.LOGDIR)
# logger.set_level(config.DEBUG)


env_name = "spades"



env = get_environment(env_name)()



ppo_model = load_model(env, 'best_model.zip')



# ppo_model = load_model(env, 'base.zip')

ppo_agent = Agent('best_model', ppo_model)


class RLPlay(PlayingClass):



    def play(rules, hand, state)        :

        env.reset()

        env.setState(state, hand)

        action = ppo_agent.choose_action(env, choose_best_action = True, mask_invalid_actions = True)

        card = getCardFromIndex(action)

        return card



