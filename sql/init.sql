CREATE DATABASE star_burger;
CREATE USER some_user WITH PASSWORD 'P@ssw0rd';
GRANT ALL ON DATABASE star_burger TO some_user;
ALTER USER some_user CREATEDB;
