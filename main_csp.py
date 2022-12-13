
#from calendar import c
import sys
from typing import List, Dict

class CSPSolve():
    """
        holds a list of the variables
        holds a dict for each variable with its domain
        holds a dict for each variable and the constraints on it
    """
    def __init__(self, variables, domains, consistency) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints: Dict[str, List[str]] = {}
        self.consistency = consistency
        self.count = 0
        for v in self.variables:
            self.constraints[v] = []

    def addConstraint(self, v1,v2,op) -> None:
        for v in self.variables:
            if v == v1 or v == v2:
                self.constraints[v].append(v1 + op + v2)
        

    def works(self, assignments: Dict[str, int], var1: str, value) -> bool:
        #print(self.constraints[var1])
        satisfied = False
        for c in self.constraints[var1]:
            #print(c)
            if c[0] == var1:
                if c[2] not in assignments:
                    satisfied = True
                    continue
                if c[1] == '=':
                    if value == assignments[c[2]] : satisfied = True
                    else : satisfied = False
                elif c[1] == '<':
                    if value < assignments[c[2]] : satisfied = True
                    else : satisfied = False
                elif c[1] == '>':
                    if value > assignments[c[2]] : satisfied = True
                    else : satisfied = False
                elif c[1] == '!=':
                    if value != assignments[c[2]] : satisfied = True
                    else : satisfied = False
            if c[2] == var1:
                if c[0] not in assignments:
                    satisfied = True
                    continue
                if c[1] == '=':
                    if assignments[c[0]] == value : satisfied = True
                    else : satisfied = False
                elif c[1] == '<':
                    if assignments[c[0]] < value : satisfied = True
                    else : satisfied = False
                elif c[1] == '>':
                    if assignments[c[0]]> value: satisfied = True
                    else : satisfied = False
                elif c[1] == '!=':
                    if assignments[c[0]] != value : satisfied = True
                    else : satisfied = False
            if (satisfied == False):
                return satisfied
        if len(self.constraints[var1]) == 0:
            satisfied = True
        return satisfied

    def chooseTechnique(self,technique) -> Dict:
        if technique == "none":
            return self.backTracking({})
        elif technique == "fc":
            oDomains = []
            return self.forwardChecking({},oDomains)
            
    
    def forwardChecking(self, assignments,oDomains) -> Dict:
        if len(assignments) == len(self.variables):
            #print(assignments)
            return assignments
        variable = self.variableH1(assignments)
        #print(variable)
        #print(assignments)
        for value in self.leastConstrainingValue(variable, assignments):
            #print(value)
            if self.works(assignments,variable, value):
                assignments[variable] = value
                #print(self.domains)
                oDomains.append(self.domains.copy())
                for y in self.variables:
                    if y != variable:
                        self.removeDomains(y,assignments,variable)
                emptyDomain = False
                for x in self.variables:
                    if len(self.domains[x]) == 0 and x not in assignments:
                        emptyDomain = True
                        break
                if emptyDomain == False:
                    result = self.forwardChecking(assignments,oDomains)
                    if result != None:
                        return result
                    self.domains = oDomains.pop()
                    assignments.pop(variable)    
                    #print(self.domains)
                else:
                    self.domains = oDomains.pop()
                #print(self.domains)
                    assignments.pop(variable)
                    self.printBranch(assignments,variable,value)
            else:
                self.printBranch(assignments,variable,value)
        return None

    def removeDomains(self, var2, assignment,variable):
        #print(self.constraints[variable])
        for c in self.constraints[variable]:
            if (c[0] == var2 or c[2] == var2) and var2 not in assignment:
                oldDomains = self.domains[var2]
                del self.domains[var2]
                self.domains[var2] = []
                for value in oldDomains:
                    if c[0] == var2:
                        if c[1] == '=':
                            if value == assignment[variable] : self.domains[var2].append(value)
                        elif c[1] == '<':
                            if value < assignment[variable] : self.domains[var2].append(value)
                        elif c[1] == '>':
                            if value > assignment[variable] : self.domains[var2].append(value)
                        elif c[1] == '!=':
                            if value != assignment[variable] : self.domains[var2].append(value)
                    elif c[2] == var2:
                        if c[1] == '=':
                            if assignment[variable] == value : self.domains[var2].append(value)
                        elif c[1] == '<':
                            if assignment[variable] < value : self.domains[var2].append(value)
                        elif c[1] == '>':
                            if assignment[variable] > value: self.domains[var2].append(value)
                        elif c[1] == '!=':
                            if assignment[variable] != value : self.domains[var2].append(value)
                #print(var2,self.domains[var2])


    def backTracking(self, assignments)->Dict:
        if len(assignments) == len(self.variables):
            #print(assignments)
            return assignments
        variable = self.variableH1(assignments)
        #print(variable)
        #print(assignments)
        for value in self.leastConstrainingValue(variable, assignments):
            #print(value)
            if self.works(assignments,variable, value):
                assignments[variable] = value
                result = self.backTracking(assignments)
                if result != None:
                    return result  
                assignments.pop(variable)
            else:
                #print(assignments)
                self.printBranch(assignments,variable,value)
        return None

    def printBranch(self, assignments,variable, value):
        self.count+=1
        print(self.count,". ",end="",sep="")
        for x, y in assignments.items():
            print(x,"=",y,", ",end="",sep="")
        print(variable, "=",value,sep="",end=" ")
        print(" failure")
        

    #most constrained variable heuristic
    def variableH1(self, assignments) -> str:
        numValuesPerVar = []
        maxNum = []
        for v in self.variables:
            if v not in assignments.keys():
                numValuesPerVar.append(len(self.domains[v]))
        minNum = min(numValuesPerVar)
        for x in self.variables:
            if x not in assignments.keys():
                if len(self.domains[x]) == minNum:
                    maxNum.append(x)
        #print(maxNum)
        if len(maxNum) == 1:
            return maxNum.pop()
        else:
            return self.variableH2(maxNum, assignments)

    #most constraining variable heuristic
    def variableH2(self, list, assignments) -> str:
        numConstraints = []
        minVar = []
        for v in list: #need to count constraints with unassigned vars
            numConstraints.append(self.countRemainingCon(assignments, v))
        maxCon = max(numConstraints)
        for x in list:
            if self.countRemainingCon(assignments,x) == maxCon:
                minVar.append(x)
        #print(minVar)
        if(len(minVar) == 1):
            return minVar.pop()
        else: #break tie alphabetically
            return min(minVar)

    def countRemainingCon(self, assignments, var) -> int:
        count = 0
        for c in self.constraints[var]:
            if c[0] == var:
                if c[2] not in assignments:
                    count += 1
            if c[2] == var:
                if c[0] not in assignments:
                    count += 1
        return count


    def leastConstrainingValue(self, variable: str, assignments) -> list:
        orderedValueList = {}
        
        for value in self.domains[variable]:
            count = 0
            
            for var2 in self.variables:
                inConstraint = False
                if var2 not in assignments and var2 != variable:
                    for constraint in self.constraints[var2]:
                        #print(constraint)
                        if (var2 == constraint[0] and variable == constraint[2]) or (var2 == constraint[2] and variable == constraint[0]):
                            count += self.countLegalDomains(value,constraint,var2)
                            inConstraint = True
                    if inConstraint == False:
                        count += len(self.domains[var2])
                    #print(count, var2)
            orderedValueList[value] = count

        #want to return variables domain ordered not the amount of legal moves for the other variables
        #print(orderedValueList, sorted(orderedValueList, key=orderedValueList.get))
        return sorted(orderedValueList, key=orderedValueList.get,reverse=True)
    
    
    def countLegalDomains(self,value1, c, var2) -> int:
        count = 0
        for value in self.domains[var2]:
            
            if c[0] == var2:
                if c[1] == '=':
                    if value == value1 : count += 1
                elif c[1] == '<':
                    if value < value1 : count += 1
                elif c[1] == '>':
                    if value > value1 : count += 1
                elif c[1] == '!=':
                    if value != value1 : count += 1
            elif c[2] == var2:
                if c[1] == '=':
                    if value1 == value : count += 1
                elif c[1] == '<':
                    if value1 < value : count += 1
                elif c[1] == '>':
                    if value1 > value: count += 1
                elif c[1] == '!=':
                    if value1 != value : count += 1
        
        return count
    

if __name__ == "__main__":
    
    variablesFile = open(sys.argv[1], 'r')
    constraintsFile = open(sys.argv[2], 'r')
    consistency = sys.argv[3]

    domains = {}
    constraints = []
    variables = []
    #add the variables and domains
    for line in variablesFile:
        variables.append(line[0])
        domains.update({line[0]: line[3:].split()})
    #create the object for the problem
    csp = CSPSolve(variables, domains, consistency)
    #add the constraints to the problem
    for line in constraintsFile:
        csp.addConstraint(line[0],line[4],line[2])
    #print(csp.constraints)
    #print(csp.leastConstrainingValue('F',assignments={}))
    solution = csp.chooseTechnique(consistency)
    if solution != None:
        print(csp.count+1,". ",end="",sep="")
        for x, y in solution.items():
            print(x,"=",y,end="",sep="")
            if(x != list(solution)[-1]):
                print(", ",end="")
        print("  solution")