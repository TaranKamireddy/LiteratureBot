# Literature Bot

This is a Python bot I made to play the card game Literature. It started as a fun challenge between me and a friend as we both wanted to make competing bots to see whose strategy would come out on top. We used to play the game a lot during late nights in college, and building a bot for it felt like a cool way to revisit those memories.

## 🎴 What’s Literature?

Literature is a team-based card game, sort of like Go Fish but with more strategy. It’s played with two teams of 2 or more players. There are 8 "sets" in the game, each one being either 2-7 or 9-A of a suit (e.g. 2♣ to 7♣ or 9♠ to A♠). The four 8s are removed, leaving 48 cards to be split among the players.

Players take turns asking opponents for cards from sets they already hold part of. If the opponent has the card, they must give it, and the turn continues. Otherwise, the turn passes. Teams score points by calling complete sets and correctly naming who has each card. First team to collect (or correctly call) the most sets wins.

For a more comprehensive ruleset visit: https://en.wikipedia.org/wiki/Literature_(card_game)
The full rules and some logic examples are in the comments inside the script if you're curious.

## 🤖 About the Bot

This bot plays Literature without any machine learning or LLMs—just logic, heuristics, and memory. It keeps track of card knowledge, team structure, and makes decisions based on known or inferred info.

There are a few types of bots implemented:
- randPlayer: makes random (legal) moves
- goodPlayer: the strongest bot
- weightPlayer: just based on weights
- manualPlayer: for human input/debugging

You can find my design thoughts and strategy notes in the notes.txt file. It’s not super polished, just a dump of ideas and debugging thoughts from over time.

## ▶️ Running It

No setup needed—just run the script in Python:
```
python3 literature_bot.py
```

It'll simulate a game between a logical bot and a random bot, and print out the results to the terminal.

## 🛠 Notes

- This project was mainly for fun, not for polished performance.
- I didn’t use any external libraries except for Python’s built-in ones.
- The code isn’t heavily commented, but function and variable names are fairly self-explanatory.
- Might update it over time with stronger bots or GUI options.

If you're into card games or just enjoy coding up game logic, give it a look. Feedback and ideas are always welcome!