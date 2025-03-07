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
                    <meta charset="utf-8">
                    <title>文件下载</title>
                    <style>
                        body {{font-family: Arial, sans-serif; margin: 40px;}}
                        .download-btn {{
                            display: inline-block;
                            padding: 10px 15px;
                            background-color: #4CAF50;
                            color: white;
                            text-decoration: none;
                            border-radius: 4px;
                            margin: 10px 0;
                        }}
                        #status {{margin-top: 20px; color: #555;}}
                    </style>
                </head>
                <body>
                    <h1>可用下载</h1>
                    <p><a href="/audio.wav" class="download-btn">下载音频文件</a></p>
                    <p><a href="/text.txt" class="download-btn">下载文本信息</a></p>
                </body>
            </html>
            """
            self.wfile.write(html.encode())

        elif self.path == '/audio.wav':
            # 提供音频文件下载
            try:
                # 使用绝对路径
                script_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(script_dir, 'sample.wav')

                if not os.path.exists(file_path):
                    print(f"错误: 文件不存在 '{file_path}'")
                    self.send_error(404, "File not found")
                    return

                # 获取文件大小
                file_size = os.path.getsize(file_path)

                with open(file_path, 'rb') as file:
                    content = file.read()

                    self.send_response(200)
                    # 使用通用二进制类型
                    self.send_header('Content-Type', 'application/octet-stream')
                    self.send_header('Content-Length', str(file_size))
                    self.send_header('Content-Disposition', 'attachment; filename="audio.wav"')
                    # 添加跨域支持
                    self.send_header('Access-Control-Allow-Origin', '*')
                    # 禁止缓存
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.end_headers()

                    # 写入文件内容
                    self.wfile.write(content)
                    print(f"成功发送文件: {file_path}, 大小: {file_size} 字节")
            except FileNotFoundError:
                print("错误: 文件未找到")
                self.send_error(404, "File not found")
            except Exception as e:
                print(f"错误: {e}")
                self.send_error(500, f"Internal server error: {str(e)}")

        elif self.path == '/text.txt':
            # 提供文本文件下载
            text_content = "这是要分享的文本信息"
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(text_content.encode('utf-8'))))
            self.send_header('Content-Disposition', 'attachment; filename="info.txt"')
            self.send_header('Cache-Control', 'no-cache')
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
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, FileShareHandler)

    # 检查文件是否存在
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'sample.wav')
    print(f"检查音频文件: {file_path}")
    print(f"文件存在: {os.path.exists(file_path)}")
    if os.path.exists(file_path):
        print(f"文件大小: {os.path.getsize(file_path)} 字节")

    # 获取云服务器的公网IP
    public_ip = "1.94.225.94"
    print(f"服务器已启动:")
    print(f"主页链接: http://{public_ip}:{port}")
    print(f"音频下载链接: http://{public_ip}:{port}/audio.wav")
    print(f"文本下载链接: http://{public_ip}:{port}/text.txt")
    print("\n按 Ctrl+C 停止服务器")

    httpd.serve_forever()

if __name__ == '__main__':
    run_server()