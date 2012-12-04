#!/usr/bin/sh
DB=globalclip
DBUSER=postgres
dropdb -U $DBUSER $DB
createdb -U $DBUSER $DB
psql -U $DBUSER -d $DB -f server.sql

