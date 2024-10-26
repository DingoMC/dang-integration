"""dang$$ MinigamesPoints ORM

This module contains MinigamesPoints Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSQL, ExecuteSQLUpdate, ConstructWhere, ConstructFilter, ConstructUpdateRow, ConstructUpdateColumn

class MinigamesPoints:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "MinigamesPoints"'
        if join is not None:
            sql_query += ' mp' # "MinigamesPoints" AS mp
            if 'MCUser' in join: # "MCUser" AS u
                sql_query += ' LEFT JOIN "MCUser" u ON mp.uuid = u.uuid'
            if 'Minigames' in join: # "Minigames" AS m
                sql_query += ' LEFT JOIN "Minigames" m ON mp.minigame_id = m.id'
        sql_query += ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def insert (uuid : str, minigame_id : int, points : int = 0):
        sql_query = 'INSERT INTO "MinigamesPoints" (uuid, minigame_id, points) VALUES '
        sql_query += '(\'' + uuid + '\', \'' + str(minigame_id) + '\', \'' + str(points) + '\') RETURNING id'
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "MinigamesPoints" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
        
    @staticmethod
    def updateColumn (value_field: str, criteria_field: str, values: list[str], criteria: list[str], where: dict = None):
        sql_query = 'UPDATE "MinigamesPoints" SET ' + ConstructUpdateColumn(value_field, criteria_field, values, criteria)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
