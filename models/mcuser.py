"""dang$$ MCUser ORM

This module contains MCUser Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSQL, ExecuteSQLUpdate, ConstructWhere, ConstructFilter, ConstructUpdateRow, ConstructUpdateColumn

class MCUser:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "MCUser"'
        if join is not None:
            sql_query += ' u' # "MCUser" AS u
            if 'MCRank' in join: # "MCRank" AS r
                sql_query += ' JOIN "MCRank" r ON u.points BETWEEN r.min AND r.max'
            if 'MCStaffRank' in join: # "MCStaffRank" AS sr
                sql_query += ' LEFT JOIN "MCStaffRank" sr ON u.staff_rank_id = sr.id'
            if 'MinigamesPoints' in join: # "MinigamesPoints" AS mp
                sql_query += ' LEFT JOIN "MinigamesPoints" mp ON u.uuid = mp.uuid'
                if 'Minigames' in join: # "Minigames" AS m
                    sql_query += ' LEFT JOIN "Minigames" m ON mp.minigame_id = m.id'
            if 'Punishments' in join: # "Punishments" AS p
                sql_query += ' LEFT JOIN "Punishments" p ON u.uuid = p.player'
            if 'Playtime' in join: # "Playtime" AS pt
                sql_query += ' LEFT JOIN "Playtime" pt ON u.uuid = pt.uuid'
                if 'Server' in join: # "Server" AS s
                    sql_query += ' LEFT JOIN "Server" s ON pt.server_id = s.id'
            if 'MCUserKDR' in join: # "MCUserKDR" AS muk
                sql_query += ' LEFT JOIN "MCUserKDR" muk ON u.uuid = muk.uuid'
        sql_query += ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def insert (uuid : str, mcuuid : str, dcid : str, prefix : str, points : int = 0):
        sql_query = 'INSERT INTO "MCUser" (uuid, mcuuid, dcid, prefix, points) VALUES '
        sql_query += '(\'' + uuid + '\', \'' + mcuuid + '\', \'' + dcid + '\', \'' + prefix + '\', \'' + str(points) + '\') RETURNING uuid'
        result = ExecuteSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "MCUser" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
        
    @staticmethod
    def updateColumn (value_field: str, criteria_field: str, values: list[str], criteria: list[str], where: dict = None):
        sql_query = 'UPDATE "MCUser" SET ' + ConstructUpdateColumn(value_field, criteria_field, values, criteria)
        sql_query += ConstructWhere(where)
        ExecuteSQLUpdate(sql_query)
        
    @staticmethod
    def count (where: dict = None):
        sql_query = 'SELECT COUNT(*) FROM "MCUser"' + ConstructWhere(where)
        result = ExecuteSQL(sql_query)
        return int(result[0][0])
    