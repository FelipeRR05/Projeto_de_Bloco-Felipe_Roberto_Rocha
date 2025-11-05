-- Exercicio 2: Crie o script DDL a partir do seu modelo para criar o BD em PostgreSQL com todos os objetos pertinentes (tabelas, relacionamentos e etc.)
BEGIN;

CREATE TABLE IF NOT EXISTS public."Users"
(
    user_id serial,
    full_name text NOT NULL,
    experience_level text,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS public."Workout_Sessions"
(
    session_id serial,
    user_id integer NOT NULL,
    session_date date NOT NULL,
    PRIMARY KEY (session_id)
);

CREATE TABLE IF NOT EXISTS public."Exercise_Logs"
(
    log_id serial,
    session_id integer NOT NULL,
    exercise_name text NOT NULL,
    weight_kg numeric,
    reps_executed integer,
    PRIMARY KEY (log_id)
);

ALTER TABLE IF EXISTS public."Workout_Sessions"
    ADD FOREIGN KEY (user_id)
    REFERENCES public."Users" (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Exercise_Logs"
    ADD FOREIGN KEY (session_id)
    REFERENCES public."Workout_Sessions" (session_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;


-- Exercicio 3: Popule as tabelas com dados básicos usando scripts DML
INSERT INTO "Users" (full_name, experience_level) VALUES
('Felipe Roberto Rocha', 'Intermediário'),
('Rayan Vitor', 'Iniciante'),
('Carlos Cuesta', 'Avançado');

INSERT INTO "Workout_Sessions" (user_id, session_date) VALUES
(1, '2025-11-01'),
(1, '2025-11-03'),
(2, '2025-11-04');

INSERT INTO "Exercise_Logs" (session_id, exercise_name, weight_kg, reps_executed) VALUES
(1, 'Agachamento Livre', 60.0, 10),
(1, 'Supino Reto', 40.0, 12),
(2, 'Levantamento Terra', 80.0, 8),
(2, 'Remada Curvada', 35.0, 10);


-- Exercicio 4: Realize um script DQL contendo três consultas, a saber: 
-- a) consulta com INNER JOIN:
SELECT
    U.full_name,
    WS.session_date,
    EL.exercise_name,
    EL.weight_kg,
    EL.reps_executed
FROM
    "Users" AS U
INNER JOIN
    "Workout_Sessions" AS WS ON U.user_id = WS.user_id
INNER JOIN
    "Exercise_Logs" AS EL ON WS.session_id = EL.session_id;

-- b) consulta com LEFT JOIN:
SELECT
    U.full_name,
    U.experience_level,
    WS.session_date
FROM
    "Users" AS U
LEFT JOIN
    "Workout_Sessions" AS WS ON U.user_id = WS.user_id;
	
-- c) consulta com RIGHT JOIN:
SELECT
    WS.session_id,
    WS.session_date,
    EL.exercise_name,
    EL.weight_kg
FROM
    "Exercise_Logs" AS EL
RIGHT JOIN
    "Workout_Sessions" AS WS ON EL.session_id = WS.session_id;