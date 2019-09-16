import os,configparser,pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

class Config(object):
    def __init__(self,config_filename="dbMysqlConfig.cnf"):
        print(os.path.dirname(__file__))
        file_path=os.path.join(os.path.dirname(__file__),config_filename)
        self.cf=configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self,section):
        return self.cf.options(section)

    def get_content(self,section):
        result={}
        for option in self.get_options(section):
            value=self.cf.get(section,option)
            result[option]=int(value) if value.isdigit() else value
        return result
    
# 数据库连接基础信息
class BasePymysqlPool(object):
        def __init__(self,host,port,user,password,db_name):
            self.db_host=host
            self.db_port=int(port)
            self.user=user
            self.password=password
            self.db=db_name
            self.comm=None
            self.cursor=None
            
class MyPymysqlPool(BasePymysqlPool):
    """
    Mysql数据库对象，负责产生数据库连接，此类中的连接采用连接池实现
        获取连接对象：conn=Mysql.getConn()
        释放连接对象: conn.clse或del conn
    """
    #连接池对象
    __pool=None
    
    def __init__(self,conf_name=None):
        self.conf=Config().get_content(conf_name)
        super(MyPymysqlPool,self).__init__(**self.conf)
        #数据库构造函数，从连接池中取出连接，并生成操作游标
        self.__conn=self.__getConn()
        self.__cursor=self.__conn.cursor()
    
    def __getConn(self):
        """
        @Summary:静态方法，从连接池中取出连接
        :return: Mysqldb.connection
        """
        if MyPymysqlPool.__pool is None:
            __pool= PooledDB(creator=pymysql,
                             mincached=1,
                             maxcached=20,
                             host=self.db_host,
                             port=self.db_port,
                             user=self.user,
                             passwd=self.password,
                             db=self.db,
                             use_unicode=False,
                             charset="utf8mb4",
                             cursorclass=DictCursor)
        return __pool.connection()

    def getAll(self,sql,param=None):
        """
        @Summary:执行查询，并取出所有查询结果集
        :param sql: 查询sql ，如果有查询条件，请指定条件列表，并将条件值使用参数【param】传递进来
        :param param: 可选参数，条件列表值(元组/列表)
        :return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count=self.__cursor.execute(sql)
        else:
            count=self.__cursor.execute(sql,param)
        if count>0:
            result=self.__cursor.fetchmany()
        else:
            result=False
        return result

    def getOne(self,sql,param=None):
        """
        @Summary:执行查询，并取出所有查询结果集
        :param sql: 查询sql ，如果有查询条件，请指定条件列表，并将条件值使用参数【param】传递进来
        :param param: 可选参数，条件列表值(元组/列表)
        :return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count=self.__cursor.execute(sql)
        else:
            count=self.__cursor.execute(sql,param)
        if count>0:
            result=self.__cursor.fetchone()
        else:
            result=False
        return result

    def getMany(self,sql,num,param=None):
        """
        @summayr:执行查询，并取出num条结果
        :param sql: 查询sql
        :param num: 取得的结果条数
        :param param: 可选参数，条件列表值
        :return: 查询到的结果集 result list/boolean
        """

        if param is None:
            count=self.__cursor.execute(sql)
        else:
            count=self.__cursor.execute(sql,param)
        if count > 0:
            result=self.__cursor.fetchmany(num)
        else:
            result=False
        return  result

    def insertMany(self,sql,values):
        """
        @summary:向表中插入多条数据
        :param sql: 要插入的sql格式
        :param values: 要插入的记录数据
        :return: count 受影响的行数
        """
        count=self.__cursor.executemany(sql,values)
        return count

    def __query(self,sql,param=None):
        if param is None:
            count=self.__cursor.execute(sql)
        else:
            count=self.__cursor.execute(sql,param)
        return count

    def update(self,sql,param=None):
        """
        @summay:更新数据
        :param sql:更新的sql及条件，使用（%s,%s）
        :param param: 要更新的只 tuple/list
        :return: count 受影响的行数
        """
        return self.__query(sql,param)

    def insert(self,sql,param=None):
        """
        @summary：插入数据
        :param sql:更新的sql及条件，使用（%s,%s）
        :param param: 要更新的只 tuple/list
        :return: count 受影响的行数
        """
        return self.__query(sql,param)

    def delete(self,sql,param=None):
        """
        @summary:删除数据
        :param sql:更新的sql及条件，使用（%s,%s）
        :param param: 要更新的只 tuple/list
        :return: count 受影响的行数
        """
        return self.__query(sql,param)

    def begin(self):
        """
        @summary:开启事物
        """
        self.__conn.autocommit(0)
    def end(self,option='commit'):
        """
        @summary:结束事物
        """
        if option=='commit':
            self.__conn.commit()
        else:
            self.__conn.rollback()

    def dispose(self,isEnd=1):
        """
        @summary:释放连接池资源
        """
        if isEnd==1:
            self.end('commit')
        else:
            self.end('rollback')
        self.__cursor.close()
        self.__conn.close()

    def commit(self):
        self.__conn.commit()

mysql=MyPymysqlPool("dbMysql")

if __name__=='__main__':
    mysql=MyPymysqlPool("dbMysql")
    sqlAll="select * from user"
    result=mysql.getOne(sqlAll)
    print(result)
    # config=Config()
    # print(config.get_sections())
    # print(config.get_content('dbMysql'))
    # print(Config.get_content(config))