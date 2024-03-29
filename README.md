# Would You Rather Battle Bot

A Discord bot that uses a feedforward neural network (a multilayer perceptron) to predict what you will choose given two options regarding who you would rather battle.

## Commands

- $bb$start
  - Starts up a new battle if one is not already in progress. If one is already in progress, this command brings up the current battle details. It also gives a prediction about what you will choose based on past data.
- $bb$select \[Decision\]
  - Used for selecting one of the options by replacing \[Decision\] with the option you choose, e.g. $bb$select 2 horses
- $bb$reset
  - Clears previous selection data for the user who calls the command

## Required installations

- Python 3
- pandas
- scikit-learn
- discord.py

The dependencies below Python 3 can be installed using the pip command that comes with Python 3.

### Installing the bot

```bash
# Clone the repository
git clone https://github.com/Pyristix/would-you-rather-battle-bot.git
```

### Configuring the bot

After cloning the project and installing all dependencies, you need to add your Discord API bot token to the bottom of the battle_bot.py file in the indicated area.

### Starting the bot

```bash
python3 battle_bot.py
```
