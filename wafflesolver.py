import wafflestate
from copy import deepcopy
import os
import cycle_decomposition
import time
import heapq
from collections import Counter


start_time = time.time()
solve_counter = 0


# helper to check if a candidate word is valid
def is_valid_candidate(waffle, candidate, key, rem_chars):
    rem_chars_counter = Counter(rem_chars)
    if key.startswith("i"):
        row = int(key[1:])
        for j, char in enumerate(candidate):
            # there's a letter in the waffle already and it's wrong
            if waffle[row][j] != " " and waffle[row][j] != char:
                return False
            # empty space, do we still have required letter available?
            if waffle[row][j] == " ":
                if rem_chars_counter[char] == 0:
                    return False
                rem_chars_counter[char] -= 1
    # same but rows
    elif key.startswith("j"):
        col = int(key[1:])
        for i, char in enumerate(candidate):
            if waffle[i][col] != " " and waffle[i][col] != char:
                return False
            if waffle[i][col] == " ":
                if rem_chars_counter[char] == 0:
                    return False
                rem_chars_counter[char] -= 1

    return True


# helper function to apply a candidate word to the waffle
def apply_candidate_in_place(waffle, candidate, key, rem_chars):
    if not is_valid_candidate(waffle, candidate, key, rem_chars):
        return False

    original_state = []
    if key.startswith("i"):
        row = int(key[1:])
        for j, char in enumerate(candidate):
            if waffle[row][j] == " ":
                original_state.append((row, j))
                waffle[row][j] = char
                rem_chars.remove(char)

    elif key.startswith("j"):
        col = int(key[1:])
        for i, char in enumerate(candidate):
            if waffle[i][col] == " ":
                original_state.append((i, col))
                waffle[i][col] = char
                rem_chars.remove(char)

    return original_state


# helper function to revert a candidate word from the waffle when stepping back in the recursion
def revert_candidate(waffle, original_state, rem_chars):
    for i, j in original_state:
        rem_chars.append(waffle[i][j])
        waffle[i][j] = " "


def recursive_solve(waffle, candidate_list, rem_chars, depth=0):
    if len(rem_chars) == 0:
        return waffle

    for key, candidates in candidate_list:
        for candidate in candidates:
            # try to apply the candidate
            original_state = apply_candidate_in_place(waffle, candidate, key, rem_chars)
            if not original_state:
                continue
            # applying the candidate worked, we must go deeper!
            result = recursive_solve(waffle, candidate_list, rem_chars, depth + 1)
            if result:
                return result
            # that didn't work, revert the waffle and continue
            # all this applying and reverting is to avoid expensive deepcopying
            revert_candidate(waffle, original_state, rem_chars)

    return None


