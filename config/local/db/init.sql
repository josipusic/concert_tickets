CREATE USER concert_tickets WITH PASSWORD 'concert_tickets';
ALTER ROLE concert_tickets SET client_encoding TO 'utf8';
ALTER ROLE concert_tickets SET default_transaction_isolation TO 'read committed';
ALTER ROLE concert_tickets SET timezone TO 'UTC';
CREATE DATABASE concert_tickets ENCODING 'utf8' OWNER concert_tickets;
