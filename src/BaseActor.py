class BaseMessenger():
    def __init__(self, executor):
        self._executor = executor
    
    def stateRequest(self):
        return self._executor.getState()

class BaseExecutor():
    def __init__(self, messenger = BaseMessenger):
        self._messenger = None
        self._state = None
        self._initActor(messenger)

    def _initActor(self, messengerClass):
        self._state = 'Created'
        self._messenger = messengerClass(self)

    def getActorMessenger(self):
        return self._messenger
        
    def getState(self):
        return self._state

    def setState(self, value):
        self._state = value


