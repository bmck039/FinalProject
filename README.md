# Intro
This represents the card game Spades, implemented in such a way as to make other games straightforward to create as well. [util.py](/util.py) contains the Game class, a Rules interface that controls how the game is played, a representation of Cards, and an interface for a Player. For convenience, a basePlayer class is provided for handling basic tasks involved with player creation. An explanation of the rules of Spades can be found [here](https://www.thesprucecrafts.com/spades-complete-card-game-rules-412490).

### Setup
* #### Macos or Windows (without Nvidia GPU):
```
python -m pip install numpy torch stable-baselines3 gymnasium
```
* #### Windows (With Nvidia GPU):
```
python -m pip install numpy torch stable-baselines3 gymnasium --index-url https://download.pytorch.org/whl/cu121
```

### Run
```
python play.py
```

## Resources: 
- Bidding Algorithm: https://ecai2020.eu/papers/235_paper.pdf
- Monte Carlo Tree Search: https://ai-boson.github.io/mcts/
- Reinforcement Learning on Spades: https://cs229.stanford.edu/proj2021spr/report2/81999416.pdf
- SIMPLE Reinforcement learning library: https://github.com/davidADSP/SIMPLE

## ToDo
- [ ] Complete Bidding Algorithm (AIPlayer.getBid(state)) in [players.py](/players.py)
- [ ] Implement AIPlayer.play(state) in [players.py](/players.py)
  - [ ] Implement bidding nil
  - [x] Implement regular bidding
- [ ] ~~expectiminimax player agent~~
- [x] MCTS player agent
- [ ] RL player agent
- [x] Tournament of different agents
  - [x] save results to CSV file for further analysis
- [x] Make Spades object track points [util.py](/util.py)
- [x] create isWon(state) method on Rules interface and implement in Spades object [util.py](/util.py)
- [x] Allow Game to run turns until a win state in [util.py](/util.py), have [play.py](/play.py) use this method
- [x] Force the player to replay if their original move is not valid
- [x] Generate graphs