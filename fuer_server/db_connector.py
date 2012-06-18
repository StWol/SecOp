import MySQLdb
import numpy as np

class _Connector(object):

    def __init__(self):
        # just for the sake of information
        self.instance = "Instance at %d" % self.__hash__()
        try:
            self.conn = MySQLdb.connect (host="141.62.65.151",
                                    user = "stan",
                                    passwd = "money!",
                                    db = "secop_web")
                              
            print "Mit secop verbunden"
                                
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        self.cursor = self.conn.cursor ()
    
    def get_select(self, sql):
        result = []
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            result = self.cursor.fetchall()
            result = np.array(result)
            #result = np.transpose(result)
            return result
            
        except MySQLdb.Error, e:
            self.conn.rollback()
            print "Error %d: %s" % (e.args[0], e.args[1])

_connector = _Connector()

def Connector(): 
    
    return _connector
