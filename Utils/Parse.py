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
import io

from music21 import converter, clef, note, articulations
import music21.environment as environment
class NoteInfo:
  def __init__(self, pitch=-1, finger=0, duration=0.0, staff=0, measure=-1, beat=0.0, note=note.Note(), index=0):
    self.Pitch = pitch
    self.Finger = finger
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
  tie_type = ''
  if x.tie != None:
    tie_type = x.tie.type
  if x.articulations != []:
    # iterate over x's articulation list; find first instance of a finger number
    # and assign this as x's finger number.
    # NOTE: not sure what to do if a single note/chord contains multiple finger 
    # annotations
    # print('Chord:', x, 'Note:', pitch)
    # print('Articulations:', n.articulations)
    for a in x.articulations:
      if type(a) is articulations.Fingering:
        Finger = a.fingerNumber
        break
    #print('Articulations for note below: {}'.format(x.articulations))
  else:
    Finger = 1
  Measure = x.measureNumber
  Beat = round(x.beat, 10)
  Duration = round(x.duration.quarterLength, 10)
  # MIDIDIDIDIDIDI
  s = "Pitch: " + str(x.pitch) + ", Measure: "  + str(Measure) + ", Beat: " + str(Beat) + ", Finger: " + str(Finger) + ", Tie: " + tie_type
  #print(s)
  return NoteInfo(convertMidiToAugMidi(x.pitch.midi), Finger, Duration, prev_staff, Measure, Beat, x)

def getChordNoteProperties(n, x, pitch, prev_staff):
  tie_type = ''
  if x.tie != None:
    tie_type = x.tie.type

  Finger = -1
  if n.articulations != []:
    # iterate over x's articulation list; find first instance of a finger number
    # and assign this as x's finger number.
    # NOTE: not sure what to do if a single note/chord contains multiple finger 
    # annotations
    # print('Chord:', x, 'Note:', pitch)
    # print('Articulations:', n.articulations)
    for a in n.articulations:
      if type(a) is articulations.Fingering:
        Finger = a.fingerNumber
        break
    #print('Articulations for note below: {}'.format(x.articulations))
  else:
    Finger = 1
  Measure = x.measureNumber
  Beat = round(x.beat, 10)
  Duration = round(x.duration.quarterLength, 10)
  # MIDIDIDIDIDI
  s = "Pitch: " + str(pitch) + ", Measure: "  + str(Measure) + ", Beat: " + str(Beat) + ", Finger: " + str(Finger) + ", Tie: " + tie_type
  #print(s)
  return NoteInfo(convertMidiToAugMidi(pitch.midi), Finger, Duration, prev_staff, Measure, Beat, x)

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
  # events = {}                           # dictionary of events (every unique note onset and offset)
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
        # if all fingerings annotated on root note of chord...
        if len(x._notes[0].articulations) > 1:
          fingerings = []
          for a in x._notes[0].articulations:
            if(a.name == 'fingering'):
              fingerings.append(int(a.fingerNumber))
          for i in range(len(fingerings)):
            x._notes[i].articulations.append(articulations.Fingering(fingerings[i]))
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

def setNoteIndex(notes):
  index = 0
  for measure,beats in sorted(notes.items()):
    for beat,ns in sorted(beats.items()):
      for note in ns:
        note.Index = index
        index += 1
  return notes

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

