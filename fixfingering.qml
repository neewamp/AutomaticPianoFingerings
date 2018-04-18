//=============================================================================
//  MuseScore
//  Music Composition & Notation
//
//  Copyright (C) 2012 Werner Schweer
//  Copyright (C) 2013, 2014 Nicolas Froment, Joachim Schmitz
//  Copyright (C) 2014 Jörn Eichler
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License version 2
//  as published by the Free Software Foundation and appearing in
//  the file LICENCE.GPL
//=============================================================================

import QtQuick 2.0
import MuseScore 1.0

MuseScore {
    version:  "1.0"
    description: "This plugin moves fingering in the given range to stack with others in the chord and avoid the staff."
    menuPath: "Plugins.Notes.Fix Fingering"
    
    // Apply the given function to all notes in selection
    // or, if nothing is selected, in the entire score
    
    function applyToNotesInSelection() {
        var cursor = curScore.newCursor();
        cursor.rewind(1);
        var startStaff;
        var endStaff;
        var endTick;
        var fullScore = false;
        if (!cursor.segment) { // no selection
            fullScore = true;
            startStaff = 0; // start with 1st staff
            endStaff = curScore.nstaves - 1; // and end with last
        } else {
            startStaff = cursor.staffIdx;
            cursor.rewind(2);
            if (cursor.tick == 0) {
                // this happens when the selection includes
                // the last measure of the score.
                // rewind(2) goes behind the last segment (where
                // there's none) and sets tick=0
                endTick = curScore.lastSegment.tick + 1;
            } else {
                endTick = cursor.tick;
            }
            endStaff = cursor.staffIdx;
        }
        console.log(startStaff + " - " + endStaff + " - " + endTick)
        for (var staff = startStaff; staff <= endStaff; staff++) {

            cursor.rewind(1); // sets voice to 0
            cursor.voice = 0; //voice has to be set after goTo
            cursor.staffIdx = staff;
            
            if (fullScore)
                cursor.rewind(0) // if no selection, beginning of score

            var topFromStaff = -1
            var bottomFromStaff = 5
            var distToNote = 1.5
            var distToBeam = 1
            var offset = 0.25
            var spacing = 1.25

            var segment = cursor.segment
            while (segment && (fullScore || segment.tick < endTick)) {
                var voice = (staff === 0 ? 3 : 0)
                var numFingers = 0
                var count = 0
                var totalFingers = 0;
                var x = 0;
                y = (staff === 0 ? topFromStaff : bottomFromStaff)
                while (count < 4) {
                    //cursor.voice = voice;
                    if (segment.segmentType === Segment.ChordRest
                        && segment.elementAt(staff*4 + voice)
                        && segment.elementAt(staff*4 + voice).notes                              
                    ) { // go through every chord
                        var notes = segment.elementAt(staff*4 + voice).notes
                        for (var i = 0; i < notes.length; i++) { // notes in chord: 1st pass
                            // count total fingering elements in chord
                            var note = notes[i]
                            var noteElements = note.elements
                            for (var j = 0; j < noteElements.length; j++) { // elements in note: 1st pass
                                if (noteElements[j].type === Element.FINGERING) {
                                    totalFingers++;
                                }
                            }
                            // calculate relative y point
                            if (staff === 0) {
                                  y = Math.min(y, note.pos.y - distToNote)
                                  // notes under a beam
                                  if (note.parent.beam && note.pos.y > note.parent.beam.bbox.y) {
                                      y = Math.min(y, note.parent.beam.bbox.y - distToBeam)
                                  }
                            } else {
                                  y = Math.max(y, note.pos.y + distToNote)
                                  // notes under a beam
                                  if (note.parent.beam && note.pos.y < note.parent.beam.bbox.y) {
                                       y = Math.max(y, note.parent.beam.bbox.y + note.parent.beam.bbox.height + distToBeam)
                                  } else if (note.parent.hook && note.parent.hook.pos.y > 4.25) {
                                      y = Math.max(y, distToBeam + note.parent.hook.pos.y)
                                  }
                            }
                        }
                    }
                    voice = (staff === 0 ? voice - 1 : voice + 1)
                    count++;
                }
                count = 0;
                numFingers = 0;
                var voice = (staff === 0 ? 3 : 0)
                while (count < 4) {
                    //cursor.voice = voice;
                    if (segment.segmentType === Segment.ChordRest
                        && segment.elementAt(staff*4 + voice)
                        && segment.elementAt(staff*4 + voice).notes                              
                    ) { // go through every chord
                        var notes = segment.elementAt(staff*4 + voice).notes
                        for (var i = 0; i < notes.length; i++) { // notes in chord: 2nd pass
                            var note = notes[i]
                            var noteElements = note.elements
                            for (var j = 0; j < noteElements.length; j++) { // elements in note: 2nd pass
                                if (noteElements[j].type === Element.FINGERING) {
                                    var fingering = noteElements[j]
                                    fingering.pos.x = note.bbox.width/2
                                    fingering.pos.x += note.pos.x < -1.0 ? -note.pos.x : 0 // for "displaced" notes in chord
                                    if (staff === 0) {
                                        fingering.pos.y = y - note.pos.y - numFingers*spacing //- offset
                                    } else {
                                        fingering.pos.y = y - note.pos.y + (totalFingers-numFingers-1)*spacing //+ offset
                                    }
                                    numFingers++
                                }
                            }
                        }
                    }
                    voice = (staff === 0 ? voice - 1 : voice + 1)
                    count++
                }
                segment = segment.next
            }
        }
    }
    
    onRun: {
        if (typeof curScore === 'undefined')
            Qt.quit();
        
        applyToNotesInSelection()
        
        Qt.quit();
    }
}
