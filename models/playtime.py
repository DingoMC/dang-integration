"""dang$$ Playtime ORM

This module contains Playtime Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSQL, ExecuteSQLUpdate, ConstructWhere, ConstructFilter, ConstructUpdateRow, ConstructUpdateColumn

class Playtime:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "Playtime"'
        if join is not None:
            sql_query += ' pt' # "Playtime" AS pt
            if 'MCUser' in join: # "MCUser" AS u
                sql_query += ' LEFT JOIN "MCUser" u ON pt.uuid = u.uuid'
            if 'Server' in join: # "Server" AS s
                sql_query += ' LEFT JOIN "Server" s ON pt.server_id = s.id'
        sql_query += ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def insert (uuid : str, server_id : int, hours : int = 0):
        sql_query = 'INSERT INTO "Playtime" (uuid, server_id, hours) VALUES '
        sql_query += '(\'' + uuid + '\', \'' + str(server_id) + '\', \'' + str(hours) + '\') RETURNING id'
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "Playtime" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
    
    @staticmethod
    def updateColumn (value_field: str, criteria_field: str, values: list[str], criteria: list[str], where: dict = None):
        sql_query = 'UPDATE "Playtime" SET ' + ConstructUpdateColumn(value_field, criteria_field, values, criteria)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)