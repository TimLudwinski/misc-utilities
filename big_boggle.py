import sys
import random
import json

# Note: the dice are probably propriatry, so I'm not including them here.  
with open("boggle-dice.json") as f:
    dice = json.load(f) # This is a list of dice.  Each dice is a list of 6 letters (except for one, which has two letter combinations).  

# Shuffle the dice locations
random.shuffle(dice)

print("".join([ "-" ] * (5*5 + 1)))
for i in range(5):
    sys.stdout.write("|")
    for j in range(5):
        char = random.choice(dice[i + j*5]).title() # For each dice, choose a random side
        sys.stdout.write(" " + char.ljust(2, " ") + " |")
    sys.stdout.write("\n")
    print("".join([ "-" ] * (5*5 + 1)))
