import re
import sys
import random
import math
from collections import defaultdict


def generate_word():
    word = "#"
    current = ''
    while current != '#':
        if current == '': current = '#'
        current = generate_phoneme(current)
        word += " " + current
    return word

def generate_phoneme(phoneme):
    rand = random.uniform(0,1)
    for following in bigram[phoneme]:
        rand -= bigram[phoneme][following]
        if rand < 0.0: return following
    return following


language = open(sys.argv[1])

counts = defaultdict(lambda:0)
bicounts = defaultdict(lambda:defaultdict(lambda:0))

for line in language:
    line = "# " + line.strip() + " #"
    phonemes = re.split(r'[\s]+', line) #all we have in a line are whitespaces
    phonemes[1]="#"
    
    for i in range(len(phonemes)-2): #phonemes[0] = pound symbol, phonemes[1] = word
        counts[phonemes[i+1]] = counts[phonemes[i+1]] + 1
        #print(counts)
        bicounts[phonemes[i+1]][phonemes[i+2]] = bicounts[phonemes[i+1]][phonemes[i+2]] + 1

language.close()

bigram = defaultdict(lambda:{})
log_sum = 0.0
perplexity=0.0

for phoneme1 in counts:
    for phoneme2 in bicounts[phoneme1]:
        a=len(bicounts[phoneme1])
        bigram[phoneme1][phoneme2] = float(bicounts[phoneme1][phoneme2]+1)/float(counts[phoneme1]+a)
        print(bigram[phoneme1][phoneme2])

for i in range(25):
    print(generate_word())


testfile = open(sys.argv[2])

test_counts = defaultdict(lambda:0)
test_bicounts = defaultdict(lambda:defaultdict(lambda:0))

for line in testfile:
    line = "# " + line.strip() + " #"
    test_phonemes = re.split(r'[\s]+', line) #all we have in a line are whitespaces
    test_phonemes[1]="#"
    
    for i in range(len(test_phonemes)-2): #phonemes[0] = pound symbol, phonemes[1] = word
        test_counts[test_phonemes[i+1]] = counts[test_phonemes[i+1]] + 1
        test_bicounts[phonemes[i+1]][test_phonemes[i+2]] = test_bicounts[test_phonemes[i+1]][test_phonemes[i+2]] + 1

testfile_bigram = defaultdict(lambda:{})
log_sum = 0.0
log_sum_1 = 0.0
perplexity=0.0

for phoneme1 in test_counts:
    for phoneme2 in test_bicounts[phoneme1]:
        a=len(test_bicounts[phoneme1])
        testfile_bigram[phoneme1][phoneme2] = float(test_bicounts[phoneme1][phoneme2]+1)/float(test_counts[phoneme1]+a)
        log_sum_1 += math.log(testfile_bigram[phoneme1][phoneme2],2)
        #print(testfile_bigram[phoneme1][phoneme2])
    log_sum += log_sum_1

testfile.close()

testfile = open(sys.argv[2])

def perplexity(testfile):
    perplexity = 0.0
    N=0.0
    for line in testfile.readlines():
        line = "# " + line.strip() + " #"
        test_phonemes = re.split(r'[\s]+', line) #all we have in a line are whitespaces
        test_phonemes[1]="#"
        N += len(test_phonemes)-2
        print(N)
    print(log_sum)
    perplexity = 2**((log_sum)*((-1)/N))
    print(perplexity)
    return perplexity

print(testfile)

perplexity(testfile)


    





