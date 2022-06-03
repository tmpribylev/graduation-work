from db_actor_model.model import *
import datetime
from sqlalchemy import and_, func, case
from sqlalchemy.orm import lazyload
from sqlalchemy.exc import SQLAlchemyError


def all_processes(session):
    data = session.query(Processes).all()
    return data


def create_act_process(session, process):
    new_act_process = ActProcesses(
        act_process_address= process['act_process_address'],
        act_process_state_id= process['act_process_state_id'],
        process_process_id= process['process_process_id']
    )
    session.add(new_act_process)
    session.flush()
    return new_act_process.act_process_id

def update_process_state(session, process_id, state_id):
    data = session \
        .query(ActProcesses) \
        .filter(ActProcesses.act_process_id == process_id) \
        .update({"act_process_state_id": state_id})

    return data
