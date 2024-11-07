import brotli
import base64
import json
import time
import cycle_decomposition
start_time = time.time()


# just a helper to load the puzzles from wafflegame.com

with open("archive-waffle5-brotli-2024-11-07.json") as f:
    content5 = json.load(f)
with open("archive-waffle7-brotli-2024-11-07.json") as f:
    content7 = json.load(f)

def main():
    archive_list = []
    with open("archive-waffle5-brotli-2024-11-07.json") as f:
        content5 = json.load(f)
    with open("archive-waffle7-brotli-2024-11-07.json") as f:
        content7 = json.load(f)
    for key, b64string in content5.items():
        compressed_data = base64.b64decode(b64string)

        # Decompress the data
        try:
            decompressed_data = brotli.decompress(compressed_data)
            decompressed_string = decompressed_data.decode('utf-8')
            
            # Convert the string to a dictionary
            puzzle_dict = json.loads(decompressed_string)
            puzzle = puzzle_dict["puzzle"]
            
            solution = puzzle_dict["solution"]
            #print(puzzle)
            #print(solution)
            #cycle_decomposition.main(puzzle,solution)
        except brotli.error as e:
            print(f"Decompression error: {e}")
        archive_list.append([puzzle,solution])

    for key, b64string in content7.items():

        compressed_data = base64.b64decode(b64string)

        # Decompress the data
        try:
            decompressed_data = brotli.decompress(compressed_data)
            decompressed_string = decompressed_data.decode('utf-8')
            
            # Convert the string to a dictionary
            puzzle_dict = json.loads(decompressed_string)
            puzzle = puzzle_dict["puzzle"]
            
            solution = puzzle_dict["solution"]
            #print(puzzle)
            #print(solution)
            #cycle_decomposition.main(puzzle,solution)
        except brotli.error as e:
            print(f"Decompression error: {e}")
        archive_list.append([puzzle,solution])
    with open("collected_puzzles_and_solutions.json", "w") as outfile:
        json.dump(archive_list, outfile, indent=4)
    return archive_list
        


    end_time = time.time()

    total_time = end_time - start_time

    print("total time to solve all waffles:",total_time)

if __name__ == "__main__":
    archive_list = main()
    for item in archive_list:
        cycle_decomposition.main(item[0],item[1])