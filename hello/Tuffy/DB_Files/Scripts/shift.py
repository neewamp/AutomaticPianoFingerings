import sys

def PrintPred(name, param1, param2):
  print(name.format(param1, param2))

def shift(offset, file):
  with open(file) as fread:
    predicates = fread.readlines()
  print("First({0!s})".format(offset))
  for i in predicates:
    if i[0:3] == "Fin":
      strin = (i[7:-2]).split(',')
      PrintPred("Finger({0!s}, {1!s})", strin[0], int(strin[1])+offset)
    elif i[0:3] == "Not":
      strin = (i[5:-2]).split(',')
      PrintPred("Note({0!s}, {1!s})", strin[0], int(strin[1])+offset)
    elif i[0:3] == "Suc":
      strin = (i[5:-2]).split(',')
      PrintPred("Succ({0!s}, {1!s})", int(strin[0])+offset, int(strin[1])+offset)
    elif i[0:3] == "Con":
      strin = (i[11:-2]).split(',')
      PrintPred("Concurrent({0!s}, {1!s})", int(strin[0])+offset, int(strin[1])+offset)
    elif i[0:3] == "Sta":
      strin = (i[6:-2]).split(',')
      PrintPred("Staff({0!s}, {1!s})", int(strin[0]), int(strin[1])+offset)

shift(int(sys.argv[1]), sys.argv[2])
