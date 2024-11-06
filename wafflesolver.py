import wafflestate
from copy import deepcopy
import os
import cycle_decomposition
import time
import heapq
from collections import Counter


start_time = time.time()
solve_counter = 0


def is_valid_candidate(waffle, candidate, key, rem_chars):
    rem_chars_counter = Counter(rem_chars)
    if key.startswith("i"):
        row = int(key[1:])
        for j, char in enumerate(candidate):
            if waffle[row][j] != " " and waffle[row][j] != char:
                return False
            if waffle[row][j] == " ":
                if rem_chars_counter[char] == 0:
                    return False
                rem_chars_counter[char] -= 1

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


def revert_candidate(waffle, original_state, rem_chars):
    for i, j in original_state:
        rem_chars.append(waffle[i][j])
        waffle[i][j] = " "


def recursive_solve(waffle, candidate_list, rem_chars, depth=0):
    # global solve_counter
    # solve_counter += 1
    # print("solve_counter", solve_counter)
    if len(rem_chars) == 0:
        return waffle

    for key, candidates in candidate_list:
        for candidate in candidates:
            original_state = apply_candidate_in_place(waffle, candidate, key, rem_chars)
            if not original_state:
                continue

            result = recursive_solve(waffle, candidate_list, rem_chars, depth + 1)
            if result:
                return result

            revert_candidate(waffle, original_state, rem_chars)

    return None


def better_candidates(waffle):

    simplified_array = []
    rem_chars = []
    all_chars = set()
    n = len(waffle[0])

    if n == 5:
        wordlist_unfiltered = wordlist_unfiltered_5
    elif n == 7:
        wordlist_unfiltered = wordlist_unfiltered_7

    candidate_list = {}
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

    # simple first wordlist filtering checking against available characters
    for w in wordlist_unfiltered:
        for i in range(len(waffle[0])):
            if w[i] not in all_chars:
                break
            else:
                if i == n - 1:
                    wordlist.append(w)

    for i in range(n)[0::2]:
        green_index_list = []
        yellow_must_have_index_list = []
        yellow_chars = []
        gray_index_list = []
        open_position_list = []
        pos = "i" + str(i)
        candidates = wordlist
        for j in range(n):
            char = waffle[i][j][0]
            colour = waffle[i][j][1]
            if colour == "g":
                green_index_list.append(j)
            elif colour == "y":
                yellow_chars.append(char)
                open_position_list.append(j)
                if j in range(n)[1::2]:
                    yellow_must_have_index_list.append(j)
            elif colour == "n":
                gray_index_list.append(j)
                open_position_list.append(j)

        candidates = [
            w
            for w in candidates
            if all(w[j] == waffle[i][j][0] for j in green_index_list)
        ]
        for index in yellow_must_have_index_list:

            candidates = [
                w
                for w in candidates
                if any(
                    w[j] == waffle[i][index][0]
                    for j in open_position_list
                    if j != index
                )
            ]
            #candidates = [w for w in candidates if w[index] != char]

        for index in gray_index_list:
            char = waffle[i][index][0]
            candidates = [w for w in candidates if w[index] != char]
            if char not in yellow_chars:
                candidates = [
                    w
                    for w in candidates
                    if not any(w[j] == char for j in open_position_list)
                ]

        candidate_list[pos] = candidates

    for j in range(n)[0::2]:
        green_index_list = []
        yellow_must_have_index_list = []
        yellow_chars = []
        gray_index_list = []
        open_position_list = []
        pos = "j" + str(j)
        candidates = wordlist
        for i in range(n):
            char = waffle[i][j][0]
            colour = waffle[i][j][1]
            if colour == "g":
                green_index_list.append(i)
            elif colour == "y":
                yellow_chars.append(char)
                open_position_list.append(i)
                if i in range(n)[1::2]:
                    yellow_must_have_index_list.append(i)
            elif colour == "n":
                gray_index_list.append(i)
                open_position_list.append(i)
        candidates = [
            w
            for w in candidates
            if all(w[i] == waffle[i][j][0] for i in green_index_list)
        ]

        for index in yellow_must_have_index_list:
            char = waffle[index][j][0]
            candidates = [
                w
                for w in candidates
                if any(w[i] == char for i in open_position_list if i != index)
            ]
            #candidates = [w for w in candidates if w[index] != char]

        for index in gray_index_list:
            char = waffle[index][j][0]
            candidates = [w for w in candidates if w[index] != char]
            if char not in yellow_chars:
                candidates = [
                    w
                    for w in candidates
                    if not any(w[i] == char for i in open_position_list)
                ]

        candidate_list[pos] = candidates

    sorted_candidate_list = sorted(
        candidate_list.items(), key=lambda item: len(item[1])
    )
    # for item in sorted_candidate_list:
    #    print(len(item[1]))
    return simplified_array, sorted_candidate_list, rem_chars


