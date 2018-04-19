# TODO: add duration for tied notes to initial note

# Bug: separating fingering annotations for each note in chord?!

## Predicate Representation
# Staff(s, t)
# Note(p, t)
# Finger(f, t)
# Succ(t1, t2)
# Concurrent(t1,t2)
# Distance(t1,t2, l)

import sys
import math

from music21 import converter, clef, note, articulations
import music21.environment as environment
class NoteInfo:
  def __init__(self, pitch=-1, duration=0.0, staff=0, measure=-1, beat=0.0, note=note.Note(), index=0):
    self.Pitch = pitch
    self.Duration = duration
    self.Staff = staff
    self.Measure = measure
    self.Beat = beat
    self.Note = note
    self.Index = index

  def __eq__(self, other):
    """Overrides the default implementation"""
    if isinstance(self, other.__class__):
        return self.__dict__ == other.__dict__
    return False

class EventNoteInfo:
  def __init__(self, note, from_previous=False):
    self.Note = note
    self.fromPrevious = from_previous

def convertMidiToAugMidi(midi_num):
  E_PITCH = 4
  NUM_PITCHES = 12
  octave_num = math.floor(midi_num / NUM_PITCHES)
  aug_midi_num = midi_num + 2 * octave_num
  if midi_num % NUM_PITCHES > E_PITCH:
    aug_midi_num += 1
  # print('Midi num: {}, aug midi num: {}'.format(midi_num, aug_midi_num))
  return aug_midi_num

def getNoteProperties(x, prev_staff):
  t = ''
  s = "Pitch: " + str(x.pitch.midi) + ", Measure: "  + str(x.measureNumber) + ", Beat: " +  str(round(x.beat, 10));
  s += ", "
  if x.tie != None:
    t = x.tie.type
  s += t
  Measure = x.measureNumber
  Beat = round(x.beat, 10)
  Duration = round(x.duration.quarterLength, 10)
  # MIDIDIDIDIDIDI
  return NoteInfo(convertMidiToAugMidi(x.pitch.midi), Duration, prev_staff, Measure, Beat, x)

def getChordNoteProperties(n, x, pitch, prev_staff):
  t = ''
  s = "Pitch: " + str(pitch.midi) + ", Measure: "  + str(x.measureNumber) + ", Beat: " +  str(round(x.beat, 10));
  s += ", "
  if x.tie != None:
    t = x.tie.type
  s += t
  Measure = x.measureNumber
  Beat = round(x.beat, 10)
  Duration = round(x.duration.quarterLength, 10)
  # MIDIDIDIDIDI
  return NoteInfo(convertMidiToAugMidi(pitch.midi), Duration, prev_staff, Measure, Beat, x)

def getClef(prev_staff, clef):
  if clef.sign == 'G':
    prev_staff = 1
  elif clef.sign == 'F':
    prev_staff = -1
  return prev_staff

def convertSong(song_file):
  song = converter.parse(song_file)

  all_notes = song.recurse(classFilter=('Note','Chord'))   # list of all notes in song
  notes = {}                              # list of all notes in song, processed
  # cur_notes = []                        # notes that could overlap with current event
  # events = {}                           # dictionary of events ('every unique note onset and offset)
                                          # key is onset; value is list of overlapping notes

  prev_staff = getClef(0, song.parts[0][1].clef) # what if right hand part starts out as bass clef?
  start_tie_notes = []
  for i in range(len(all_notes)):
    x = all_notes[i]
    if (x.isNote or x.isChord) and (x.tie is None or x.tie.type == 'start'):
      # check staff/clef (music21 iterates over all notes in treble, then all notes in bass; it also only includes staff info for
      # notes in first measure)
      # print('x: {}, prev_staff: {}'.format(x, prev_staff))
      if x.activeSite.clef is not None:
        prev_staff = getClef(prev_staff, x.activeSite.clef)
      if x.isChord:
        notes_tmp = []
        for p, n in zip(x.pitches, x._notes):
          notes_tmp.append(getChordNoteProperties(n, x, p, prev_staff))
        for n in notes_tmp:
          measure = n.Measure
          if measure not in notes:
            notes[measure] = {}
          if n.Beat not in notes[measure]:
            notes[measure][n.Beat] = []
          notes[measure][n.Beat].append(n)
          if x.tie is not None and x.tie.type == 'start':
            start_tie_notes.append(n)
      elif x.isNote:
        note = getNoteProperties(x, prev_staff)
        measure = note.Measure
        if measure not in notes:
          notes[measure] = {}
        if note.Beat not in notes[measure]:
          notes[measure][note.Beat] = []
        notes[measure][note.Beat].append(note)
        if x.tie is not None and x.tie.type == 'start':
          start_tie_notes.append(note)
    elif (x.isNote or x.isChord) and x.tie is not None and (x.tie.type == 'continue' or x.tie.type == 'stop'):
      if x.isChord:
        start_notes = []
        for s_note in start_tie_notes:
          for p in x.pitches:
            # print('s_note: {}, chord note: {}, m: {}, s_note offset: {}, x offset: {}'.format(s_note.Pitch, p, s_note.Measure, calcOffset(s_note, song), round(x.getOffsetInHierarchy(song), 5)))
            if convertMidiToAugMidi(p.midi) == s_note.Pitch and calcOffset(s_note, song) == round(x.getOffsetInHierarchy(song), 5):
              s_note.Duration += round(x.duration.quarterLength, 10)
              start_notes.append(s_note)
              break
        if start_notes is not None and x.tie.type == 'stop':
          # print('stop working')
          for s_n in start_notes:
            # print(s_n.Note)
            start_tie_notes.remove(s_n)
        elif start_notes is None:
          print('Start notes is none; continuing note: {}'.format(x))    
        # print() 
      elif x.isNote:
        start_note = None
        for s_note in start_tie_notes:
          # print('s_note: {}, m: {}, s_note offset: {}, x offset: {}'.format(s_note.Note.pitch, s_note.Measure, calcOffset(s_note, song), x.getOffsetInHierarchy(song)))
          if s_note.Pitch == convertMidiToAugMidi(x.pitch.midi) and calcOffset(s_note, song) == round(x.getOffsetInHierarchy(song), 5):
            s_note.Duration += round(x.duration.quarterLength, 10)
            start_note = s_note
            break
        if start_note is not None and x.tie.type == 'stop':
          start_tie_notes.remove(start_note)  # should only remove if an ending tie!
        elif start_note is None:
          note = getNoteProperties(x, prev_staff)
          print('Start note is none; continuing note: (n: {}, m: {}, d: {})'.format(note.Note, note.Measure, note.Duration))     
        # print()
  return notes, song
  
