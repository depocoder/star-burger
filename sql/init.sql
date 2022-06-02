CREATE DATABASE star_burger;
CREATE USER some_user WITH PASSWORD 'P@ssw0rd';
GRANT ALL ON DATABASE star_burger TO some_user;
ALTER USER some_user CREATEDB;
update pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'star_burger';
