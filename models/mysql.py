import pymysql
import config


conn = pymysql.connect(
    host=config.MYSQL_HOST,
    port=config.MYSQL_PORT,
    user=config.MYSQL_USER,
    password=config.MYSQL_PWD,
    db=config.MYSQL_DB,
    charset=config.MYSQL_CHARSET,
    autocommit=False,  # 不自动提交，当数据有变动时，需要手动执行一下conn.commit()方法
    cursorclass=pymysql.cursors.DictCursor,  # 让cursor.fetchall()等方法，返回的是一个键值对的格式。默认是一个元组
)


class MysqlDB(object):

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        单例
        :param args:
        :param kwargs:
        :return:
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def execute_sql(self, sql, args):
        try:
            # 检测连接状态，如果断了，则重连
            conn.ping(reconnect=True)

            # 创建游标
            cursor = conn.cursor()

            # 执行sql
            cursor.execute(sql, tuple(args))
            return cursor
        except:
            # 断开了连接，且reconnect为False，则报异常
            return None

    def select(self, table="", where=dict()):
        """
        查询
        :param table: 表名
        :param where: where条件的字典
        :return:
        """
        if not table:
            # 表为空
            return None

        # 参数
        args = []

        sql = "SELECT * FROM `{}` WHERE 1=1".format(table)
        for key, val in where.items():
            # 拼接sql
            sql += " AND {}=%s".format(key)
            # 追加值到args列表
            args.append(val)

        cursor = self.execute_sql(sql, args)
        res = cursor.fetchall()
        cursor.close()
        return res

    def insert(self, table="", data=dict()):
        """
        插入数据
        :param table: 表名
        :param data: 字段名为key，字段值为val的字典
        :return: 插入的数据id（cursor.lastrowid）
        """

        if not table or not data:
            # 表名为空 或者 待插入的数据为空
            return None

        # 参数
        args = []

        # 拼接sql字符串
        fields = "("
        values = "("
        for key, val in data.items():
            fields += "{}, ".format(key)
            values += "%s, "

            # 追加值到args列表
            args.append(val)
        fields = fields.strip().strip(",") + ")"
        values = values.strip().strip(",") + ")"
        sql = "INSERT INTO `{}`{} VALUES {}".format(table, fields, values)

        cursor = self.execute_sql(sql, args)
        if not cursor:
            # 执行sql报错
            return None

        # 提交
        conn.commit()
        lastrowid = cursor.lastrowid
        cursor.close()
        return lastrowid

    def update(self, table="", where=dict(), data=dict()):
        """
        更新数据
        :param table: 表名
        :param where: 更新条件
        :param data: 待更新的数据
        :return: 受影响的行数（cursor.rowcount）
        """

        if not table or not data:
            # 表名为空 或者 待更新的数据为空
            return None

        # 参数
        args = []

        sets = ""
        for key, val in data.items():
            sets += "{}=%s,".format(key)

            # 追加值到args列表
            args.append(val)
        sets = sets.strip().strip(",")

        wheres = ""
        for key, val in where.items():
            wheres += "AND {}=%s".format(key)
            args.append(val)
        wheres.strip()

        sql = "UPDATE `{}` SET  {} WHERE 1=1 {}".format(table, sets, wheres)

        cursor = self.execute_sql(sql, args)
        if not cursor:
            # 执行sql报错
            return None

        # 提交
        conn.commit()
        # 受影响的行数
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def delete(self, table="", where=dict()):
        """
        删除
        :param table: 表名
        :param where: 字段名为key，字段值为val的字典
        :return: 受影响的行数（cursor.rowcount）
        """
        if not table:
            # 表名为空
            return None

        # 参数
        args = []

        wheres = ""
        for key, val in where.items():
            wheres += " AND {}=%s".format(key)
            args.append(val)
        wheres.strip()

        sql = "DELETE FROM `{}` WHERE 1=1 {}".format(table, wheres)
        cursor = self.execute_sql(sql, args)
        if not cursor:
            # 执行sql报错
            return None

        # 提交
        conn.commit()
        # 受影响的行数
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount
