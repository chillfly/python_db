import tornado.web
import config
import json


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        # 预处理，做一些预防性的操作
        token = self.request.headers.get("token", "")
        # if config.TOKEN != token:
        #     # token验证不通过，报错
        #     self.send_error(401, reason="not authed")
        #     return

    def write_json(self, status_code=200, data={}):
        data = json.dumps(data)
        self.set_header("Content-Type", "text/json;charset=utf-8")
        self.set_status(status_code)
        self.write(data)

    def on_finish(self):
        print("finish")

    def init_arguments(self, arguments: dict):
        """
        初始化参数，将参数转换为非bytes字段，且取最新的参数
        :param kwargs:
        :return:
        """
        for key, val in arguments.items():
            # 取最新的一个数据，且转换bytes
            arguments[key] = self.bytes_transfer(val[-1])
        return arguments

    def bytes_transfer(self, val):
        if not isinstance(val, bytes):
            # 不是bytes字节，直接返回
            return val

        if val.isdigit():
            # 纯数字
            val = int(val)
        else:
            # 不是纯数字，返回字符串
            val = str(val, encoding='utf8')

        return val