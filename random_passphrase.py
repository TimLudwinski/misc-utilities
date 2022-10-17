"""
Password Complexity (comparing random letters vs random words):

8 Random Lowercase Letters (26^8)
208,827,064,576
8 Random Letters (any case) ((26*2)^8)
53,459,728,531,456
Three Random Words (58000^3)
195,112,000,000,000
8 Random Letters (any case) and Numbers  ((26*2+10)^8)
218,340,105,584,896
8 Random Letters, Numbers and Symbols in the number row ((26*2+10+16)^8)
1,370,114,370,683,136
12 Random Lowercase Letters (26^8)
95,428,956,661,682,176
Four Random Words (58000^4)
11,316,496,000,000,000,000
12 Random Letters, Numbers and Symbols in the number row ((26*2+10+16)^8)
50,714,860,157,241,037,295,616
Five Random Words (58000^5)
656,356,768,000,000,000,000,000
16 Random Letters, Numbers and Symbols in the number row ((26*2+10+16)^8)
1,877,213,388,752,445,800,995,314,794,496
Seven Random Words (58000^5)
656,356,768,000,000,000,000,000
2.207984167552e+33
"""
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