def printNotes(notes, song, out=sys.stdout): 

  # get all event onsets for both treble and bass clef 
  treble_events = {}
  treble_sounding_notes = []
  bass_events = {}
  bass_sounding_notes = []
  for measure,beats in sorted(notes.items()):
    # print('Measure {}:'.format(measure))
    for beat,ns in sorted(beats.items()):
      # print('\tBeat {}:'.format(beat))
      for n in ns:
        onset = calcOnset(n, song)
        offset = calcOffset(n, song)

        if n.Staff == 1:
          # add onset and/or offset to treble events
          if onset not in treble_events:
            treble_events[onset] = []
            # print(onset, n.Pitch, n.Measure, n.Beat)
          if offset not in treble_events:
            treble_events[offset] = []
            # print(offset, n.Pitch, n.Measure, n.Beat, n.Duration)

          # add current note to events
          for e_onset, e_notes in sorted(treble_events.items()):
            if onset == e_onset:
              treble_events[e_onset].append(EventNoteInfo(n))
            elif offset > e_onset and onset < e_onset:
              treble_events[e_onset].append(EventNoteInfo(n, True))

          # add currently sounding treble notes to new events
          treble_sounding_notes_tmp = [ t_sn for t_sn in treble_sounding_notes ]
          for sn in treble_sounding_notes:
            sn_onset = calcOnset(sn, song)
            sn_offset = calcOffset(sn, song)
            if sn_offset > onset and sn_onset < onset:
              treble_events[onset].append(EventNoteInfo(sn, True))
            elif sn_offset > offset and sn_onset < offset:
              treble_events[offset].append(EventNoteInfo(sn, True))
            elif sn_offset < onset: # this depends on the notes being sorted beforehand
              treble_sounding_notes_tmp.remove(sn)

          treble_sounding_notes = treble_sounding_notes_tmp
          treble_sounding_notes.append(n)

        elif n.Staff == -1:
          # add onset and/or offset to bass events
          if onset not in bass_events:
            bass_events[onset] = []
            # print(onset, n.Pitch, n.Measure)
          if offset not in bass_events:
            bass_events[offset] = []
            # print(offset, n.Pitch, n.Measure)

          # add current note to events
          for e_onset, e_notes in sorted(bass_events.items()):
            if onset == e_onset:
              bass_events[e_onset].append(EventNoteInfo(n))
            elif offset > e_onset and onset < e_onset:
              bass_events[e_onset].append(EventNoteInfo(n, True))

          # add currently sounding treble notes to new events
          bass_sounding_notes_tmp = [ t_sn for t_sn in bass_sounding_notes ]
          for sn in bass_sounding_notes:
            sn_onset = calcOnset(sn, song)
            sn_offset = calcOffset(sn, song)
            if sn_offset > onset and sn_onset < onset:
              bass_events[onset].append(EventNoteInfo(sn, True))
            elif sn_offset > offset and sn_onset < offset:
              bass_events[offset].append(EventNoteInfo(sn, True))
            elif sn_offset < onset: # this depends on the notes being sorted beforehand
              bass_sounding_notes_tmp.remove(sn)

          bass_sounding_notes = bass_sounding_notes_tmp
          bass_sounding_notes.append(n)

        # print('\t\tNote:')
        # print('\t\t\tPitch: {}'.format(n.Pitch))
        # print('\t\t\tFinger: {}'.format(n.Finger))
        # print('\t\t\tDuration: {}'.format(n.Duration))
        # print('\t\t\tStaff: {}'.format(n.Staff))
        # print('\t\t\tMeasure: {}'.format(n.Measure))
        # print('\t\t\tBeat: {}'.format(n.Beat))
        # print('\t\t\tNote: {}'.format(n.Note))
        # print('\t\t\tIndex: {}'.format(n.Index))

  # print('Treble events:')
  # for e_onset, e_notes in sorted(treble_events.items()):
  #   print('Onset:', e_onset)
  #   for n in e_notes:
  #     print('\t{}'.format(n.Note.Pitch))

  # print('Bass events:')
  # for e_onset, e_notes in sorted(bass_events.items()):
  #   print('Onset:', e_onset)
  #   for n in e_notes:
  #     print('\t{}'.format(n.Note.Pitch))

  # print notes, fingers, and staffs
  for measure, beats in sorted(notes.items()):
    # print('\nMeasure {}:'.format(measure))
    for beat,ns in sorted(beats.items()):
      # print('\tBeat {}:'.format(beat))
      for n in ns:
        out.write('Note({}, {})\n'.format(n.Pitch, n.Index))
        #out.write('Note({}, {}, {})\n'.format(n.Pitch, n.Note.pitches, n.Index))
        out.write('Finger({}, {})\n'.format(n.Finger, n.Index))
        if n.Staff == -1:
          out.write('Staff({}, {})\n'.format(n.Staff, n.Index))
        elif n.Staff == 1:
          out.write('Staff({}, {})\n'.format(n.Staff, n.Index))
        else:
          out.write('Staff({}, {}, {})\n'.format('unknown', n.Staff, n.Index))


  # print concurrent notes for treble and bass
  for t_onset, t_notes in sorted(treble_events.items()):
    for t_note1 in t_notes:
      for t_note2 in t_notes:
        if t_note1 != t_note2 and not (t_note1.fromPrevious and t_note2.fromPrevious) and (t_note1.Note.Index < t_note2.Note.Index):
          out.write('Concurrent({}, {})\n'.format(t_note1.Note.Index, t_note2.Note.Index))
          #out.write('Concurrent({}, {}, {}, {})\n'.format(t_note1.Note.Index, t_note1.Note.Note.pitches, t_note2.Note.Index, t_note2.Note.Note.pitches))

  for b_onset, b_notes in sorted(bass_events.items()):
    for b_note1 in b_notes:
      for b_note2 in b_notes:
        if b_note1 != b_note2 and not (b_note1.fromPrevious and b_note2.fromPrevious) and (b_note1.Note.Index < b_note2.Note.Index):
          out.write('Concurrent({}, {})\n'.format(b_note1.Note.Index, b_note2.Note.Index))
          #out.write('Concurrent({}, {}, {}, {})\n'.format(b_note1.Note.Index, b_note1.Note.Note.pitches, b_note2.Note.Index, b_note2.Note.Note.pitches))

  # print successors for treble and bass
  treble_event_onsets = sorted(treble_events.keys())
  for i in range(len(treble_event_onsets)):
    if i != (len(sorted(treble_events.keys())) - 1):
      cur_event_notes = treble_events[treble_event_onsets[i]]
      next_event_notes = treble_events[treble_event_onsets[i + 1]]

      for c_note in cur_event_notes:
        for n_note in next_event_notes:
          if calcOffset(c_note, song) == calcOnset(n_note, song):
            out.write('Succ({}, {})\n'.format(c_note.Note.Index, n_note.Note.Index))
            #out.write('Succ({}, {}, {}, {})\n'.format(c_note.Note.Index, c_note.Note.Note.pitches, n_note.Note.Index, n_note.Note.Note.pitches))

  bass_event_onsets = sorted(bass_events.keys())
  for i in range(len(bass_event_onsets)):
    if i != (len(sorted(bass_events.keys())) - 1):
      cur_event_notes = bass_events[bass_event_onsets[i]]
      next_event_notes = bass_events[bass_event_onsets[i + 1]]

      for c_note in cur_event_notes:
        for n_note in next_event_notes:
          if calcOffset(c_note, song) == calcOnset(n_note, song):
            out.write('Succ({}, {})\n'.format(c_note.Note.Index, n_note.Note.Index))
            #out.write('Succ({}, {}, {}, {})\n'.format(c_note.Note.Index, c_note.Note.Note.pitches, n_note.Note.Index, n_note.Note.Note.pitches))

def notesString(song_file,output):
  notes, song = convertSong(song_file)
  notes = setNoteIndex(notes)
  printNotes(notes, song, output)

def main():
  output = io.StringIO()
  print('starting parsing')
  notesString(sys.argv[1],output)
  contents = output.getvalue()
  output.close()
  print(contents)

if __name__ == "__main__":
  main()

