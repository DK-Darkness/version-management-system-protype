from application import app
import sys
import os

def main(port):
    app.run(debug=True,host='0.0.0.0',port=port)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'migration':
            os.system('python3 ./application/models/model.py')  # 初始化数据库
        elif sys.argv[1] == '-port':
            main(int(sys.argv[2]))  # 根据收到的参数指定端口执行
        else:
            main(5000)  # 默认5000端口
    except:
        main(5000)  # 在启动参数异常时以默认参数启动