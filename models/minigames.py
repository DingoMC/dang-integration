"""dang$$ Minigames ORM

This module contains Minigames Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSQL, ExecuteSQLUpdate, ConstructWhere, ConstructFilter, ConstructUpdateRow, ConstructUpdateColumn

class Minigames:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "Minigames"'
        sql_query += ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def insert (code : str, name : str, short_name : str, color: str, objective: str = None):
        sql_query = 'INSERT INTO "Minigames" (code, name, short_name, color, objective) VALUES '
        sql_query += '(\'' + code + '\', \'' + name + '\', \'' + short_name + '\', \'' + color + '\', \'' + objective + '\') RETURNING id'
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "Minigames" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
    
    @staticmethod
    def updateColumn (value_field: str, criteria_field: str, values: list[str], criteria: list[str], where: dict = None):
        sql_query = 'UPDATE "Minigames" SET ' + ConstructUpdateColumn(value_field, criteria_field, values, criteria)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
        
    @staticmethod
    def count (where: dict = None):
        sql_query = 'SELECT COUNT(*) FROM "Minigames"' + ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return int(result[0][0])
