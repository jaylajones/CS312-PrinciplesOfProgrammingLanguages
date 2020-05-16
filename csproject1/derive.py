# Read the length N from the command argument (or from input).
# Read and store all the productions.
# Push the start symbol onto the  worklist.
# While the worklist is not empty:
# Get and delete one potential sentence s from the worklist.
# If the | s | > N, continue.
# If s has no nonterminals, print s and continue.
# Choose the leftmost nonterminal NT.
# For all productions NT -> rhs:
#	Replace NT in s with rhs; call it tmp.
#	Store tmp on worklist.
# WANT A READ ONLY FILE, DONT DAMAGE IT
import string
from collections import deque


def Deriver():

    N = int(input("input an arbitrary N:"))
    file_N = input("Chosen file: ")
    StartSymbol = None
    templist = []

# WANT A READ ONLY FILE, DONT DAMAGE IT
# need A deque to just pop off the values from wherever it wants
# easier than getting a big loop from [-1]
    grammars = dict()

    # Includes all symbols excluding "=" and Start symbol

    file_parser = open(file_N, "r")

    for line in file_parser:
        values = line.split()
        NonTerminal = values[0]
        DerivedValues = values[2:]
    # for item in values:

        # This means we have just started our tree and the start symbol is the first value in values
        if StartSymbol == None:
            StartSymbol = values[0]
            worklist = deque([[StartSymbol]])

        if NonTerminal not in (grammars):
            grammars[NonTerminal] = [DerivedValues]

        else:
            grammars[NonTerminal].append(DerivedValues)

    while(len(worklist) > 0):
        s = worklist.popleft()
        if len(s) > N:
            continue
        i = 0
        r = 0
        ##
        for val in s:
            if val in grammars:
                NonterminalNext = val
                r = 1
                break
            i += 1
        if(r == 0):
            stream = ""
            for piece in s:
                stream += piece + " "
            print(stream)
        else:
            for j in grammars[NonterminalNext]:
                tmp = s[:i] + j + s[i+1:]
                if tmp not in templist:
                    templist.append(tmp)
                    worklist.append(tmp)


if __name__ == "__main__":
    Deriver()
    # NewDeriver()
