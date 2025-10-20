import random
import time
import sys

# Player state stored in a dictionary
player = {
    'skill': 0,
    'stamina': 0,
    'luck': 0,
    'backpack': {'gold': 10, 'map': 1},
    'potion': None
}

# Function to print text slowly for dramatic effect
def slow_print(text, delay=0.03, skippable=True):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    if skippable:
        input("Press Enter to continue...")

# Function to handle input validation
def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt).lower().strip()
        if choice in valid_options:
            return choice
        print(f"Please choose one of: {', '.join(valid_options)}")

# Function to display player status
def display_status(player):
    print(f"\nStatus: Skill: {player['skill']}, Stamina: {player['stamina']}, Luck: {player['luck']}")
    print(f"Backpack: {', '.join(f'{k}: {v}' for k, v in player['backpack'].items())}")
    if player['potion']:
        print(f"Potion: {player['potion'].capitalize()}")

# Function to generate player stats
def generate_stats(player):
    player['skill'] = random.randint(1, 6) + 6
    player['stamina'] = random.randint(1, 6) + random.randint(1, 6) + 12
    player['luck'] = random.randint(1, 6) + 6

# Function to display game introduction
def display_intro():
    slow_print('''Only the foolhardy or the very brave would willingly risk a journey into Darkwood Forest, where strange, twisting paths wind their way into the eerie depths. 
Who knows what monstrous creatures lurk in the threatening shadows, or what deadly adventure await the unwary traveller.''')
    choice = get_valid_input('You dare enter (yes/no): ', ['yes', 'no'])
    if choice == 'yes':
        slow_print('''In a desperate race against time, deep within Darkwood, your quest is to find the missing pieces of the legendary Hammer of Stonebridge, which was fashioned by dwarfs to protect peaceful Stonebridge against its ancient doom.

Many dangers lie ahead and your success is by no means certain. Powerful adversaries are ranged against you and often your only choice is to kill or be killed.

You have in your possession a sword and backpack containing provisions for the trip.''')
        return True
    else:
        slow_print('Thank you for playing!')
        return False

# Function to choose a potion
def choose_potion(player):
    slow_print('''You are armed with a sword and dressed in leather armour. You may choose to take a bottle of any of the following potions:

Potion of Skill - restores SKILL points
Potion of Strength - restores STAMINA
Potion of Fortune - restores LUCK and adds 1 initial LUCK''')
    potion = get_valid_input('Which potion do you wish to choose? (skill, strength, fortune): ',
                            ['skill', 'strength', 'fortune'])
    player['potion'] = potion
    if potion == 'fortune':
        player['luck'] += 1  # Increase initial Luck by 1
    slow_print(f'A potion of {potion} has been added to your pack.')

# Function to display the background story
def display_background():
    slow_print('''BACKGROUND:
You are an adventurer, a sword for hire, and have been roaming the northern borderlands of your kingdom. 
Having always spurned the dullness of village life, you now wander the lands in search of wealth and danger.
Despite the long walks and rough outdoor life, you are content with your unknown destiny. The world holds no fears
for you as you are a skillful warrior, well practiced in the art of slaying evil men and beasts with your trusty sword.
Not once during the last 10 days since entering the northern borderlands have you set eyes upon another person.
This does not worry you at all, as you are happy with your own company and enjoy the slow, sunny days hunting, eating, and sleeping.''')
    print()
    slow_print('''It is evening, and having feasted on a dinner of rabbit, spit-roasted on an open fire, you settle down
to sleep beneath your sheepskin blanket. There's a full moon, and the light sparkles on the blade of
your broadsword, skewered into the ground by your side. You gaze at it, wondering when you will next
have to wipe the blood of some vile creature from its sharp edge. These are strange lands, inhabited by
twisted and loathsome beasts — goblins, trolls, and even dragons.''')
    print()
    slow_print('''As the flame of your campfire gently dies, you begin to drift asleep, and images of screaming,
green-faced trolls flicker through your mind.

Suddenly, in the bushes to your left, you hear the loud crack of a twig breaking under a clumsy foot. You
leap up and grab your sword from the ground. You stand motionless but alert, ready to pounce on your
unseen adversary.

Then you hear a groan, followed by the dull thud of a body falling to the ground. Is it
a trap? Slowly, you walk over to the bush where the noise is coming from and carefully pull back the
branches.

You look down to see a little old man with a great bushy beard, his face contorted with pain.
You crouch down to remove the iron helmet covering his balding head and notice two crossbow bolts
protruding from the stomach of his plump, chainmail-clad torso.

Picking him up, you carry him over to the fire and stir the dying embers into life. After
covering him with the sheepskin blanket, you manage to get the old man to drink a little water. He
coughs and moans. He sits up rigid, eyes staring fixedly ahead, and starts to shout:

"I'll get them! Get them! Don't you fear, Gillibran,
Bigleg is coming to bring you the hammer. Oh yes,
indeed I am. Oh yes..."

The dwarf, whose name you presume to be Bigleg, is obviously delirious from the poison-tipped bolts
lodged in his stomach. You watch as he slumps down again to the ground, then whisper his name
in his ear. His eyes stare unblinkingly at you as he again starts to shout.''')
    print()
    slow_print('''"Ambush! Look out! Ambush! Aagh! The hammer!
Take the hammer to Gillibran! Save the dwarfs!"

His eyes half-close, and the pain seems to ease a little. As the delirium subsides, he speaks to you again
in a low whisper:

"Help us, friend... take the hammer to Gillibran...
only the hammer will unite our people against
the trolls... We were on our way to Darkwood in
search of the hammer... ambushed by the little
people... others died... the map in my pouch
will take you to the home of Yaztromo, the master
mage of these parts... he has great magics for sale
to protect you against the creatures of Darkwood...
take my gold... I beg you to find the hammer
and take it to Gillibran, my Lord of Stonebridge.
You will be well rewarded..."

Bigleg opens his mouth to start another sentence, but nothing comes out except his last dying breath.

You sit down and ponder Bigleg’s words. Who is Gillibran? Who is Yaztromo?
What is all the fuss about the dwarfish hammer?

You reach over to the still body of Bigleg and remove the pouch from the leather belt around his waist.
Inside, you find 10 Gold Pieces and a map.

Jingling the coins in your hand, you think of the possible rewards which may await you just for
returning a hammer to a village of dwarfs. You decide to try to find the hammer in Darkwood
Forest — it's been a few weeks since your last good battle, and, what is more, you are likely to be well
paid for this one.

With your mind made up, you settle down to sleep, having taken back the sheepskin blanket from poor
Bigleg. In the morning, you bury the old dwarf and gather up your possessions. You examine the
map, look up to the sun, and find your bearings. Whistling merrily, you head off south at a good
pace, eager to meet this man Yaztromo and see what he has to offer.''')
    print()
    slow_print(f'You have added {player["backpack"]["gold"]} Gold and a map to your backpack.')

