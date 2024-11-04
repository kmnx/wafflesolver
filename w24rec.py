import wafflestate
from copy import deepcopy
import os
import cycle_decomposition
import time
import heapq

start_time = time.time()
solve_count = 0
def get_candidates(waffle, wordlist):
    #waffle.print_state()
    simplified_array = waffle
    candidate_list = {}
    state = waffle
    
    i0,i2,i4,i6,j0,j2,j4,j6 = [],[],[],[],[],[],[],[]
    for i in range(0, len(waffle), 2):
        for word in wordlist:
            #print(word)
            for j in range(len(waffle)):
                #print(word[j])
                #print(waffle[i][j])
                if waffle[i][j] == word[j] or waffle[i][j] == ' ':
                    if j == len(waffle[0])-1:
                        if i == 0:
                            i0.append(word)
                        elif i == 2:
                            i2.append(word)
                        elif i == 4:
                            i4.append(word)
                        elif i == 6:
                            i6.append(word)
                else:
                    break
    for j in range(0, len(waffle), 2):    
        for word in wordlist:
            #print(word)
            #if word == "tonight"   :
                #print("tonight")
            for i in range(len(waffle)):
                #print(word[i])
                #print(waffle[i][j])
                if waffle[i][j] == word[i] or waffle[i][j] == ' ':
                    if i == len(waffle[0])-1:
                        if j == 0:
                            j0.append(word)
                        elif j == 2:
                            j2.append(word)
                        elif j == 4:
                            j4.append(word)
                        elif j == 6:
                            j6.append(word)
                else:
                    break
    for array in [i0,i2,i4,i6,j0,j2,j4,j6]:
        # sort each alphabetically
        array.sort()
    if len(waffle) == 5:
        candidates = {"i0":i0,"i2":i2,"i4":i4,"j0":j0,"j2":j2,"j4":j4}
    elif len(waffle) == 7:
        candidates = {"i0":i0,"i2":i2,"i4":i4,"j0":j0,"j2":j2,"j4":j4,"i6":i6,"j6":j6}
    return candidates


def prep(waffle):
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

    #print("Open Chars:", rem_chars)
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

   
    # wordlist preprocessing, keep only words with chars existing in waffle
    print("len wordlist pre filter", len(wordlist_unfiltered))
    wordlist = []
    for w in wordlist_unfiltered:
        for i in range(len(waffle[0])):
            if w[i] not in all_chars:
                break
            else:
                if i == n-1:
                    wordlist.append(w)
    print("len wordlist post filter", len(wordlist))

    # more preprocessing, per line
    candidate_list = get_candidates(simplified_array, wordlist)
    sorted_candidate_list = sorted(candidate_list.items(), key=lambda item: len(item[1]))
    #print(candidate_list)
    sorted_candidate_list = [list(item) for item in sorted_candidate_list]
    print(simplified_array)
    
    return simplified_array, sorted_candidate_list, rem_chars
def is_solved(waffle):
    for i in range(len(waffle)):
        for j in range(len(waffle[0])):
            if waffle[i][j] == " " and [i,j] not in [[1,1],[1,3],[1,5],[3,1],[3,3],[3,5],[5,1],[5,3],[5,5]]:
                return False
        
    return True
def is_valid_candidate(waffle, candidate, key, rem_chars):
    if key.startswith("i"):
        row = int(key[1:])
        for j, char in enumerate(candidate):
            if (waffle[row][j] != ' ' and waffle[row][j] != char) or (waffle[row][j] == ' ' and char not in rem_chars):
                return False
    elif key.startswith("j"):
        col = int(key[1:])
        for i, char in enumerate(candidate):
            if (waffle[i][col] != ' ' and waffle[i][col] != char) or (waffle[i][col] == ' ' and char not in rem_chars):
                return False
    return True


def apply_candidate(waffle, candidate, key, rem_chars):
    #print("Waffle at start apply:")
    #for line in waffle:
    #    print(line)
    if not is_valid_candidate(waffle, candidate, key,rem_chars):
        return None, None
    new_waffle = deepcopy(waffle)
    new_rem_chars = deepcopy(rem_chars)
    if key.startswith("i"):
        row = int(key[1:])
        for j, char in enumerate(candidate):
            if new_waffle[row][j] != char:
                if new_waffle[row][j] == " ":
                    if char in new_rem_chars:
                        new_waffle[row][j] = char
                        new_rem_chars.remove(char)
                    else:
                        return None,None
                else:
                    return None,None
    elif key.startswith("j"):
        col = int(key[1:])
        for i, char in enumerate(candidate):
            if new_waffle[i][col] != char:
                if new_waffle[i][col] == " ":
                    if char in new_rem_chars:
                        new_waffle[i][col] = char
                        new_rem_chars.remove(char)
                    else:
                        return None,None
                else:
                    return None,None

    return new_waffle,new_rem_chars
def recursive_solve(waffle,candidate_list,rem_chars):
    global solve_count
    solve_count += 1
    if len(rem_chars) == 0:
        return waffle
   
    for key, candidates in candidate_list:
        new_candidate_list = deepcopy(candidate_list)
        new_candidate_list.pop(0)
        new_rem_chars = deepcopy(rem_chars)
        for index,candidate in enumerate(candidates):
            new_waffle, real_new_rem_chars = apply_candidate(waffle, candidate, key, new_rem_chars)
            if new_waffle is None:
                continue
            else:
                result = recursive_solve(new_waffle, new_candidate_list,real_new_rem_chars)
                if result:
                    return result
    return None


def solve(rawwaffle, sorted_candidates,rem_chars):
    #print(rawwaffle, sorted_candidates)
    length = len(rawwaffle[0])
    big_stack = []
    startwaffle = deepcopy(rawwaffle)
    #big_stack.append([rawwaffle,sorted_candidates,rem_chars])
    priority = -len(rem_chars)

    heapq.heappush(big_stack, (priority, [startwaffle, sorted_candidates, rem_chars]))

    while big_stack:
        #pack = big_stack.pop(0)
        pack = heapq.heappop(big_stack)
        safe_waffle, safe_sorted_candidates,safe_rem_chars = pack[1][0],pack[1][1],pack[1][2]
        current_candidates = deepcopy(safe_sorted_candidates)
        #print(safe_waffle, safe_sorted_candidates,safe_rem_chars)
        line_candidates = current_candidates.pop(0)
        #print(line_candidates)
        for word in line_candidates[1]:
            next_candidates = current_candidates
            currentwaffle = deepcopy(safe_waffle)
            current_rem_chars = deepcopy(safe_rem_chars)
            
            #print(word)
            direction = line_candidates[0][0]
            main_index = line_candidates[0][1]
            #print(main_index)
            ##print(direction)
            if direction == "i":
                i = int(line_candidates[0][1])
                for n in range(length):
                    # break if a char is different
                    if word[n] != currentwaffle[i][n]:
                        if currentwaffle[i][n] == " ":
                            if word[n] in current_rem_chars:
                                currentwaffle[i][n] = word[n]
                                current_rem_chars.remove(word[n])
                            else:
                                break
                        else:
                            break
                    

                    if (n == (length-1)):
                        if len(current_rem_chars) == 0 and len(current_candidates) == 0:
                            #print(currentwaffle)
                            return(currentwaffle)
                        else:
                            #print("-----solved a line------")
                            #for line in currentwaffle:
                            #    print(line)
                            #print("word is", word)
                            #print("rem chars", current_rem_chars)
                            #print("next candidates", next_candidates)
                            #print("len next candidates", len(next_candidates))
                            #print(currentwaffle,current_candidates,current_rem_chars)
                            #big_stack.append([currentwaffle,next_candidates,current_rem_chars])
                            priority = -len(current_rem_chars)

                            heapq.heappush(big_stack, (priority, [currentwaffle, next_candidates, current_rem_chars]))

            elif direction == "j":
                j = int(line_candidates[0][1])
                for n in range(length):
                    # break if a char is different
                    if word[n] != currentwaffle[n][j]:
                        if currentwaffle[n][j] == " ":
                            if word[n] in current_rem_chars:
                                currentwaffle[n][j] = word[n]
                                current_rem_chars.remove(word[n])
                            else:
                                break
                        else:
                            break
                    

                    if (n == (length-1)):
                        if len(current_rem_chars) == 0 and len(current_candidates) == 0:
                            #print(currentwaffle)
                            return(currentwaffle)
                        else:
                            #print("-----solved a line------")
                            #for line in currentwaffle:
                            #    print(line)
                            #print("word is", word)
                            #print("rem chars", current_rem_chars)
                            #print("next candidates", next_candidates)
                            #print("len next candidates", len(next_candidates))
                            #print(currentwaffle,current_candidates,current_rem_chars)
                            #big_stack.append([currentwaffle,next_candidates,current_rem_chars])
                            priority = -len(current_rem_chars)

                            heapq.heappush(big_stack, (priority, [currentwaffle, next_candidates, current_rem_chars]))

                    
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

        
def main(initial_state):
    startstate = deepcopy(initial_state)
    waffle, sorted_candidates, rem_chars = prep(initial_state)
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
    '''
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
    '''
    main(wafflestate.initial_state_seven_4)
    #main(wafflestate.initial_state_seven_5)
    #main(wafflestate.initial_state_seven_6)
    # Record the end time
    end_time = time.time()

    # Calculate the total runtime
    total_runtime = end_time - start_time

    # Print the total runtime
    print(f"Total runtime: {total_runtime:.2f} seconds")
    