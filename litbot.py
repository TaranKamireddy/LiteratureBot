import random
import time
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

#ideas for strats
#want to make a move for a card with the least guessing and
#choose the person with the highest chance of having it
#this should make it so it mostly goes for 1 card at a time

NUMPLAYERS = 6

DECK = [2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14,
        15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27,
        28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53]

NTOC = {2:'2C',3:'3C',4:'4C',5:'5C',6:'6C',7:'7C',9:'9C',10:'10C',11:'JC',12:'QC',13:'KC',14:'AC',
        15:'2D',16:'3D',17:'4D',18:'5D',19:'6D',20:'7D',22:'9D',23:'10D',24:'JD',25:'QD',26:'KD',27:'AD',
        28:'2H',29:'3H',30:'4H',31:'5H',32:'6H',33:'7H',35:'9H',36:'10H',37:'JH',38:'QH',39:'KH',40:'AH',
        41:'2S',42:'3S',43:'4S',44:'5S',45:'6S',46:'7S',48:'9S',49:'10S',50:'JS',51:'QS',52:'KS',53:'AS'}

CTON = {'2C':2,'3C':3,'4C':4,'5C':5,'6C':6,'7C':7,'9C':9,'10C':10,'JC':11,'QC':12,'KC':13,'AC':14,
        '2D':15,'3D':16,'4D':17,'5D':18,'6D':19,'7D':20,'9D':22,'10D':23,'JD':24,'QD':25,'KD':26,'AD':27,
        '2H':28,'3H':29,'4H':30,'5H':31,'6H':32,'7H':33,'9H':35,'10H':36,'JH':37,'QH':38,'KH':39,'AH':40,
        '2S':41,'3S':42,'4S':43,'5S':44,'6S':45,'7S':46,'9S':48,'10S':49,'JS':50,'QS':51,'KS':52,'AS':53}

SETS = [{2, 3, 4, 5, 6, 7},
        {9, 10, 11, 12, 13, 14},
        {15, 16, 17, 18, 19, 20},
        {22, 23, 24, 25, 26, 27},
        {32, 33, 28, 29, 30, 31},
        {35, 36, 37, 38, 39, 40},
        {41, 42, 43, 44, 45, 46},
        {48, 49, 50, 51, 52, 53}]

CTOSET = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
          9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 
          16: 2, 17: 2, 18: 2, 19: 2, 20: 2, 15: 2, 
          22: 3, 23: 3, 24: 3, 25: 3, 26: 3, 27: 3, 
          32: 4, 33: 4, 28: 4, 29: 4, 30: 4, 31: 4, 
          35: 5, 36: 5, 37: 5, 38: 5, 39: 5, 40: 5, 
          41: 6, 42: 6, 43: 6, 44: 6, 45: 6, 46: 6, 
          48: 7, 49: 7, 50: 7, 51: 7, 52: 7, 53: 7}

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

def printCards(cards):
  if type(cards) == set:
    print(" ".join([NTOC[card] for card in list(cards)]))
  else:
    print(" ".join([NTOC[card] for card in list(cards.hand)]))

def printState(state):
  [print(str(player)) for player in state]

def printKnowledge(state):
  if type(state) != list:
    state = [state]
  for player in state:
    print(f"Player {player.playerNum}'s Knowledge:")
    for k in player.knowledge:
      print(f'  Known: ', end="")
      printCards(k["known"])
      print(f'  Known Set: ', end="")
      printCards(k["knownset"])
      print(f'  Possible: ', end="")
      printCards(k["possible"])
      print(f'  # of Cards: {k['numCards']}')

def searchSpace(hand):
  space = set()
  for card in list(hand):
    cardset = [s for s in SETS if card in s][0]
    space = space | cardset
  space = space - hand

  return space

def setFromCard(card):
  for set in SETS:
    if card in set:
      return set

