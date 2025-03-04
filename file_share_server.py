from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket

class FileShareHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # 提供下载页面
            self.send_response(200)
            self.send_header('Content-type', 'text/html ; charset=utf-8')
            self.end_headers()
            
            html = f"""
            <html>
                <head>
                    <meta charset="utf-8">  # 添加meta标签声明编码
                    <title>文件下载</title>
                </head>
                <body>
                    <h1>可用下载</h1>
                    <p><a href="/audio.wav">下载音频文件</a></p>
                    <p><a href="/text.txt">下载文本信息</a></p>
                </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path == '/audio.wav':
            # 提供音频文件下载
            try:
                with open('sample.wav', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'audio/wav')
                    self.send_header('Content-Disposition', 'attachment; filename="audio.wav"')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")
                
        elif self.path == '/text.txt':
            # 提供文本文件下载
            text_content = "这是要分享的文本信息"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-Disposition', 'attachment; filename="info.txt"')
            self.end_headers()
            self.wfile.write(text_content.encode('utf-8'))

def get_local_ip():
    try:
        # 获取本机IP地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FileShareHandler)
    local_ip = get_local_ip()
    print(f"服务器已启动:")
    print(f"主页链接: http://{local_ip}:{port}")
    print(f"音频下载链接: http://{local_ip}:{port}/audio.wav")
    print(f"文本下载链接: http://{local_ip}:{port}/text.txt")
    print("\n按 Ctrl+C 停止服务器")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()