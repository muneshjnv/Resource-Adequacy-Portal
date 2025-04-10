-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.actual_demand
(
    state_id integer NOT NULL,
    process_date date NOT NULL,
    modified_date timestamp without time zone,
    demand_met double precision[],
    scada_demand double precision[],
    forecast double precision[],
    CONSTRAINT actual_demand_pkey PRIMARY KEY (state_id, process_date)
);

CREATE TABLE IF NOT EXISTS public.actual_demand_email_status
(
    process_date date NOT NULL,
    email_sent boolean DEFAULT false,
    all_states_uploaded boolean DEFAULT false,
    CONSTRAINT actual_demand_email_status_pkey PRIMARY KEY (process_date)
);

CREATE TABLE IF NOT EXISTS public.demand_forecast_intraday_test
(
    "timestamp" timestamp with time zone NOT NULL,
    state_id integer NOT NULL,
    forecasted_demand double precision NOT NULL
);

CREATE TABLE IF NOT EXISTS public.file_contents
(
    state_id integer NOT NULL,
    upload_date date NOT NULL,
    file_data jsonb,
    CONSTRAINT file_contents_pkey PRIMARY KEY (state_id, upload_date)
);

CREATE TABLE IF NOT EXISTS public.file_uploads
(
    state_id integer NOT NULL,
    upload_date date NOT NULL,
    upload_time timestamp without time zone NOT NULL,
    revision_no integer NOT NULL,
    uploaded_by character varying(100) COLLATE pg_catalog."default" NOT NULL,
    file_name text COLLATE pg_catalog."default",
    file_data jsonb NOT NULL,
    CONSTRAINT file_uploads_pkey PRIMARY KEY (state_id, upload_date, revision_no)
);

CREATE TABLE IF NOT EXISTS public.intraday_file_uploads
(
    state_id integer NOT NULL,
    upload_date date NOT NULL,
    upload_time timestamp without time zone NOT NULL,
    revision_no integer NOT NULL,
    uploaded_by character varying(100) COLLATE pg_catalog."default" NOT NULL,
    file_name text COLLATE pg_catalog."default",
    file_data jsonb NOT NULL,
    CONSTRAINT intraday_file_uploads_pkey PRIMARY KEY (state_id, upload_date, revision_no)
);

CREATE TABLE IF NOT EXISTS public.login_attempts
(
    ip_address character varying(45) COLLATE pg_catalog."default" NOT NULL,
    username character varying(255) COLLATE pg_catalog."default",
    attempt_time timestamp without time zone NOT NULL,
    device_id character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT login_attempts_pkey PRIMARY KEY (ip_address, attempt_time)
);

CREATE TABLE IF NOT EXISTS public.month_ahead_file_uploads
(
    state_id integer NOT NULL,
    from_date date NOT NULL,
    to_date date NOT NULL,
    upload_time timestamp without time zone,
    revision_no integer NOT NULL,
    uploaded_by character varying(100) COLLATE pg_catalog."default",
    file_name character varying(1000) COLLATE pg_catalog."default",
    file_data jsonb,
    CONSTRAINT month_ahead_file_uploads_pkey PRIMARY KEY (state_id, from_date, to_date, revision_no)
);

CREATE TABLE IF NOT EXISTS public.states
(
    state_id integer NOT NULL,
    state_name character varying(255) COLLATE pg_catalog."default",
    username character varying(255) COLLATE pg_catalog."default" NOT NULL,
    password_hash character varying(2000) COLLATE pg_catalog."default" NOT NULL,
    acronym character varying(30) COLLATE pg_catalog."default",
    user_role character varying(50) COLLATE pg_catalog."default" NOT NULL,
    reporting_name character varying(100) COLLATE pg_catalog."default",
    reporting_state_id integer,
    CONSTRAINT states_pkey PRIMARY KEY (state_id)
);

CREATE TABLE IF NOT EXISTS public.user_sessions
(
    session_id serial NOT NULL,
    username character varying(255) COLLATE pg_catalog."default" NOT NULL,
    session_token character varying(512) COLLATE pg_catalog."default" NOT NULL,
    ip_address character varying(45) COLLATE pg_catalog."default" NOT NULL,
    device_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    user_agent text COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT now(),
    last_activity timestamp without time zone DEFAULT now(),
    expires_at timestamp without time zone NOT NULL,
    is_active boolean DEFAULT true,
    CONSTRAINT user_sessions_pkey PRIMARY KEY (session_id),
    CONSTRAINT user_sessions_session_token_key UNIQUE (session_token),
    CONSTRAINT user_sessions_username_session_token_key UNIQUE (username, session_token)
);

CREATE TABLE IF NOT EXISTS public.week_ahead_file_uploads
(
    state_id integer NOT NULL,
    from_date date NOT NULL,
    to_date date NOT NULL,
    upload_time timestamp without time zone,
    revision_no integer NOT NULL,
    uploaded_by character varying(100) COLLATE pg_catalog."default",
    file_name character varying(1000) COLLATE pg_catalog."default",
    file_data jsonb,
    CONSTRAINT week_ahead_file_uploads_pkey PRIMARY KEY (state_id, from_date, to_date, revision_no)
);

CREATE TABLE IF NOT EXISTS public.year_ahead_file_uploads
(
    state_id integer NOT NULL,
    from_date date NOT NULL,
    to_date date NOT NULL,
    upload_time timestamp without time zone,
    revision_no integer NOT NULL,
    uploaded_by character varying(100) COLLATE pg_catalog."default",
    file_name character varying(1000) COLLATE pg_catalog."default",
    file_data jsonb,
    CONSTRAINT year_ahead_file_uploads_pkey PRIMARY KEY (state_id, from_date, to_date, revision_no)
);

ALTER TABLE IF EXISTS public.file_contents
    ADD CONSTRAINT file_contents_state_id_fkey FOREIGN KEY (state_id)
    REFERENCES public.states (state_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.file_uploads
    ADD CONSTRAINT file_uploads_state_id_fkey FOREIGN KEY (state_id)
    REFERENCES public.states (state_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.intraday_file_uploads
    ADD CONSTRAINT intraday_file_uploads_state_id_fkey FOREIGN KEY (state_id)
    REFERENCES public.states (state_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.month_ahead_file_uploads
    ADD CONSTRAINT month_ahead_file_uploads_state_id_fkey FOREIGN KEY (state_id)
    REFERENCES public.states (state_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.week_ahead_file_uploads
    ADD CONSTRAINT week_ahead_file_uploads_state_id_fkey FOREIGN KEY (state_id)
    REFERENCES public.states (state_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.year_ahead_file_uploads
    ADD CONSTRAINT year_ahead_file_uploads_state_id_fkey FOREIGN KEY (state_id)
    REFERENCES public.states (state_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;