from .BaseActor import *
from .ArtifactActor import *
from .BusinessProcessActor import *

class RestrictionMessenger(BaseMessenger):
    def __init__(self, executor):
        super().__init__(executor)

class RestrictionExecutor(BaseExecutor):
    def __init__(self, id=None, name=None, inputArtifacts={}, outputArtifact={'artFalse' : 'False', 'artTrue' : 'True'}, expression='', businessProcess=None):
        super().__init__(RestrictionMessenger)
        self._id = id
        self._name = name
        self._inputArtifacts = inputArtifacts
        self._outputArtifacts = outputArtifact
        self._businessProcess = businessProcess
        self._expression = expression.replace(' ', '')
        self._artifactReferences = {}
        self._state = 'Inactivated'

    def getState(self):
        artifacts = self._businessProcess.artifactRequest()

        full = True
        atrifactReferences = {}
        for artifactName in self._inputArtifacts.keys():
            if artifactName not in artifacts.keys():
                full = False
                break
            else:
                atrifactReferences.update({artifactName : artifacts[artifactName]})

        if full:
            self._executeExpression()
            self._state = 'Activated'
            self._artifactReferences = atrifactReferences

        return super().getState()

    def createArtifact(self, name):
        params = self._outputArtifacts.get(name)
        newArtifact = ArtifactExecutor(name=name, value=params, businessProcesses=[self._businessProcess])
        self._businessProcess.addArtifactRequest(newArtifact.getActorMessenger())

    def executeExpression(self):
        expressionList = self._splitExpression()
        RPN = self._toReversePolishNotation(expressionList)
        result = self._executeRPN(RPN)
        if result:
            for item in self._outputArtifacts.items():
                if item[1] == 'True':
                    self.createArtifact(item[0])
                    break
        else:
            for item in self._outputArtifacts.items():
                if item[1] == 'False':
                    self.createArtifact(item[0])
                    break

    def _executeRPN(self, RPN):
        special_symbols = ['&', '|', '==', '!=', '!']
        executeStack = []
        while RPN != []:
            item = RPN.pop(0)
            
            if item not in special_symbols:
                executeStack.append(item)
            elif item in ['==', '!=']:
                oper1 = executeStack.pop()
                oper2 = executeStack.pop()

                if oper1 not in self._artifactReferences.keys():
                    oper1 = oper1[1:len(oper1)-1]
                else:
                    oper1 = self._artifactReferences[oper1].valueRequest()

                if oper2 not in self._artifactReferences.keys():
                    oper2 = oper2[1:len(oper2)-1]
                else:
                    oper2 = self._artifactReferences[oper2].valueRequest()
                
                if item == '==':
                    result = oper1 == oper2
                    executeStack.append(result)
                else:
                    result = oper1 != oper2
                    executeStack.append(result)
            elif item == '&':
                oper1 = executeStack.pop()
                oper2 = executeStack.pop()

                result = oper1 & oper2
                executeStack.append(result)
            elif item == '|':
                oper1 = executeStack.pop()
                oper2 = executeStack.pop()

                result = oper1 | oper2
                executeStack.append(result)
            elif item == '!':
                oper1 = executeStack.pop()

                result = not oper1
                executeStack.append(result)
        
        ans = executeStack.pop()
        return ans
                
    def _splitExpression(self):
        special_symbols = ['!', '=', '&', '|', '(', ')']
        expressionList = []
        str = ''

        for s in self._expression:
            if s not in special_symbols:
                str += s
            
            else:
                if str != '':
                    expressionList.append(str)
                    str = ''
                expressionList.append(s)
        if str != '':
            expressionList.append(str)
        
        return expressionList
                
        
    def _toReversePolishNotation(self, expression):
        charStack = []
        finalStack = []
        priority = {'!': 4, '==': 3, '!=': 3, '&': 2, '|': 1}
        i = 0

        while i < len(expression):
            item = expression[i]
            if (item == '!' and expression[i+1] == '=') | (item == '='):
                i += 1
                item += expression[i]
            
            if item == ')':
                while charStack[-1] != '(':
                    finalStack.append(charStack.pop())
                charStack.pop()

            elif item == '(':
                charStack.append(item)
                
            elif item not in priority.keys():
                finalStack.append(item)

            else:
                while True:
                    if charStack != []:
                        if priority[charStack[-1]] > priority[item]:
                            finalStack.append(charStack.pop())
                        else:
                            charStack.append(item)
                            break
                    else:
                        charStack.append(item)
                        break
            
            i += 1
        
        while charStack != []:
            finalStack.append(charStack.pop())
        
        return finalStack
                



