import wafflestate
import os
import cycle_decomposition
import time
from copy import deepcopy
from collections import Counter

# 05-2025
# fastest one so far
# the part of "available characters per position" could still be improved but it's already quite fast


def main(waffle):
    #print("Initial state:", waffle)
    start_main_time = time.time()
    n = len(waffle)
    if n == 5:
        wordlist_unfiltered = wordlist_unfiltered_5
    elif n == 7:
        wordlist_unfiltered = wordlist_unfiltered_7

    solved_waffle = solve(waffle, wordlist_unfiltered)
    end_main_time = time.time()
    print("main time:", end_main_time-start_main_time)
    scrambled = "" 
    solution_string = ""
    for line in waffle:
        printline = ""
        for char in line:
            scrambled += char[0]
            printline += char[0] + " "
        print(printline)

    print(" ")
    print("Solution: ")
    for line in solved_waffle:
        printline = ""
        for char in line:
            solution_string += char
            printline += char + " "
        print(printline)
    # the actually interesting part, finding the least amount of swaps through cycle decomposition
    cycle_decomposition.main(scrambled, solution_string)

    
def recursive_solve(waffle_skeleton, candidates, rem_chars, n, sorted_candidate_indices, depth=0):
    
    # base case: solved if all remaining letters are used up
    if all(v == 0 for v in rem_chars.values()):
        return [row[:] for row in waffle_skeleton]  # Return a copy of the solved board
    # select candidate list based on sorted_candidate_indices
    length, orientation, index = sorted_candidate_indices[depth]
    
    # orientation: 0=row, 1=col
    for word in candidates[orientation][index]:
        # track changes for rollback
        changed = []
        can_apply = True
        if orientation == 0:  # Row
            for j in range(n):
                if waffle_skeleton[index][j] == " ":
                    if rem_chars[word[j]] == 0:
                        can_apply = False
                        break
                    changed.append((index, j, waffle_skeleton[index][j]))
                    waffle_skeleton[index][j] = word[j]
                    rem_chars[word[j]] -= 1
                elif waffle_skeleton[index][j] != word[j]:
                    can_apply = False
                    break
        else:  # Column
            for i in range(n):
                if waffle_skeleton[i][index] == " ":
                    if rem_chars[word[i]] == 0:
                        can_apply = False
                        break
                    changed.append((i, index, waffle_skeleton[i][index]))
                    waffle_skeleton[i][index] = word[i]
                    rem_chars[word[i]] -= 1
                elif waffle_skeleton[i][index] != word[i]:
                    can_apply = False
                    break

        if can_apply:
            result = recursive_solve(waffle_skeleton, candidates, rem_chars, n, sorted_candidate_indices, depth+1)
            if result:
                return result

        # rollback changes
        for i, j, prev in changed:
            rem_chars[waffle_skeleton[i][j]] += 1
            waffle_skeleton[i][j] = prev

    return None  # no solution found at this branch
    