def randOpponent(playerNum): #, team=False):
  #if team:
  return random.randint((c := playerNum < (h := NUMPLAYERS//2)) * h,  c * h + h - 1)
  #return random.randint((c := team ^ (playerNum < (h := NUMPLAYERS//2))) * h,  c * h + h - 1)

def initialKnowledge(hand, playerNum):
  knowledge = []
  setDeck = set(DECK)
  for i in range(NUMPLAYERS):
    playerKnowledge = {"known":set(),"knownset":set(),"possible":set(),"numCards":len(hand)}
    if i != playerNum:
      playerKnowledge['possible'] = setDeck - hand
    else:
      playerKnowledge['known'] = hand
    knowledge.append(playerKnowledge)
  
  return knowledge

def easyCall(hand):
  for set in SETS:
    if set.issubset(hand):
      return set
  return None


#idea for knowledge structure: [{"known":set(),"knownset":set(),"possible":set(),"numCards":int}, ...]
#could also do [{"card1":rank, "card2":rank}, ...]
#could do bucketing [[rank1 cards, rank2 cards, rank3 cards, numCards], ...]
class Player:
  def __init__(self, playerNum, hand):
    self.hand = hand
    self.playerNum = playerNum
    # setDeck = set(DECK)
    # self.knowledge = [setDeck - hand for _ in range(NUMPLAYERS - 1)]
    # self.knowledge.insert(playerNum, hand)
    self.knowledge = initialKnowledge(hand, playerNum)
    self.search = searchSpace(hand)
    # self.numCards = [len(DECK)//NUMPLAYERS for _ in range(NUMPLAYERS)]
    self.asks = set()
    # print(self.search)
    # print(self.knowledge)
    # input()

  def __str__(self):
    return f'Player {self.playerNum}: {" ".join([NTOC[card] for card in list(self.hand)])}'

  def remover(self, card, player, rank):
    if card in self.knowledge[player][rank]:
      self.knowledge[player][rank].remove(card)

  def update(self, move, success):
    asker, askee, card = move
    normal = (asker < NUMPLAYERS//2) ^ (askee < NUMPLAYERS//2)
    self.asks.add(move)
    prev = self
    if not success:
      if not (SETS[CTOSET[card]] & self.knowledge[asker]['known']):
        for c in SETS[CTOSET[card]]:
          if c != card:
            if c in self.knowledge[asker]['possible']:
              self.knowledge[asker]['knownset'].add(c)
              self.knowledge[asker]['possible'].remove(c)
      # print(self.knowledge)
      self.remover(card, asker, 'possible')
      self.remover(card, asker, 'knownset')
      self.remover(card, askee, 'possible')
      self.remover(card, askee, 'knownset')

    if success:
      if self.playerNum == askee:
        self.hand.remove(card)
        self.search = searchSpace(self.hand)
      elif self.playerNum == asker and normal:
        self.hand.add(card)
        self.search = searchSpace(self.hand)

      self.knowledge[askee]['numCards']-=1
      self.remover(card, askee, 'known')
      if normal:
        self.knowledge[asker]['numCards']+=1
        self.knowledge[asker]['known'].add(card)
      # if card in self.knowledge[askee]['known']:
      #   self.knowledge[askee]['known'].remove(card)

      for i in range(NUMPLAYERS):
        if i != self.playerNum: 
          self.remover(card, i, 'possible')
          self.remover(card, i, 'knownset')
      
      for c in SETS[CTOSET[card]]:
        for i in range(NUMPLAYERS):
          if c in self.knowledge[i]['knownset']:
            self.knowledge[i]['knownset'].remove(c)
            self.knowledge[i]['possible'].add(c)

    for i in range(NUMPLAYERS):
      for c in list(self.knowledge[i]['knownset']):
        if len(SETS[CTOSET[c]] & self.knowledge[i]['knownset']) == 1:
          # printKnowledge(self)
          # print(f'\n Card {NTOC[c]} for Player {i}')
          for idx in range(NUMPLAYERS):
            self.remover(c, idx, 'knownset')
            self.remover(c, idx, 'possible')
          self.knowledge[i]['known'].add(c)
          # printKnowledge(self)
          # print("ur the cause lil bro")
          # input()


    # for i in range(NUMPLAYERS):
    #   if self.knowledge[i]['numCards'] == len(self.knowledge)
    for k in self.knowledge:
      if k['numCards'] == len(k['known']) + len(k['knownset']) + len(k['possible']):
        for c in list(k['knownset'] | k['possible']):
          k['known'].add(c)
          for idx in range(NUMPLAYERS):
            self.remover(c, idx, 'knownset')
            self.remover(c, idx, 'possible')
      if k['numCards'] == len(k['known']):
        k['knownset'].clear()
        k['possible'].clear()

    # unique = {}
    # for k in self.knowledge:
    #   for rank in ['knownset', 'possible']:
    #     for c in k[rank]:
    #       if c not in unique:
    #         unique[c] = 1
    #       else:
    #         unique[c]+=1
    # print(unique)
    # unique = {c for c,n in unique.items() if n == 1}
    # printCards(unique)
    # input()

    allfound = set()
    possession = {}
    duplicate = set()
    for i,k in enumerate(self.knowledge):
      for rank in ['knownset', 'possible']:
        for c in k[rank]:
          if c in allfound:
            duplicate.add(c)
          else:
            allfound.add(c)
            possession[c] = i
    unique = allfound - duplicate
    if unique:
      print("\n")
      printKnowledge(self)
      print("whoopty doo unique coming for you")
      printCards(unique)
    # print(unique)
    # print(possession)
    # input()
    for c in unique:
      i = possession[c]
      self.knowledge[i]['known'].add(c)
      self.remover(c, i, 'knownset')
      self.remover(c, i, 'possible')
    if unique:
      printKnowledge(self)
    #   input()
    
    
# Player 0: 6H 7H 3H
# Player 1: 3S 2H 5H
# Player 2: 2S 6S 2D 6D 4H
# Player 3:
# Player 4:
# Player 5: 4S 5S 7S 3D 4D 5D 7D
    # for k in self.knowledge:
    #   for rank in ['knownset', 'possible']:
    #     for c in k[rank]:

    for k in self.knowledge:
      if len(k['known']) > k['numCards']:
        printKnowledge(prev)
        printKnowledge(self)
        print('womp womp')
        input()
        break


        

    


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
    # if (call := easyCall(self.hand)):
    #   return [(self.playerNum, self.playerNum, card) for card in list(call)]

    # #TODO need to change this stupid ahh code because if the opponets are all gone
    # #it wont call cuz i dont have advanced caling yet
    # askee = randOpponent(self.playerNum) #fancy way to get opponents to ask
    # while self.knowledge[askee]['numCards'] == 0: 
    #   print("uh oh")
    #   askee = randOpponent(self.playerNum)

    # card = random.choice([*self.search])
    # # print(askee, NTOC[card])
    # move = [(self.playerNum, askee, card)]
    # print("")
    moves = []

    if (call := easyCall(self.hand)):
      return [(self.playerNum, self.playerNum, card) for card in list(call)]
     
    team = self.playerNum >= (h := NUMPLAYERS//2)
    #TODO Fix complex calling
    combined = {card for player in self.knowledge[team * h:team * h + h] for card in player['known']}
    for card in self.knowledge[self.playerNum]['known']:
      if SETS[CTOSET[card]].issubset(combined):
        for c in SETS[CTOSET[card]]:
          for i in range(team * h, team * h + h):
            if c in self.knowledge[i]['known']:
              moves.append((self.playerNum, i, c))
        # print(moves)
        # input()
        return moves

    for rank in ['known', 'knownset', 'possible']:
      for i in range((not team) * h, (not team) * h + h):
        # print(self.knowledge[i][rank], self.search)
        match = self.knowledge[i][rank] & self.search
        # print(match, '\n')
        if match:
          moves.append((self.playerNum, i, list(match)[0]))
          return moves
        
    
    opponents = [i for i in range((not team) * h, (not team) * h + h) if self.knowledge[i]['numCards']]
    if not opponents:
      print("uh oh no ppl to ask :(")
      # input()
    askee = random.choice(opponents)
    # askee = randOpponent(self.playerNum) #fancy way to get opponents to ask
    # while self.knowledge[askee]['numCards'] == 0:
    #   printKnowledge(self)
    #   print("uh oh")
    #   input()
    #   askee = randOpponent(self.playerNum)

    card = random.choice([*self.search])
    # print(askee, NTOC[card])
    moves = [(self.playerNum, askee, card)]
      
    return moves
    #use knowledge to make move

def makeGame(NumPlayers=NUMPLAYERS):
  cards = DECK.copy()
  cards = shuffle(cards)
  state = distribute(cards, NumPlayers)
  return state

def playGame(state, NumPlayers=NUMPLAYERS):
  printState(state)
  gameOver = False
  turn = random.randint(0, NumPlayers-1)
  countMoves = 0
  countCalls = 0
  score = [0, 0]
  teams = [[i for i in range(0,NumPlayers//2)], [i for i in range(NumPlayers//2, NumPlayers)]]
  while not gameOver:
    #gets move
    moves = state[turn].getMove()
    valid = True
    success = True
    team = turn >= NumPlayers//2
    calling = len(moves) > 1

    if calling:
      print(f'Player {turn} is calling')

    #is valid?
    for move in moves:
      valid = isValid(state, move, calling) and valid
      if valid:
        success = move[2] in state[move[1]].hand and success

    #not valid :(
    if not valid:
      print("not valid lil bro: ", moves)
      continue
    else:
      if calling:
        countCalls+=1
      else:
        countMoves+=1

    # printState(state)
    # printKnowledge(state)
    #plays moves
    

    if calling:
      if success:
        # printState(state)
        # printKnowledge(state)
        for move in moves:
          print(f'Player {turn} asks Player {move[1]} for {NTOC[move[2]]}\n')
          playMove(state, move)
          if not state[move[1]].hand:
            teams[move[1] >= NumPlayers//2].remove(move[1])
          print(success,'\n')
        # printState(state)
        # printKnowledge(state)
        # input()
        score[team] += 1
      else:
        for move in moves:
          askee = move[1]
          if move[2] not in state[move[1]].hand:
            for player in state:
              if move[2] in player.hand:
                askee = player.playerNum
          playMove(state, (move[0], askee, move[2]))
          if not state[askee].hand:
            teams[askee >= NumPlayers//2].remove(askee) 
          
        score[not team] += 1  
    else:
      print(f'Player {turn} asks Player {move[1]} for {NTOC[move[2]]}\n')
      playMove(state, moves[0])
      print(success,'\n')

      if not state[moves[0][1]].hand:
        teams[not team].remove(moves[0][1])
    if not state[turn].hand and turn in teams[team]:
      teams[team].remove(turn)

    
    # printState(state)
    # printKnowledge(state)
    checkKnowledge(state)

    #changes turns
    if success:
      printState(state)
      # [printCards(player.search) for player in state]

      #check game over
      if finished(state):
        gameOver = True
      elif not state[turn].hand:
        print(teams)
        if teams[team]:
          print(turn)
          turn = random.choice(teams[team])
        else:
          print(turn)
          turn = random.choice(teams[not team])
    else:
      if len(moves) > 1:
        turn = random.choice(teams[not team])
      else:
        turn = moves[0][1]

  print(f'\nTotal number of moves: {countMoves}')
  print(f'Total number of calls: {countCalls}')
  print(f'Score: {score[0]} - {score[1]}')

  # printKnowledge(state)

  return countCalls

def checkKnowledge(state):
  for i,player in enumerate(state):
    hand = player.hand
    for idx in range(NUMPLAYERS):
      k = state[idx].knowledge[i]
      if not hand.issubset((k['known'] | k['knownset'] | k['possible'])):
        printState(state)
        printKnowledge(state[idx])
        print(player.asks)
        print(i)
        print('im going to laksdkfsajdjflsd somebody')
        input()
      if not k['known'].issubset(hand):
        printState(state)
        printKnowledge(state[idx])
        print(player.asks)
        print(i)
        print('im going to hurt somebody')
        input()

def finished(state):
  for player in state:
    if player.hand:
      return False
  return True

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

def isValid(state, move, calling = False):
  #checks both that move is in the search space and that the opponent has cards
  #will eventually have to do more validation like is person a teammate and has that set been called already
  #technically the latter is already accounted for but a proper error message would be nice
  #this method probably takes up a lot of time but is mostly for debugging
  return (move[2] in searchSpace(state[move[0]].hand) or calling) and state[move[1]].hand 

def main():
  count = 0
  state = makeGame()
  calls = playGame(state)
  # calls = 0
  # start = time.time()
  # while True:
  #   count+=1
  #   state = makeGame()
  #   try:
  #     calls = playGame(state)
  #   except:
  #     # input()
  #     print("fail")
  # end = time.time()
  # print(f'Count: {count}')
  # print(f'Average time per game: {(end - start)/count:.6f} seconds')

if __name__ == "__main__":
  main()

