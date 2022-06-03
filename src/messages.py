from typing import List


class ChangeStatusMessage(object):
    def __init__(self, status, value=None):
        self.status = status
        self.value = value

class InitTask(object):
    def __init__(self, name, status, artefacts, source_actor):
        self.status = status
        self.name = name
        self.required_artefacts = artefacts  # ['Artefact_1']
        self.source_actor = source_actor

class CompleteTask(object):
    def __init__(self,artefacts):
        self.artefacts = artefacts

class InitArtefact(object):
    def __init__(self, status,id, name, source_actor, value = None):
        self.id = id
        self.status =  status
        self.name = name
        self.value = value
        self.source_actor = source_actor

class InitProcess(object):
    def __init__(self, id, name, status, source_actor):
        self.id = id
        self.status = status
        self.name = name
        self.source_actor = source_actor

class ObjectStatus(object):
    def __init__(self, status, type, name,artefacts = None, value=None):
        self.type = type
        self.status = status
        self.name = name
        self.value = value

class GetTasksInfo(object):
    pass

class GetStatus(object):
    pass

