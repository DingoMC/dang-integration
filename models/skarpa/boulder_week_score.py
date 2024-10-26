"""dang$$ BoulderWeekScore ORM

This module contains BoulderWeekScore Skarpa Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSkarpaSQL, ExecuteSkarpaSQLUpdate, ConstructFilter, ConstructWhere, ConstructInsert, ConstructOrderBy, ConstructUpdateRow, ConstructUpsert

class BoulderWeekScore:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None, order_by: dict = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "BoulderWeekScore"'
        if join is not None:
            sql_query += ' bws'
            if 'BoulderWeek' in join:
                sql_query += ' LEFT JOIN "BoulderWeek" bw ON bw.id = bws.boulder_week_id'
        sql_query += ConstructWhere(where)
        sql_query += ConstructOrderBy(order_by)
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def insert (fields: list[str], values: list[list[str]]):
        sql_query = 'INSERT INTO "BoulderWeekScore" ' + ConstructInsert(fields, values) + ' RETURNING id'
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "BoulderWeekScore" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSkarpaSQLUpdate(sql_query)
      
    @staticmethod  
    def count (where: dict = None, join: list[str] = None):
        sql_query = 'SELECT COUNT(*) FROM "BoulderWeekScore"'
        if join is not None:
            sql_query += ' bws'
        sql_query += ConstructWhere(where)
        result = ExecuteSkarpaSQL(sql_query)
        return int(result[0][0])
    
    @staticmethod
    def upsert (updateFields: dict, insertFields: list[str], insertValues: list[str], onConflict: list[str]):
        sql_query = 'INSERT INTO "BoulderWeekScore" ' + ConstructUpsert(updateFields, insertFields, insertValues, onConflict)
        ExecuteSkarpaSQLUpdate(sql_query)