def get_candidates(waffle):

    simplified_array = []
    rem_chars = []
    all_chars = set()
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
    # for line in simplified_array:
    #    print(line)
    # wordlist = wordlist_unfiltered
    # simple first wordlist filtering checking against available characters
    for w in wordlist_unfiltered:
        for i in range(len(waffle[0])):
            if w[i] not in all_chars:
                break
            else:
                if i == n - 1:
                    wordlist.append(w)
    # filter by rows
    for i in range(n)[0::2]:
        # print("i", i)
        pos = "i" + str(i)
        candidates = wordlist

        for j in range(n):

            char = waffle[i][j][0]
            colour = waffle[i][j][1]
            if colour == "g":
                candidates = [w for w in candidates if w[j] == char]

            elif colour == "y":
                # yellow chars not at intersections allow candidates but not at current position
                if j in range(n)[1::2]:
                    candidates = [
                        w for w in candidates if (char in w) and (w[j] != char)
                    ]
                    # print("yellowfilter safe:", len(candidates))

                else:
                    # y at intersection might be part of a different word
                    # exclude current position
                    candidates = [w for w in candidates if (w[j] != char)]
                    # print("yellowfilter intersect:", len(candidates))
                    # print("candidates after filtering y intersect", candidates)
            # exclude grey at position
            elif colour == "n":
                candidates = [w for w in candidates if (w[j] != char)]
                # print("greyfilter:", len(candidates))
        # candidate_list.append([pos, candidates])
        candidate_list[pos] = candidates
        # print(len(candidates))
    # filter by columns
    for j in range(n)[0::2]:
        # print("j", j)
        maybelist = []
        grey_list = []
        pos = "j" + str(j)
        candidates = wordlist
        for i in range(n):
            char = waffle[i][j][0]
            colour = waffle[i][j][1]
            if colour == "g":
                candidates = [w for w in candidates if w[i] == char]
                # print("greenfilter", len(candidates))
            elif colour == "y":
                if i in range(n)[1::2]:
                    candidates = [w for w in candidates if char in w]
                    candidates = [w for w in candidates if (w[i] != char)]
                else:
                    candidates = [w for w in candidates if (w[i] != char)]
                # print("yellowfilter", len(candidates))
            elif colour == "n":
                candidates = [w for w in candidates if (w[i] != char)]
                # print("greyfilter", len(candidates))
        for i in range(n):
            colour = waffle[i][j][1]
            if colour in ["y", "g"]:
                maybelist.append(waffle[i][j][0])
        for i in range(n):
            colour = waffle[i][j][1]
            if colour == "n":
                grey_list.append(waffle[i][j][0])

        # filter candidates again for characters with grey and yellow
        # can't just throw out candidates after a grey character because they might already be green elsewhere
        # or there might be a two identical characters in an unsolved line, one grey, one yellow
        # like unsolved: "munii" for solved "minus", as one "i" is grey and one is yellow
        for no in grey_list:
            # print(grey_list,no)
            for idx, candidate in enumerate(candidates):
                # print(idx,candidate)
                # splitc = [c for c in candidate]
                if no not in candidate:
                    # if candidate in solutions:
                    # print("no not in splitc:", candidate)
                    pass

                else:
                    if no not in maybelist:
                        del candidates[idx]
                        # print("deleting", idx)
        # print("after grey list",len(candidates))

        candidate_list[pos] = candidates
    # sorted_candidate_list = candidate_list

    sorted_candidate_list = sorted(
        candidate_list.items(), key=lambda item: len(item[1])
    )
    # for item in sorted_candidate_list:
    #    print(len(item[1]))
    return simplified_array, sorted_candidate_list, rem_chars


def main(initial_state):
    startstate = deepcopy(initial_state)
    this_run_start_time = time.time()

    filter_start_time = time.time()

    waffle, sorted_candidates, rem_chars = better_candidates(initial_state)
    filter_end_time = time.time()

    # Calculate the total runtime
    filter_total_runtime = filter_end_time - filter_start_time

    # Print the total runtime
    print(f"Total filter runtime: {filter_total_runtime:.2f} seconds")
    solution = recursive_solve(waffle, sorted_candidates, rem_chars)

    scrambled = ""
    solution_string = ""
    print("Scrambled: ")
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
    cycle_decomposition.main(scrambled, solution_string)
    this_run_end_time = time.time()

    # Calculate the total runtime
    this_run_total_runtime = this_run_end_time - this_run_start_time

    # Print the total runtime
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
    # print("len dict", len(wordlist_unfiltered))
    wordlist_unfiltered_7 = [w for w in wordlist_unfiltered_7]
    # print("len dict", len(wordlist_unfiltered))
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
