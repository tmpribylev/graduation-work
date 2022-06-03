from .BaseActor import *
from .ArtifactActor import *
from .BusinessProcessActor import *

class TaskMessenger(BaseMessenger):
    def startRequest(self):
        self._executor.execute()

    def addArtifact(self, artifactName):
        self._executor.createArtifact(artifactName)

    def checkArtifactStateRequest(self):
        self._executor.checkArtifactState()

class TaskExecutor(BaseExecutor):
    def __init__(self, id=None, name=None, inputArtifacts={}, outputArtifacts={}, businessProcess=None):
        super().__init__(TaskMessenger)
        self._id = id
        self._name = name
        self._inputArtifacts = inputArtifacts
        self._outputArtifacts = outputArtifacts
        self._createdArtifacts = {}
        self._businessProcess = businessProcess

    def execute(self):
        if self._state != 'Execute':
            self.state = 'Execute'

    def createArtifact(self, name):
        params = self._outputArtifacts.get(name)
        newArtifact = ArtifactExecutor(name=name, value=params, businessProcesses=[self._businessProcess])
        self._createdArtifacts.update({name, newArtifact.getActorMessenger()})
        self._businessProcess.addArtifactRequest(newArtifact.getActorMessenger())

        if len(self._createdArtifacts.keys())==len(self._outputArtifacts.keys()):
            self._state = 'Complite'

    def checkArtifactState(self):
        if self._state == 'Execute':
            for item in self._inputArtifacts.items():
                artifactState = item[1].stateRequest()
                if artifactState != 'Avaliable':
                    self._state = "Blocked"
                    return
            
            self._state = 'Execute'
