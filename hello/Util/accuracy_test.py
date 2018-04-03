import sys


def Test_Accuracy(test_labels, true_labels):
  with open(test_labels, 'r') as fread:
    test = fread.readlines()

  if len(test) == 0:
    print("Error. Empty file given")
    exit()

  with open(true_labels, 'r') as fread:
    true = fread.readlines()

  if len(test) == 0:
    print("Error. Empty file given")
  counter = 0
  for note in test:
    if note in true:
      counter += 1
  
  print(len(test))
  return(100*counter/len(test))

print(Test_Accuracy(sys.argv[1], sys.argv[2]))
