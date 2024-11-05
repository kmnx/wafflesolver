import wafflestate
from copy import deepcopy
import os
import cycle_decomposition
import time
import heapq
from collections import Counter


start_time = time.time()
solve_count = 0


        
    return True
def is_valid_candidate(waffle, candidate, key, rem_chars):
    rem_chars_counter = Counter(rem_chars)
    if key.startswith("i"):
        row = int(key[1:])
        for j, char in enumerate(candidate):
            if waffle[row][j] != ' ' and waffle[row][j] != char:
                return False
            if waffle[row][j] == ' ':
                if rem_chars_counter[char] == 0:
                    return False
                rem_chars_counter[char] -= 1

    elif key.startswith("j"):
        col = int(key[1:])
        for i, char in enumerate(candidate):
            if waffle[i][col] != ' ' and waffle[i][col] != char:
                return False
            if waffle[i][col] == ' ':
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
        #if waffle[i][j] != " ":
        rem_chars.append(waffle[i][j])
        waffle[i][j] = " "
def recursive_solve(waffle, candidate_list, rem_chars, depth=0):
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
def refilter(candidates):
    for list in candidates:
        print(list[0],len(list[1]))
    for candidatelist in candidates:
        zero = set()
        two = set()
        four = set()
        six = set()
        current_orientation = candidatelist[0][0]
        current_char_index = int(candidatelist[0][1])
        for candidate in candidatelist[1]:
            zero.add(candidate[0])
            two.add(candidate[2])
            four.add(candidate[4])
            six.add(candidate[6])
            #print("Zero:", zero)
        if candidatelist[0][0] == "i":
            x = int(candidatelist[0][1])
            for other_candidatelist in candidates:
                if other_candidatelist[0][0] == "j":
                    other_index = int(other_candidatelist[0][1])
                    # j0 j2 j4 j6
                    # we need to compare candidate from j with i-position
                    # so since j is 2
                    # we need to compare it with x
                    if other_index == 0:
                        for other_candidate in other_candidatelist[1]:
                            if other_candidate[x] not in zero:
                                other_candidatelist[1].remove(other_candidate)
                    elif other_index == 2:
                        for other_candidate in other_candidatelist[1]:
                            if other_candidate[x] not in two:
                                other_candidatelist[1].remove(other_candidate)
                    elif other_index == 4:
                        for other_candidate in other_candidatelist[1]:
                            if other_candidate[x] not in four:
                                other_candidatelist[1].remove(other_candidate)
                    elif other_index == 6:
                        for other_candidate in other_candidatelist[1]:
                            if other_candidate[x] not in six:
                                other_candidatelist[1].remove(other_candidate)
                                                            
        elif candidatelist[0][0] == "j":
            y = int(candidatelist[0][1])
            for other_candidatelist in candidates:
                if other_candidatelist[0][0] == "i":
                    other_index = int(other_candidatelist[0][1])
                    if other_index == 0:
                        for other_candidate in other_candidatelist[1]:
                            if other_candidate[y] not in zero:
                                other_candidatelist[1].remove(other_candidate)
                    elif other_index == 2:
                        for other_candidate in other_candidatelist[1]:
                            if other_candidate[y] not in two:
                                #print(other_candidate[y])
                                #print(two)
                                other_candidatelist[1].remove(other_candidate)
                    elif other_index == 4:
                        for other_candidate in other_candidatelist[1]:
                            if other_candidate[y] not in four:
                                other_candidatelist[1].remove(other_candidate)
                    elif other_index == 6:
                        for other_candidate in other_candidatelist[1]:
                            if other_candidate[y] not in six:
                                other_candidatelist[1].remove(other_candidate)
                    
                        
        print("wha")
            

        #
        
        
    for list in candidates:
        print(list[0],len(list[1]))
    return candidates
