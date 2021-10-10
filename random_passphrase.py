import random
import argparse

SYS_RAND = random.SystemRandom()

WORD_LIST_FILE = "all_words_alpha.txt" # This contains way too many obscure words
WORD_LIST_FILE = "corncob_lowercase_word_list.txt" # This contains less obscure words (but still a lot of compound words and obscure stuff)
with open(WORD_LIST_FILE) as f:
    WORD_LIST = [ word.strip() for word in f ]

def get_random_password(num_words, sep=" "):
    wordL = []
    for _i in range(num_words):
        wordL.append(SYS_RAND.choice(WORD_LIST))

    return sep.join(wordL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a pass phrase with random words.')
    parser.add_argument('num_words', type=int, nargs='?', default=4, help='The length of the pass phrase in number of words')
    parser.add_argument('--separator', type=str, default=' ', help='')
    parser.add_argument('--print-entropy',  action='store_true', help='Display the complexity of the password')
    parser.add_argument('--num-passphrases', type=int, default=1, help='Generate and Print multiple pass phrases')
    args = parser.parse_args()
    
    if args.print_entropy:
        print("Entropy: {0:,}".format(len(WORD_LIST) ** args.num_words))
    for _ in range(args.num_passphrases):
        print("Pass Phrase: {0}".format(get_random_password(args.num_words, args.separator)))
