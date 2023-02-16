# Description: A file for defining functions listing different notes to use for exercises:
# First created: 02/11/22

def populate_natural_sharps(midi_val):
    # Function for returning note letters for a given MIDI value (assuming sharps convention)

    if 0 <= midi_val % 12 <= 1:  # 0 for C, 1 for C#
        note = "c"
    elif 2 <= midi_val % 12 <= 3:  # 2 for D, 3 for D#
        note = "d"
    elif midi_val % 12 == 4:  # 4 for E
        note = "e"
    elif 5 <= midi_val % 12 <= 6:  # 5 for F, 6 for F#
        note = "f"
    elif 7 <= midi_val % 12 <= 8:  # 7 for G, 8 for G#
        note = "g"
    elif 9 <= midi_val % 12 <= 10:  # 9 for A, 10 for A#
        note = "a"
    else:  # must be 11 for B
        note = "b"
    return note


def populate_natural_flats(midi_val):
    # Function for returning note letters for a given MIDI value (assuming sharps convention)

    if midi_val % 12 == 0:  # 0 for C
        note = "c"
    elif 1 <= midi_val % 12 <= 2:  # 1 for Db, 2 for D
        note = "d"
    elif 3 <= midi_val % 12 <= 4:  # 3 for Eb, 4 for E
        note = "e"
    elif midi_val % 12 == 5:  # 5 for F
        note = "f"
    elif 6 <= midi_val % 12 <= 7:  # 6 for Gb, 7 for G
        note = "g"
    elif 8 <= midi_val % 12 <= 9:  # 8 for Ab, 9 for A
        note = "a"
    else:  # must be 10 or 11 for B
        note = "b"
    return note


def add_octave_punctuation(midi_val, note_in):
    # Function for adding the correct number of apostrophes/commas to a note string in order to get the correct
    # octave with Abjad

    # Find punctuation "order" required. +ve for apostrophes, -ve for commas
    punctuation_order = round((midi_val - 48 + 12) / 12 - (midi_val % 12) / 12)

    # Add punctuation
    if punctuation_order >= 0:
        punctuation = ''.join(["'"] * punctuation_order)
    else:
        punctuation = ''.join([","] * -punctuation_order)

    # Concatenate note string with punctuation reflective of octave
    noteout = note_in + punctuation
    return noteout


def all_notes_sharps(midi_val_start, midi_val_end, added_sharps=""):
    # Function for creating a table containing all the notes between MIDIstart and MIDIend, using sharps for accidentals
    # Optional added_sharps input for keys such as F#

    # Initialise list of MIDI values and notes:
    midi_vals = range(midi_val_start, midi_val_end + 1)

    # Loop through MIDI values to populate notes:
    notes = []
    for midi_val in midi_vals:

        # Populate natural notes:
        notes.append(populate_natural_sharps(midi_val))

        # Add sharps:
        if midi_val % 12 in [1, 3, 6, 8, 10]:  # Indicators of being sharp
            notes[-1] = notes[-1] + "s"

        # Now consider added sharps
        if notes[-1] == "f" and "e" in added_sharps:
            notes[-1] = "es"

        # Add apostrophes:
        notes[-1] = add_octave_punctuation(midi_val, notes[-1])

    # Populate dictionary (/table)
    table = dict(zip(midi_vals, notes))
    return table


def all_notes_flats(midi_val_start, midi_val_end):
    # Function for creating a table containing all the notes between MIDIstart and MIDIend, using flats for accidentals

    # Initialise list of MIDI values and notes:
    midi_vals = range(midi_val_start, midi_val_end + 1)

    # Loop through MIDI values to populate notes:
    notes_text = []
    for midi_val in midi_vals:
        # Populate natural notes:
        notes_text.append(populate_natural_flats(midi_val))
        # Add flats:
        if midi_val % 12 in [1, 3, 6, 8, 10]:  # Indicators of being flat
            notes_text[-1] = notes_text[-1] + "f"
        # Add apostrophes:
        notes_text[-1] = add_octave_punctuation(midi_val, notes_text[-1])

    # Populate dictionary (/table)
    table = dict(zip(midi_vals, notes_text))
    return table


