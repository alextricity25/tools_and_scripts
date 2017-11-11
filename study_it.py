# Read in a text file and output the file one line at a time with random
# words omitted. The program will wait for input after each line, asking
# for the omitted words. If the input doesn't match the words that have been
# omitted, the "missed" counter will be incremented and the next line will
# be printed. The input is not case-sensitive.
# This program can be also used with the "--generate" flag to generate the
# entire file at once. This is useful to create "fill-in-the-blank" type
# quizzes.

# EXCLUDED WORDS don't work

import argparse
import random
import re
import sys
import time
import string


def cal_len(word):
    """
    Count the number of alphanumeric characters in a word
    """
    count = 0
    good_chars = string.ascii_letters + "0123456789" + "'"
    for letter in word:
        if letter in good_chars:
            count += 1
    return count

# The parser object for the scripts arguments
parser = argparse.ArgumentParser(
    usage='%(prog)s',
    description='Bible Quiz Generator/Interactive Quiz',
    )

parser.add_argument(
    '-f',
    '--file',
    help='The file to generate the quiz from. File must be line delimited.',
    required=True
)

parser.add_argument(
    '-g',
    '--generate',
    help='Generate a quiz based off the input file',
    required=False,
    action='store_true',
    default=False
)

parser.add_argument(
    '-d',
    '--debug',
    help='Debug this program',
    action='store_true',
    required=False
)

parser.add_argument(
    '-l',
    '--level',
    help="Difficulty level",
    required=False,
    default=2,
    type=int
)

parser.add_argument(
    '-v',
    '--verses-only',
    help="Only stop to ask for input when the program encounters a verse from the input file. All other lines will just be printed.",
    required=False,
    default=False,
    action='store_true'
)

parser.add_argument(
    '-r',
    '--references-only',
    help="Only require the verse references to be typed out by the user, not the entire verse.",
    required=False,
    default=False,
    action='store_true'
)

parser.add_argument(
    '-q',
    '--print-questions',
    help='When specified, the program will print lines that begin with Q#: and not replace any words',
    default=False,
    required=False,
    action='store_true'
)

parser.add_argument(
    '-s',
    '--skip-verse-study',
    default=False,
    required=False,
    action='store_true'
)

parser.add_argument(
    '-p',
    '--print-references',
    help="Always print verse references",
    default=False,
    required=False,
    action='store_true'
)

parser.add_argument(
    '-o',
    '--outline-mode',
    help="Do not omit verses after a dash",
    default=False,
    required=False,
    action='store_true'
)

args = parser.parse_args()

# CONSTANT VARIABLES:
## These are excluded words - words that are *not* to be omitted
## from the sentence
## TODO - Make these configurable
EXCLUDED_WORDS = ["in", "as",
                  "a", "and",
                  "the", "of",
                  "his", "became",
                  "also", "is",
                  "this", "you",
                  "it", "to",
                  "he", "what",
                  "be", "i",
                  "your", "do",
                  "not", "that",
                  "by", "about",
                  "word", "being",
                  "if", "who",
                  "are", "for",
                  "were", "we",
                  "should", "every",
                  "one", "these",
                  "which", "have",
                  "been", "but",
                  "has", "with",
                  "our", "up",
                  "its", "because",
                  "on", "all",
                  "implies", "indicates",
                  "many", "go",
                  "or", "it's"]

# How many words, minimum, should we try to omit per sentence?
DIFFICULTY = args.level

# VARIABLES
missed = 0
total = 0
## A list of strings of missed sentences
missed_sentences = []


