import os
import sys
from copy import deepcopy
import wafflestate
import astar

sys.setrecursionlimit(10**6)


class WaffleNode:
    def __init__(self, n):
        self.n = n
        self.state = [[0 for x in range(n)] for y in range(n)]
        self.attempts = 0
        self.solved = False
        print("innit")
        # print(self.state)

    def print_state(self):
        for i in range(self.n):
            string = ""
            for j in range(self.n):
                string = string + self.state[i][j][0] + " "
            print(string)

    def print_state_solved(self):
        for i in range(self.n):
            string = ""
            for j in range(self.n):
                if self.state[i][j][1] in ["m", "g"]:
                    string = string + self.state[i][j][0] + " "
                else:
                    string = string + " " + " "
            print(string)
        print("\n word insert attempts: ", self.attempts, "\n")

    def insert(self, row, column, char, colour):
        self.state[row][column] = [char, colour]


def switch_chars(waffle, candidate, pos):
    if pos[0] == "i":
        irange = [int(pos[1])]
        jrange = range(waffle.n)
    elif pos[0] == "j":
        jrange = [int(pos[1])]
        irange = range(waffle.n)

    found_chars = 0
    parse_pos = 0
    wordlength = waffle.n
    # check and switch row/column depending on irange/jrange
    for i in irange:
        for j in jrange:
            wanted_char = candidate[parse_pos]
            parse_pos += 1
            # char is already green or "maybe"
            if waffle.state[i][j][1] in ["g", "m"]:
                # but wrong for candidate
                if waffle.state[i][j][0] != wanted_char:
                    return None
                else:
                    found_chars += 1
            # char is correct but not yet marked
            elif waffle.state[i][j][0] == wanted_char:
                waffle.state[i][j][1] = "m"
                found_chars += 1
            else:
                # char is wrong and can be switched, try to find correct one
                found_char = False
                for m in range(wordlength):
                    if found_char:
                        break
                    for n in range(wordlength):
                        if found_char:
                            break
                        # waffle.state[m][n] is ['char','colour']
                        if waffle.state[m][n][0] == wanted_char:
                            if waffle.state[m][n][1] not in ["g", "m"]:
                                # switch
                                (waffle.state[m][n][0], waffle.state[i][j][0],) = (
                                    waffle.state[i][j][0],
                                    waffle.state[m][n][0],
                                )
                                waffle.state[i][j][1] = "m"
                                waffle.state[m][n][1] = "u"
                                found_char = True
                                found_chars += 1
                        # a wanted char couldnt be found, stop searching
                        if (
                            (n == waffle.n)
                            and (m == waffle.n)
                            and (found_char is False)
                        ):
                            return None

    if found_chars == wordlength:
        return waffle
    else:
        return None


def line_is_solved(waffle, pos):
    if pos[0] == "i":
        irange = [int(pos[1])]
        jrange = range(waffle.n)
    elif pos[0] == "j":
        irange = range(waffle.n)
        jrange = [int(pos[1])]
    charcounter = 0
    for n in irange:
        for m in jrange:
            if waffle.state[n][m][1] in ["g", "m"]:
                charcounter += 1
    if charcounter == waffle.n:
        return True
    else:
        return False


def unsolve(waffle, pos):
    if pos[0] == "i":
        irange = [int(pos[1])]
        jrange = range(waffle.n)
    elif pos[0] == "j":
        jrange = [int(pos[1])]
        irange = range(waffle.n)[1::2]
    for n in irange:
        for m in jrange:
            if waffle.state[n][m][1] == "m":
                waffle.state[n][m][1] = "u"


def solve(waffle, candidate_list):
    # positions as list to ensure processing order top to bottom, left to right

    positions = []
    for n in range(waffle.n)[0::2]:
        positions.append("i" + str(n))
    for n in range(waffle.n)[0::2]:
        positions.append("j" + str(n))

    for pos in positions:
        # skip further candidates for solved lines
        if line_is_solved(waffle, pos):
            # if it's the last line then whole waffle must be solved
            if pos == positions[-1]:
                waffle.solved = True

        else:
            for candidate in candidate_list[pos]:
                if waffle.solved is False:
                    waffle.attempts += 1
                    switchedwaffle = switch_chars(waffle, candidate, pos)
                    if switchedwaffle:
                        waffle.print_state_solved()
                        # last line attempt successful, attempt next line
                        solve(switchedwaffle, candidate_list)
                    if waffle.solved is False:
                        # undo solved markers after stepping out of failed recursion
                        unsolve(waffle, pos)

            return switchedwaffle


# preprocessing not strictly necessary for recursive solution
# but increases recursion speed 1000x-100000x
def get_candidates(waffle, wordlist):
    waffle.print_state()
    candidate_list = {}
    state = waffle.state
    # filter rows
    for i in range(n)[0::2]:
        pos = "i" + str(i)
        candidates = wordlist
        for j in range(waffle.n):
            char = state[i][j][0]
            colour = state[i][j][1]
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
                # print("candidates after filtering grey", candidates)
        # candidate_list.append([pos, candidates])
        candidate_list[pos] = candidates
    # filter columns
    for j in range(n)[0::2]:
        pos = "j" + str(j)
        candidates = wordlist
        for i in range(waffle.n):
            char = state[i][j][0]
            colour = state[i][j][1]
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

        candidate_list[pos] = candidates

    return candidate_list


def prep(waffle, initial_state):
    all_chars = set()
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

    for i in range(n):
        for j in range(n):
            waffle.state[i][j] = initial_state[i][j]
            all_chars.add(initial_state[i][j][0])
    # naive wordlist processing, keep only words with chars existing in waffle
    print("len wordlist pre filter", len(wordlist_unfiltered))
    for i in range(waffle.n):
        wordlist = [w for w in wordlist_unfiltered if (w[i] in all_chars)]
    print("len wordlist post filter", len(wordlist))

    # more preprocessing, per line
    candidate_list = get_candidates(waffle, wordlist)
    return waffle, candidate_list, wordlist_unfiltered


def main(initial_state):

    waffle = WaffleNode(n)
    startstate = deepcopy(initial_state)

    waffle, candidate_list, wordlist_unfiltered = prep(waffle, initial_state)

    # uncomment to ignore preprocessing, use raw dictionary, watch number go up
    """
    candidate_list = {}
    for i in range(waffle.n)[0::2]:
        pos = "i" + str(i)
        print(pos)
        candidates = wordlist_unfiltered
        candidate_list[pos] = candidates
    for j in range(waffle.n)[0::2]:
        pos = "j" + str(j)
        print(pos)
        candidates = wordlist_unfiltered
        candidate_list[pos] = candidates
    """
    # go!
    solvedwaffle = solve(waffle, candidate_list)
    print("\n 🧇 🧇 🧇 Sucess! 🧇 🧇 🧇 \n")
    solvedwaffle.print_state_solved()
    print("press Enter to continue")
    input()
    astar_start = ""
    astar_end = ""
    for x in range(n):
        startline = []
        endline = []
        for y in range(n):
            astar_start = astar_start + startstate[x][y][0]
            astar_end = astar_end + solvedwaffle.state[x][y][0]

    print(astar_start)
    print(astar_end)
    astar.main(astar_start, astar_end)


if __name__ == "__main__":

    # Set n to 5 or 7 depending on waffle size
    # wafflestates are in wafflestate.py
    n = 7
    if n == 5:
        initial_state = wafflestate.initial_state_five_7
    elif n == 7:
        initial_state = wafflestate.initial_state_seven_3
    main(initial_state)
