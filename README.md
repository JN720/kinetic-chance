# kinetic-chance

After the original digital version in Python, which I developed back in my first year of high school, I decided to revisit the project 
around the beginning of my senior year and created the flagship CLI version in C++. As I progressed into my first year of university and began working
with more intensive machine learning projects, I had the idea to completely revamp Chance from a turn-based CLI game into something far
more dynamic. Furthermore, as I had spent significant time in the past few months learning Deep Reinforcement Learning and a few of the
algorithms contemporarily used, I decided to undertake the additional task of adapting the game to an environment, and creating agents
using Proximal Policy Optimization to create AI agents to play the game. Therefore, I chose PyGame as the engine to build the game, due to its
ease of compatibility as an RL environment.

**This project is still under light development** as the original goal of creating the agents has been achieved. Currently, the agent checkpoints I have chase 
and target the opponent with their moves. I plan to occasionally add small improvements including implementing more advanced reward calculation functionality, 
adding a player vs AI mode, more UI, and implementing sprite graphics.

# How to Play

Kinetic Chance is a 2-player game with the blue and red squares competing to defeat the other. Movement is done by WASD and IJKL respectively. 
Each player has a green health bar and a blue mana bar.
There are 2 ways to convert it into a move: through literacy and through streak. The former is more stable and simply involves holding the E and O keys for
blue and red respectively, and builds up literacy. The second method is streak, which can be faster and more efficient but is luck-based. It takes a constant
amount of mana and attempts to convert it to streak. As the name suggests, succeeding allows one to use a stronger move but a single streak failure will cause
you to lose all your current stacked streak. The keybinds for streak are Q and U respectively. If a player has either enough streak or literacy, they can
cast the selected move with F or ; respectively. Lastly, moves can be switched with C and X or , and . where the first keybind cycles left and the second
cycles right.
