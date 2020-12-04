# 版本管理系统开发手册
## 一 · 文件说明

1. runserver.py

  用来接收启动参数，初始化数据库或者拉起进程

2. db目录

  用于存储生成的数据库文件，如果要初始化数据库，请先删除这个文件夹下的db文件

3. application程序主目录

- 3.1.  \_\_init\_\_.py

  加载controller模块，初始化app

- 3.2.  application/controller/base_controller.py

  MVC架构中的C -- Controller控制器，用于处理接收到的请求，操作数据模型（Model），给用户返回渲染过后的View（页面）。

- 3.3.  application/models/model.py

  MVC架构中的M -- Model数据模型，用于与数据库交互。

- 3.4  application/static

  用于存储css，js，图片文件等的文件夹，upload文件夹用于存储用户上传的文件

- 3.5. application/templates

  用于存储模板文件，MVC架构中的V -- View页面

## 二 · 启动与后台逻辑
runserver.py 通过import application 会自动加载 \_\_init\_\_.py，\_\_init\_\_.py中的方法会根据参数拉起主进程，同时其中import的controller模块将会与之关联开始处理请求。

根据web访问url匹配进入相应的方法执行相关的操作，然后调用model层操作数据库，最后将结果渲染到html返回给用户。

详细部分请参考代码注释。

View相关的代码注释请在index.html中查看。

