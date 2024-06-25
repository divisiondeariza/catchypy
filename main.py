#!/usr/bin/env python3

#------------------------------------------------------------------------
# pylive: ex-add-notes
#
# Add 16 randomly-generated notes to a clip.
# The first track must be a MIDI track.
#------------------------------------------------------------------------

from pydoc import cli
from tracemalloc import start
import live
import time
import random
from live.classes.clip import Clip

from catchipy.catchitrack import CatchiTrack
from pychord import ChordProgression

def note_name_to_number(note_name: str) -> int:
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_number = note_names.index(note_name)
    return note_number

def new_clip(clip_length, track, notes, clip_index=0):
    if not track.is_midi_track:
        raise ValueError("First track must be a MIDI track")
    clip = Clip(track, clip_index, clip_length)
    track.set_clip(clip, clip_index)
    
    for note in notes:
        clip.add_note(*note)

class Note:
    def __init__(self, pitch, start_time, duration, velocity, mute):
        self.pitch = pitch
        self.start_time = start_time
        self.duration = duration
        self.velocity = velocity
        self.mute = mute

class Noteset:
    def __init__(self, clip_length):
        self.clip_length = clip_length
        self.notes = []

    def __iter__(self):
        return self

    def __next__(self):
        if not self.notes:
            raise StopIteration

        return self.notes.pop(0)

    def add_note(self, pitch, start_time, duration, velocity, mute):
        self.notes.append(Note(pitch, start_time, duration, velocity, mute))






def main():

    set = live.Set(scan=True)

    cp = ChordProgression(["D", "C", "G", "D"])

    clip_length = 8
    clip_index = 0
    
    track = CatchiTrack(set.tracks[1])

    notes = []
    for i, chord in enumerate(cp.chords):
        
        for j, note in enumerate(chord.components(3)):
            pitch = note_name_to_number(note) + (12 * 3)
            random_delta = (random.randrange(8) - 4)/32
            start_time = ((i + j * 0.125) / len(cp.chords) + random_delta) * clip_length
            notes.append((pitch, start_time, 0.25, 127, False))

    
    new_clip(clip_length, track, notes, clip_index)

    #--------------------------------------------------------------------------------
    track = CatchiTrack(set.tracks[2])
    notes = []
    for i in range(4):
        notes.append((36, i, 0.5, 127, False))
    
    for i in range(4):
        notes.append((37, i + 0.5, 0.5, 127, False))
        notes.append((37, i + 0.5 + 0.25, 0.5, 127, False))


    new_clip(clip_length, track, notes, clip_index=clip_index)




def generate_random_note(clip_length: float):
    #--------------------------------------------------------------------------------
    # Generate a random note in a minor scale.
    #--------------------------------------------------------------------------------
    scale = (0, 2, 3, 5, 7, 8, 10)
    degree = random.choice(scale)
    octave = random.randrange(3) - 3
    fundamental = 60
    pitch = fundamental + (octave * 12) + degree

    #--------------------------------------------------------------------------------
    # Generate a random start time, rounded to the nearest note
    #--------------------------------------------------------------------------------
    start_time = int(random.uniform(0, clip_length - 0.5) * 4) / 4

    duration = 0.5
    velocity = random.randrange(0, 127)
    mute = False

    return pitch, start_time, duration, velocity, mute


if __name__ == "__main__":
    main()