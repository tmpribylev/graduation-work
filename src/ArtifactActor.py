from .BaseActor import *

class ArtifactMessenger(BaseMessenger):
    def valueRequest(self):
        return self._executor.getValue()

    def newValueRequest(self, value):
        self._executor.setValue(value)

    def newStateRequest(self, state):
        self._executor.updateState(state)

    def stateSend(name, state, receiver):
        receiver.receiveArtifactState(name, state)

class ArtifactExecutor(BaseExecutor):
    def __init__(self, id=None, name=None, value=None, businessProcesses=[]):
        super().__init__(ArtifactMessenger)
        self._id = id
        self._name = name
        self._value = value
        self._businessProcesses = businessProcesses
        self._state = 'Available'

    def updateState(self, value):
        super().setState(value)
        for actor in self._businessProcesses:
            self._messenger.stateSend(self._name, self._state, actor)


    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value