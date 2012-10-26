DROP TABLE IF EXISTS accounts CASCADE;
CREATE TABLE accounts (
    id serial PRIMARY KEY,
    created timestamp with time zone default now(),
    email varchar(100),
    password varchar(200),
    activation_key varchar(500) null,
    isactive boolean default false
);

DROP INDEX IF EXISTS account_email CASCADE;
CREATE UNIQUE INDEX account_email ON accounts(email);

DROP INDEX IF EXISTS account_activation_key CASCADE;
CREATE UNIQUE INDEX account_activation_key ON accounts(activation_key);


DROP INDEX IF EXISTS unique_account_credentials CASCADE;
CREATE UNIQUE INDEX unique_account_credentials ON accounts(email,password);


DROP INDEX IF EXISTS account_sessions CASCADE;
CREATE TABLE account_sessions (
    id serial PRIMARY KEY,
    created timestamp with time zone default now(),
    owner int references accounts(id),
    source_ip varchar(100),
    session_key varchar(100)
);

DROP INDEX IF EXISTS unique_account_session CASCADE;
CREATE UNIQUE INDEX unique_account_session ON account_sessions(owner,source_ip);

DROP TABLE IF EXISTS clipboard_write CASCADE;
CREATE TABLE clipboard_write (
    id serial PRIMARY KEY,
    created timestamp with time zone default now(),
    owner int references accounts(id),
    source_ip varchar(100),
    clipboard text
);

