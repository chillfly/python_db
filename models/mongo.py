import pymongo
import config


# 创建一个mongo客户端
client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)

# 有该数据库，则使用；没有，则创建
db = client[config.MONGO_DB]
