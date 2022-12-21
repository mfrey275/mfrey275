import sys
import math
import random
from collections import defaultdict
from nltk.tree import Tree

def readGrammarFile(grammarfile):

    f = open(grammarfile, "r")

    terminal_rules = defaultdict(lambda:[])
    nonterminal_rules = defaultdict(lambda:defaultdict(lambda:[]))

    for line in f:
        fields = line.split()
        if (len(fields) > 1):
            prob = float(fields[0])
            lhs = fields[1]
            rhs = fields[2:]

            if (len(rhs) == 1):
                terminal_rules[rhs[0]].append((lhs, prob))
            elif (len(rhs) == 2):
                nonterminal_rules[rhs[0]][rhs[1]].append((lhs, prob))


    return (nonterminal_rules, terminal_rules)

def read_sentences(sentencefile):

    f = open(sentencefile, "r")

    sentences = []

    for line in f:
        sentences.append(line.split())

    return sentences


def cky(grammar, sentence, T):
    nonterminal_rules, terminal_rules = grammar

    #print(nonterminal_rules)
    chart = defaultdict(lambda:defaultdict(lambda:[]))

    # loop across diagonal 
    for i in range(len(sentence)):
        for j in range(len(sentence) - i):


            #if terminal, fill chart with terminal 
            # 0,0 = word 1 -- 1,1 = word 2 -- 2,2 = word 3 == etc. 
            ### grandma   love     s      bart    and     marge    period.
            ### #0#       #1#     #2#     #3#     #4#     #5        #6#
            #0# NP, 3.7
            #1#          V, 5.09   
            #2#                 Pl, Vsuff
            #3#                            NP
            #4#                                   Conj
            #5#                                            NP
            #6#                                                     Per.

            if i == 0:
                for rule in terminal_rules[sentence[j]]:
                    #goes across diagonal cells
                    chart[j][j].append((rule[0],rule[1],(sentence[j], "terminal")))

            #else check non-terminals 
            else:
                #Establish where left and bottom cell are
                for mid in range(j, j+i):
                    left_cells = chart[mid][j]
                    bottom_cells = chart[j+i][mid+1]

                #For left and bottom cell, see if bottom rule (which bottom cell can make rule with left cell)

                    for left_cell in left_cells:
                        #print(left_cell)
                        for bottom_cell in bottom_cells:
                            #print (bottom_cell[0])
                            #print (nonterminal_rules[left_cell[0]])
                            if bottom_cell[0] in nonterminal_rules[left_cell[0]]:
                                #for each rules that can be combined given cell
                                for rule in nonterminal_rules[left_cell[0]][bottom_cell[0]]:
                                    prob = rule[1] + left_cell[1] + bottom_cell[1]
                                    backpointer = (left_cell, bottom_cell)
                                    chart[j+i][j].append((rule[0], prob, backpointer))
    #location of complete parse
    parses = chart[len(sentence)-1][0]

    for parse in parses:
        print(str(parse[1]) + ": " + parse_diagram(parse) + "\n")
    if T:
        t = Tree.fromstring(" ( " + parse_diagram(best_parse(parses)) + " ) ")
        t.draw()

                #print("left = " + str(left_cells))
                #print("bottom = " + str(bottom_cells))
                
def parse_diagram(parse):
    if parse[2][1] == "terminal":
        #returns the terminal
        return parse[0] + " ( " + parse[2][0] + " ) "
    else:
        #returns nonterminal
        return parse[0] + " ( " + parse_diagram(parse[2][0]) + ") (" + parse_diagram(parse[2][1]) + " ) "

def best_parse(parses):
    return min(parses, key=lambda parse: parse[1])



            #print("j = " + str(j) + ", j = " + str(j))
            #print(chart[j][j])
    #print(chart)


            # j+i = column , j = row --> non terminal loop
            # no list compr --> for current cell - mid (range j, j+i) left = mid , j -- bot = j+i, mid+1


def main():
    grammar_file = sys.argv[1]
    sentence_file = sys.argv[2]

    grammar = readGrammarFile(grammar_file)
    sentences = read_sentences(sentence_file)

    for sentence in sentences:
        cky(grammar, sentence, T=True)


if __name__ == "__main__":
    main()
