import sys
import random
import argparse

def parseArgs():
  parser = argparse.ArgumentParser('MLN Cost Estimator')
  parser.add_argument('--db_file', type=str, default ='../DB_Files/testr.db', help= 'DB file location')
  parser.add_argument('--mln_file', type=str, default ='../MLN_Weights/base_rules_right.mln', help= 'MLN Rules file location')
  parser.add_argument('--dm_file', type=str, default ='../Constants/fingering_vns.db', help= 'Distance matrix file location')
  parser.add_argument('--key_file', type=str, default = '../Constants/keys.db', help= 'Key type file location')
  FLAGS = None
  FLAGS, unparsed = parser.parse_known_args()
  return FLAGS

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def readDB(db_file):
  fingers = {}
  notes = {}
  succs = {}
  concurrents = {}
  rev_concurrents ={}
  preds = {}
  with open(db_file) as db_input:
    facts = db_input.readlines()
    for fact in facts:
      split1 = fact.split('(')
      split2 = split1[1].split(')')
      split3 = split2[0].split(',')
      if(split1[0] == "Finger"):
        fingers[int(split3[1])] = int(split3[0])
      elif(split1[0] == "Concurrent"):
        if split3[0] in concurrents:
          concurrents[int(split3[0])].append(int(split3[1]))
          rev_concurrents[int(split3[1])].append(int(split3[0]))
        else:
          concurrents[int(split3[0])] = [int(split3[1])]
          rev_concurrents[int(split3[1])] = [int(split3[0])]
      elif(split1[0] == "Note"):
          notes[int(split3[1])] = int(split3[0])
      elif(split1[0] == "Succ"):
        if int(split3[0]) in succs:
          succs[int(split3[0])].append(int(split3[1]))
          preds[int(split3[1])] = [int(split3[0])]
        else:
          succs[int(split3[0])] = [int(split3[1])]
          if int(split3[1]) in preds:
            preds[int(split3[1])].append(int(split3[0]))
          else:
            preds[int(split3[1])] = [int(split3[0])]


  pred_list = [notes, succs, preds, concurrents, rev_concurrents]
  return pred_list, fingers

def readDistanceMatrix(dm_file):
  mincomf = {}
  minprac ={}
  minrel = {}
  maxcomf = {}
  maxprac= {}
  maxrel = {}
  with open(dm_file) as dm_input:
    preds = dm_input.readlines()
    for pred in preds:
      if pred[0] != '\n':
        split1 = pred.split('(')
        split2 = split1[1].split(')')
        split3 = split2[0].split(',')
        finger1 = int(split3[0]) 
        finger2 = int(split3[1])
        value = int(split3[2])
        if(split1[0] == "MinComf"):
          mincomf[(finger1,finger2)] = value
        elif(split1[0] == "MinPrac"):
          minprac[(finger1,finger2)] = value
        elif(split1[0] == "MinRel"):
          minrel[(finger1,finger2)] = value
        elif(split1[0] == "MaxComf"):
          maxcomf[(finger1,finger2)] = value
        elif(split1[0] == "MaxPrac"):
          maxprac[(finger1,finger2)] = value
        elif(split1[0] == "MaxRel"):
          maxrel[(finger1,finger2)] = value
  distance_matrix = [mincomf, minprac, minrel, maxcomf,maxprac,maxrel]
  return distance_matrix

def readKeys(key_file):
  whites = []
  blacks = []
  with open(key_file) as key_input:
    keys = key_input.readlines()
    for key in keys:
      if key[0] != '\n':
        split1 = key.split('(')
        split2 = split1[1].split(')')
        if split1[0] == "White":
          whites.append(int(split2[0]))
        elif split1[0] == "Black":
          blacks.append(int(split2[0]))
  keys = [whites, blacks]
  return keys



# Currently only using very limited version, specifically only works
# on the current model, and expects exact formats for rules
# TODO: Use regular expressions instead of this method
def readRules(rule_file):
  rule_list = []
  weights = []
  with open(rule_file) as rule_input:
    rules = rule_input.readlines()
    for rule in rules:
      preds = rule.split(" ")
      if isNumber(preds[0]):  #only weight lines start with a number
        weights.append(float(preds[0]))
        preds = rule.split('v')

  return weights, rule_list

def evaluateRules(facts,queries,weights, distance_matrix, keys):
  #unrval all lists
  mincomf = distance_matrix[0]
  minprac =distance_matrix[1]
  minrel = distance_matrix[2]
  maxcomf = distance_matrix[3]
  maxprac= distance_matrix[4]
  maxrel = distance_matrix[5]
  whites = keys[0]
  blacks = keys[1]
  fingers = queries
  notes = facts[0]
  succs = facts[1]
  preds = facts[2]
  concurrents = facts[3]

