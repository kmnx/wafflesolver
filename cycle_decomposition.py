import copy
import heapq
import time


def main(scrambled, solution):
    start_time = time.time()
    cyclopedia = set()
    solutionstack = []
    bigstack = []
    solved_at_start = []

    if len(solution) == 49:
        success = 20
    elif len(solution) == 25:
        success = 10
    # weed out already solved ones
    for i in range(len(scrambled)):
        if scrambled[i] == solution[i]:
            solved_at_start.append(i)
    # generate starting swaps
    for i in range(len(scrambled)):
        if i not in solved_at_start:
            for index, char in enumerate(solution):
                if char == scrambled[i]:
                    localcycle = [i, index]
                    newwholecycle = [localcycle]
                    priority = 0
                    for cycle in newwholecycle:
                        if len(cycle) == 2:
                            priority += 2 * 10000

                    heapq.heappush(bigstack, (-priority, newwholecycle))

    while bigstack:
        _, wholecycle = heapq.heappop(bigstack)
        visitedlist = copy.deepcopy(solved_at_start)

        for cycle in wholecycle:
            for i in cycle:
                visitedlist.append(i)
        if len(visitedlist) == len(solution):
            solutionstack.append(wholecycle)
            solvecounter = 0
            for cycle in wholecycle:
                solvecounter = solvecounter + len(cycle) - 1
            if solvecounter == success:
                break

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
                        # if index points to beginning of current cycle, open a new cycle
                        if index == localcycle[0]:
                            whole_frozen = []
                            for item in wholecycle:
                                localset = frozenset(item)
                                whole_frozen.append(localset)
                            whole_frozen_set = frozenset(whole_frozen)
                            if whole_frozen_set in cyclopedia:
                                continue
                            else:
                                cyclopedia.add(whole_frozen_set)

                            nextlocalcycle = []
                            for i in range(len(scrambled)):
                                for index, char in enumerate(solution):
                                    if (
                                        (char == scrambled[i])
                                        and i not in visitedlist
                                        and index not in visitedlist
                                    ):

                                        newwholecycle = copy.deepcopy(wholecycle)
                                        nextlocalcycle = [i, index]
                                        newwholecycle.append(nextlocalcycle)
                                        priority = 0
                                        cyclesumprio = 0
                                        for cycle in newwholecycle:
                                            cyclesumprio += 100
                                            if len(cycle) == 2:
                                                priority += 2 * 10000

                                        heapq.heappush(
                                            bigstack, (-priority, newwholecycle)
                                        )
                    else:
                        if index not in visitedlist:
                            newwholecycle = copy.deepcopy(wholecycle)
                            newlocalcycle = copy.deepcopy(localcycle)
                            newwholecycle[-1].append(index)
                            priority = 0
                            cyclesumprio = 0
                            for cycle in newwholecycle:
                                cyclesumprio += 100
                                if len(cycle) == 2:
                                    priority += 2 * 10000

                            heapq.heappush(bigstack, (-priority, newwholecycle))

    # Sort bigstack by the number of sublists in each list
    sorted_solutionstack = sorted(solutionstack, key=len, reverse=True)

    for item in sorted_solutionstack:
        print(item)
        scrambled_list = copy.deepcopy(list(scrambled))
        swapcount = 0
        for cycle in item:
            swapcount += len(cycle) - 1
            cycle.reverse()
            for i in range(len(cycle) - 1):
                scrambled_list[cycle[i]], scrambled_list[cycle[i + 1]] = (
                    scrambled_list[cycle[i + 1]],
                    scrambled_list[cycle[i]],
                )
        print("Swaps: ", swapcount)
        print("".join(scrambled_list))
        break

    # Record the end time
    end_time = time.time()

    # Calculate the total runtime
    total_runtime = end_time - start_time

    # Print the total runtime
    print(f"Total runtime: {total_runtime:.2f} seconds")


# scrambled = "DBDFAFECBCAE"
# solution = "AABBCCDDEEFF"
# waffle 310
# scrambled = "csroeu z votoaen f aeertr"
# solution = "curver o nafootz s eeater"
# scrambled = "thfeccun h t isistasni n i husitisgl g o ndigceiu"
# solution = "deficiti i h osustainc h l iunitings n c hsuggest"
scrambled = "adotpwet a b rahscocde n e dtpibueen r h rtrgceuh"
solution = "chopperh u r eabscondt t d htributee n c aragweed"
# scrambled = "tcvcsrou o r dbpneares o i itsueiett e g coiehkar"
# solution = "revisito e e rbandageo t s etouristi r c ocheckup"
if __name__ == "__main__":
    main(scrambled, solution)
