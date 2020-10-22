from application import app
from flask import request,render_template,url_for,redirect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.models.model import *

import os
import json


engine = create_engine('sqlite:///db/sqlite3.db?check_same_thread=False', echo=True)  # 数据库连接
SessionDB = sessionmaker(bind=engine)  # 数据库session
sessionDB = SessionDB()  # 数据库session实例


@app.route('/',methods=['GET'])
def get_products():
    versions = sessionDB.query(Version).all()
    return render_template('index.html',versions=versions)


@app.route('/add',methods=['GET'])
def get_addpage():
    
    return render_template('add.html')


@app.route('/add',methods=['POST'])
def add_product():

    f = request.files['file']
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    upload_path = os.path.join(basepath,'../static/uploads',f.filename)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)

    file_path = '/static/uploads/{}'.format(f.filename)
    form = request.form.to_dict()
    version = Version(customer=form['customer'],chip_num=form['chip_num'],ver_name=form['ver_name'], \
        git_node=form['git_node'],commit_time=int(form['commit_time']),file_path=file_path)
    
    sessionDB.add(version)
    sessionDB.commit()

    return redirect(url_for('get_products'))


@app.route('/delete',methods=['POST'])
def delete_product():
    ver_id = request.form.to_dict()['id']
    file_path = sessionDB.query(Version).filter(Version.ver_id == int(ver_id))[0].file_path
    file_path = 'application'+file_path
    os.remove(file_path)
    sessionDB.query(Version).filter(Version.ver_id == int(ver_id)).delete()
    sessionDB.commit()

    return redirect(url_for('get_products'))


@app.route('/query',methods=['POST'])
def get_product_query():

    form = request.form.to_dict()
    
    if form['customer'] == '':
        if form['chip_num'] == '':
            if form['ver_name'] == '':
                versions = sessionDB.query(Version).all()
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

@app.route('/querygit',methods=['POST'])
def get_product_detail():

    form = request.form.to_dict()
    if form['git_node'] == '':
        versions = sessionDB.query(Version).all()
    else:
        versions = sessionDB.query(Version).filter(Version.git_node == form['git_node'])
    
    return render_template('index.html',versions=versions)