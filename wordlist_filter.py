import string


def filter_words_by_length_and_characters(input_file, output_file, length):
    with open(input_file, "r") as infile:
        words = infile.readlines()

    # Define the set of valid characters (26 standard letters of the alphabet)
    valid_characters = set(string.ascii_lowercase)

    # Filter words by the specified length and valid characters
    filtered_words = [
        word.strip()
        for word in words
        if len(word.strip()) == length
        and all(char in valid_characters for char in word.strip().lower())
    ]

    # Save the filtered words to the output file
    with open(output_file, "w") as outfile:
        for word in filtered_words:
            outfile.write(word.lower() + "\n")


# Example usage
input_file = "wordlist_english_dict.txt"
output_file = "wordlist_7.txt"
length = 7

filter_words_by_length_and_characters(input_file, output_file, length)
