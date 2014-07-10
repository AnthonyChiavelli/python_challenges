import string


def encode(input_string):
    """
    Encodes the text of the supplied string in ROT13, and reverses
    every other word.

    >>> encode("Hello world!")
    'byyrU jbeyq!'

    """

    # Construct a mapping of each letter (in either case) to its ROT13 partner
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    a_thru_n, n_thru_z = alphabet[0:13], alphabet[13:]
    rot13_mapping = string.maketrans(alphabet + alphabet.upper(),
                                     n_thru_z + a_thru_n + n_thru_z.upper() + a_thru_n.upper())

    # Iterate over words of input string
    words = input_string.split(" ")
    for index, word in enumerate(words):
        # Reverse odd words
        if index % 2 == 0:
            word = word[::-1]

        # Replace letters in word according to map
        words[index] = string.translate(word, rot13_mapping)

    # Rejoin and return
    return " ".join(words)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(encode("Hello world!"))
