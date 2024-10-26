"""dang$$ LeadRouteScore ORM

This module contains LeadRouteScore Skarpa Model
Created by: DingoMC
Cores: akka, umbry

"""

from dingorm import ExecuteSkarpaSQL, ExecuteSkarpaSQLUpdate, ConstructFilter, ConstructWhere, ConstructInsert, ConstructOrderBy, ConstructUpdateRow

class LeadRouteScore:
    @staticmethod
    def select (filter: list[str] = None, where: dict = None, join: list[str] = None, order_by: dict = None):
        sql_query = 'SELECT ' + ConstructFilter(filter) + ' FROM "LeadRouteScore"'
        if join is not None:
            sql_query += ' lrs'
            if 'LeadRoute' in join:
                sql_query += ' LEFT JOIN "LeadRoute" lr ON lr.id = lrs.lead_route_id'
        sql_query += ConstructWhere(where)
        sql_query += ConstructOrderBy(order_by)
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def insert (fields: list[str], values: list[list[str]]):
        sql_query = 'INSERT INTO "LeadRouteScore" ' + ConstructInsert(fields, values) + ' RETURNING id'
        result = ExecuteSkarpaSQL(sql_query)
        return result
    
    @staticmethod
    def updateRow (fields: dict, where: dict = None):
        sql_query = 'UPDATE "LeadRouteScore" SET '
        sql_query += ConstructUpdateRow(fields)
        sql_query += ConstructWhere(where)
        ExecuteSkarpaSQLUpdate(sql_query)
      
    @staticmethod  
    def count (where: dict = None):
        sql_query = 'SELECT COUNT(*) FROM "LeadRouteScore"' + ConstructWhere(where)
        result = ExecuteSkarpaSQL(sql_query)
        return int(result[0][0])
    
    @staticmethod
    def upsert (updateFields: dict, insertFields: list[str], insertValues: list[list[str]], onConflict: dict = None):
        cnt = LeadRouteScore.count(onConflict)
        if cnt == 0:
            result = LeadRouteScore.insert(insertFields, insertValues)
            return result
        LeadRouteScore.updateRow(updateFields, onConflict)
