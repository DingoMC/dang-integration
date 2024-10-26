"""dang$$ MCUserLocation ORM

This module contains MCUserLocation Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSQL, ExecuteSQLUpdate, ConstructWhere, ConstructFilter, ConstructUpdateRow, ConstructUpdateColumn

class MCUserLocation:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "MCUserLocation"'
        if join is not None:
            sql_query += ' mul' # "MCUserLocation" AS mul
            if 'MCUser' in join: # "MCUser" AS u
                sql_query += ' JOIN "MCUser" u ON u.uuid = mul.uuid'
            if 'Server' in join: # "Server" AS s
                sql_query += ' JOIN "Server" s ON s.id = mul.server_id'
            if 'MinigamesSubServer' in join: # "MinigamesSubServer" AS mss
                sql_query += ' JOIN "MinigamesSubServer" mss ON (mul.server_id = 3 AND mss.id = mul.subserver)'
        sql_query += ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def insert (uuid : str, server_id : int, subserver : int = -1):
        sql_query = 'INSERT INTO "MCUserLocation" (uuid, server_id, subserver) VALUES '
        sql_query += '(\'' + uuid + '\', \'' + str(server_id) + '\', \'' + str(subserver) + '\') RETURNING id'
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "MCUserLocation" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
        
    @staticmethod
    def updateColumn (value_field: str, criteria_field: str, values: list[str], criteria: list[str], where: dict = None):
        sql_query = 'UPDATE "MCUserLocation" SET ' + ConstructUpdateColumn(value_field, criteria_field, values, criteria)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
    
    @staticmethod
    def count (where: dict = None):
        sql_query = 'SELECT COUNT(*) FROM "MCUserLocation"' + ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return int(result[0][0])
    
    @staticmethod
    def upsert (updateFields: dict, insertUUID: str, insertServerID: int, insertSubServer: int = -1, onConflict: dict = None):
        cnt = MCUserLocation.count(onConflict)
        if cnt == 0:
            result = MCUserLocation.insert(insertUUID, insertServerID, insertSubServer)
            return result
        MCUserLocation.updateRow(updateFields, onConflict)
    