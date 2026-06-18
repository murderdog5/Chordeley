from datasets import load_dataset
import re
import collections

ds = load_dataset("ailsntua/Chordonomicon")
df = ds["train"].to_pandas()

result = []
for row in df["chords"]:
    chord_list_for_row = []
    for chord in row.split():
        if not re.fullmatch("<.*?>",chord):
            chord_list_for_row.append(chord)
    result.append(chord_list_for_row)

print(result[0])