# this wordfilter thing is monstrous, you can also get away with simply filtering the wordlist by the starting grid.
# keeping candidates with green letters at the right location and removing all with yellow/grey at current location.
# but filtering correctly makes the seach afterwards much faster
# every unfiltered word can increase the bruteforcing time exponentially so it's totally worth it
def get_candidates(waffle):

    simplified_array = []
    rem_chars = []
    n = len(waffle[0])

    if n == 5:
        wordlist_unfiltered = wordlist_unfiltered_5
    elif n == 7:
        wordlist_unfiltered = wordlist_unfiltered_7

    candidate_list = {}
    rem_chars = []
    all_chars = set()
    n = len(waffle[0])

    # generate the simplified waffle skeleton with just the solved letters in it
    for row in waffle:
        simplified_row = []
        for pair in row:
            if pair[1] == "g":
                simplified_row.append(pair[0])
            else:
                if pair[1] != "g":
                    simplified_row.append(" ")
                    if pair[0] != " ":
                        rem_chars.append(pair[0])
            if pair[0] != " ":
                all_chars.add(pair[0])

        simplified_array.append(simplified_row)
    wordlist = []

    # simple first wordlist filtering against available characters
    for w in wordlist_unfiltered:
        for i in range(len(waffle[0])):
            if w[i] not in all_chars:
                break
            else:
                if i == n - 1:
                    wordlist.append(w)

    # filter by rows
    for i in range(n)[0::2]:
        pos = "i" + str(i)
        candidates = wordlist

        for j in range(n):
            char = waffle[i][j][0]
            colour = waffle[i][j][1]
            # green tile, keep all words with the same letter at this position
            if colour == "g":
                candidates = [w for w in candidates if w[j] == char]
            # yellow tile, remove all words with the yellow letter at this position
            elif colour == "y":
                # bit dirty, remoove all words with the same letter at this position and keep the ones that have it anywhere at all
                # this also leaves words where the yellow letter might be at a solved position but whatever
                # it'll be refiltered later, also we only should have candidates with correct greens anyway
                if j in range(n)[1::2]:
                    candidates = [
                        w for w in candidates if (char in w) and (w[j] != char)
                    ]
                # oh no an intersection, all we can do is remove all words with the same letter at this position
                # actually we could also filter both the row and column but eh
                # it would only make sense in the solving part, for filtering it's meaningless
                else:
                    candidates = [w for w in candidates if (w[j] != char)]
            # grey tile, remove all words with the same letter at this position
            elif colour == "n":
                candidates = [w for w in candidates if (w[j] != char)]
        # let's get fancy. track all greens, open positions, required yellows, greys. "must_have_yellow" are yellow tiles that must be in the candidate
        position_dict = {
            "green": [],
            "must_have_yellow": [],
            "open": [],
            "yellow_chars": [],
            "grey_index_list": [],
        }
        # fill the dictionary
        for j in range(n):
            colour = waffle[i][j][1]
            if colour == "g":
                position_dict["green"].append(j)
            elif colour == "y":
                position_dict["yellow_chars"].append(waffle[i][j][0])
                if j in range(n)[1::2]:
                    position_dict["must_have_yellow"].append(j)
                    position_dict["open"].append(j)
                else:
                    position_dict["open"].append(j)
            else:
                position_dict["grey_index_list"].append(j)
                position_dict["open"].append(j)

        # go through through all the yellow characters that must be in the word
        for index in position_dict["must_have_yellow"]:
            char = waffle[i][index][0]
            # remove all words which don't have the yellow character at one of the open positions, except the yellow one itself
            candidates = [
                w
                for w in candidates
                if any(w[j] == char for j in position_dict["open"] if j != index)
            ]
            candidates = [w for w in candidates if w[index] != char]
        # go through all the grey characters
        for index in position_dict["grey_index_list"]:
            char = waffle[i][index][0]
            # remove all words which have the grey character at this position
            candidates = [w for w in candidates if (w[index] != char)]
            # if the grey character is not in the yellow list, it's definitely not in the word at all
            # required because an unsolved line might have two identical characters, one yellow one grey.
            if char not in position_dict["yellow_chars"]:
                candidates = [
                    w
                    for w in candidates
                    if not any(w[j] == char for j in position_dict["open"])
                ]

        candidate_list[pos] = candidates

    # filter by columns
    # identical to the row filter, but with columns
    for j in range(n)[0::2]:

        pos = "j" + str(j)
        candidates = wordlist
        for i in range(n):
            char = waffle[i][j][0]
            colour = waffle[i][j][1]
            if colour == "g":
                candidates = [w for w in candidates if w[i] == char]
            elif colour == "y":
                if i in range(n)[1::2]:
                    candidates = [w for w in candidates if char in w]
                    candidates = [w for w in candidates if (w[i] != char)]
                else:
                    candidates = [w for w in candidates if (w[i] != char)]
            elif colour == "n":
                candidates = [w for w in candidates if (w[i] != char)]
        position_dict = {
            "green": [],
            "must_have_yellow": [],
            "open": [],
            "yellow_chars": [],
            "gray_index_list": [],
        }
        for i in range(n):
            colour = waffle[i][j][1]
            if colour == "g":
                position_dict["green"].append(i)
            elif colour == "y":
                position_dict["yellow_chars"].append(waffle[i][j][0])
                if i in range(n)[1::2]:
                    position_dict["must_have_yellow"].append(i)
                    position_dict["open"].append(i)
                else:
                    position_dict["open"].append(i)
            elif colour == "n":
                position_dict["gray_index_list"].append(i)
                position_dict["open"].append(i)

        for index in position_dict["must_have_yellow"]:
            char = waffle[index][j][0]
            candidates = [
                w
                for w in candidates
                if any(w[i] == char for i in position_dict["open"] if i != index)
            ]
            candidates = [w for w in candidates if w[index] != char]

        for index in position_dict["gray_index_list"]:
            char = waffle[index][j][0]
            candidates = [w for w in candidates if (w[index] != char)]
            if char not in position_dict["yellow_chars"]:
                candidates = [
                    w
                    for w in candidates
                    if not any(w[i] == char for i in position_dict["open"])
                ]

        candidate_list[pos] = candidates
    # sort the candidates by length so the recursion starts with the smallest wordlist
    sorted_candidate_list = sorted(
        candidate_list.items(), key=lambda item: len(item[1])
    )
    for key, candidates in sorted_candidate_list:
        print(key, len(candidates))
    return simplified_array, sorted_candidate_list, rem_chars


