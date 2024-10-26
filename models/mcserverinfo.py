"""dang$$ MCServerInfo ORM

This module contains MCServerInfo Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSQL, ExecuteSQLUpdate, ConstructWhere, ConstructFilter, ConstructUpdateRow, ConstructUpdateColumn

class MCServerInfo:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "MCServerInfo"'
        sql_query += ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def insert (dns : str, desc : str, latency : int, players: int, players_max : int, version : str, sample : str = "None"):
        sql_query = 'INSERT INTO "MCServerInfo" (dns, description, latency, players, players_max, version, sample) VALUES '
        sql_query += '(\'' + dns + '\', \'' + desc + '\', \'' + latency + '\', \'' + players + '\', \'' + players_max + '\', \'' + version + '\', \'' + sample + '\') RETURNING id'
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "MCServerInfo" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
    
    @staticmethod
    def updateColumn (value_field: str, criteria_field: str, values: list[str], criteria: list[str], where: dict = None):
        sql_query = 'UPDATE "MCServerInfo" SET ' + ConstructUpdateColumn(value_field, criteria_field, values, criteria)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
      
    @staticmethod  
    def count (where: dict = None):
        sql_query = 'SELECT COUNT(*) FROM "MCServerInfo"' + ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return int(result[0][0])
