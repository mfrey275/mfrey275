# the A and B matrices as dictionaries
A = {'N':{'N':0.54, 'V':0.23, 'R':0.08, '#':0.15}, 'V':{'N':0.62, 'V':0.17, 'R':0.11, '#':0.10}, 'R':{'N':0.17, 'V':0.68, 'R':0.10, '#':0.05}, '#':{'N':0.7, 'V':0.2, 'R':0.1, '#':0.0}}
B = {'N':{'time':0.98, 'flies':0.015, 'quickly':0.005, '#':0.0}, 'V':{'time':0.33, 'flies':0.64, 'quickly':0.03, '#':0.0}, 'R':{'time':0.01, 'flies':0.01, 'quickly':0.98, '#':0.0}, '#':{'time':0.0, 'flies':0.0, 'quickly':0.0, '#':1.0}}
# Define a new emission matrix B2 for Question 4
B2 = {'N':{'swat':0.0, 'time':0.4, 'flies':0.59, 'quickly':0.005, '#':0.0}, 'V':{'swat':0.52, 'time':0.15, 'flies':0.3, 'quickly':0.03, '#':0.0}, 'R':{'swat':0.0, 'time':0.01, 'flies':0.01, 'quickly':0.98, '#':0.0}, '#':{'swat':0.0, 'time':0.0, 'flies':0.0, 'quickly':0.0, '#':1.0}}
# two data structures you may find useful for mapping between tags and their (arbitrary) indices
tagnum = {"N":0,"V":1,"R":2,"#":3}    #gives index for a given tag
numtag = ['N','V','R','#']   #gives tag for a given index

wordlist = ['time', 'flies', 'quickly', '#']

def print_table(table, words, ef='%.4f', colwidth=12):
    tags = A.keys()
    print(''.ljust(colwidth), end='')
    for w in words:
        print(str(w).ljust(colwidth), end='')
    print()
    for n in range(len(A.keys())):
        print(str(numtag[n]).ljust(colwidth), end='')
        for t in range(len(words)):
            out = str(table[t][n])
            if type(table[t][n]) == tuple: 
                form=ef+",%s"
                out = form % (table[t][n][0], table[t][n][1])
            elif type(table[t][n]) == float:
                out = str(ef % table[t][n])
            print(out.ljust(colwidth), end='')
        print()

def forward(ws, A, B):
    ## PART 1 YOUR FORWARD CODE GOES HERE
    # add '#' to the beginning and end of ws
    pound = ('#',)
    newseq = pound + ws + pound
    T = len(newseq)
    # range of number of states
    N = len(numtag)
    # create table to show results
    table = [[0]*N for i in range(T)]
    prob = 0.0
    # initialize '#' prob = 1 at time step 1 and all other probs = 0
    for i in range(N):
        table[0][i] = (B['#'][wordlist[i]])
        prob += table[0][i]
    for t in range(1,T):
        for j in range(N):
            for i in range(N):
                # sum(t-1 probability*transition prob*emission prob) 
                table[t][j] += table[t-1][i]*A[numtag[i]][numtag[j]]*B[numtag[j]][newseq[t]]
    # returns probability of '#' in last cell of the table
    return(table[t][j])

def viterbi(ws, A, B):
    ## PART 2 YOUR VITERBI CODE GOES HERE
    pound = ('#',)
    newseq = pound + ws + pound
    T = len(newseq)
    N = len(numtag)
    # create table v for viterbi probabilities
    v = [[0]*N for i in range(T)]
    # create table b for backpointers
    b = {}
    # initialize '#' v prob = 1 at time step 1 and all other probs = 0
    for i in range(N):
        v[0][i] = (B['#'][wordlist[i]])
        b[i] = [i]
    for t in range(1, T):
        best_path = {}
        for j in range(N):
            for i in range(N):
                (prob, state) = max((v[t-1][i]*A[numtag[i]][numtag[j]]*B[numtag[j]][newseq[t]], i) for i in range(N))
                v[t][j] = prob
                best_path[j] = b[state] + [j]
        # keep only the best path
        b = best_path
    # gives tag for number index of the state
    for i in range(T):
        best_path[3][i] = numtag[best_path[3][i]]
    return (prob, best_path[3])

### MAIN CODE GOES HERE ###
seq = ('time','flies','quickly')
print("calculating forward probability of", seq, ":\n", forward(seq, A, B))
print("calculating most likely tags for", seq, ":\n", viterbi(seq, A, B))
seq = ('quickly', 'time','flies')
#print("calculating forward probability of", seq, ":\n", forward(seq, A, B))
#print("calculating most likely tags for", seq, ":\n", viterbi(seq, A, B))
seq = ('swat','flies','quickly')
#print("calculating most likely tags for", seq, ":\n", viterbi(seq, A, B2))
