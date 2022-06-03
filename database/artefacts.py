from db_actor_model.model import *
import datetime
from sqlalchemy import and_,func, case
from sqlalchemy.orm import lazyload
from sqlalchemy.exc import SQLAlchemyError


def all_artefacts(session):
   data = session.query(Artefacts).all()
   return data

def update_artefact_state(session, artefact_id, state_id, value = "no_value"):
    update_json = {"act_artefact_state_id": state_id}
    if value != "no_value":
        update_json['act_artefact_values']
    data = session \
        .query(ActArtefacts) \
        .filter(ActArtefacts.act_artefact_id == artefact_id) \
        .update(update_json)
    return data

def create_act_artefact(session, artefact):
   new_act_artefact = ActArtefacts(
    act_artefact_address = artefact['act_artefact_address'],
    act_artefact_values = artefact['act_artefact_values'],
    act_artefact_state_id = artefact['act_artefact_state_id'] ,
    artefact_artefact_id = artefact['artefact_artefact_id'])
   session.add(new_act_artefact)
   session.flush()
   return new_act_artefact.act_artefact_id