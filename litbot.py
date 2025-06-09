import random

#list of players with set of cards in num format ex [{1,2,3},{23,45,25}]
#2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14
#15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27
#28, etc basically +13 for next suit

# 6 * 2 * 4 = 48
# even factors of 48 are 2, 4, 6, 8, 12, 16, 24

# playGame will first randomly pick a starting Player
# then it will call makeMove for that player
# once makeMove is called, update will be called on all
# players. a move can be two things, a call or an ask. 
# an ask will be defined as Asker, Askee, and Card. a call 
# is more complicated. a call will be defined as a series
# of asks to first opponents and then teammates. if a call
# is correct the scores will change accordingly

#assumptions:
#all players start with equal number of cards
#team distributions are balanced
#only 2 teams

NUMPLAYERS = 6

DECK = [2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14,\
        15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27,\
        28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40,\
        41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53]

NTOC = {2:'2C',3:'3C',4:'4C',5:'5C',6:'6C',7:'7C',9:'9C',10:'10C',11:'JC',12:'QC',13:'KC',14:'AC',\
        15:'2D',16:'3D',17:'4D',18:'5D',19:'6D',20:'7D',22:'9D',23:'10D',24:'JD',25:'QD',26:'KD',27:'AD',\
        28:'2H',29:'3H',30:'4H',31:'5H',32:'6H',33:'7H',35:'9H',36:'10H',37:'JH',38:'QH',39:'KH',40:'AH',\
        41:'2S',42:'3S',43:'4S',44:'5S',45:'6S',46:'7S',48:'9S',49:'10S',50:'JS',51:'QS',52:'KS',53:'AS'}

CTON = {'2C':2,'3C':3,'4C':4,'5C':5,'6C':6,'7C':7,'9C':9,'10C':10,'JC':11,'QC':12,'KC':13,'AC':14,\
        '2D':15,'3D':16,'4D':17,'5D':18,'6D':19,'7D':20,'9D':22,'10D':23,'JD':24,'QD':25,'KD':26,'AD':27,\
        '2H':28,'3H':29,'4H':30,'5H':31,'6H':32,'7H':33,'9H':35,'10H':36,'JH':37,'QH':38,'KH':39,'AH':40,\
        '2S':41,'3S':42,'4S':43,'5S':44,'6S':45,'7S':46,'9S':48,'10S':49,'JS':50,'QS':51,'KS':52,'AS':53}

SETS = [{2, 3, 4, 5, 6, 7},
        {9, 10, 11, 12, 13, 14},
        {15, 16, 17, 18, 19, 20},
        {22, 23, 24, 25, 26, 27},
        {32, 33, 28, 29, 30, 31},
        {35, 36, 37, 38, 39, 40},
        {41, 42, 43, 44, 45, 46},
        {48, 49, 50, 51, 52, 53}]

def shuffle(cards):
  random.shuffle(cards)
  return cards

def distribute(cards, NumPlayers=NUMPLAYERS):
  state = []

  for i in range(NumPlayers):
    hand = set()
    for j in range(b := len(cards)//NumPlayers):
      hand.add(cards[j + i*b])
    state.append(Player(i, hand))

  return state

def printHand(hand):
  print(" ".join([NTOC[card] for card in list(hand)]))

def printState(state):
  [print(str(player)) for player in state]

def searchSpace(hand):
  space = set()
  for card in list(hand):
    cardset = [s for s in SETS if card in s][0]
    space = space | cardset
  
  return space

def setFromCard(card):
  for set in SETS:
    if card in set:
      return set

def randOpponent(playerNum): #, team=False):
  #if team:
  return random.randint((c := playerNum < (h := NUMPLAYERS//2)) * h,  c * h + h - 1)
  #return random.randint((c := team ^ (playerNum < (h := NUMPLAYERS//2))) * h,  c * h + h - 1)


class Player:
  def __init__(self, playerNum, hand):
    self.hand = hand
    self.playerNum = playerNum
    setDeck = set(DECK)
    self.knowledge = [setDeck - hand for _ in range(NUMPLAYERS - 1)]
    self.knowledge.insert(playerNum, hand)
    self.search = searchSpace(hand)
    self.numCards = [len(DECK)//NUMPLAYERS for _ in range(NUMPLAYERS)]
    # print(self.search)
    # print(self.knowledge)
    # input()

  def __str__(self):
    return f'Player {self.playerNum}: {" ".join([NTOC[card] for card in list(self.hand)])}'

  def update(self, move, success):
    if success:
      if self.playerNum == move[0]:
        self.hand.add(move[2])

      elif self.playerNum == move[1]:
        self.hand.remove(move[2])
      
      self.search = searchSpace(self.hand)


    # self.knowledge
    #do something to knowledge
    #knowledge includes your own hand, previous asks, number of cards each player has, and how many of each set a player might potentially have
    #cards they have, cards in a set they asked for, and cards that they could have
    # known, 


  def getMove(self):
    #look through knowledge and see where it intersects with search
    # askee = -1
    # card = -1
    # for i,player in enumerate(self.knowledge):
    #   if i < NUMPLAYERS//2 == self.playerNum < NUMPLAYERS//2: #skips over teammates
    #     continue
    askee = randOpponent(self.playerNum) #fancy way to get opponents to ask
    card = random.choice([*self.search])
    # print(askee, NTOC[card])
    move = (self.playerNum, askee, card)
    # print("")
      
    return move
    #use knowledge to make move

def makeGame(NumPlayers=NUMPLAYERS):
  cards = DECK.copy()
  cards = shuffle(cards)
  state = distribute(cards, NumPlayers)
  return state

def playGame(state, NumPlayers=NUMPLAYERS):
  # printState(state)
  turn = random.randint(0, NumPlayers-1)
  countMoves = 0
  score = 0
  teams = [[i for i in range(0,NumPlayers//2)], [i for i in range(NumPlayers//2, NumPlayers)]]
  while True:
    move = state[turn].getMove()
    countMoves+=1
    print(f'Player {turn} asks Player {move[1]} for {NTOC[move[2]]}\n')
    
    if not isValid(state, move):
      print("not a valid move lil bro: ", move)
      continue

    # print(state)
    success = move[2] in state[move[1]].hand
    print(success,'\n')
    state = playMove(state, move)

    if success:
      printState(state)
    if success:
      if not state[turn].hand:
        teams[turn < NumPlayers//2].remove(turn)
        turn = random.choice(teams[turn < NumPlayers//2])
    else:
      turn = move[1]

    if isGameOver(state):
      print(f'\nTotal number of moves: {countMoves}\n')
      break

def isGameOver(state):
  combinedHand = {card for player in state[:NUMPLAYERS//2] for card in player.hand}
  for set in SETS:
    diff = len(combinedHand & set)
    if diff != 0 and diff != len(set):
      return False
  return True
  

def playMove(state, move):
  card = move[2]
  success = card in state[move[1]].hand
  # print(move, success)
  for player in state:
    player.update(move, success)
  return state

def isValid(state, move):
  #checks both that move is in the search space and that the opponent has cards
  #will eventually have to do more validation like is person a teammate and has that set been called already
  #technically the latter is already accounted for but a proper error message would be nice
  #this method probably takes up a lot of time but is mostly for debugging
  return move[2] in searchSpace(state[move[0]].hand) and state[move[1]].hand 

def main():
  state = makeGame()
  playGame(state)

if __name__ == "__main__":
  main()

