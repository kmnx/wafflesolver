import json


if __name__ == "__main__":
    with open("collected_puzzles_and_solutions.json", "r") as f:
        data = f.read()
    big_array = json.loads(data)
    for item in big_array:
        print(item[0])
        print(item[1])

        if len(item[0]) == 21:
            spaced_scrambled = ""
            spaced_scrambled = (
                item[0][0:6]
                + " "
                + item[0][6:7]
                + " "
                + item[0][7:14]
                + " "
                + item[0][14:15]
                + " "
                + item[0][15:21]
            )
            spaced_solution = ""
            spaced_solution = (
                item[1][0:6]
                + " "
                + item[1][6:7]
                + " "
                + item[1][7:14]
                + " "
                + item[1][14:15]
                + " "
                + item[1][15:21]
            )

            scrambled_grid = [[], [], [], [], []]
            solved_grid = [[], [], [], [], []]
            for i, char in enumerate(spaced_scrambled):
                scrambled_grid[i // 5].append([char, " "])

            for i, char in enumerate(spaced_solution):
                solved_grid[i // 5].append([char, " "])

            for row in scrambled_grid:
                print(row)
            print("\n")
            for row in solved_grid:
                print(row)
            input()

            for i, row in enumerate(scrambled_grid):
                for cell in row:
                    if cell[0] == " ":
                        pass
                    else:
                        if cell[0] == solved_grid[i][row.index(cell)][0]:
                            cell[1] = "g"