#evaluate all succesor rules
  cost = 0
  for index in succs:
    for index2 in succs[index]:
#      comf = mincomf[(index,index2)]
      f1,f2 = fingers[index], fingers[index2]
      distance = notes[index2]-notes[index]
# Rule 1
      if distance < mincomf[(f1,f2)]:
        cost += weights[0]*(mincomf[(f1,f2)] - distance)
      if distance > maxcomf[(f1,f2)]:
        cost += weights[1]*(distance - maxcomf[(f1,f2)])
# Rule 2
      if distance < minrel[(f1,f2)]:
        cost += weights[2]*(minrel[(f1,f2)] - distance)
      if distance > maxrel[(f1,f2)]:
        cost += weights[3]*(distance - maxrel[(f1,f2)])

# Rule 5
      if f1 == 4:
        cost += weights[7]

# Rule 6
      if f1 == 3 & f2 == 4:
        cost += weights[8]
      if f1 == 4 & f2 == 3 :
        cost += weights[9]

# Rule 7
      if f1 == 3 & f2 == 4 & (notes[index] in whites) & (notes[index2] in blacks):
        cost += weights[10]
      if f1 == 4 & f2 == 3 & (notes[index] in whites) & (notes[index2] in blacks):
        cost += weights[11]

#Rule 8
      if f1 == 1 & notes[index] in blacks:
        cost += weights[12]
      if f1 == 1 & (notes[index] in blacks) & (notes[index2] in whites):
        cost += weights[13]
      if f2 == 1 & (notes[index] in whites) & (notes[index2] in blacks):
        cost += weights[14]

# Rule 9
      if f1 == 5 & f2 != 5 & (notes[index] in blacks) & (notes[index2] in blacks):
        cost += weights[15]
      if f2 == 5 & f1 != 5 & (notes[index] in blacks) & (notes[index2] in blacks):
        cost += weights[16]



# Rule 13
      if distance < minprac[(f1,f2)]:
        cost += weights[19]*(minprac[(f1,f2)] - distance)
      if distance > maxprac[(f1,f2)]:
       cost += weights[20]*(distance - maxprac[(f1,f2)])

# Three note pairs
      if index2 in succs:
        for index3 in succs[index2]:
          f3 = fingers[index3]
          distance = notes[index3] - notes[index]
# Rule 3
          if notes[index] == notes[index3] & f1 != f3:
            cost += weights[4]
# Rule 4
          if distance < mincomf[(f1,f3)]:
            cost += weights[5]*(mincomf[(f1,f3)] - distance)
          if distance > maxcomf[(f1,f3)]:
            cost += weights[6]*(distance - maxcomf[(f1,f3)])
# Rule 12
          if f1 == f3 & notes[index] != notes[index3] &  notes[index] < notes[index2] & notes[index2] < notes[index3]:
            cost += weights[17]
          if f1 == f3 & notes[index] != notes[index3] &  notes[index] > notes[index2] & notes[index2] > notes[index3]:
            cost += weights[18]

  for index in concurrents:
    for index2 in concurrents[index]:
      distance = notes[index2] - notes[index]
      f1, f2 = fingers[index], fingers[index2]
# Rule 1
      if distance < mincomf[(f1,f2)]:
        cost += weights[21]*(mincomf[(f1,f2)] - distance)
      if distance > maxcomf[(f1,f2)]:
        cost += weights[22]*(distance - maxcomf[(f1,f2)])
# Rule 2
      if distance < minrel[(f1,f2)]:
        cost += weights[23]*(minrel[(f1,f2)] - distance)
      if distance > maxrel[(f1,f2)]:
        cost += weights[24]*(distance - maxrel[(f1,f2)])
      if distance < minprac[(f1,f2)]:
        cost += weights[25]*(minprac[(f1,f2)] - distance)
      if distance > maxprac[(f1,f2)]:
        cost += weights[26]*(distance - maxprac[(f1,f2)])

# Rule 4
          
  return cost

def singleCost(facts, queries,weights, distance_matrix, keys, index):
  #unrval all lists
  mincomf = distance_matrix[0]
  minprac =distance_matrix[1]
  minrel = distance_matrix[2]
  maxcomf = distance_matrix[3]
  maxprac= distance_matrix[4]
  maxrel = distance_matrix[5]
  whites = keys[0]
  blacks = keys[1]
  fingers = queries
  notes = facts[0]
  succs = facts[1]
  preds = facts[2]
  concurrents = facts[3]
  rev_concurrents = facts[4]

  cost = 0
  if index in succs:
    for index2 in succs[index]:
      f1,f2 = fingers[index], fingers[index2]
    
      distance = notes[index2]-notes[index]