def solve(waffle,wordlist_unfiltered):
    # Set up the skeleton waffle with only the green letters
    # and empty spaces for the rest.
    # Collect both the remaining and all existing characters.
    simplified_array = []
    rem_chars = Counter()
    rem_chars_set = set()
    all_chars = set()
    for row in waffle:
        simplified_row = []
        for pair in row:
            if pair[1] == "g":
                simplified_row.append(pair[0])
            else:
                simplified_row.append(" ")
                if pair[0] != " ":
                    rem_chars[pair[0]] += 1
                    rem_chars_set.add(pair[0])
            if pair[0] != " ":
                all_chars.add(pair[0])
        simplified_array.append(simplified_row)
    n = len(waffle[0])
    # simple first naive wordlist filtering against available characters
    wordlist = []
    for w in wordlist_unfiltered:
        for i in range(n):
            if w[i] not in all_chars:
                break
            else:
                if i == n - 1:
                    wordlist.append(w)
    wordlist_unfiltered = wordlist

    # Initialize a 2D array of sets for possible characters at each position
    position_chars = [[set() for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            # green means there's only 1 possible character
            if waffle[i][j][1] == "g":
                position_chars[i][j].add(waffle[i][j][0])
                continue
            else:
                # we assume every remaining character is possible at a free space, then slim it down
                temp_possible_chars_vert = deepcopy(rem_chars_set)
                temp_possible_chars_hori = deepcopy(rem_chars_set)
                # if current position is yellow, remove
                if waffle[i][j][1] == "y":
                    if waffle[i][j][0] in temp_possible_chars_hori:
                        temp_possible_chars_hori.remove(waffle[i][j][0])
                
                # find yellows and store them to account for cases of the same letter appearing 2 times as yellow and grey
                # check horizontal
                if i % 2 == 0:
                    yellows_in_line = set()
                    for k in range(n):
                        if waffle[i][k][1] == "y":
                            yellows_in_line.add(waffle[i][k][0])
                    for k in range(n):
                        if waffle[i][k][1] == "n" and waffle[i][k][0] not in yellows_in_line:
                            if waffle[i][k][0] in temp_possible_chars_hori:
                                temp_possible_chars_hori.remove(waffle[i][k][0])

                # check vertical
                if j % 2 == 0:
                    yellows_in_line = set()
                    for k in range(n):
                        if waffle[k][j][1] == "y":
                            yellows_in_line.add(waffle[k][j][0])
                    for k in range(n):
                        if waffle[k][j][1] == "n" and waffle[k][j][0] not in yellows_in_line:
                            if waffle[k][j][0] in temp_possible_chars_vert:
                                temp_possible_chars_vert.remove(waffle[k][j][0])
                # Add the remaining characters to the position
                position_chars[i][j] = set(temp_possible_chars_vert.intersection(temp_possible_chars_hori))

    candidates = [ [set() for _ in range(n)] for _ in range(2) ]
    # candidates for each row
    for i in range(n)[0::2]:
        must_have_yellow = {}
        open_positions = []
        slimmed_list = wordlist_unfiltered

        for j in range(n):
            slimmed_list = [word for word in slimmed_list if word[j] in position_chars[i][j]]

            if waffle[i][j][1] != "g":
                open_positions.append(j)
        # get must have yellows
        for j in range(n)[1::2]:
            if waffle[i][j][1] == "y":
                if waffle[i][j][0] not in must_have_yellow:
                    must_have_yellow[waffle[i][j][0]] = set()
                for o in open_positions:
                    if o != j:
                        must_have_yellow[waffle[i][j][0]].add(o)
        # check wordlist against yellow chars that must appear in the word
        if must_have_yellow:
            for char in must_have_yellow:
                slimmed_list = [word for word in slimmed_list if any(word[pos] == char for pos in must_have_yellow[char] )]
                
          
        candidates[0][i] = slimmed_list
    # candidates for each column
    for j in range(n)[0::2]:
        must_have_yellow = {}
        open_positions = []
        slimmed_list = wordlist_unfiltered
        
        for i in range(n):
            slimmed_list = [word for word in slimmed_list if word[i] in position_chars[i][j]]
      
            if waffle[i][j][1] != "g":
                open_positions.append(i)
        # get must have yellows
        for i in range(n)[1::2]:
            if waffle[i][j][1] == "y":
                if waffle[i][j][0] not in must_have_yellow:
                    must_have_yellow[waffle[i][j][0]] = set()
                for o in open_positions:
                    if o != i:
                        must_have_yellow[waffle[i][j][0]].add(o)
  
        if must_have_yellow:
            for char in must_have_yellow:
                slimmed_list = [word for word in slimmed_list if any(word[pos] == char for pos in must_have_yellow[char] )]
                
        candidates[1][j] = slimmed_list


    # update the possible chars at intersections from the candidates
    update_position_chars(position_chars, candidates, n)
    # update candidates based on updated position chars
    updated_candidates = update_candidates(position_chars,candidates,n)
    
    # sort candidate lists by length for faster recursive solving
    sorted_candidate_indices = []
    for orientation,candidate_list in enumerate(candidates):
        for index, wordlist in enumerate(candidate_list):
            if len(wordlist) != 0:
                sorted_candidate_indices.append([len(wordlist),orientation,index])
    
    sorted_candidate_indices = sorted(sorted_candidate_indices)
    solved_waffle = recursive_solve(simplified_array, updated_candidates, rem_chars, n, sorted_candidate_indices)

    return solved_waffle


def update_position_chars(position_chars, candidates, n):
    # Update position_chars based on candidate words
    for i in range(n)[0::2]:
        for j in range(n)[0::2]: 
            temp_possible_chars_vert = set()
            temp_possible_chars_hori = set()
            for word in candidates[0][i]:
                temp_possible_chars_hori.add(word[j])
            for word in candidates[1][j]:
                temp_possible_chars_vert.add(word[i])
                         
            position_chars[i][j] = set(temp_possible_chars_vert.intersection(temp_possible_chars_hori))
    return position_chars

def update_candidates(position_chars, candidates, n):
    # Update candidates based on position_chars
    for i in range(n)[0::2]:
        if len(candidates[0][i]) == 1:
            pass
        else:
            for j in range(n):
                candidates[0][i] = [word for word in candidates[0][i] if word[j] in position_chars[i][j]]
    
    for j in range(n)[0::2]:
        if len(candidates[1][j]) == 1:
            pass
        else:
            for i in range(n):
                candidates[1][j] = [word for word in candidates[1][j] if word[i] in position_chars[i][j]]
    return candidates


if __name__ == "__main__":
    start_time = time.time()
    cwd = os.getcwd()

    solutions_file = os.path.join(cwd, "wordlist_5.txt")
    with open(solutions_file) as file:
        wordlist_unfiltered_5 = set(line.strip() for line in file)
    wordlist_unfiltered_5 = [w.lower() for w in wordlist_unfiltered_5]

    solutions_file = os.path.join(cwd, "wordlist_7.txt")
    with open(solutions_file) as file:
        wordlist_unfiltered_7 = set(line.strip() for line in file)
    wordlist_unfiltered_7 = [w.lower() for w in wordlist_unfiltered_7]

    # wafflestates are in wafflestate.py
    main(wafflestate.initial_state_five_1)
    main(wafflestate.initial_state_five_4)
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
    main(wafflestate.initial_state_five_arxiv)
    main(wafflestate.initial_state_seven_1)
    main(wafflestate.initial_state_seven_2)
    main(wafflestate.initial_state_seven_3)
    main(wafflestate.initial_state_seven_4)
    main(wafflestate.initial_state_seven_5)
    main(wafflestate.initial_state_seven_6)

    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"Total runtime: {total_runtime:.2f} seconds")