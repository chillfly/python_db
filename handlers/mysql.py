from .base import BaseHandler
from models import mysql as mysql_model


class ResourceHandler(BaseHandler):
    def init_where(self, **kwargs):
        """
        初始化查询条件id
        :param kwargs:
        :return:
        """
        where = {}
        _id = kwargs.get("id")
        if _id:
            # 请求路径如：/author/1 ，其中1就是传递过来的id
            where["id"] = _id

        return where

    def get(self, resource, *args, **kwargs):
        """
        读取
        :param resource:
        :return:
        """
        arguments = self.init_arguments(self.request.arguments)
        where = self.init_where(**kwargs)
        where.update(arguments)
        try:
            res = mysql_model.MysqlDB().select(resource, where)
            if not res:
                # 无数据
                self.write_json(404, data={"error": "no data"})
                return

            self.write_json(data={"data": res})
        except:
            self.write_json(500, data={"error": "server error"})

    def post(self, resource, *args, **kwargs):
        """
        新建
        :param resource:
        :return:
        """
        data = self.init_arguments(self.request.arguments)
        try:
            lastrowid = mysql_model.MysqlDB().insert(resource, data)

            if not lastrowid:
                # 新增失败
                self.write_json(500, data={"msg": "insert err"})
                return

            self.write_json(201, data={"inserted_id": lastrowid})

        except:
            self.write_json(500, data={"msg": "server error"})

    def put(self, resource, *args, **kwargs):
        """
        更新
        :param resource:
        :return:
        """
        where = self.init_where(**kwargs)

        data = self.init_arguments(self.request.arguments)
        try:
            rowcount = mysql_model.MysqlDB().update(resource, where, data)
            if not rowcount:
                # 更新失败
                self.write_json(500, data={"error": "update err"})
                return

            self.write_json(data={"update_count": rowcount})
        except:
            self.write_json(500, data={"msg": "server error"})

    def delete(self, resource, *args, **kwargs):
        """
        删除
        :param resource:
        :return:
        """
        arguments = self.init_arguments(self.request.arguments)
        where = self.init_where(**kwargs)
        where.update(arguments)

        try:
            rowcount = mysql_model.MysqlDB().delete(resource, where)
            if not rowcount:
                # 删除失败
                self.write_json(500, data={"error": "delete err"})
                return

            self.write_json(204, data={"deleted_count": rowcount})
        except:
            self.write_json(500, data={"msg": "server error"})