# Rule 1
      if distance < mincomf[(f1,f2)]:
        cost += weights[0]*(mincomf[(f1,f2)] - distance)
      if distance > maxcomf[(f1,f2)]:
        cost += weights[1]*(distance - maxcomf[(f1,f2)])
# Rule 2
      if distance < minrel[(f1,f2)]:
        cost += weights[2]*(minrel[(f1,f2)] - distance)
      if distance > maxrel[(f1,f2)]:
        cost += weights[3]*(distance - maxrel[(f1,f2)])

# Rule 5
      if f1 == 4:
        cost += weights[7]

# Rule 6
      if f1 == 3 & f2 == 4:
        cost += weights[8]
      if f1 == 4 & f2 == 3 :
        cost += weights[9]

# Rule 7
      if f1 == 3 & f2 == 4 & (notes[index] in whites) & (notes[index2] in blacks):
        cost += weights[10]
      if f1 == 4 & f2 == 3 & (notes[index] in whites) & (notes[index2] in blacks):
        cost += weights[11]

#Rule 8 
      if f1 == 1 & notes[index] in blacks:
        cost += weights[12]
      if f1 == 1 & (notes[index] in blacks) & (notes[index2] in whites):
        cost += weights[13]
      if f2 == 1 & (notes[index] in whites) & (notes[index2] in blacks):
        cost += weights[14]

# Rule 9
      if f1 == 5 & f2 != 5 & (notes[index] in blacks) & (notes[index2] in blacks):
        cost += weights[15]
      if f2 == 5 & f1 != 5 & (notes[index] in blacks) & (notes[index2] in blacks):
        cost += weights[16]

# Rule 13
      if distance < minprac[(f1,f2)]:
        cost += weights[19]*(minprac[(f1,f2)] - distance)
      if distance > maxprac[(f1,f2)]:
        cost += weights[20]*(distance - maxprac[(f1,f2)])

# Three notes forward
      if index2 in succs:
        for index3 in succs[index2]:
          f3 = fingers[index3]
          distance = notes[index3] - notes[index]

# Rule 3
          if notes[index] == notes[index3] & f1 != f3:
            cost += weights[4]
# Rule 4
          if distance < mincomf[(f1,f3)]:
            cost += weights[5]*(mincomf[(f1,f3)] - distance)
          if distance > maxcomf[(f1,f3)]:
            cost += weights[6]*(distance - maxcomf[(f1,f3)])
# Rule 12
          if f1 == f3 & notes[index] != notes[index3] &  notes[index] < notes[index2] & notes[index2] < notes[index3]:
            cost += weights[17]
          if f1 == f3 & notes[index] != notes[index3] &  notes[index] > notes[index2] & notes[index2] > notes[index3]:
            cost += weights[18]

  if index in preds:
    for index2 in preds[index]:
      f2,f1 = fingers[index], fingers[index2]
    
      distance = notes[index]-notes[index2]
# Rule 1
      if distance < mincomf[(f1,f2)]:
        cost += weights[0]*(mincomf[(f1,f2)] - distance)
      if distance > maxcomf[(f1,f2)]:
        cost += weights[1]*(distance - maxcomf[(f1,f2)])
# Rule 2
      if distance < minrel[(f1,f2)]:
        cost += weights[2]*(minrel[(f1,f2)] - distance)
      if distance > maxrel[(f1,f2)]:
        cost += weights[3]*(distance - maxrel[(f1,f2)])

# Rule 6
      if f1 == 3 & f2 == 4:
        cost += weights[8]
      if f1 == 4 & f2 == 3 :
        cost += weights[9]

# Rule 7
      if f1 == 3 & f2 == 4 & (notes[index2] in whites) & (notes[index] in blacks):
        cost += weights[10]
      if f1 == 4 & f2 == 3 & (notes[index2] in whites) & (notes[index] in blacks):
        cost += weights[11]

#Rule 8 
      if f1 == 1 & (notes[index2] in blacks) & (notes[index] in whites):
        cost += weights[13]
      if f2 == 1 & (notes[index2] in whites) & (notes[index] in blacks):
        cost += weights[14]

# Rule 9
      if f1 == 5 & f2 != 5 & (notes[index2] in blacks) & (notes[index] in blacks):
        cost += weights[15]
      if f2 == 5 & f1 != 5 & (notes[index2] in blacks) & (notes[index] in blacks):
        cost += weights[16]

# Rule 13
      if distance < minprac[(f1,f2)]:
        cost += weights[19]*(minprac[(f1,f2)] - distance)
      if distance > maxprac[(f1,f2)]:
        cost += weights[20]*(distance - maxprac[(f1,f2)])

# Three notes backward
      if index2 in preds:
        for index3 in preds[index2]:
          f3 = f2
          f1 = fingers[index3]
          distance = notes[index] - notes[index3]
# Rule 3
          if notes[index] == notes[index3] & f1 != f3:
            cost += weights[4]
# Rule 4
          if distance < mincomf[(f1,f3)]:
            cost += weights[5]*(mincomf[(f1,f3)] - distance)
          if distance > maxcomf[(f1,f3)]:
            cost += weights[6]*(distance - maxcomf[(f1,f3)])
# Rule 12
          if f1 == f3 & notes[index] != notes[index3] &  notes[index] < notes[index2] & notes[index2] < notes[index3]:
            cost += weights[17]
          if f1 == f3 & notes[index] != notes[index3] &  notes[index] > notes[index2] & notes[index2] > notes[index3]:
            cost += weights[18]


  if index in concurrents:
    for index2 in concurrents[index]:
      distance = notes[index2] - notes[index]
      f1, f2 = fingers[index], fingers[index2]
# Rule 1
      if distance < mincomf[(f1,f2)]:
        cost += weights[21]*(mincomf[(f1,f2)] - distance)
      if distance > maxcomf[(f1,f2)]:
        cost += weights[22]*(distance - maxcomf[(f1,f2)])
# Rule 2
      if distance < minrel[(f1,f2)]:
        cost += weights[23]*(minrel[(f1,f2)] - distance)
      if distance > maxrel[(f1,f2)]:
        cost += weights[24]*(distance - maxrel[(f1,f2)])
      if distance < minprac[(f1,f2)]:
        cost += weights[25]*(minprac[(f1,f2)] - distance)
      if distance > maxprac[(f1,f2)]:
        cost += weights[26]*(distance - maxprac[(f1,f2)])

  if index in rev_concurrents:
    for index2 in rev_concurrents[index]:
      distance = notes[index] - notes[index2]
      f2, f1 = fingers[index], fingers[index2]
# Rule 1
      if distance < mincomf[(f1,f2)]:
        cost += weights[21]*(mincomf[(f1,f2)] - distance)
      if distance > maxcomf[(f1,f2)]:
        cost += weights[22]*(distance - maxcomf[(f1,f2)])
# Rule 2
      if distance < minrel[(f1,f2)]:
        cost += weights[23]*(minrel[(f1,f2)] - distance)
      if distance > maxrel[(f1,f2)]:
        cost += weights[24]*(distance - maxrel[(f1,f2)])
      if distance < minprac[(f1,f2)]:
        cost += weights[25]*(minprac[(f1,f2)] - distance)
      if distance > maxprac[(f1,f2)]:
        cost += weights[26]*(distance - maxprac[(f1,f2)])



  return cost   

def hardConstraint(concurrents,rev_concurrents, fingers, index, finger):
  if index in concurrents:
    for index2 in concurrents[index]:
      if finger == fingers[index2]:
        return False
  if index in rev_concurrents:
    for index2 in rev_concurrents[index]:
      if finger == fingers[index2]:
        return False
  return True

def infer(facts, queries, weights,distance_matrix, keys, epochs):
  #unravel everythings
  fingers = queries
  concurrents = facts[3]
  rev_concurrents = facts[4]
#  for f in queries:
#    queries[f] = 1
  total_cost = evaluateRules(facts,fingers,weights, distance_matrix, keys)
  for e in range(epochs):
    shuffled = list(fingers.keys())
    random.shuffle(shuffled)
    for index in shuffled:
      cost = 10000
      bestFinger = 1
      for i in range(1,6):
        if hardConstraint(concurrents,rev_concurrents, fingers, index, i):
          fingers[index] = i
          cost_cur = singleCost(facts,fingers,weights, distance_matrix, keys, index)
          if cost > cost_cur:
            bestFinger = i
            cost = cost_cur
            fingers[index] = bestFinger
        fingers[index] = bestFinger


    if e % 10 == 0:
      new_cost = evaluateRules(facts,fingers,weights, distance_matrix, keys)
      if total_cost == new_cost:
        print("No change in 10 iterations, ending")
        return fingers
      total_cost = evaluateRules(facts,fingers,weights, distance_matrix, keys)
      print(total_cost)
  return fingers

def main():
  flags = parseArgs()
  fact_preds, query_preds = readDB(flags.db_file)
  weights, rules = readRules(flags.mln_file)
  distance_matrix = readDistanceMatrix(flags.dm_file)
  keys = readKeys(flags.key_file)
  cost = evaluateRules(fact_preds,query_preds,weights, distance_matrix, keys)
  cost1= singleCost(fact_preds,query_preds,weights, distance_matrix, keys, 226)
  fingers = infer(fact_preds,query_preds,weights, distance_matrix, keys, 226)
  rwrite = open('../Results/outputr.db', 'w')
  for key, value in sorted(fingers.items()):
    rwrite.write("Finger(%s, %s)\n" % (value,key))


  print(cost)


if __name__ == "__main__":
  main()
