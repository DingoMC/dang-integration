"""dang$$ Database Connector

This module contains Database queries/updates
Created by: DingoMC
Cores: akka, umbry

"""
import psycopg2
import os
from dotenv import load_dotenv
from utils.console import DingormExec, DingormErrorExecuteSQL

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
SKARPA_DB_HOST = os.getenv('SKARPA_DB_HOST')
SKARPA_DB_NAME = os.getenv('SKARPA_DB_NAME')
SKARPA_DB_USER = os.getenv('SKARPA_DB_USER')
SKARPA_DB_PASS = os.getenv('SKARPA_DB_PASS')

VERSION = "1.1.4"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
    
def ExecuteSkarpaSQL (sql: str):
    try:
        conn = psycopg2.connect(host=SKARPA_DB_HOST, database=SKARPA_DB_NAME, user=SKARPA_DB_USER, password=SKARPA_DB_PASS)
        conn.autocommit = True
        q = conn.cursor()
        print(DingormExec(sql))
        q.execute(sql)
    except psycopg2.Error as e:
        print(DingormErrorExecuteSQL(sql, e.pgerror))
        return []
    except:
        print(DingormErrorExecuteSQL(sql))
        return []
    result = []
    row = q.fetchone()
    while row is not None:
        result.append(row)
        row = q.fetchone()
    return result

def ExecuteSkarpaSQLUpdate (sql: str):
    try:
        conn = psycopg2.connect(host=SKARPA_DB_HOST, database=SKARPA_DB_NAME, user=SKARPA_DB_USER, password=SKARPA_DB_PASS)
        conn.autocommit = True
        q = conn.cursor()
        print(DingormExec(sql))
        q.execute(sql)
    except psycopg2.Error as e:
        print(DingormErrorExecuteSQL(sql, e.pgerror))
        return
    except:
        print(DingormErrorExecuteSQL(sql))
    
def ExecuteSQL (sql: str):
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        conn.autocommit = True
        q = conn.cursor()
        print(DingormExec(sql))
        q.execute(sql)
    except psycopg2.Error as e:
        print(DingormErrorExecuteSQL(sql, e.pgerror))
        return []
    except:
        print(DingormErrorExecuteSQL(sql))
        return []
    result = []
    row = q.fetchone()
    while row is not None:
        result.append(row)
        row = q.fetchone()
    return result

def ExecuteSQLUpdate (sql: str):
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        conn.autocommit = True
        q = conn.cursor()
        print(DingormExec(sql))
        q.execute(sql)
    except psycopg2.Error as e:
        print(DingormErrorExecuteSQL(sql, e.pgerror))
        return
    except:
        print(DingormErrorExecuteSQL(sql))
        
def ConstructInsert (fields: list[str], values: list[list[str]]):
    sql_part = '(' + ', '.join(fields) + ') VALUES'
    for i in range(0, len(values)):
        sql_part += '('
        for j in range(0, len(values[i])):
            if values[i][j] is None or str(values[i][j]) == 'NULL':
                sql_part += 'NULL'
            else:
                sql_part += '\'' + str(values[i][j]) + '\''
            if j < len(values[i]) - 1:
                sql_part += ', '
        sql_part += ')'
        if i < len(values) - 1:
            sql_part += ', '
    return sql_part

def ConstructWhere (where: dict = None):
    if where is None:
        return ''
    sql_part = ' WHERE '
    first = True
    for key, val in where.items():
        if not first:
            sql_part += ' AND '
        sql_part += str(key) + ' = \'' + str(val) + '\''
        first = False
    return sql_part

def ConstructOrderBy (order_by: dict):
    if order_by is None:
        return ''
    sql_part = ' ORDER BY '
    first = True
    for key, val in order_by.items():
        if not first:
            sql_part += ', '
        sql_part += str(key) + ' ' + str('ASC' if val == 1 else 'DESC')
        first = False
    return sql_part

def ConstructFilter (filter: list[str] = None):
    if filter is None:
        return '*'
    sql_part = ''
    for i in range(0, len(filter)):
        sql_part += filter[i]
        if i < len(filter) - 1:
            sql_part += ', '
    return sql_part

def ConstructUpdateRow (fields: dict):
    sql_part = ''
    first = True
    for key, val in fields.items():
        if not first:
            sql_part += ', '
        if val is not None and str(val) is not 'NULL':
            sql_part += str(key) + ' = \'' + str(val) + '\''
        first = False
    return sql_part

def ConstructUpdateColumn (value_field: str, criteria_field: str, values: list[str], criteria: list[str]):
    sql_part = value_field + ' = CASE ' + criteria_field
    for i in range (0, len(criteria)):
        if len(values) >= len(criteria):
            sql_part += ' WHEN ' + str(criteria[i]) + ' THEN ' + str(values[i])
    sql_part += ' ELSE ' + value_field + ' END'
    return sql_part

def ConstructOnConflict (fields: list[str]):
    sql_part = 'ON CONFLICT ('
    for i in range(0, len(fields)):
        sql_part += fields[i]
        if i < len(fields) - 1:
            sql_part += ', '
    sql_part += ')'
    return sql_part

def ConstructUpsert (updateFields: dict, insertFields: list[str], insertValues: list[str], onConflict: list[str]):
    sql_part = ConstructInsert(insertFields, [insertValues]) + ' ' + ConstructOnConflict(onConflict) + ' '
    sql_part += 'DO UPDATE SET ' + ConstructUpdateRow(updateFields)
    return sql_part
