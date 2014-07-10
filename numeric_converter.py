def convert_to_words(number):
    """
        Converts a numeral to its english equivalent
         Designed to work correctly up to the largest "sextillion" number.
        Numbers larger than that will be converted into a string that uses
        place modifiers only up to sextillion

        >>> convert_to_words(5360526)
        'five million three hundred sixty thousand five hundred twenty six'
        """

    # Map decimal places to base names
    bases = {3: "hundred", 4: "thousand", 7: "million", 10: "billion", 13: "trillion",
             16: "quadrillion", 19: "quintillion", 22: "sextillion"}
    # Number names
    ones = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    # Idiomatic names
    tens = ["ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
             "eighteen", "nineteen"]

    def closest_base(place):
        """
         Find the highest base lower than our current place
        """
        for i in range(len(bases)):
            if place in bases.keys():
                return place
            place -= 1

    # Convert number to string for easier place-wise access
    number_string = str(number)

    english_string = ""
    skips = 0

    # Examine each digit, from most significant end to least
    for index in range(len(number_string)):
        # Do any digits need to be skipped?
        if skips:
            skips -= 1
            continue

        # Our current decimal place
        place = len(number_string) - index

        # If this is a 100s or greater digit
        if place >= 3:
            # If there is a modifier word for this place
            if place in bases:
                # Print out ones name, then base modifier (e.g. two thousand)
                english_string += ones[int(number_string[index]) - 1] + " " + bases[place] + " "
                continue
            # Otherwise figure out how far we are from the closest modifier
            else:
                # Use the numbers from here up to the place of the next modifier to
                # recursively build a number string, then append on the closest modifier
                span = place - closest_base(place)
                skips = span
                f = number_string[index]
                english_string += convert_to_words(number_string[index:index + span+1]) + " "
                english_string += bases[closest_base(place)] + " "
        # If this is a 10s digit
        if place == 2:
            # If its a teens number, print out teen number and end
            if number_string[index] == "1":
                english_string += teens[int(number_string[index + 1])] + " "
                return english_string

            # If not, print out the tens number
            english_string += (tens[int(number_string[index]) - 1]) + " "

        # If this is the ones place, print out ones number and end
        if place == 1:
            # If the number ends in 0, do not add anything more
            if number_string[index] != "0":
                english_string += ones[int(number_string[index]) - 1] + " "

    return english_string.rstrip(" ")

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print convert_to_words(5360526)
    print convert_to_words(4360526)
    print convert_to_words(360526)
    print convert_to_words(60526)
    print convert_to_words(526)
    print convert_to_words(26)
    print convert_to_words(60)
    print convert_to_words(6)