def calcOnset(note, song):
  if type(note) is EventNoteInfo:
    return round(note.Note.Note.getOffsetInHierarchy(song), 5)
  elif type(note) is NoteInfo:
    return round(note.Note.getOffsetInHierarchy(song), 5)

def calcOffset(note, song):
  if type(note) is EventNoteInfo:
    return round(note.Note.Note.getOffsetInHierarchy(song) + note.Note.Duration, 5)
  elif type(note) is NoteInfo:
    return round(note.Note.getOffsetInHierarchy(song) + note.Duration, 5)

def setNoteIndex(notes):
  index = 0
  for measure,beats in sorted(notes.items()):
    for beat,ns in sorted(beats.items()):
      for note in ns:
        note.Index = index
        index += 1
  return notes

def getTuffyPredictions(tuffy_output):
  tuffy_predictions = {} #dictionary for tuffy output
  fingerings = [] #list of fingerings and associative indices to be annotated
  fings = [] #list of fingerings from fingerings list
  indices = [] #list of indices from fingerings list
  result = zip() #indices zipped with fingers
  
  for line in tuffy_output.readlines():
    fingerings.append(line)

  for finger in fingerings:
    split1 = finger.split("(")
    split2 = split1[1].split(")")
    split3 = split2[0].split(",")
    fings.append(int(split3[0]))
    indices.append(int(split3[1]))
      
    result = zip(indices, fings)
    resultSet = set(result)
    tuffy_predictions = dict(resultSet)

  return tuffy_predictions


def annotateFingerings(notes, song, tuffy_predictions): 

  # get all event onsets for both treble and bass clef 
  for measure,beats in sorted(notes.items()):
    # print('Measure {}:'.format(measure))
    for beat,ns in sorted(beats.items()):
      # print('\tBeat {}:'.format(beat))
      for n in ns:
        if(n.Index in tuffy_predictions):
          finger = tuffy_predictions[n.Index]
          n.Note.articulations.append(articulations.Fingering(finger))

def Convert(song_file, fingers):
  notes, song = convertSong(song_file)
  notes = setNoteIndex(notes)
  predictions = getTuffyPredictions(fingers)
  annotateFingerings(notes, song, predictions)
  return song

def main():
  if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<song_file>', '<tuffy_output>')
    exit(1)

  # convert song
  song_file = sys.argv[1]
  tuffy_output_file = sys.argv[2]
  notes, song = convertSong(song_file)
  notes = setNoteIndex(notes)
  tuffy_predictions = getTuffyPredictions(tuffy_output_file) # (make dictionary (key: index, value: finger number)) (e.g. { 45: 1, ...})
  #for index in sorted(tuffy_predictions.keys()):
   ##  print(index, tuffy_predictions[index])
  annotateFingerings(notes, song, tuffy_predictions)
  
  song.write('musicxml', song_file[:-4] + "_annotated.xml")

if __name__ == "__main__":
  main()
