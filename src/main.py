import mido

# notes = [(frequency, duration), ...]


def track_to_notes(mid):
    notes = []

    track = mid.tracks[0]

    for i, message in enumerate(track):
        if i == len(track) - 1:
            break

        if message.type == "note_on" and message.velocity > 0:
            note = (
                round(note_to_frequency(message.note)),
                round(
                    mido.tick2second(track[i + 1].time, mid.ticks_per_beat, 500000), 2
                ),
            )
            notes.append(note)
        elif message.type == "note_off" or (
            message.type == "note_on" and message.velocity == 0
        ):
            note = (
                None,
                round(
                    mido.tick2second(track[i + 1].time, mid.ticks_per_beat, 500000), 2
                ),
            )
            notes.append(note)

    return notes


def note_to_frequency(pitch):
    return 440 * (2 ** ((pitch - 69) / 12))


def notes_to_circuit_python(notes):
    code = "import time\n"
    code += "import board\n"
    code += "import pwmio\n"
    code += "\n"
    code += "buzzer = pwmio.PWMOut(board.D10, variable_frequency=True)\n"
    code += "\n"
    code += f"notes = {notes}\n"
    code += "\n"
    code += "def play_notes(notes):\n"
    code += "    for note in notes:\n"
    code += "        if note[0] is None:\n"
    code += "            buzzer.duty_cycle = 0\n"
    code += "        else:\n"
    code += "            buzzer.duty_cycle = 2**15\n"
    code += "            buzzer.frequency = note[0]\n"
    code += "        time.sleep(note[1])\n"
    code += "\n"
    code += "play_notes(notes)\n"

    return code


if "__main__" == __name__:
    file_path = "data/test.mid"
    save_path = "data/test.py"
    mid = mido.MidiFile(file_path)
    notes = track_to_notes(mid)
    code = notes_to_circuit_python(notes)

    with open(save_path, "w") as f:
        f.write(code)

    print(f"saved to {save_path}")
    print("=" * 20)
    print(code)
    print("=" * 20)
    print("Code generated successfully!")
