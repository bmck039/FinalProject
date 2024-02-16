# Intro
This represents the card game Spades, implemented in such a way as to make other games straightforward to create as well. [util.py](/util.py) contains the Game class, a Rules interface that controls how the game is played, a representation of Cards, and an interface for a Player. For convenience, a basePlayer class is provided for handling basic tasks involved with player creation. An explanation of the rules is [here](https://www.thesprucecrafts.com/spades-complete-card-game-rules-412490).

### Run using the command
```
python play.py
```

## Resources: 
Bidding Algorithm: https://ecai2020.eu/papers/235_paper.pdf

## ToDo
- [ ] Complete Bidding Algorithm in [players.py](/players.py)
- [ ] Implement AIPlayer.play(state) in [players.py](/players.py)
- [x] Make Spades object track points [util.py](/util.py)
- [x] create isWon(state) method on Rules interface and implement in Spades object [util.py](/util.py)
- [x] Allow Game to run turns until a win state in [util.py](/util.py), have [play.py](/play.py) use this method
- [x] Force the player to replay if their original move is not valid