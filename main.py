
import sys
from itertools import combinations, product
from collections import OrderedDict
from copy import deepcopy

class Problem():
    def __init__(self,kb,clause,count,negate,kbOrdered) -> None:
        self.kb, self.Satclause, self.count, self.negate, self.kbOrdered = kb, clause, count, negate, kbOrdered

    """
    negates the clasue passed in
    """
    """def negate(self,specClause) -> str:
        #literals = specClause.split()
        newClause = ""
        for x in specClause.split():
            if x[0] == '~':
                if x != specClause.split()[0]:
                    newClause = newClause + " " + x[1:]
                else:
                    newClause = newClause + x[1:]

            else:
                if x != specClause.split()[0]:
                    newClause = newClause + " ~" + x
                else:
                    newClause = newClause + "~" + x
        return newClause """

        

    def resolve(self, clause1, clause2) -> str:
        """newClause = []
        resolved = False
        for x in clause1.split():
            for y in clause2.split():
                if x == self.negate(y):
                    resolved = True
                    #for a in clause1.split():
                     #   if a != x:
                      #      newClause.append(a)
                    newClause += [a for a in clause1.split() if a != x]
                    #for b in clause2.split():
                     #   if b != y:
                      #      newClause.append(b)
                    newClause += [b for b in clause2.split() if b != y]
                    return " ".join(newClause)
        
        if resolved == False:
            return "no resolution"
        #newClause = [x == self.negate(y) for (x,y) in product(clause1.split(),clause2.split())]
        #print(newClause)
        #return newClause"""
        resolved = False
        #print(clause1, clause2)
        for x in clause1:
            if negate[x] in clause2:
                #print(x)
                resolved = True
                clause1.remove(x)
                clause2.remove(negate[x])
                return clause1 + clause2
        if resolved == False:
            return "no resolution"

    def resolutionProcess(self):
        """for a in self.kb:
            b = 0
            while(b < self.kb.index(a)):
                
                if self.resolve(a,self.kb[b]) != "no resolution" and len(self.resolve(a,self.kb[b])) > 0:
                    if self.trueClause(self.resolve(a,self.kb[b])):
                        removedLit = self.removeRepLiterals(self.resolve(a,self.kb[b]))
                        if not self.logicallyEq(removedLit):
                            self.addToKb(removedLit,False)
                            print(self.count, ". ", removedLit," {",self.kb.index(a)+1,", ",b+1,"}",sep="") 
                elif len(self.resolve(a,self.kb[b])) == 0:
                    print(self.count+1,". ", "Contradiction"," {",self.kb.index(a)+1,", ",b+1,"}",sep="")
                    return "Valid"
                b+=1
        return "Fail"""
        x = 1
        while(x < len(list(self.kb))):
            b = 1
            while(b < x):
                #print(x,b)
                c1 = deepcopy(self.kb[x])
                c2 = deepcopy(self.kb[b])
                
                c = self.resolve(self.kb[x],self.kb[b])
                self.kb[x] = c1
                self.kb[b] = c2
                if c != "no resolution" and len(c) > 0:
                    if self.trueClause(c):
                        removedLit = self.removeRepLiterals(c)
                        if not self.logicallyEq(removedLit):
                            self.addToKb(removedLit,False)
                            self.kbOrdered.add(' '.join(sorted(removedLit)))
                            print(self.count-1, ". ", ' '.join(removedLit)," {",x,", ",b,"}",sep="") 
                elif len(c) == 0:
                    print(self.count,". ", "Contradiction"," {",x,", ",b,"}",sep="")
                    return "Valid"
                b+=1
                
                #print(self.kb.copy())
            x+=1
                
        return "Fail"


    def addToKb(self,specClause,first):

        if specClause == self.Satclause and first == True:
            #self.negate(specClause)
            #literals = self.negate(specClause).split()
            for x in specClause.split():
                #x might not be in negate
                if x not in negate:
                    if x[0] == '~': negate[x] = x[1:]
                    else:
                        negate[x] = '~' + x
                if negate[x] not in self.kb:
                    self.kb[self.count] = negate[x].split()
                    print(self.count,". ",negate[x]," {}",sep="")
                    if negate[x] not in negate:
                        negate[negate[x]] = x
                    #print(self.count,". ",x," {}",sep="")
                    self.count += 1
        else:
            self.kb[self.count] = (specClause)
            self.count+=1
            

    """
    tests if there are other clauses in kb that are equivalent
    only testing for something like (a b ~c) is eq to (~c a b)
    maybe need to test for more?
    """
    def logicallyEq(self, clause1) -> bool:
        """for y in self.kb:
            #literals1 = y.split()
            #literals2 = clause1.split()
            if len(y.split()) == len(clause1.split()):
                if all(x in y.split() for x in clause1.split()):return True
        return False"""
        
        if ' '.join(sorted(clause1)) in self.kbOrdered: return True
        else: return False

                

    """def logicallyEqHelp(self, clause1, clause2):
        #if len(clause1.split()) == len(clause2.split()):
         #   return all(x in clause1.split() for x in clause2.split())
        #return False
        return all(x in clause1.split() for x in clause2.split()) if len(clause1.split()) == len(clause2.split()) else False
    """

    """
    tests if clause evaluates to true or not
    """
    def trueClause(self, clause):
        #p ~p is not true, p ~q ~p
        #print(clause)
        #literals = clause.split()
    
        """for x,y in combinations(clause.split(),2):
            if x == self.negate(y) : return False
        return True"""
        #print(clause)
        for x in clause:
            if negate[x] in clause : return False
        return True

    """
    test for reduntant literals in clause and remove them
    """
    def removeRepLiterals(self, clause):
        #print(clause)
        """literals = clause.split()
        for x,y in combinations(literals,2):
            if x == y:
                literals.pop(max(i for i, item in enumerate(literals) if item == y))
        #print(" ".join(literals))
        return " ".join(literals)"""
        newC = list(OrderedDict.fromkeys(clause))
        return newC
        
    

if __name__ == "__main__":
    
    kbFile = open(sys.argv[1], 'r')
    lines = kbFile.readlines()
    clause = lines[-1]
    kb = {}
    kbOdered = set()
    negate = {}
    #kb = []
    count = 1
    for line in lines:
        if line != clause:
            #kb.append(line.strip()
            kb[count] = (line.split())
            print(count,". ",line.strip()," {}",sep="")
            kbOdered.add(' '.join(sorted(line.split())))
            for x in line.split():
                if x not in negate:
                    if x[0] == '~': negate[x] = x[1:]
                    else:
                        negate[x] = '~' + x
            count+=1
    
    #print(kbOdered)
    #print(negate)
            #print(count,". ",line.rstrip('\n')," {}",sep="")
    prob = Problem(kb,clause,count,negate,kbOdered)
    prob.addToKb(clause,True)
    #print(prob.kbOrdered)
    print(prob.resolutionProcess())

    
    
