import tornado.httpserver
import tornado.ioloop
import config
import application

from tornado.options import define, options


define("port", default=config.SERVER_PORT, help="服务端口")


def main():

    # 解析命令行，从命令行中获取数据（必须是define提前定义好的才能获取到）
    options.parse_command_line()

    # tornado.web.Application的子类
    app = application.Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
