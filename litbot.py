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

class Player:
  def __init__(self, playerNum, hand):
    self.hand = hand
    self.playerNum = playerNum
    setDeck = set(DECK)
    self.knowledge = [setDeck - hand for _ in range(NUMPLAYERS - 1)]
    self.knowledge.insert(playerNum, hand)

  def __str__(self):
    return f'Player {self.playerNum}: {" ".join([NTOC[card] for card in list(self.hand)])}'

  def update(self, move):
    self.knowledge
    #do something to knowledge

  def makeMove():
    return 
    #use knowledge to make move

def makeGame(NumPlayers=NUMPLAYERS):
  cards = DECK.copy()
  cards = shuffle(cards)
  state = distribute(cards, NumPlayers)
  return state

def playGame(state, NumPlayers=NUMPLAYERS):
  # printState(state)
  turn = random.randint(0, NumPlayers-1)
  while True:
    state[turn].makeMove()


def main():
  state = makeGame()
  playGame(state)

if __name__ == "__main__":
  main()

