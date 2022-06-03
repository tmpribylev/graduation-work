from db_actor_model.model import *
import datetime
from sqlalchemy import and_,func, case
from sqlalchemy.orm import lazyload
from sqlalchemy.exc import SQLAlchemyError


def all_tasks(session):
   data = session.query(Tasks).all()
   return data

def process_task(session, process_id):
   data = session.query(Tasks).filter(Tasks.process_process_id == process_id)\
      .options(lazyload(Tasks.required_artefacts, Artefacts.act_artefacts))\
      .all()
   return data

def task_artefacts(session, task_id):
   data = session.query(Tasks).filter(Tasks.task_id == task_id)\
      .options(lazyload(Tasks.required_artefacts, Artefacts.act_artefacts))\
      .first()
   return data


def create_act_task(session, task):
   new_act_task = ActTasks(
      act_task_address=task['act_task_address'],
      act_task_state_id=task['act_task_state_id'],
      task_task_id =task['task_task_id'],

   )
   session.add(new_act_task)
   session.flush()
   return new_act_task.act_task_id


def update_task_state(session, task_id, state_id):
   data = session \
      .query(ActTasks) \
      .filter(ActTasks.act_task_id == task_id) \
      .update({"act_task_state_id": state_id})
   return data