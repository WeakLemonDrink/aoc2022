import os
import re
import string

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

print("Day 1") # ----------------------------------------------------------------------------------
elf = 1
elf_dict = {}
elf_total_calories = 0

with open(os.path.join(DIR_PATH, "inputs", "day1.txt")) as fp:
    for line in fp:
        if line == "\n":
            # Save the calories and elf to the dict
            elf_dict[elf] = elf_total_calories
            # Reset the flags etc
            elf += 1
            elf_total_calories = 0

        else:
            elf_total_calories += int(line)

# Answer to day 1 part 1
max_calories = elf_dict[max(elf_dict, key=elf_dict.get)]
print(f"\tPart 1: Max calories carried by one elf {max_calories}")

# Answer to day 1 part 2
calories_per_elf_list = sorted(elf_dict.values())
total_for_top_3_elves = sum(calories_per_elf_list[-3:])
print(f"\tPart 2: Total calories carried by top 3 elves {total_for_top_3_elves}")


print("Day 2") # ----------------------------------------------------------------------------------
ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"

LOSE = 0
DRAW = 3
WIN = 6


my_shapes_map = {"X": ROCK, "Y": PAPER, "Z": SCISSORS}
opponent_shapes_map = {"A": ROCK, "B": PAPER, "C": SCISSORS}
outcomes_map = {"X": LOSE, "Y": DRAW, "Z": WIN}

shape_scores = {ROCK: 1, PAPER: 2, SCISSORS: 3}

outcomes = [
    # result, opponent shape, my shape
    {"result": LOSE, "opponent_shape": ROCK, "my_shape": SCISSORS},
    {"result": LOSE, "opponent_shape": PAPER, "my_shape": ROCK},
    {"result": LOSE, "opponent_shape": SCISSORS, "my_shape": PAPER},
    {"result": DRAW, "opponent_shape": ROCK, "my_shape": ROCK},
    {"result": DRAW, "opponent_shape": PAPER, "my_shape": PAPER},
    {"result": DRAW, "opponent_shape": SCISSORS, "my_shape": SCISSORS},
    {"result": WIN, "opponent_shape": ROCK, "my_shape": PAPER},
    {"result": WIN, "opponent_shape": PAPER, "my_shape": SCISSORS},
    {"result": WIN, "opponent_shape": SCISSORS, "my_shape": ROCK},
]

total_score = 0

with open(os.path.join(DIR_PATH, "inputs", "day2.txt")) as fp:
    for line in fp:
        rps_round = (opponent_shapes_map[line[0]], my_shapes_map[line[2]])
        my_shape_score = shape_scores[my_shapes_map[line[2]]]
        outcome_index = [(o["opponent_shape"], o["my_shape"]) for o in outcomes].index(rps_round)
        outcome_score = outcomes[outcome_index]["result"]

        total_score += my_shape_score + outcome_score

print(f"\tPart 1: Total score {total_score}")

total_score = 0

with open(os.path.join(DIR_PATH, "inputs", "day2.txt")) as fp:
    for line in fp:
        rps_round = (opponent_shapes_map[line[0]], outcomes_map[line[2]])
        outcome_score = outcomes_map[line[2]]
        outcome_index = [(o["opponent_shape"], o["result"]) for o in outcomes].index(rps_round)
        my_shape = outcomes[outcome_index]["my_shape"]
        my_shape_score = shape_scores[my_shape]

        total_score += my_shape_score + outcome_score

print(f"\tPart 2: Total score {total_score}")


print("Day 3") # ----------------------------------------------------------------------------------
priority_scores_dict = {}
priority_sum = 0

for i, score in enumerate(string.ascii_lowercase, start=1):
    priority_scores_dict.update({score.lower(): i})
    priority_scores_dict.update({score.upper(): i+26})

with open(os.path.join(DIR_PATH, "inputs", "day3.txt")) as fp:
    for rucksack in fp:
        compartment_length = int(len(rucksack) / 2)

        compartment_1 = set(rucksack[:compartment_length])
        compartment_2 = set(rucksack[compartment_length:])

        error_item = compartment_1 & compartment_2

        priority_sum += priority_scores_dict[error_item.pop()]


print(f"\tPart 1: Total priority score {priority_sum}")

priority_sum = 0

