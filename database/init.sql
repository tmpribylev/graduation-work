CREATE DATABASE dev;

GRANT ALL privileges on database new_mlc to mlc;
SET TIMEZONE TO 'EUROPE/MOSCOW';

/* DROP TABLES */
DROP TABLE IF EXISTS states;
DROP TABLE IF EXISTS artefacts;
DROP TABLE IF EXISTS processes;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS links_artefacts_X_tasks;
DROP TABLE IF EXISTS act_artefacts;
DROP TABLE IF EXISTS act_processes;
DROP TABLE IF EXISTS act_tasks;
DROP TABLE IF EXISTS artefact_X_task;
DROP TABLE IF EXISTS process_X_task;

/* DROP SEQUENCES */
DROP SEQUENCE IF EXISTS artefact_id_seq;
DROP SEQUENCE IF EXISTS task_id_seq;
DROP SEQUENCE IF EXISTS process_id_seq;



/* CREATE DIRECTORY TABLES */
CREATE TABLE artefacts
(
  artefact_id    TEXT NULL,
  artefact_desc  TEXT NULL,
  PRIMARY KEY (artefact_id)
);

CREATE TABLE processes
(
  process_id    TEXT NOT NULL,
  process_desc  TEXT NULL,
  PRIMARY KEY (process_id)
);

CREATE TABLE tasks
(
  task_id    TEXT NOT NULL,
  task_desc  TEXT NULL,
  priority INTEGER    NOT NULL,
  process_process_id TEXT  NOT NULL,
  PRIMARY KEY (task_id, process_process_id)
);

CREATE TABLE links_artefacts_X_tasks
(
  task_task_id    TEXT NOT NULL,
  required_artefact  TEXT NOT NULL,
  PRIMARY KEY (task_task_id, required_artefact)
);

CREATE TABLE states
(
  state_id    INTEGER  NOT NULL,
  state_desc TEXT NULL,
  PRIMARY KEY (state_id)
);

/* CREATE ACTOR TABLES */
CREATE TABLE act_artefacts
(
  act_artefact_id        INTEGER NOT NULL,
  act_artefact_address        TEXT NOT NULL,
  act_artefact_state_id  INTEGER NOT NULL,
  act_artefact_values TEXT NULL,
  artefact_artefact_id TEXT NOT NULL,
  act_process_process_id INTEGER NULL,
  start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_date TIMESTAMP DEFAULT '5999-12-31 23:59:59' NOT NULL,
  PRIMARY KEY (act_artefact_id, start_date)
);

CREATE TABLE act_processes
(
  act_process_id        INTEGER NOT NULL,
  act_process_address        TEXT NOT NULL,
  act_process_state_id  INTEGER NOT NULL,
  process_process_id TEXT NOT NULL,
  start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_date TIMESTAMP DEFAULT '5999-12-31 23:59:59' NOT NULL,
  PRIMARY KEY (act_process_id, start_date)
);

CREATE TABLE act_tasks
(
  act_task_id        INTEGER NOT NULL,
  act_task_address        TEXT NOT NULL,
  act_task_state_id  INTEGER NOT NULL,
  task_task_id TEXT NOT NULL,
  start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_date TIMESTAMP DEFAULT '5999-12-31 23:59:59' NOT NULL,
  PRIMARY KEY (act_task_id, start_date)
);


CREATE TABLE process_X_task
(
  act_process_process_id INTEGER NOT NULL,
  act_task_task_id     INTEGER NOT NULL,
  start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_date TIMESTAMP DEFAULT '5999-12-31 23:59:59' NOT NULL,
  PRIMARY KEY (act_task_task_id , act_process_process_id, start_date)
);
CREATE TABLE artefact_X_task
(
  act_artefact_artefact_id INTEGER NOT NULL,
  act_task_task_id     INTEGER NOT NULL,
  start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  end_date TIMESTAMP DEFAULT '5999-12-31 23:59:59' NOT NULL,
  PRIMARY KEY (act_task_task_id , act_artefact_artefact_id, start_date)
);


/* CREATE SEQUENCES */
CREATE SEQUENCE IF NOT EXISTS artefact_id_seq INCREMENT BY 1 MINVALUE 0 START WITH 0 OWNED BY act_artefacts.act_artefact_id;
CREATE SEQUENCE IF NOT EXISTS task_id_seq INCREMENT BY 1 MINVALUE 0 START WITH 0 OWNED BY act_tasks.act_task_id;
CREATE SEQUENCE IF NOT EXISTS process_id_seq INCREMENT BY 1 MINVALUE 0 START WITH 0 OWNED BY act_processes.act_process_id;




insert into states(state_id, state_desc)
values(1, 'exist'),
(2, 'error'),
(3, 'in_progress'),
(4, 'complete');

insert into tasks(task_id, task_desc, priority, process_process_id)
values('task_1',NULL,0,'process_1'),
('task_2',NULL,1,'process_1'),
('task_3',NULL,2,'process_1'),
('task_4',NULL,3,'process_1'),
('task_1_1',NULL,0,'process_2'),
('task_1_2',NULL,1,'process_2');

insert into processes(process_id)
values('process_1'),
('process_2');


insert into artefacts(artefact_id)
values('artefact_1'),
('artefact_2');

insert into links_artefacts_X_tasks(task_task_id, required_artefact)
values('task_1', 'artefact_1'),
('task_2','artefact_1'),
('task_2','artefact_2'),
('task_3','artefact_1'),
('task_3','artefact_2'),
('task_4','artefact_1'),
('task_1_1','artefact_1'),
('task_1_2','artefact_2');