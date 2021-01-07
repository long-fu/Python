import tornado.ioloop
import tornado.web

def readfile(file):
    r_f = open(file,'rb')
    bit = r_f.read()
    r_f.close()
    return bit

class i_index(tornado.web.RequestHandler):
    # def set_default_headers(self):
    #     self.set_header("Access-Control-Allow-Origin", "*")
    #     self.set_header("Access-Control-Allow-Headers", "Content-Type")
    #     self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
    #     self.set_header ('Content-Type', 'audio/mpeg')

    def get(self):
        filename = "/Users/flqy/Desktop/PythonProject/mamamoo/Be.mp3"
        # self.set_header ('Accept-Ranges', 'bytes')
        self.set_header ('Content-Type', 'audio/mpeg')
        # Connection: keep-alive
        self.set_header ('Content-Disposition', 'inline; filename=\"Be.mp3\"')
        self.set_header ('Connection', 'keep-alive')
        print("请求本地的资源")
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
            f.close()
        self.finish()
    pass

class ii_index(tornado.web.RequestHandler):
    # def set_default_headers(self):
    #     self.set_header("Access-Control-Allow-Origin", "*")
    #     self.set_header("Access-Control-Allow-Headers", "Content-Type")
    #     self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")

    def get(self):
        bit = readfile("/Users/flqy/Desktop/PythonProject/mamamoo/gogobebe.mp3")
        
        self.set_header ('Content-Disposition', 'inline; filename=gogobebe.mp3')
        self.set_header ('Content-Type', 'audio/mpeg')
        self.set_header ('Connection', 'keep-alive')
        self.write(bit)
        self.finish()
    pass

class iii_index(tornado.web.RequestHandler):
    # def set_default_headers(self):
    #     self.set_header("Access-Control-Allow-Origin", "*")
    #     self.set_header("Access-Control-Allow-Headers", "Content-Type")
    #     self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
        
    def get(self):
        bit = readfile("/Users/flqy/Desktop/PythonProject/mamamoo/maria.mp3")
        # self.set_header('Content-Type', 'audio/mpeg; charset=utf-8')
        self.set_header('Content-Type', 'text/plain; charset=utf-8')
        
        self.set_header ('Content-Disposition', 'inline; filename=maria.mp3')
        # self.set_header ('Connection', 'keep-alive')
        
        self.write(bit)
        self.finish()
    pass

class iv_index(tornado.web.RequestHandler):

        
    def get(self):
        print("请求最后一首歌")
        bit = readfile("/Users/flqy/Desktop/PythonProject/mamamoo/starry night.mp3")
        self.set_header ('Connection', 'keep-alive')
        self.set_header ('Content-Type', 'text/plain; charset=utf-8')
        self.set_header ('Content-Disposition', 'inline; filename=\"starry night.mp3\"')
        self.write(bit)
        self.finish()
    pass

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # _body = self.request.body
        # print("请求body", _body)
        self.write("Hello, world")
        self.finish()
    def post(self):
        _body = self.request.body
        print("请求body", _body)
        self.write("Hello, world")
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/i.mp3', i_index),
        (r'/ii.mp3', ii_index),
        (r'/iii.mp3', iii_index),
        (r'/iv.mp3', iv_index),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