def get_candidates(waffle):

    simplified_array = []
    rem_chars = []
    all_chars = set()
    n = len(waffle[0])
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


    cwd = os.getcwd()
    if n == 5:
        solutions_file = os.path.join(cwd, "wordlist_5.txt")
        with open(solutions_file) as file:
            wordlist_unfiltered = set(line.strip() for line in file)
        wordlist_unfiltered = [w.lower() for w in wordlist_unfiltered if len(w) == 5]

    elif n == 7:
        solutions_file = os.path.join(cwd, "wordlist_english_dict.txt")
        with open(solutions_file) as file:
            wordlist_unfiltered = set(line.strip() for line in file)
        print("len dict", len(wordlist_unfiltered))
        wordlist_unfiltered = [w.lower() for w in wordlist_unfiltered if len(w) == 7]
        print("len dict", len(wordlist_unfiltered))

    candidate_list = {}
    rem_chars = []
    all_chars = set()
    n = len(waffle[0])
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
    wordlist = []
    for w in wordlist_unfiltered:
        for i in range(len(waffle[0])):
            if w[i] not in all_chars:
                break
            else:
                if i == n-1:
                    wordlist.append(w)

    for i in range(n)[0::2]:
        pos = "i" + str(i)
        candidates = wordlist
        for j in range(n):
            char = waffle[i][j][0]
            colour = waffle[i][j][1]
            if colour == "g":
                candidates = [w for w in candidates if w[j] == char]
                # print("candidates after filtering green", candidates)
            elif colour == "y":
                # yellow chars not at intersections must be in candidates
                if j in range(n)[1::2]:
                    candidates = [w for w in candidates if char in w]
                    # but must be excluded at current position
                    # print("candidates after filtering y", candidates)
                    candidates = [w for w in candidates if (w[j] != char)]
                    # print("candidates after filtering y at pos", candidates)
                else:
                    # y at intersection might be part of a different word
                    # exclude current position
                    candidates = [w for w in candidates if (w[j] != char)]
                    # print("candidates after filtering y intersect", candidates)
            # exclude grey at position
            elif colour == "n":
                candidates = [w for w in candidates if (w[j] != char)]
        # candidate_list.append([pos, candidates])
        candidate_list[pos] = candidates
    # filter columns
    for j in range(n)[0::2]:
        maybelist = []
        nolist = []
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
        for i in range(n):
            colour = waffle[i][j][1]
            if colour in ["y", "g"]:
                maybelist.append(waffle[i][j][0])
        for i in range(n):
            colour = waffle[i][j][1]
            if colour == "n":
                nolist.append(waffle[i][j][0])

        
        for no in nolist:
            for idx, candidate in enumerate(candidates):
                #if candidate in solutions:
                    #print("solution:", candidate)
                splitc = [c for c in candidate]
                if no not in splitc:
                    #if candidate in solutions:
                        #print("no not in splitc:", candidate)
                    pass

                else:
                    if no in maybelist:
                        pass
                    else:
                        del candidates[idx]

        candidate_list[pos] = candidates
    
    sorted_candidate_list = sorted(candidate_list.items(), key=lambda item: len(item[1]))
    return simplified_array, sorted_candidate_list, rem_chars



def main(initial_state):
    startstate = deepcopy(initial_state)
    waffle, sorted_candidates, rem_chars = get_candidates(initial_state)
    solution = recursive_solve(waffle,sorted_candidates,rem_chars)
    
    scrambled = ""
    solution_string = ""
    for line in startstate:
        for char in line:
            scrambled += char[0]
    for line in solution:
        print(line)
        for char in line:
            solution_string += char
    cycle_decomposition.main(scrambled, solution_string)

    #print("Element with Shortest Candidates:", shortest_candidates)
    
if __name__ == "__main__":
    # Set n to 5 or 7 depending on waffle size
    # wafflestates are in wafflestate.py
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
    #main(wafflestate.initial_state_seven_5)
    #main(wafflestate.initial_state_seven_6)
    # Record the end time
    end_time = time.time()

    # Calculate the total runtime
    total_runtime = end_time - start_time

    # Print the total runtime
    print(f"Total runtime: {total_runtime:.2f} seconds")
    