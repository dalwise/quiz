#!/usr/bin/env python

"""Return longest word in a file that is a compound of other words

Run as:
python quiz.py <file_with_1_word_per_line>

ALGORITHM: Since you are asking for a fresh solution, instead of giving
a classical trie-based solution to the problem I am using a different
data structure: a dynamic array of hashmaps. Each word is inserted into a
hashmap determined by the lenght of the word. Each hashmap (starting from
the one for the longest words) is then iterated over to determine whether
the contained word it is a compound of other words.

The choice of data structure leads to a different set of compromises
compared to the trie-based solution. If we call n the number of words,
k the maximum lenght of a word and c the total number of characters:

TIME: Creating the initial data structure to store all words is O(c) in
both cases. Note that even though a hashmap is generally considered O(1)
for insertions, we actually need to read in each character of the string
that we want to insert in order to calculate the hashmap.  However for the
hashmap-based solution is generally faster to create the data structure
since there are less comparisons and pointer accesses involved to create
it. Finding the word is very fast with the hashmap solution if one of
the longer words is a compound word, since it will be checked first and
returned immediately. The classical solution checks every word to see if
it is a compound and is efficient in checking each word. It is faster if
there are no compound words in the list, since in this case both solutions
would have to check every word. The hashmap solution needs to calculate a
hash of many substrings within each word, so it will be slower if all words
need to be checked.

SPACE: Both solutions are again O(c), but the trie is expected to occupy
less memory.

MAINTANABILITY: Using only basic data structures supported by the standard
library of the chosen language (arrays and hashmaps) allows for very concise
code with no external dependencies. These two factors make the code easier
to maintain.

ALTERNATIVES: A better time efficiency than both the commented solutions can
be achieved by creating a trie and also a list of dynamic arrays of words,
where the array is determined by word lenght. This achieves better expected
time in most cases, but at the expense of higher space and complexity
requirements.

ERROR CHECKING: In the interest of clearly and concisely showing the
algorithm, error conditions are not checked for. Production code would need
error checking, for example for empty input lines or for incorrect calls
to the program.

COMPATIBILITY: The code is compatible with Python2 and Python3. It runs
considerably faster on Python2.
"""

import sys

def longest_compound(filename):
    """Return longest compound word found in filename"""
    words = [] # List of sets. The lenght of a word determines its set
    with open(filename) as word_file:
        for line in word_file:
            word = line.strip()
            words += [set() for _ in range(len(word)-len(words))]
            words[len(word)-1].add(word)

    def check_word(w, this_word_valid=True):
        """Check if w is compound. Unless original w also check if in array"""
        return any(w[:i] in words[i-1] and (i == len(w) or check_word(w[i:]))
                   for i in range(1, len(w)+this_word_valid))

    for current_set in words[::-1]: # Iterate through words from longest
        for word in current_set:
            if check_word(word, False):
                return word # Return as soon as a compound is found
    return ""

print(longest_compound(sys.argv[1]))
