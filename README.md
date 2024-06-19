# py-shobu

### Game rules
[https://rules.dized.com/game/VJQ5V5aAR4aqK31q1V1OXA/QxFjI3hVRLSgodBga_Ajtg/playing-the-game](https://rules.dized.com/game/VJQ5V5aAR4aqK31q1V1OXA/QxFjI3hVRLSgodBga_Ajtg/playing-the-game)

### Classes
**shobu.py** file contains 3 classes:
- **Shobu** - class representing game with usefull methods like **make_move**, **undo_move**, **get_legal_moves** or **clone**. Game position can be obtained by **to_string** method.
- **Move** - class representing moves. List of Moves is returned by **get_legal_moves**. **Sobus**'s **make_move** also take **Move** as parameter. Can be instantiated from string and represented as one.
- **GameMaster** - class that allows bots to play game using stdin stodut communication by using **play_game** method.
  
File **play.py** is a script enabling playing game with simple visualization.

### Communication format
#### Game position
On each turn **GameMaster** will print id of active player followed by a game state looking like this:<br/><br/>
    b wwww________bbbb wwww________bbbb wwww________bbbb wwww________bbbb <br/><br/>
First character is 'b' if black is the active player and 'w' otherwise. Four next segments coressponds to:
1. Black player's black board (bottom left)
2. Black player's white board
3. White player's black board
4. White player's white board (top right)

Each board has tiles numberd from 0 to 15 from top left to bottom right. In the position string 'w' and 'b' means that corresponding tile is occupied by stone of this color and '_' means that tile is empty.\
**Shobu** instance can be created from given position **Shobu.from_string** method.

#### Moves
Moves have following notation:
- if move have length of 2, first letter of notation is '2'
- next 1 or 2 letter determine move direction. There are following options:
  - U (up)
  - UR (up right)
  - R
  - DR
  - D
  - DL
  - L
  - UL
- next letter is 'w' if passive part of the move is to be made on white home board and 'b' otherwise
- then follows index of tile on "passive" board from which stone will be moved
- next letter is 'h' if aggressive move is to be made on player home board and 'f' otherwise
- last part of notation is the index of tile on "aggressive" board from which stone will be moved

#### Example
After following moves:
- 2ULb14f15
- DLw3f1
  
This position will be reached:<br/><br/>
b w_www_______bb_b wwww________bbbb wwww________bbbb www__bw_____bbb_<br/><br/>
![position](https://github.com/opprotossball/py-shobu/blob/main/examples/sample_position.png)
