import re
import sys
import random
from collections import defaultdict

def generate_word():
    word = "# #"
    current = ''
    context = ("#","#")
    while current != '#':
        if current == '' : context = ('#','#')
        current = generate_phoneme(context)
        context = (context[1], current)
        word += " " + current
    return word

def generate_phoneme(pair):
    rand = random.uniform(0,1)
    for following in trigram[pair]:
        rand -= trigram[pair][following]
        if rand < 0.0 : return following
    return following
    

language = open(sys.argv[1])

bicounts = defaultdict(lambda:0)
tricounts = defaultdict(lambda:defaultdict(lambda:0))

for line in language :
    line = "# # " + line.strip() + " #"
    phonemes = re.split(r'[\s]+', line)
    phonemes[2]="#" 

    for i in range(len(phonemes)-3):
        pair = (phonemes[i+1],phonemes[i+2])
        bicounts[pair] = bicounts[pair] + 1
        tricounts[pair][phonemes[i+3]] = tricounts[pair][phonemes[i+3]] + 1

language.close()

trigram = defaultdict(lambda:{})

for pair in tricounts:
    for phoneme in tricounts[pair]:
        trigram[pair][phoneme] = float(tricounts[pair][phoneme])/float(bicounts[pair])

for i in range(25):
    print(generate_word())
