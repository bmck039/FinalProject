from gym.envs.registration import register

register(
    id='spades-v0',
    entry_point='spades.envs.spades:SpadesGym',
)
