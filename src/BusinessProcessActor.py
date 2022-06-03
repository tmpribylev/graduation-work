from .TaskActor import *
from .ArtifactActor import *
from .RestrictionActor import *
from .BaseActor import *


class BusinessProcessMessenger(BaseMessenger):
    def chooseTaskRequest(self):
        return self._executor.getNextTaskList()

    def startTaskRquest(self, taskName):
        return self._executor.startTask(taskName)

    def artifactsListRequest(self):
        return self._executor.getArtifactList()

    def tasksOnExecutionListRequest(self):
        return self._executor.getTasksOnExecutionList()
        
    def compliteTasksListRequest(self):
        return self._executor.getCompliteTasksList()

    def activatedRestrictionsListRequest(self):
        return self._executor.getActivatedRestrictionsList()
        

class BusinessProcessExecutor(BaseExecutor):
    # def __init__(self, id=None, name=None, inputArtifacts={}, outputArtifacts={}, businessProcess=None):
    #     super().__init__(BusinessProcessMessenger)
    #     self._id = id
    #     self._name = name
    #     self._inputArtifacts = inputArtifacts
    #     self._outputArtifacts = outputArtifacts
    #     self._createdArtifacts = {}
    #     self._businessProcess = businessProcess

    # def execute(self):
    #     if self._state != 'Execute':
    #         self.state = 'Execute'

    # def createArtifact(self, name):
    #     params = self._outputArtifacts.get(name)
    #     newArtifact = ArtifactExecutor(name=name, value=params, businessProcesses=[self._businessProcess])
    #     self._createdArtifacts.update({name, newArtifact.getActorMessenger()})
    #     self._businessProcess.addArtifactRequest(newArtifact.getActorMessenger())

    #     if len(self._createdArtifacts.keys())==len(self._outputArtifacts.keys()):
    #         self._state = 'Complite'

    # def checkArtifactState(self):
    #     if self._state == 'Execute':
    #         for item in self._inputArtifacts.items():
    #             artifactState = item[1].stateRequest()
    #             if artifactState != 'Avaliable':
    #                 self._state = "Blocked"
    #                 return
            
    #         self._state = 'Execute'
