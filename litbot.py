import random
from abc import ABC, abstractmethod
import time

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

def distribute(cards, players):
  state = []

  for i,v in enumerate(players):
    hand = set()
    for j in range(b := len(cards)//NUMPLAYERS):
      hand.add(cards[j + i*b])
    if v == 'P':
      state.append(goodPlayer(i, hand))
    elif v == 'R':
      state.append(randPlayer(i, hand))
  return state

def printCards(cards):
  if type(cards) == set:
    print(" ".join([NTOC[card] for card in cards]))
  else:
    print(" ".join([NTOC[card] for card in cards.hand]))

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
class Player(ABC):
  def __init__(self, playerNum, hand):
    self.hand = hand
    self.playerNum = playerNum
    self.knowledge = initialKnowledge(hand, playerNum)
    self.search = searchSpace(hand)
    self.asks = set()

  def __str__(self):
    return f'Player {self.playerNum}: {" ".join([NTOC[card] for card in list(self.hand)])}'

  def remover(self, card, player, rank):
    if card in self.knowledge[player][rank]:
      self.knowledge[player][rank].remove(card)

  def update(self, move, success):
    asker, askee, card = move
    normal = (asker < NUMPLAYERS//2) ^ (askee < NUMPLAYERS//2) #xor to find team asking not team
    self.asks.add(move)
    prev = self #for debugging
    #wrong ask
    if not success:
      if not (SETS[CTOSET[card]] & self.knowledge[asker]['known']):
        #if the asker is known to have a card in that set then don't push cards to knownset
        for c in SETS[CTOSET[card]]: #add cards to knownset from possible
          if c != card:
            if c in self.knowledge[asker]['possible']:
              self.knowledge[asker]['knownset'].add(c)
              self.knowledge[asker]['possible'].remove(c)
      self.remover(card, asker, 'possible')
      self.remover(card, asker, 'knownset')
      self.remover(card, askee, 'possible')
      self.remover(card, askee, 'knownset')

    #good ask
    if success:
      if self.playerNum == askee:
        self.hand.remove(card)
        self.search = searchSpace(self.hand)
      elif self.playerNum == asker and normal:
        self.hand.add(card)
        self.search = searchSpace(self.hand)

      wasKnown = card in self.knowledge[askee]['known']

      self.knowledge[askee]['numCards']-=1
      self.remover(card, askee, 'known')
      if normal:
        self.knowledge[asker]['numCards']+=1
        self.knowledge[asker]['known'].add(card)

      for i in range(NUMPLAYERS):
        # if i != self.playerNum: 
        self.remover(card, i, 'possible')
        self.remover(card, i, 'knownset')
      
      #if the card was in known then you should keep the cards from that set in knownset
      #otherwise, you can move them back to possible
      if not wasKnown:
        for c in SETS[CTOSET[card]]:
          if c in self.knowledge[askee]['knownset']:
            self.knowledge[askee]['knownset'].remove(c)
            self.knowledge[askee]['possible'].add(c)
          

      #idk why this is happening to everyone
      #for every card in the set remove it from everyone's knownset and move it to possible
      #why did I write this stupid ass code
      # for c in SETS[CTOSET[card]]:
      #   for i in range(NUMPLAYERS):
      #     if c in self.knowledge[i]['knownset']:
      #       self.knowledge[i]['knownset'].remove(c)
      #       self.knowledge[i]['possible'].add(c)

    #Only 1 card from set in knownset
    for i in range(NUMPLAYERS):
      for c in list(self.knowledge[i]['knownset']):
        if len(SETS[CTOSET[c]] & self.knowledge[i]['knownset']) == 1:
          for idx in range(NUMPLAYERS):
            self.remover(c, idx, 'knownset')
            self.remover(c, idx, 'possible')
          self.knowledge[i]['known'].add(c)

    #Number of cards in hand is equal to number of cards in knowledge
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

    #Finds unique cards among players
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
    for c in unique:
      i = possession[c]
      self.knowledge[i]['known'].add(c)
      self.remover(c, i, 'knownset')
      self.remover(c, i, 'possible')
      for cs in SETS[CTOSET[c]]:
          if cs != c:
            if cs in self.knowledge[i]['knownset']:
              self.knowledge[i]['knownset'].remove(cs)
              self.knowledge[i]['possible'].add(cs)
    
    for k in self.knowledge:
      if len(k['known']) > k['numCards']:
        printKnowledge(prev)
        printKnowledge(self)
        print('womp womp')
        input()
        break

  @abstractmethod
  def getMove(self):
    pass

class goodPlayer(Player):
  def getMove(self):
    moves = []

    #Guarantee Easy Calling
    if (call := easyCall(self.hand)):
      print('Easy Call')
      return [(self.playerNum, self.playerNum, card) for card in list(call)]

    team = self.playerNum >= (h := NUMPLAYERS//2)
    #Guarantee Complex Calling
    combined = {card for player in self.knowledge[team * h:team * h + h] for card in player['known']}
    for card in self.knowledge[self.playerNum]['known']:
      if SETS[CTOSET[card]].issubset(combined):
        for c in SETS[CTOSET[card]]:
          for i in range(team * h, team * h + h):
            if c in self.knowledge[i]['known']:
              moves.append((self.playerNum, i, c))
        print('Complex Call')
        return moves

    #idea: don't ask for known cards in a set unless you know enough of them
    # ranks = []
    # for rank in ['known', 'knownset', 'possible']:
    #   for i in range((not team) * h, (not team) * h + h):
    #     match = self.knowledge[i][rank] & self.search
    #     if match:
    #       moves.append((self.playerNum, i, list(match)[0]))
    #       return moves

    # Guarantee Ask
    # for i in range((not team) * h, (not team) * h + h):
    #   match = self.knowledge[i]['known'] & self.search
    #   if match:
    #     moves.append((self.playerNum, i, list(match)[0]))
    #     print('Guarantee Ask')
    #     return moves

    #new attempt at weighted
    #weighted idea {card: [weight, weight, weight, ...]}
    #weighted idea {card: (bestOpponentWeight, opponent)}
    weighted = {card:[0]*6 for card in self.search}
    knownset = set()
    for card in self.search:
      for i, k in enumerate(self.knowledge):
        if card in k['known']:
          weighted[card][i] = 1
        elif (isKS := card in k['knownset']) or card in k['possible']:
          if isKS:
            knownset.add((card, i))
          weighted[card][i] = 1
          newWeight = 1/len([prob for prob in weighted[card] if prob])
          for idx, prob in enumerate(weighted[card]):
              weighted[card][idx] = newWeight if prob else 0
    for (card, i) in knownset:
      weighted[card][i] += 0.2
    # print(weighted)
    # input()
    bestMoves = []
    bestChance = 0
    for card, weights in weighted.items():
      # print(card, weights)
      # print((not team) * h, (not team) * h + h)
      notTeam = weights[(not team) * h:(not team) * h + h]
      # print(notTeam)
      currChance = max(notTeam)
      if bestChance > 0 and bestChance == currChance:
        bestMoves.append((self.playerNum, notTeam.index(currChance) + (not team) * h, card))
      if bestChance < currChance:
        bestChance = currChance
        bestMoves = [(self.playerNum, notTeam.index(currChance) + (not team) * h, card)]
  
    if bestMoves:
      bestMove = random.choice(bestMoves)
      moves.append(bestMove)
      # printKnowledge(self)
      print('Guess Ask')
      print(bestMove, bestChance)
      # input()
      # print(bestMove, bestChance)
      # input()
      # print(bestMoves)
      return moves

    # weighted = {card:(1, self.playerNum) for card in self.hand}
    #attempt at weighted gone wrong :O (move count went up)
    # weighted = {}
    # # setsToCall = set()
    # for card in self.search:
    #   # setsToCall.add(CTOSET[card])
    #   for i, k in enumerate(self.knowledge):
    #     if card in k['known']:
    #       weighted[card] = (1, i)
    #     elif (b := card in k['knownset']) or card in k['possible']:
    #       if card in weighted:
    #         prob, askee = weighted[card]
    #         # print(askee, team)
    #         # askee 
    #         if (askee >= NUMPLAYERS//2) == team:
    #         #team to team: swap
    #         #team to opp: swap
    #           askee = i
    #         #opp to team: don't swap
    #         elif (i >= NUMPLAYERS//2) != team:
    #         #known opp to possible opp: dont swap
    #           if b:
    #         #possible opp to known opp: swap
    #             askee = i
    #             # prob += -300
    #             # print('i love trains')
    #             # input()
    #         # print(askee)
    #         # input()
    #         weighted[card] = (1 / (1/prob + 1), askee)
    #       else:
    #         weighted[card] = (1, i)
    
    # bestChance = 0
    # bestCard = 0
    # for card, weight in weighted.items():
    #   # print(card, weight)
    #   # input()
    #   if (weight[1] >= NUMPLAYERS//2) != team:
    #     if weight[0] > bestChance:
    #       # print('Guess Ask')
    #       # print(card, weight)
    #       # input()
    #       bestChance = weight[0]
    #       bestCard = card

    # if bestCard > 0:
    #   moves.append((self.playerNum, weighted[bestCard][1], bestCard))
    #   print('Guess Ask')
    #   print(moves)
    #   print(bestCard, bestChance)
    #   printKnowledge(self)
    #   print(len(weighted))
    #   print(len(self.search))
    #   # if bestChance > 0.5 and bestChance < 1:
    #     # input()
    #   # input()
    #   return moves
    # input()
    
    opponents = [i for i in range((not team) * h, (not team) * h + h) if self.knowledge[i]['numCards']]
    if not opponents:
      print("uh oh no ppl to ask :(")
      weighted = {card:(1, self.playerNum) for card in self.hand}
      setsToCall = set()
      for card in self.search:
        setsToCall.add(CTOSET[card])
        for i, k in enumerate(self.knowledge):
          if card in k['known']:
            weighted[card] = (1, i)
          elif (b := card in k['knownset']) or card in k['possible']:
            if card in weighted:
              prob = weighted[card][0]
              askee = [weighted[card][1], i][b]
              weighted[card] = (1 / (1/prob + 1), askee)
            else:
              weighted[card] = (1, i)
      print(weighted)
      bestChance = 0
      bestSet = -1
      for s in setsToCall:
        chance = sum([weighted[card][0] for card in SETS[s]])
        if chance > bestChance:
          bestChance = chance
          bestSet = s
      
      for card in SETS[bestSet]:
        w = weighted[card]
        moves.append((self.playerNum, w[1], card))
      
      print(moves)
      print('Force Call')
      return moves


    #Random Move
    askee = random.choice(opponents)
    card = random.choice([*self.search])
    # print(askee, NTOC[card])
    moves = [(self.playerNum, askee, card)]
    # print(weighted)
    # printKnowledge(self)
    # print('random')
    # input()
    return moves
    #use knowledge to make move

class randPlayer(Player):
  def getMove(self):
    if (call := easyCall(self.hand)):
      return [(self.playerNum, self.playerNum, card) for card in list(call)]

    team = self.playerNum >= (h := NUMPLAYERS//2)
    opponents = [i for i in range((not team) * h, (not team) * h + h) if self.knowledge[i]['numCards']]
    if not opponents:
      print("uh oh no ppl to ask :(")
      # input()
    askee = random.choice(opponents)
    card = random.choice([*self.search])
    # print(askee, NTOC[card])
    moves = [(self.playerNum, askee, card)]
      
    return moves


def makeGame(players=['P']*NUMPLAYERS):
  cards = DECK.copy()
  cards = shuffle(cards)
  state = distribute(cards, players)
  return state

def playGame(state, NumPlayers=NUMPLAYERS):
  printState(state)
  gameOver = False
  turn = random.randint(0, NumPlayers-1)
  countMoves = 0
  countCalls = 0
  moveAccuracy = 0
  score = [0, 0]
  teams = [[i for i in range(0,NumPlayers//2)], [i for i in range(NumPlayers//2, NumPlayers)]]
  
  while not gameOver:
    #gets move
    moves = state[turn].getMove()
    valid = True
    success = True
    team = turn >= NumPlayers//2
    calling = len(moves) > 1

    #is valid?
    for move in moves:
      valid = isValid(state, move, calling) and valid
      if valid:
        success = move[2] in state[move[1]].hand and success

    #not valid :(
    if not valid:
      print("not valid lil bro: ", moves)
      input()
      continue
    else:
      if calling:
        countCalls+=1
      else:
        countMoves+=1
        if success:
          moveAccuracy += 1

    # printState(state)
    # if random.randint(1, 50) == 33:
    #   printKnowledge(state)
    #   input()

    # input()
    #plays moves
    

    if calling:
      print(f'Player {turn} is calling')
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
        print(f'Player {turn} called wrong')
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

      if not state[moves[0][1]].hand: #super ugly code 
        teams[not team].remove(moves[0][1])
    if not state[turn].hand and turn in teams[team]:
      teams[team].remove(turn)

    
    # printState(state)
    # printKnowledge(state)
    # checkKnowledge(state)
    # printKnowledge(state)

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
      if calling:
        if finished(state):
          gameOver = True
        elif teams[not team]:
          turn = random.choice(teams[not team])
        else:
          turn = random.choice(teams[team])
      else:
        turn = moves[0][1]
    # printState(state)
    # input()

  print(f'\nTotal number of moves: {countMoves}')
  print(f'Move Accuracy: {moveAccuracy}/{countMoves} or {100 * moveAccuracy/countMoves:.2f}%')
  print(f'Total number of calls: {countCalls}')
  print(f'Score: {score[0]} - {score[1]}')

  # printKnowledge(state)

  return (score, countMoves, countCalls, moveAccuracy)

# def checkKnowledge(state):
#   for i,player in enumerate(state):
#     hand = player.hand
#     for idx in range(NUMPLAYERS):
#       k = state[idx].knowledge[i]
#       if not hand.issubset((k['known'] | k['knownset'] | k['possible'])):
#         printState(state)
#         printKnowledge(state[idx])
#         print(player.asks)
#         print(i)
#         print('im going to laksdkfsajdjflsd somebody')
#         input()
#       if not k['known'].issubset(hand):
#         printState(state)
#         printKnowledge(state[idx])
#         print(player.asks)
#         print(i)
#         print('im going to hurt somebody')
#         input()

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
  moveCount = 0
  moveAccuracy = 0
  players = ['P']*(NUMPLAYERS//2) + ['P']*(NUMPLAYERS//2)
  # state = makeGame(players)
  # stats = playGame(state)
  # calls = 0
  start = time.time()
  while count < 10:
    count+=1
    state = makeGame(players)
    # try:
    stats = playGame(state)
    moveCount += stats[1]
    moveAccuracy += stats[3]
    # except:
    #   print("fail")
  end = time.time()
  print(f'Count: {count}')
  print(f'Average move count: {moveCount/count:.3f} moves')
  print(f'Average move accuracy: {100 * moveAccuracy/moveCount:.2f}%')
  print(f'Average time per game: {(end - start)/count:.6f} seconds')

if __name__ == "__main__":
  main()

