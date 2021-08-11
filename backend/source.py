from sqlalchemy import create_engine, inspect

engine = create_engine('postgresql://hus:1058@localhost/hus')
class Source():
    def tableNames(self):
        inspector = inspect(engine)
        return inspector.get_table_names()
    
    def columnNames(self,table_name):
        inspector = inspect(engine)
        l = list()
        for column in inspector.get_columns(table_name):
            l.append(column['name'])
        return l
    
    def dataList(self,table_name,x,y):
        x_set = engine.execute("SELECT {} FROM {}".format(x,table_name))
        y_set = engine.execute("SELECT {} FROM {}".format(y,table_name))
        d = {}
        x = []
        y = []
        for v in x_set:
            x.append(v[0])
        for v in y_set:
            y.append(v[0])
        d['x'] = x
        d['y'] = y
        return d
        
        