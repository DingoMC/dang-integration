"""dang$$ SpeedDay ORM

This module contains SpeedDay Skarpa Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSkarpaSQL, ExecuteSkarpaSQLUpdate, ConstructFilter, ConstructWhere, ConstructInsert, ConstructOrderBy, ConstructUpdateRow

class SpeedDay:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None, order_by: dict = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "SpeedDay"'
        if join is not None:
            sql_query += ' sd'
        sql_query += ConstructWhere(where)
        sql_query += ConstructOrderBy(order_by)
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def insert (fields: list[str], values: list[list[str]]):
        sql_query = 'INSERT INTO "SpeedDay" ' + ConstructInsert(fields, values) + ' RETURNING id'
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "SpeedDay" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSkarpaSQLUpdate(sql_query)
      
    @staticmethod  
    def count (where: dict = None, join: list[str] = None):
        sql_query = 'SELECT COUNT(*) FROM "SpeedDay"'
        if join is not None:
            sql_query += ' sds'
            if 'SpeedDay' in join:
                sql_query += ' LEFT JOIN "SpeedDay" sd ON sd.id = sds.lead_route_id'
        sql_query += ConstructWhere(where)
        result = ExecuteSkarpaSQL(sql_query)
        return int(result[0][0])
    
    @staticmethod
    def upsert (updateFields: dict, insertFields: list[str], insertValues: list[str], onConflict: dict = None):
        cnt = SpeedDay.count(onConflict)
        if cnt == 0:
            result = SpeedDay.insert(insertFields, [insertValues])
            return result
        SpeedDay.updateRow(updateFields, onConflict)
