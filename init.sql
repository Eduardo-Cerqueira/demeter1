/*
* Create a group
*/
CREATE ROLE demeter_dev
    WITH NOLOGIN;

/*
* Create database
*/
CREATE DATABASE demeter;

/*
* Transfer ownership to group
*/
ALTER DATABASE demeter
    OWNER TO demeter_dev;

/*
* Grant permissions to group
*/
GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES
    IN SCHEMA public
    TO demeter_dev;

/*
* Give CREATE permission to demeter_dev group
*/
GRANT CREATE
    ON SCHEMA public
    TO demeter_dev;

/*
* Create app user
*/
CREATE ROLE app
    WITH LOGIN
    PASSWORD 'app'
    INHERIT;

/*
* Add app to demeter_dev group
*/

GRANT demeter_dev
    TO app;
