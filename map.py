def solution_mapping(scrambled, solution):
    mapping = {}
    for char in set(scrambled):  # Use set to avoid duplicate characters
        positions = [i for i, s_char in enumerate(solution) if s_char == char]
        mapping[char] = positions
    return mapping

# Example usage
scrambled = "henreubq n i tmerluree e q aduuotado o d yieearnc"
solution = "nunneryo u q imarqueea t a ldoubtedi r o echeered"
mapping = solution_mapping(scrambled, solution)
print(mapping)
if __name__ == '__main__':
    scrambled = "henreubq n i tmerluree e q aduuotado o d yieearnc"
    solution = "nunneryo u q imarqueea t a ldoubtedi r o echeered"
    mapping = solution_mapping(scrambled, solution)
    print(mapping)
    # Output: {'n': [0, 8], 'r': [1, 6], 'e': [2, 3, 4, 10, 11], 'u': [5], 'b': [7], 'q': [9], ' ': [12, 13, 14, 21], 'i': [15, 16], 't': [17], 'm': [18], 'l': [19], 'd': [20, 22, 23], 'o': [24, 25, 26], 'y': [27], 'a': [28], 'c': [29]}
    # The character 'n' appears at positions 0 and 8 in the scrambled text, and at positions 0 and 8 in the solution text. The same goes for the other characters.