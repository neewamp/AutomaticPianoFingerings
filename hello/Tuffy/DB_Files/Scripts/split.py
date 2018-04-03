
import sys

def splitDB(tuffy_output_file):
 
  fingers = {} #list of fingerings from fingerings list
  notes = {}
  succs = {}
  staves = {}
  concurrents = {}
  firstR = False
  firstL = False
  with open(tuffy_output_file) as tuffy_output:
    preds = tuffy_output.readlines()

    for pred in preds:
      split1 = pred.split("(")
      split2 = split1[1].split(")")
      split3 = split2[0].split(",")
      if(split1[0] == "Finger"):
        fingers[int(split3[1][1:])] = int(split3[0]) 
      elif(split1[0] == "Concurrent"):
        if int(split3[0]) in concurrents:
          concurrents[int(split3[0])].append(int(split3[1]))
        else:
          concurrents[int(split3[0])] = [int(split3[1])]
      elif(split1[0] == "Note"):
        notes[int(split3[1][1:])] = int(split3[0])
      elif(split1[0] == "Staff"):
        staves[int(split3[1][1:])] = int(split3[0])
      elif(split1[0] == "Succ"):
        if int(split3[0]) in succs:
          succs[int(split3[0])].append(int(split3[1]))
        else:
          succs[int(split3[0])] = [int(split3[1])]
  
  with open(tuffy_output_file[:-3] + "_right.db", 'w') as rwrite:
    with open(tuffy_output_file[:-3] + "_left.db", 'w') as lwrite:

      for key, value in sorted(fingers.items()):
        if staves[key] == 1:
          if firstR == False:
            rwrite.write("First(%s)\n" % (key))
            firstR = True
          rwrite.write("Finger(%s, %s)\n" % (value,key))
        else:
          if firstL == False:
            lwrite.write("First(%s)\n" % (key))
            firstL = True
          lwrite.write("Finger(%s, %s)\n" % (value,key))

      for key, value in sorted(notes.items()):
        if staves[key] == 1:
          rwrite.write("Note(%s, %s)\n" % (value,key))
        else:
          lwrite.write("Note(%s, %s)\n" % (value,key))
      for key, value in sorted(succs.items()):
        if staves[key] == 1:
          for i in value:
            rwrite.write("Succ(%s, %s)\n" % (key,i))
        else:
          for i in value:
            lwrite.write("Succ(%s, %s)\n" % (key,i))
      for key, value in sorted(concurrents.items()):
        if staves[key] == 1:
          for i in value:
            rwrite.write("Concurrent(%s, %s)\n" % (key,i))
        else:
          for i in value:
            lwrite.write("Concurrent(%s, %s)\n" % (key,i))


def main():
  if len(sys.argv) != 2:
    print('Usage: ', sys.argv[0], ' <input_db_file>')
  else:
    splitDB(sys.argv[1])

if __name__ == "__main__":
  main()
