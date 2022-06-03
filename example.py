from src import Artefact
from src import Process
from database import ARTEFACTS, PROCESSES
from src.messages import *
from thespian.actors import *
from database.tasks import *
from database.artefacts import *
from database.processes import *
from db_actor_model.database import get_db_local
from fastapi.encoders import jsonable_encoder


class SourceActor(ActorTypeDispatcher):
    def __init__(self, *args, **kw):
        self.artefacts = {}
        self.processes = {}

    def receiveMsg_ObjectStatus(self, message, sender):
        if message.type == 'artefact':
            self.artefacts[message.name] = {'address': sender, 'status': message.status, 'value': message.value}
            print(f"Update artefacts info: {self.artefacts[message.name]}")
        elif message.type == 'process':
            self.processes[message.name] = {'address': sender, 'status': message.status}
            print(f"Update processes info: {self.processes[message.name]}")

    def receiveMsg_str(self, message, sender):
        if message == 'start_system':
            session = get_db_local()
            db_artefacts = jsonable_encoder(all_artefacts(session))
            for i in db_artefacts:
                artefact = self.createActor(Artefact)
                art_id = create_act_artefact(session, {'act_artefact_address': str(artefact),
                                                       'act_artefact_values': 3,
                                                       'act_artefact_state_id': 1,
                                                       'artefact_artefact_id': i['artefact_id']})

                self.send(artefact, InitArtefact(name=i['artefact_id'],
                                                 id=art_id,
                                                 status='exist',
                                                 value=3,
                                                 source_actor=self.myAddress))
                ARTEFACTS[art_id] = artefact
                print(ARTEFACTS)

            process = self.createActor(Process)
            proc_id = create_act_process(session, {'act_process_address': str(process),
                                                   'act_process_state_id': 3,
                                                   'process_process_id': 'process_1'})
            self.send(process, InitProcess(id=proc_id,
                                           name='process_1',
                                           status='in_progress',
                                           source_actor=self.myAddress))
            PROCESSES[proc_id] = process
            print(PROCESSES)

        elif message == 'break_artefact':
            self.send(self.artefacts['Artefact_1']['address'], ChangeStatusMessage(status='broken'))

        elif message == 'complete_task':
            print(self.artefacts)
            self.send(self.processes['Process_1']['address'], CompleteTask(artefacts=self.artefacts))

        elif message == 'processes_info':
            print(f"Processes info: {self.processes}")
        elif message == 'tasks_info':
            self.send(self.processes['Process_1']['address'], GetTasksInfo())
        elif message == 'artefacts_info':
            print(f"Artefacts info: {self.artefacts}")
        elif message == 'fix_artefact':
            self.send(self.artefacts['Artefact_1']['address'], ChangeStatusMessage(status='exist'))


def print_menu():
    menu = 'Меню\n'
    menu += '\t1. Запустить систему\n'
    menu += '\t2. Изменить статус артефакта(на broken)\n'
    menu += '\t3. Выполнить таску\n'

    menu += '\t4. Статусы процессов\n'
    menu += '\t5. Статусы задач\n'
    menu += '\t6. Статусы артефактов\n'
    menu += '\t7. Изменить статус артефакта(на "exist")\n'

    menu += '\t8. Стоп\n'
    print(menu)


def execute_menu(inp, source, system):
    if inp == 1:
        system.ask(source, 'start_system')
        print('Start system')
    if inp == 2:
        system.ask(source, 'break_artefact')
    if inp == 3:
        system.ask(source, 'complete_task')
    if inp == 4:
        system.ask(source, 'processes_info')
    if inp == 5:
        system.ask(source, 'tasks_info')
    if inp == 6:
        system.ask(source, 'artefacts_info')
    if inp == 7:
        system.ask(source, 'fix_artefact')


if __name__ == '__main__':
    #session = get_db_local()

    #data = process_task(session, 'process_1')
    #data = task_artefacts(session, 'task_1')
    # data = all_artefacts(session)
    #print(jsonable_encoder(data))

    system = ActorSystem()
    source = system.createActor(SourceActor)
    inp = -1
    while inp != 8:
        print_menu()
        inp = int(input())
        execute_menu(inp, source, system)