def natural_notes(midi_val_start, midi_val_end):
    # Function for creating a table containing only natural notes between MIDIstart and MIDIend

    # Initialise list of MIDI values and notes:
    midi_vals = range(midi_val_start, midi_val_end + 1)
    midi_vals = [item for item in midi_vals if item % 12 not in [1, 3, 6, 8, 10]]  # Just naturals! Uses modulo 12

    # Loop through MIDI values to populate notes:
    notes_text = []
    for midi_val in midi_vals:
        # Populate natural notes:
        notes_text.append(populate_natural_sharps(midi_val))
        # Add apostrophes:
        notes_text[-1] = add_octave_punctuation(midi_val, notes_text[-1])

    # Populate dictionary (/table)
    table = dict(zip(midi_vals, notes_text))
    return table


def notes_in_major(midi_val_start, midi_val_end, key):
    # Function for creating a table with notes only from major

    # Create table for 2nd octave (C2 to D#2)
    table_flats = all_notes_flats(36, 47)
    table_sharps = all_notes_sharps(36, 47)
    table_midi_vals = list(table_flats.keys()) + list(table_sharps.keys())
    table_notes = list(table_flats.values()) + list(table_sharps.values())

    # Search table to find root note
    midi_root = []
    for ix in range(0, len(table_midi_vals)):
        if table_notes[ix] == key:
            midi_root = table_midi_vals[ix]

    # Define major key values relative to root (1)
    major_key_vals = [0, 2, 4, 5, 7, 9, 11]  # [P1, M2, M3, P4, P5, M6, M7]

    # Define MIDI values list:
    midi_vals = range(midi_val_start, midi_val_end + 1)

    # Create a boolean list of elements to remove
    midi_val_remove = []
    for midi_val in midi_vals:
        # Degree of the scale in MIDI terms
        midi_degree = (midi_val - midi_root) % 12
        if midi_degree not in major_key_vals:
            midi_val_remove.append(True)
        else:
            midi_val_remove.append(False)

    # Create new midi values list
    new_midi_vals = []
    for bln, val in zip(midi_val_remove, midi_vals):
        if not bln:
            new_midi_vals.append(val)

    # Create list of note strings. Loop through MIDI values to populate notes:
    notes = []
    if key in ['c', 'g', 'd', 'a', 'e', 'b', 'fs']:
        for new_midi_val in new_midi_vals:

            # Populate natural notes:
            notes.append(populate_natural_sharps(new_midi_val))

            # Add sharps:
            if new_midi_val % 12 in [1, 3, 6, 8, 10]:  # Indicators of being sharp
                notes[-1] = notes[-1] + "s"

            # Make exception for the key of F#:
            if key == 'fs' and notes[-1] == "f":
                notes[-1] = 'es'

            # Add apostrophes:
            notes[-1] = add_octave_punctuation(new_midi_val, notes[-1])

    else:  # Assume flats used in key signature
        for new_midi_val in new_midi_vals:
            # Populate natural notes:
            notes.append(populate_natural_flats(new_midi_val))
            # Add flats:
            if new_midi_val % 12 in [1, 3, 6, 8, 10]:  # Indicators of being flat
                notes[-1] = notes[-1] + "f"
            # Add apostrophes:
            notes[-1] = add_octave_punctuation(new_midi_val, notes[-1])

    # Populate dictionary (/table)
    table = dict(zip(new_midi_vals, notes))
    return table


def find_interval_major(root_val, key, interval_degree):
    # Function for finding the notes a given interval away within a key

    # Create table. if 2nd, maximum interval of 2, if a third, 4, etc.
    if interval_degree >= 0:
        table = notes_in_major(root_val, root_val + interval_degree * 3, key)  # 3 is arbitrarily large enough
    else:
        table = notes_in_major(root_val + interval_degree * 3, root_val, key)

    midi_note = list(table)[interval_degree - 1]
    note = list(table.values())[interval_degree - 1]

    return midi_note, note


def string_notes(_string_midi_open):
    # Basic function for creating a dictionary of frets to MIDI values for strings
    _frets = list(range(0, 23))
    _notes = list(range(_string_midi_open, _string_midi_open + _frets[-1] + 1))
    _string_dict = {'frets': _frets, 'notes': _notes}

    return _string_dict


def create_answer_note_table(key):
    # Function for creating a reference table for answers to be displayed once the user has answered an exercise
    # question

    # Check if input key suggests sharps in the key signature
    if key in ['g', 'd', 'a', 'e', 'b', 'fs']:

        # If the key is F#, make an exception!
        if key == 'fs':
            table_answers = all_notes_sharps(1, 100, 'e')
        else:
            table_answers = all_notes_sharps(1, 100)
    else:
        table_answers = all_notes_flats(1, 100)

    return table_answers
