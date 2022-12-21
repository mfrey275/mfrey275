import sys
import math
from collections import defaultdict
from nltk.tree import Tree

def readGrammarFile(grammarf):

    terminal_rules = defaultdict(lambda:[])
    nonterminal_rules = defaultdict(lambda:defaultdict(lambda:[]))

    for line in grammarf:
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

def readSentences(sentencef):
    
    sentences = []
    for line in sentencef:
        sentences.append(line.split())
    return sentences

def cky(grammar, sentence, T):
    nonterminal_rules, terminal_rules = grammar

    chart = defaultdict(lambda:defaultdict(lambda:[]))

    #loop through chart
    for i in range(len(sentence)):
        for j in range(len(sentence) - i):
            if i == 0:
                for rule in terminal_rules[sentence[j]]:
                    #goes across diagonal cells
                    chart[j][j].append((rule[0],rule[1],(sentence[j], "terminal")))
            #check non-terminals 
            else:
                #find cell to left and bottom of current cell
                for mid in range(j, j+i):
                    left_cells = chart[mid][j]
                    bottom_cells = chart[j+i][mid+1]

                    #which rules can combine with left and bottom cells
                    for left_cell in left_cells:
                        for bottom_cell in bottom_cells:
                            if bottom_cell[0] in nonterminal_rules[left_cell[0]]:
                                #for each rules that can be combined with given cell
                                for rule in nonterminal_rules[left_cell[0]][bottom_cell[0]]:
                                    prob = rule[1] + left_cell[1] + bottom_cell[1]
                                    backpointer = (left_cell, bottom_cell)
                                    chart[j+i][j].append((rule[0], prob, backpointer))
    #location of complete parse
    parses = chart[len(sentence)-1][0]
    
    #formats bracketed parse and tree
    for parse in parses:
        print(str(parse[1]) + ": " + diagram(parse) + "\n")
    if T:
        t = Tree.fromstring(" ( " + diagram(best_parse(parses)) + " ) ")
        t.draw()

#make the parse diagram             
def diagram(parse):
    if parse[2][1] == "terminal":
        #returns the terminal
        return parse[0] + " ( " + parse[2][0] + " ) "
    else:
        #returns nonterminal
        return parse[0] + " ( " + diagram(parse[2][0]) + ") (" + diagram(parse[2][1]) + " ) "

def best_parse(parses):
    return max(parses, key=lambda parse: parse[1])

def main():
    grammarf = open(sys.argv[1], "r")
    sentencef = open(sys.argv[2], "r")

    grammar = readGrammarFile(grammarf)
    sentences = readSentences(sentencef)

    for sentence in sentences:
        cky(grammar, sentence, T=True)

    grammarf.close()
    sentencef.close()

if __name__ == "__main__":
    main()
