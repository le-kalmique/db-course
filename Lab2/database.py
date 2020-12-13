import psycopg2
from config import Config

connect = psycopg2.connect(f"host={Config.host} dbname={Config.db_name} user={Config.user} password={Config.passwd}")
cursor = connect.cursor()


# define custom sql functions
def defineGenerateStringFunc():
    cursor.execute('create or replace function generateString(length int) '
                   'returns text '
                   'language plpgsql '
                   'as '
                   '$$ '
                   'declare '
                   'outputString text; '
                   'begin '
                   'select string_agg(chr(trunc(97 + random()*25)::int), \'\') '
                   'from generate_series(1, length) '
                   'into outputString; '
                   'return outputString; '
                   'end; '
                   '$$; ')
    connect.commit()


def defineGenerateDateFunc():
    cursor.execute('create function generatedate() returns text '
                   'language plpgsql '
                   'as '
                   '$$ '
                   'declare '
                   'outputDate text; '
                   'begin '
                   'select concat((1990 + trunc(random() * 30 + 1)::int)::text, '
                   '"-0", trunc(random() * 9 + 1)::text, "-", '
                   '(8 + trunc(random() * 20 + 1)::int)::text) '
                   'into outputDate; '
                   'return outputDate; '
                   'end; '
                   '$$; ')
    connect.commit()


def defineGenerateIntFunc():
    cursor.execute('create function generateint(max integer) returns text '
                   'language plpgsql '
                   'as '
                   '$$ '
                   'declare '
                   'outputInt int; '
                   'begin '
                   'select trunc(random() * max + 1) '
                   'into outputInt; '
                   'return outputInt; '
                   'end; '
                   '$$; ')
    connect.commit()


def defineGetRandowRowFunc():
    cursor.execute('create or replace function getrandomrow(table_name text) returns text '
                   'language plpgsql '
                   'as '
                   '$$ '
                   'declare '
                   'output int; '
                   'begin '
                   'EXECUTE format(\'select id from "%s" ORDER BY random() LIMIT 1\', table_name) '
                   'into output; '
                   'return output; '
                   'end; '
                   '$$; ')
    connect.commit()


def initCustomFunctions():
    defineGenerateStringFunc()
    defineGenerateDateFunc()
    defineGenerateIntFunc()
    defineGetRandowRowFunc()
