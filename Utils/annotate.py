import io
from Utils.Parse import *
from Utils.split import *
import Utils.right_annotation as ra
import Utils.left_annotation as la
import Utils.Converter as Con
import music21

def Annotate(song_file, output_name):
    inp = song_file
    #Get parsed output
    output = io.StringIO()
    notesString(inp,output)

    #Split the database
    left = io.StringIO()
    right = io.StringIO()
    output.seek(0)
    Split(output,left,right)

    results = io.StringIO()
    right.seek(0)
    ra.right_fingers(right,results)

    left.seek(0)
    la.left_fingers(left,results)

    results.seek(0)
    song = Con.Convert(inp, results)
    
    song.write('musicxml', output_name)

    results.close()
    left.close()
    right.close()
    output.close()


# Annotate('yesterday.xml')
