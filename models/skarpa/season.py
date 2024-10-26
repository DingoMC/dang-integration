"""dang$$ Season ORM

This module contains Season Skarpa Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSkarpaSQL, ExecuteSkarpaSQLUpdate, ConstructFilter, ConstructWhere, ConstructInsert, ConstructOrderBy, ConstructUpdateRow

class Season:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None, order_by: dict = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "Season"'
        if join is not None:
            sql_query += ' s'
            if 'Competition' in join:
                sql_query += ' LEFT JOIN "Competition" c ON s.id = c.season_id'
            if 'SeasonScore' in join:
                sql_query += ' LEFT JOIN "SeasonScore" ss ON s.id = ss.season_id'
        sql_query += ConstructWhere(where)
        sql_query += ConstructOrderBy(order_by)
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def insert (fields: list[str], values: list[list[str]]):
        sql_query = 'INSERT INTO "Season" ' + ConstructInsert(fields, values) + ' RETURNING id'
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "Season" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSkarpaSQLUpdate(sql_query)
      
    @staticmethod  
    def count (where: dict = None):
        sql_query = 'SELECT COUNT(*) FROM "Season"' + ConstructWhere(where)
        result = ExecuteSkarpaSQL(sql_query)
        return int(result[0][0])
    
    @staticmethod
    def upsert (updateFields: dict, insertFields: list[str], insertValues: list[list[str]], onConflict: dict = None):
        cnt = Season.count(onConflict)
        if cnt == 0:
            result = Season.insert(insertFields, insertValues)
            return result
        Season.updateRow(updateFields, onConflict)
