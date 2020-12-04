from application import app
from flask import request,render_template,url_for,redirect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.models.model import *

import os
import json
import time


engine = create_engine('sqlite:///db/sqlite3.db?check_same_thread=False', echo=True)  # 数据库连接
SessionDB = sessionmaker(bind=engine)  # 数据库session
sessionDB = SessionDB()  # 数据库session实例

# 主页用于展示所有
@app.route('/',methods=['GET'])  # 用来匹配请求路径与请求方法
def get_products():
    versions = sessionDB.query(Version).all()  # 查询数据库，查询全部
    return render_template('index.html',versions=versions)  # 将数据渲染到View并返回页面

# 获取添加
@app.route('/add',methods=['GET'])
def get_addpage():

    return render_template('add.html')

# 添加
@app.route('/add',methods=['POST'])
def add_product():

    f = request.files['file']  # 获取form中上传的文件
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    filename = ''.join(f.filename.split('.')[:-1])+'_'+str(int(time.time()))+'.'+str(f.filename.split('.')[-1])  # 根据时间自动重命名避免重名覆盖
    upload_path = os.path.join(basepath,'../static/uploads',filename)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)  # 保存上传的文件

    file_path = '/static/uploads/{}'.format(filename)  # 生成用于下载上传的文件的链接
    form = request.form.to_dict()  # 获取表单信息转换成python字典
    version = Version(customer=form['customer'],chip_num=form['chip_num'],ver_name=form['ver_name'], \
        git_node=form['git_node'],commit_time=float(form['commit_time']),file_path=file_path,comment=form['comment'],git_url=form['git_url'])  # 根据页面传过来的数据创建数据模型实例
    
    sessionDB.add(version)  # 存入到数据库
    sessionDB.commit()  # 保存对数据库的修改

    return redirect(url_for('get_products'))  # 重定向到获取全部数据的方法返回index页面

# 删除
@app.route('/delete',methods=['POST'])
def delete_product():
    ver_id = request.form.to_dict()['id']  # 提取表单中的id（主键）用来删除数据库中的数据
    file_path = sessionDB.query(Version).filter(Version.ver_id == int(ver_id))[0].file_path  # 根据id查找数据库中的文件路径
    file_path = 'application'+file_path  # 合成实际存储路径
    os.remove(file_path)  # 删除文件
    sessionDB.query(Version).filter(Version.ver_id == int(ver_id)).delete()  # 删除数据库中的相应数据
    sessionDB.commit()  # 提交对数据库的更改

    return redirect(url_for('get_products'))

# 条件查询
@app.route('/query',methods=['POST'])
def get_product_query():

    form = request.form.to_dict()

    # 条件查找，可以单个条件查找也可以两个或三个条件同时查找
    if form['customer'] == '':  # 判断相应的查询条件是否为空，选择相应的查询命令
        if form['chip_num'] == '':
            if form['ver_name'] == '':
                versions = sessionDB.query(Version).all()  # 三个条件都为空查询所有
            else:
                versions = sessionDB.query(Version).filter(Version.ver_name == form['ver_name'])
        else:
            if form['ver_name'] == '':
                versions = sessionDB.query(Version).filter(Version.chip_num == form['chip_num'])
            else:
                versions = sessionDB.query(Version).filter(Version.chip_num == form['chip_num'], Version.ver_name == form['ver_name'])
    else:
        if form['chip_num'] == '':
            if form['ver_name'] == '':
                versions = sessionDB.query(Version).filter(Version.customer == form['customer'])
            else:
                versions = sessionDB.query(Version).filter(Version.customer == form['customer'], Version.ver_name == form['ver_name'])
        else:
            if form['ver_name'] == '':
                versions = sessionDB.query(Version).filter(Version.customer == form['customer'], Version.chip_num== form['chip_num'])
            else:
                versions = sessionDB.query(Version).filter(Version.customer == form['customer'], Version.chip_num == form['chip_num'], Version.ver_name == form['ver_name'])

    return render_template('index.html',versions=versions) 

# git节点查询，因为唯一，所以没和条件查找放一起
@app.route('/querygit',methods=['POST'])
def get_product_detail():

    form = request.form.to_dict()
    if form['git_node'] == '':
        versions = sessionDB.query(Version).all()
    else:
        versions = sessionDB.query(Version).filter(Version.git_node == form['git_node'])
    
    return render_template('index.html',versions=versions)

#####################################
#            TW发布版本 
#####################################

@app.route('/twview',methods=['GET'])
def get_products_tw():
    twversions = sessionDB.query(TWVersion).all()
    return render_template('twview.html',twversions=twversions)


@app.route('/twadd',methods=['GET'])
def get_addpage_tw():
    
    return render_template('twadd.html')


@app.route('/twadd',methods=['POST'])
def add_product_tw():

    f = request.files['file']
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    filename = ''.join(f.filename.split('.')[:-1])+'_'+str(int(time.time()))+'.'+str(f.filename.split('.')[-1])
    upload_path = os.path.join(basepath,'../static/uploads',filename)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)

    file_path = '/static/uploads/{}'.format(filename)
    form = request.form.to_dict()
    twversion = TWVersion(customer=form['customer'],chip_num=form['chip_num'],ver_name=form['ver_name'], \
        release_date=int(form['release_date']),file_path=file_path, comment=form['comment'])
    
    sessionDB.add(twversion)
    sessionDB.commit()

    return redirect(url_for('get_products_tw'))


@app.route('/twdelete',methods=['POST'])
def delete_product_tw():
    ver_id = request.form.to_dict()['id']
    file_path = sessionDB.query(TWVersion).filter(TWVersion.ver_id == int(ver_id))[0].file_path
    file_path = 'application'+file_path
    os.remove(file_path)
    sessionDB.query(TWVersion).filter(TWVersion.ver_id == int(ver_id)).delete()
    sessionDB.commit()

    return redirect(url_for('get_products_tw'))

@app.route('/twquery',methods=['POST'])
def get_product_query_tw():

    form = request.form.to_dict()
    
    if form['customer'] == '':
        if form['chip_num'] == '':
            if form['ver_name'] == '':
                twversions = sessionDB.query(TWVersion).all()
            else:
                twversions = sessionDB.query(TWVersion).filter(TWVersion.ver_name == form['ver_name'])
        else:
            if form['ver_name'] == '':
                twversions = sessionDB.query(TWVersion).filter(TWVersion.chip_num == form['chip_num'])
            else:
                twversions = sessionDB.query(TWVersion).filter(TWVersion.chip_num == form['chip_num'], TWVersion.ver_name == form['ver_name'])
    else:
        if form['chip_num'] == '':
            if form['ver_name'] == '':
                twversions = sessionDB.query(TWVersion).filter(TWVersion.customer == form['customer'])
            else:
                twversions = sessionDB.query(TWVersion).filter(TWVersion.customer == form['customer'], TWVersion.ver_name == form['ver_name'])
        else:
            if form['ver_name'] == '':
                twversions = sessionDB.query(TWVersion).filter(TWVersion.customer == form['customer'], TWVersion.chip_num== form['chip_num'])
            else:
                twversions = sessionDB.query(TWVersion).filter(TWVersion.customer == form['customer'], TWVersion.chip_num == form['chip_num'], TWVersion.ver_name == form['ver_name'])

    return render_template('twview.html',twversions=twversions) 