with open(os.path.join(DIR_PATH, "inputs", "day3.txt")) as fp:
    group = []
    priority_sum = 0

    for rucksack in fp:
        group.append(set(rucksack.strip()))

        if len(group) == 3:
            badge_set = group[0] & group[1] & group[2]

            priority_sum += priority_scores_dict[badge_set.pop()]
            group = []

print(f"\tPart 2: Total badge priority score {priority_sum}")


print("Day 4") # ----------------------------------------------------------------------------------

pair_str_regex = re.compile(r"(?P<elf_1_start>\d+)-(?P<elf_1_end>\d+),(?P<elf_2_start>\d+)-(?P<elf_2_end>\d+)")
total_fully_contained = 0
total_overlaps = 0

with open(os.path.join(DIR_PATH, "inputs", "day4.txt")) as fp:
    for line in fp:
        match = re.search(pair_str_regex, line.strip())

        if match:
            assignment_1 = {i for i in range(int(match.group("elf_1_start")), int(match.group("elf_1_end"))+1)}
            assignment_2 = {i for i in range(int(match.group("elf_2_start")), int(match.group("elf_2_end"))+1)}

            assignment_intersection = assignment_1 & assignment_2

            if assignment_intersection == assignment_1 or assignment_intersection == assignment_2:
                total_fully_contained += 1
                total_overlaps += 1
            elif any(assignment_intersection):
                total_overlaps += 1
        else:
            print(f"match for {line} not found.")

print(f"\tPart 1: Total assignments fully contained {total_fully_contained}")
print(f"\tPart 2: Total overlaps {total_overlaps}")


print("Day 5") # ----------------------------------------------------------------------------------

moves = []
stacks_9000 = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
stacks_9001 = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
part_1_finished_word = ""
part_2_finished_word = ""

move_str_regex = re.compile(r"move (?P<number_of_steps>\d+) from (?P<stack_start>\d+) to (?P<stack_end>\d+)")

with open(os.path.join(DIR_PATH, "inputs", "day5.txt")) as fp:
    for line in fp:
        match = re.search(move_str_regex, line)

        if match:
            moves.append(
                {
                    "number_of_steps": int(match.group("number_of_steps")),
                    "stack_start": int(match.group("stack_start")),
                    "stack_end": int(match.group("stack_end")),
                }
            )
        else:
            number_of_slices = len(line) // 4
            slice_start = 0

            for i in range(number_of_slices):
                if line[slice_start] == "[":
                    stacks_9000[i+1].insert(0, line[slice_start+1])
                    stacks_9001[i+1].insert(0, line[slice_start+1])

                slice_start += 4

# For part 1
for move in moves:
    for step in range(move["number_of_steps"]):
        package = stacks_9000[move["stack_start"]].pop()
        stacks_9000[move["stack_end"]].append(package)

for _, value in stacks_9000.items():
    part_1_finished_word += value[-1]

print(f"\tPart 1: {part_1_finished_word}")

# For part 2
for move in moves:
    stack_start = stacks_9001[move["stack_start"]]
    stack_end = stacks_9001[move["stack_end"]]
    packages_to_move = stack_start[-move["number_of_steps"]:]

    # Update the lists
    stacks_9001.update(
        {
            move["stack_start"]: stack_start[:-move["number_of_steps"]],
            move["stack_end"]: stack_end + packages_to_move,
        }
    )

for _, value in stacks_9001.items():
    part_2_finished_word += value[-1]

print(f"\tPart 2: {part_2_finished_word}")


print("Day 6") # ----------------------------------------------------------------------------------
def get_number_of_chars_processed(marker_length):
    with open(os.path.join(DIR_PATH, "inputs", "day6.txt")) as fp:
        for line in fp:
            for i in range(len(line)):
                if i < len(line) - (marker_length - 1):
                    marker = line[i:i + marker_length]
                    number_of_unique_chars = len(set(marker))

                    if number_of_unique_chars == marker_length:
                        number_of_chars_processed = i + marker_length
                        break

    return number_of_chars_processed

part_1_get_number_of_chars_processed = get_number_of_chars_processed(4)
print(f"\tPart 1: {part_1_get_number_of_chars_processed} chars need to be processed")

part_2_get_number_of_chars_processed = get_number_of_chars_processed(14)
print(f"\tPart 2: {part_2_get_number_of_chars_processed} chars need to be processed")