# Function to handle Yaztromo's introduction
def yaztromo_intro():
    slow_print('''Your walk to Yaztromo’s takes a little over half a day, and you arrive at his stone tower home dirty
and hungry. As the tower is set back on the edges of Darkwood, some fifty metres away from the path you have been following, it is difficult to find.

Finally, you walk up to the huge oak door, somewhat relieved to find that it does exist and that
Bigleg had not been speaking wildly in his delirium.

A large brass bell and gong hang from the stone archway. As you ring the bell, a shiver runs down
your spine and you realize that the loud bong invades a deep silence which you had not noticed
before. There are no sounds of birds or animals to be heard.

You wait anxiously at the door and hear slow footsteps descending stairs from the tower above.
A small wooden slot in the door slides open, and two eyes appear and examine you.

"Well, who are you?" demands a grumpy voice through the hole.

You answer that you are an adventurer in search of the master mage Yaztromo, intending to purchase
magical items from him to combat the creatures of Darkwood Forest.

"Oh! Well, in that case, if you are interested in buying
some of my merchandise, you'd better come up. I
am Yaztromo."''')
    print()
    slow_print("He then turns and slowly climbs the stone stairs.")
    choice = get_valid_input('Will you:\nFollow him up the stairs?\nDraw your sword and attack him\n(follow/attack): ', ['follow', 'attack'])
    if choice == 'follow':
        slow_print('''You follow the huffing and puffing old man in his tattered robes up the spiral staircase to a large room
at the top of the tower. Shelves, cupboards, and cabinets line the walls, all filled with bottles, jars,
weapons, armour, and all manner of strange artefacts.

Yaztromo shuffles past the general clutter and slumps down in an old oak chair. He reaches into
his top pocket and pulls out a fragile pair of gold-rimmed spectacles. Placing these on his nose, he
picks up a piece of slate and chalk from a table next to his chair and begins to write frantically.

He then hands you the slate.''')
        return 'shop'  # Placeholder for future shop implementation
    else:
        slow_print('''You draw your sword and attack Yaztromo! He turns, surprised, and raises his hand. A bolt of energy
knocks you back, ending your adventure prematurely.''')
        return 'game_over'

# Main game loop
def main():
    if not display_intro():
        return  # Exit if player chooses not to enter
    print()
    get_valid_input('Type "ready" when you wish to generate your strengths and weaknesses: ', ['ready'])
    generate_stats(player)
    display_status(player)
    print()
    choose_potion(player)
    display_status(player)
    print()
    display_background()
    print()
    next_section = yaztromo_intro()
    if next_section == 'game_over':
        slow_print("Game Over!")
        return
    # Placeholder for future sections (e.g., Yaztromo's shop)
    slow_print("To be continued... (Yaztromo's shop and further adventures coming soon!)")

# Start the game
if __name__ == "__main__":
    main()
