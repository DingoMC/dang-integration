"""dang$$ MCUserKDR ORM

This module contains MCUserKDR Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSQL, ExecuteSQLUpdate, ConstructWhere, ConstructFilter, ConstructUpdateRow, ConstructUpdateColumn

class MCUserKDR:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "MCUserKDR"'
        if join is not None:
            sql_query += ' muk' # "MCUserKDR" AS muk
            if 'MCUser' in join: # "MCUser" AS u
                sql_query += ' JOIN "MCUser" u ON u.uuid = muk.uuid'
            if 'Server' in join: # "Server" AS s
                sql_query += ' JOIN "Server" s ON s.id = muk.server_id'
        sql_query += ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def insert (uuid : str, server_id : int, kills : int, deaths : int, kdr : float = 0.0):
        sql_query = 'INSERT INTO "MCUserKDR" (uuid, server_id, kills, deaths, kdr) VALUES '
        sql_query += '(\'' + uuid + '\', \'' + str(server_id) + '\', \'' + str(kills) + '\', \'' + str(deaths) + '\', \'' + str(kdr) + '\') RETURNING id'
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "MCUserKDR" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
        
    @staticmethod
    def updateColumn (value_field: str, criteria_field: str, values: list[str], criteria: list[str], where: dict = None):
        sql_query = 'UPDATE "MCUserKDR" SET ' + ConstructUpdateColumn(value_field, criteria_field, values, criteria)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
    
    @staticmethod
    def count (where: dict = None):
        sql_query = 'SELECT COUNT(*) FROM "MCUserKDR"' + ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return int(result[0][0])
    
    @staticmethod
    def upsert (updateFields: dict, insertUUID : str, insertServerID : int, insertKills : int, insertDeaths : int, insertKDR : float = 0.0, onConflict: dict = None):
        cnt = MCUserKDR.count(onConflict)
        if cnt == 0:
            result = MCUserKDR.insert(insertUUID, insertServerID, insertKills, insertDeaths, insertKDR)
            return result
        MCUserKDR.updateRow(updateFields, onConflict)
    