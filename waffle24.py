import wafflestate
from copy import deepcopy
import os
import cycle_decomposition
import time
import heapq

start_time = time.time()

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

    #print("Simplified Array:", simplified_array)
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
    
    return simplified_array, sorted_candidate_list, rem_chars
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

                    

        

def main(initial_state):
    #waffle = WaffleNode(n)
    startstate = deepcopy(initial_state)
    #rawwaffle = initial_state = [[0 for x in range(n)] for y in range(n)]
    waffle, sorted_candidates, rem_chars = prep(initial_state)
    solution = solve(waffle,sorted_candidates,rem_chars)
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
    