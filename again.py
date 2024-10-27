import copy

#scrambled = "DBDFAFECBCAE"
#solution = "AABBCCDDEEFF"
# waffle 310
scrambled = "csroeu z votoaen f aeertr"
solution = "curver o nafootz s eeater"
#scrambled = "tcvcsrou o r dbpneares o i itsueiett e g coiehkar"
#solution = "revisito e e rbandageo t s etouristi r c ocheckup"
solutionstack = []
bigstack = []
cyclopedia = set()
solved_at_start = []
twolist = []
# weed out already solved ones
for i in range(len(scrambled)):
    if scrambled[i] == solution[i]:
        #twocycle = [i,i]
        #twoset = frozenset(twocycle)
        #twolist.append([i,i])
        solved_at_start.append(i)
        print(i, scrambled[i],solution[i])

for i in range(len(scrambled)):
    if i not in solved_at_start:
        for index, char in enumerate(solution):
            if char == scrambled[i]:
                #print(i,index)
                localcycle = [i,index]
                bigstack.append([localcycle])

    

while bigstack:
    wholecycle = bigstack.pop()
    #print(wholecycle)
    
    # get last cyclev
    visitedlist = copy.deepcopy(solved_at_start)
    
    for cycle in wholecycle:
        for i in cycle:
            visitedlist.append(i)
    if len(visitedlist) == len(solution):
        solutionstack.append(wholecycle)
        continue
    localcycle = wholecycle[-1]
    for index, char in enumerate(solution):
        # character is one we're looking for
        if char == scrambled[localcycle[-1]]:
            # skip current index if same position
            if localcycle[-1] == index:
                pass
            else:
                # index already checked
                if index in localcycle:
                    #print("oh")
                    # if it's the very first one, open a new cycle
                    if index == localcycle[0]:
                        localset = frozenset(localcycle)
                        
                        if localset in cyclopedia:
                            # we just stop, if it's in there we will find the other permutations
                            #print("found ",localset, "in the cyclopedia")
                            continue
                        else:
                            #cyclopedia.add(localset)
                            pass

                        nextlocalcycle = []
                        for i in range(len(scrambled)):
                            for index,char in enumerate(solution):
                                if (char == scrambled[i]) and i not in visitedlist and index not in visitedlist:
                                    
                                    newwholecycle = copy.deepcopy(wholecycle)
                                    nextlocalcycle = [i,index]
                                    #print(i,index)
                                    newwholecycle.append(nextlocalcycle)
                                    bigstack.append(newwholecycle)
                
                else:
                    if index not in visitedlist:
                        #print(index)
                        newwholecycle = copy.deepcopy(wholecycle)
                        newlocalcycle = copy.deepcopy(localcycle)
                        newwholecycle[-1].append(index)
                        bigstack.append(newwholecycle)


# Sort bigstack by the number of sublists in each list
sorted_solutionstack = sorted(solutionstack, key=len)

# Print the sorted bigstack
for item in sorted_solutionstack:
    print(item)
    scrambled_list = copy.deepcopy(list(scrambled))
    for cycle in item:
        cycle.reverse()
        for i in range(len(cycle) - 1):
            scrambled_list[cycle[i]], scrambled_list[cycle[i + 1]] = scrambled_list[cycle[i + 1]], scrambled_list[cycle[i]]

    print(''.join(scrambled_list))