#!/bin/bash

strip-hints spades.py -o SIMPLE/app/environments/spades/spades/envs/spades.py
strip-hints probabilities.py -o SIMPLE/app/environments/spades/spades/envs/probabilities.py
cp "probabilities.json" "SIMPLE/app/environments/spades/spades/envs/probabilities.json"
strip-hints util.py -o SIMPLE/app/environments/spades/spades/envs/util.py

strip-hints play.py -o SIMPLE/app/play.py
strip-hints players.py -o SIMPLE/app/players.py
strip-hints MCTS.py -o SIMPLE/app/MCTS.py
strip-hints RL.py -o SIMPLE/app/RL.py
strip-hints util.py -o SIMPLE/app/util.py
strip-hints probabilities.py -o SIMPLE/app/probabilities.py
cp "probabilities.json" "SIMPLE/app/probabilities.json"
strip-hints spades.py -o SIMPLE/app/spades.py