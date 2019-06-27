from .base import BaseHandler
from models import mongo as mongo_model
from bson import ObjectId


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
            if not isinstance(_id, ObjectId):
                # 根据主键查找内容，主键必须是ObjectId类型
                _id = ObjectId(_id)
            where["_id"] = _id

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
            res = mongo_model.db[resource].find(where)
            if res.count() == 0:
                # 无数据
                self.write_json(404, data={"error": "no data"})
                return

            data = {"data": []}
            for item in res:
                if "_id" in item.keys():
                    # 将objectId格式转换为str，方便输出
                    item["_id"] = str(item["_id"])
                data["data"].append(item)
            self.write_json(data=data)
        except:
            self.write_json(500, data={"msg": "server error"})

    def post(self, resource, *args, **kwargs):
        """
        新建
        :param resource:
        :return:
        """
        data = self.init_arguments(self.request.arguments)
        try:
            res = mongo_model.db[resource].insert_one(data)
            if not res.inserted_id:
                # 插入失败
                self.write_json(500, data={"error": "insert err"})
                return

            self.write_json(201, data={"inserted_id": str(res.inserted_id)})
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
            res = mongo_model.db[resource].update_one(where, {"$set": data})
            if not res.modified_count:
                # 更新失败
                self.write_json(500, data={"error": "update err"})
                return

            self.write_json(data={"update": "true"})
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
            res = mongo_model.db[resource].delete_many(arguments)
            if not res.deleted_count:
                # 删除失败
                self.write_json(500, data={"error": "delete err"})
                return

            self.write_json(204, data={"deleted_count": str(res.deleted_count)})
        except:
            self.write_json(500, data={"msg": "server error"})