def main(initial_state):
    startstate = deepcopy(initial_state)
    this_run_start_time = time.time()

    filter_start_time = time.time()
    # waffle, sorted_candidates, rem_chars = simplistic_candidates(initial_state)
    waffle, sorted_candidates, rem_chars = get_candidates(initial_state)
    filter_end_time = time.time()

    # Calculate the total runtime
    filter_total_runtime = filter_end_time - filter_start_time

    # Print the total runtime
    print(f"Total filter runtime: {filter_total_runtime:.2f} seconds")
    solution = recursive_solve(waffle, sorted_candidates, rem_chars)

    scrambled = ""
    solution_string = ""
    for line in startstate:
        printline = ""
        for char in line:
            scrambled += char[0]
            printline += char[0] + " "
        print(printline)

    print(" ")
    print("Solution: ")
    for line in solution:
        printline = ""
        for char in line:
            solution_string += char
            printline += char + " "
        print(printline)
    # the cool part, let's find the shortest path:
    cycle_decomposition.main(scrambled, solution_string)
    this_run_end_time = time.time()

    # Calculate the total runtime
    this_run_total_runtime = this_run_end_time - this_run_start_time
    print(f"This run runtime: {this_run_total_runtime:.2f} seconds")
    print("- - - - - - -")


if __name__ == "__main__":
    # Set n to 5 or 7 depending on waffle size
    # wafflestates are in wafflestate.py
    cwd = os.getcwd()

    solutions_file = os.path.join(cwd, "wordlist_5.txt")
    with open(solutions_file) as file:
        wordlist_unfiltered_5 = set(line.strip() for line in file)
    wordlist_unfiltered_5 = [w.lower() for w in wordlist_unfiltered_5]

    solutions_file = os.path.join(cwd, "wordlist_7.txt")
    with open(solutions_file) as file:
        wordlist_unfiltered_7 = set(line.strip() for line in file)
    wordlist_unfiltered_7 = [w for w in wordlist_unfiltered_7]
    n = 5

    main(wafflestate.initial_state_five_1)
    main(wafflestate.initial_state_five_2)
    main(wafflestate.initial_state_five_3)
    main(wafflestate.initial_state_five_4)
    main(wafflestate.initial_state_five_5)
    main(wafflestate.initial_state_five_6)
    main(wafflestate.initial_state_five_7)
    main(wafflestate.initial_state_five_8)
    main(wafflestate.initial_state_five_9)
    main(wafflestate.initial_state_five_10)
    main(wafflestate.initial_state_five_11)
    main(wafflestate.initial_state_five_12)
    main(wafflestate.initial_state_five_13)
    main(wafflestate.initial_state_five_14)
    main(wafflestate.initial_state_five_15)
    main(wafflestate.initial_state_five_16)
    main(wafflestate.initial_state_five_17)
    main(wafflestate.initial_state_five_18)

    main(wafflestate.initial_state_seven_1)
    main(wafflestate.initial_state_seven_2)
    main(wafflestate.initial_state_seven_3)
    main(wafflestate.initial_state_seven_4)
    main(wafflestate.initial_state_seven_5)
    main(wafflestate.initial_state_seven_6)
    # Record the end time
    end_time = time.time()

    # Calculate the total runtime
    total_runtime = end_time - start_time

    # Print the total runtime
    print(f"Total runtime: {total_runtime:.2f} seconds")