# Read the file line by line
with open(args.file, "r") as f:
    for line in f:
        # Preserve indentation
        whitespace_mt = re.search(r'^[ \t]+', line)
        if whitespace_mt:
            leading_whitespace = whitespace_mt.group(0)
        else:
            leading_whitespace = ''

        if not args.generate:
            time.sleep(1)
        # If it's a blank line, print a newline and move on.
        if re.match(r'^\s*$', line):
            print ""
            continue

        # Variables
        words_omitted = 0
        replace_indicies = []
        sentence_list = line.split()
        omitted_words = []
        verse_reference_indicies = []
        sentence = ""
        
        # For Bible verse studying.
        # If the line is a verse, omit the last and penultimate index
        # This should remove the verse reference completely. This way,
        # the user has to supply the entire reference everytime
        if args.debug:
            print "DEBUG - Trying to match the line:"
            print line
        verse_reference_mt = re.search(r"\(*[0-9]* *[A-Za-z\.]+ [0-9]+:[0-9]+-*[0-9]*\)*", line)
        count = 0
        #if re.match(r"[0-9]+:[0-9]+", sentence_list[-1]):
        if verse_reference_mt:
            # This assumes the verse reference is at the end of the line
            count = -1
            verse_reference = verse_reference_mt.group(0)
            while abs(count) <= len(verse_reference.split()):
                if not args.print_references and not args.outline_mode:
                    replace_indicies.append(count)
                else:
                    verse_reference_indicies.append(count)
                count = count - 1

        # Count the number of words in a line without the EXCLUDED_WORDS
        words = 0
        for word in sentence_list:
            if word.lower().strip() not in EXCLUDED_WORDS and re.match(r"[0-9a-zA-Z\.]+", word):
                if args.debug:
                    print "DEBUG - Adding word {} to word count!".format(word)
                words += 1
                if args.debug:
                    print "DEBUG - word count is now: {}".format(words)

        # We also have to consider any words that have already been
        # omitted i.e verse references. We don't want to include this in the
        # word count
        if not args.print_references and not args.outline_mode:
            words = words - abs(count)

        # Outline mode will not consider all words after
        # the '-', which are typically verses.
        if args.outline_mode:
            try:
                verses_count = len(sentence_list[sentence_list.index('-'):])
                if args.debug:
                    print "DEBUG -Subtracting verses_count from words"
                    print "DEBUG - verses_count: {}".format(verses_count)
               # Subtract 1, otherwise the prepending point reference will be
               # counted. ie. (I, a, ii)
                words = words - verses_count - 1
                if args.debug:
                    print "DEBUG - Words after subtracting: {}".format(words)
            except:
                if args.debug:
                    print "DEBUG - This line does not have any verse references"
                verses_count = 0
               # Subtract 1, otherwise the prepending point reference will be
               # counted. ie. (I, a, ii)
                words = words - 1

        # If the -q options is specified, the program will simply print any lines
        # that begin with 'Q#:'
        if re.search(r'Q[0-9]:', line) and args.print_questions:
            print line
            continue


        # Omit random words in the line
        while words_omitted < min(words, DIFFICULTY):
            if args.debug:
                print "DEBUG - The number of words in this sentence is: {}".format(words)
                print "DEBUG - THe minimum between {} and {} is {}".format(words, DIFFICULTY, min(words, DIFFICULTY))
                print "DEBUG - Words omitted: {}".format(words_omitted)
                print "DEBUG - min() {}".format(min(words, DIFFICULTY))
                print "DEBUG - replace_indcies list: {}".format(replace_indicies)
                print "DEBUG - line: {}".format(line)
            # This protects the verse reference from
            # being omitted when the print-reference
            # option is used
            reference_count = count if args.print_references else 0
            if args.outline_mode:
                upper_l = len(sentence_list) - verses_count - 1
                if args.debug:
                    print "DEBUG - rand_index upper_l: {}".format(upper_l)
                rand_index = random.randint(0, upper_l)
            else:
                rand_index = random.randint(0, len(sentence_list) - 1 - reference_count)
            # Check to see if word is EXCLUDED, and prevent any duplicates
            #print "Word: {}".format(sentence_list[rand_index])
            if args.print_references:
                if rand_index in verse_reference_indicies:
                    continue

            if sentence_list[rand_index].lower() in EXCLUDED_WORDS or rand_index in replace_indicies:
                continue
            elif re.match(r"[0-9a-zA-Z\.]{2,}", sentence_list[rand_index]):
                words_omitted += 1
                replace_indicies.append(rand_index)

        # Sort the replace_indecies list.
        # This list contains the indicies of the sentence_list structure
        # to be replaced with underscores.
        replace_indicies.sort()
        # Replace omitted words with underscores
        for index in replace_indicies:
            omitted_words.append(sentence_list[index])
            #sentence_list[index] = "_"*len(sentence_list[index])
            # Calculate the number of alphanums in the word
            length = cal_len(sentence_list[index])
            if re.match(r'^[A-Za-z0-9]+\.$', sentence_list[index]):
                continue
            sentence_list[index] = re.sub(r"[\-0-9A-Za-z\']+", '_' * length, sentence_list[index])
        # Print the line, with random words omitted
        ## Print the leading whitespace only when args.generate is on
        ## This way indentation will be preserved when generating quizes
        if args.generate:
            print leading_whitespace,
        print " ".join(sentence_list)

        # If the line is a verse, let's study it a little more...
        # The program will not continue until the user inputs the right
        # verse and reference
        if verse_reference_mt and not args.generate and not args.outline_mode:
            _ = ""
            while _.lower().strip() != line.lower().strip():
                _ = raw_input("Type the {} out:\n".format(
                    "reference" if args.references_only else "verse")
                    )
                if _ == 'skip':
                    break
                if _ == 'print':
                    print line
                    continue
                if args.references_only and re.search(_, verse_reference):
                    print "Amen!"
                    break
                elif _.lower().strip() == line.lower().strip():
                    print "Amen!"
                else:
                    print "Not quite, try again.."
                    print "The verse reference is {}. Look it up if you need to.".format(
                           verse_reference)

            # Skip the additional verse study, which requires
            # the verse to be typed out from memory
            if args.skip_verse_study:
                continue

            # Reset '_'
            _ = ""
            # If it's a verse, and we have broken out of the while loop
            # above, then we are going to ask for the whole verse this time.
            print "\n"*100
            print "Amen! Now type the entire verse out from memory:"
            while _.lower().strip() != line.lower().strip() and not args.references_only:
                _ = raw_input("The verse is {}. (Type 'skip' to skip this step)\n".format(verse_reference))
                if _ == 'skip':
                    break
                if _ == 'print':
                    print line
                    continue
                if _.lower().strip() == line.lower().strip():
                    print "Amen!"
                    break
                else:
                    print "Incorrect, try again. Look it up if you need to"
                    if args.debug:
                        print "DEBUG - THe verse is: {}".format(line)
            continue

        # Ask for user input
        if not args.generate and not args.verses_only:
            sentence = raw_input("Type the full sentence:\n")
        # Check the input
        if sentence.lower().strip() == line.lower().strip() and not args.generate:
            print "Amen!"
        elif not args.generate and not args.verses_only:
            print "Not quite :(. The line is:"
            print line
            missed += 1
            missed_sentences.append(line)
        if not args.generate and not args.verses_only:
            total += 1
            print "Score so far: {}/{}".format(total - missed, total)
            print "-"*25

    # End of File
    if not args.generate:
        print "Your final score is: {}/{}".format(total - missed, total)
        print "You missed the following sentences:"
        for sentence in missed_sentences:
            print sentence

