"""dang$$ SpeedDayScore ORM

This module contains SpeedDayScore Skarpa Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSkarpaSQL, ExecuteSkarpaSQLUpdate, ConstructFilter, ConstructWhere, ConstructInsert, ConstructOrderBy, ConstructUpdateRow

class SpeedDayScore:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None, order_by: dict = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "SpeedDayScore"'
        if join is not None:
            sql_query += ' sds'
            if 'SpeedDay' in join:
                sql_query += ' LEFT JOIN "SpeedDay" sd ON sd.id = sds.speed_day_id'
        sql_query += ConstructWhere(where)
        sql_query += ConstructOrderBy(order_by)
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def insert (fields: list[str], values: list[list[str]]):
        sql_query = 'INSERT INTO "SpeedDayScore" ' + ConstructInsert(fields, values) + ' RETURNING id'
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "SpeedDayScore" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSkarpaSQLUpdate(sql_query)
      
    @staticmethod  
    def count (where: dict = None, join: list[str] = None):
        sql_query = 'SELECT COUNT(*) FROM "SpeedDayScore"'
        if join is not None:
            sql_query += ' sds'
            if 'SpeedDay' in join:
                sql_query += ' LEFT JOIN "SpeedDay" sd ON sd.id = sds.speed_day_id'
        sql_query += ConstructWhere(where)
        result = ExecuteSkarpaSQL(sql_query)
        return int(result[0][0])
    
    @staticmethod
    def upsert (updateFields: dict, insertFields: list[str], insertValues: list[str], onConflict: dict = None):
        cnt = SpeedDayScore.count(onConflict)
        if cnt == 0:
            result = SpeedDayScore.insert(insertFields, [insertValues])
            return result
        SpeedDayScore.updateRow(updateFields, onConflict)
