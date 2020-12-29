import re
import functools

class Term:
    def __init__(self, term):
        self.setCoefficient(term)
        self.setExponent(term) # x^0 = 1
        
    def setCoefficient(self, term):
        self.coefficient = re.search(r'(?<!\^)[-+]?\d+', term)
        self.coefficient = ( int(self.coefficient.group(0)) if self.coefficient 
                             else -1 if term[0] == '-' else 1 )

    def setExponent(self, term):
        if 'x' in term:
            self.exponent   = re.search(r'(?<=\^)\d+', term)
            self.exponent   = int(self.exponent.group(0)) if self.exponent else 1
        else: self.exponent = 0

def expandPolynomial(poly):
    eqList = re.findall(r'\(([^()]+)\)', poly)
    if len(eqList) == 1: eqList = eqList * 2
    return functools.reduce(productTwoEquations, eqList)

def splitIntoTerms(equation):
    termList = re.findall(r'[-+][^-+]+|^[^-+]+(?=[-+])', equation)
    return [Term(term) for term in termList]

def productTwoEquations(eq1, eq2):
    eq1 = splitIntoTerms(eq1)
    eq2 = splitIntoTerms(eq2)
    expandedPoly = ''
    for term1 in eq1:
        for term2 in eq2:
            expandedPoly += '+' + getProduct(term1, term2)
    expandedPoly = formatPoly(expandedPoly)
    return simplify(expandedPoly)

def getProduct(term1, term2):
    newCoefficient = str(term1.coefficient*term2.coefficient)
    newX           = 'x' if term1.exponent > 0 or term2.exponent > 0 else ''
    newExponent    = term1.exponent + term2.exponent
    newExponent    = '^'+str(newExponent) if newExponent > 1 else ''
    return newCoefficient + newX + newExponent

def simplify(expandedPoly):
    termList = splitIntoTerms(expandedPoly)
    expDict  = divideTermsIntoExps(termList)
    return combineGroupedTermsIntoEquation(expDict)

def divideTermsIntoExps(termList):
    expDict  = {}
    for term in termList:
        if term.exponent in expDict:
            expDict[term.exponent].append(term)
        else: expDict[term.exponent] = [term]
    return expDict

def combineGroupedTermsIntoEquation(expDict):
    for key, termList in expDict.items():
        if len(termList) > 1:
            expDict[key] = functools.reduce(addition, termList)
        if len(termList) == 1:
            term = expDict[key][0]
            x    = 'x' if term.exponent > 0 else ''
            exp  = '^'+str(term.exponent) if term.exponent > 1 else ''
            expDict[key] = str(term.coefficient)+x+exp
    
    expList = sorted(expDict, reverse=True)
    simplifiedPoly = ''
    for exp in expList: simplifiedPoly += '+' + expDict[exp]
    return formatPoly(simplifiedPoly)

def addition(term1, term2):
    if type(term1) == str: term1 = Term(term1)
    newCoefficient = str(term1.coefficient+term2.coefficient)
    newX           = 'x' if term1.exponent > 0 else ''
    newExponent    = '^'+str(term1.exponent) if term1.exponent > 1 else ''
    return newCoefficient+newX+newExponent

def formatPoly(poly):
    zeroesRemoved    = re.sub(r'[-+]0x(\^\d)?', '', poly)
    oneInOneXRemoved = re.sub(r'(?<!\d)1(?=x)', '', zeroesRemoved)
    return oneInOneXRemoved.replace('+-', '-')[1:]

print(expandPolynomial(input('Please enter a polynomial to be expanded:\n')))