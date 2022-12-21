import re
import sys
import random
from collections import defaultdict
from math import log

# keeps generating phons until # is randomly generated, then returns the whole word
def generate_bigram_word():
    word = "#"
    current = ''
    while current != '#':
        if current == '': current = '#'
        current = generate_phon(current)
        word += " " + current
    return word

# same as generate_bigram_word but for trigrams
def generate_trigram_word():
    word = "# #"
    current = ''
    context = ("#","#")
    while current != '#':
        if current == '': context = ('#','#')
        current = generate_phons(context)
        context = (context[1],current)
        word += " " + current
    return word

# given a phone, randomly generates and returns the next word using the bigram model
def generate_phon(phon):
    rand = random.uniform(0,1)
    for following in bigram[phon]: 
        rand -= bigram[phon][following]
        if rand < 0.0: return following
    return following
    
# randomly generates word for the trigram model
def generate_phons(pair):
    rand = random.uniform(0,1)
    for following in trigram[pair]: 
        rand -= trigram[pair][following]
        if rand < 0.0: return following
    return following

def generate_bigram(trainf):
    counts = defaultdict(lambda:0)
    bicounts = defaultdict(lambda:defaultdict(lambda:0))
    
    # this loops through all the data and stores counts
    for line in trainf:
        line = "# " + line.strip() + " #"
        phons = re.split(r'[\s]+', line)
        # removes the word orthography element from the list
        phons.pop(1)
        for i in range(len(phons)-1):
            counts[phons[i]] = counts[phons[i]] + 1
            bicounts[phons[i]][phons[i+1]] = bicounts[phons[i]][phons[i+1]] + 1
    # this loops through all word pairs and computes relative frequency estimates
    for phon1 in counts:
        wholeAlphabet = len(bicounts[phon1])
        for phon2 in bicounts[phon1]:
            # runs smoothed probability when smooth = 1
            bigram[phon1][phon2] = float(bicounts[phon1][phon2]+smooth)/float(counts[phon1]+(wholeAlphabet*smooth))
            #log_sum2 += log(bigram[phon1][phon2],2)
        #log_sum += log_sum2
    for i in range(25):
        print(generate_bigram_word())

def generate_trigram(trainf):
    bicounts = defaultdict(lambda:0)
    tricounts = defaultdict(lambda:defaultdict(lambda:0))
    # this loops through all the data and stores counts
    for line in trainf:
        line = "# # " + line.strip() + " #"
        phons = re.split(r'[\s]+', line)
        # removes the word orthography element from the list
        phons.pop(2)
        for i in range(len(phons)-2): 
            pair = (phons[i],phons[i+1])
            bicounts[pair] = bicounts[pair] + 1
            tricounts[pair][phons[i+2]] = tricounts[pair][phons[i+2]] + 1
    # this loops through all word pairs and computes relative frequency estimates
    for pair in tricounts:
        wholeAlphabet = len(tricounts[pair])
        for phon in tricounts[pair]:
            # runs smoothed probability when smooth = 1
            trigram[pair][phon] = float(tricounts[pair][phon]+smooth)/float(bicounts[pair]+(wholeAlphabet*smooth))
            #log_sum2 += log(trigram[pair][phon],2)
        #log_sum += log_sum2
    for i in range(25):
        print(generate_trigram_word())
    

def perplexity(testf):
    N = 0.0
    for line in testf.readlines():
        line = "# " + line.strip() + " #"
        test_phon = re.split(r'[\s]+', line)
        test_phon[1] = "#"
        N += len(test_phon)-2
        print(N)
    print(log_sum)
    perplex = 2**((log_sum)*((-1)/N))
    print(perplex)
    return perplex

bigram = defaultdict(lambda:{})
trigram = defaultdict(lambda:{})

log_sum = 0.0
log_sum2 = 0.0
perplex = 0.0

# if there is 3rd argument the add-1 smoothed probability is calculated
if len(sys.argv) == 4:
    smooth = 1
elif len(sys.argv) == 3:
    smooth = 0

def main():
    
    trainf = open(sys.argv[1])
    N = sys.argv[2]

    if N == '2': generate_bigram(trainf)
    elif N == '3': generate_trigram(trainf)
    else: print("This model can only do bigrams and trigrams :(")

    trainf.close()

    testf = open(sys.argv[3])
    perplexity(testf)

    testf.close()

if __name__ == "__main__":
    main()
