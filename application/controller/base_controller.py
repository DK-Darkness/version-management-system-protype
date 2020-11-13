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
    filename = ''.join(f.filename.split('.')[:-1])+'_'+str(int(time.time()))+'.'+str(f.filename.split('.')[-1])
    upload_path = os.path.join(basepath,'../static/uploads',filename)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)

    file_path = '/static/uploads/{}'.format(filename)
    form = request.form.to_dict()
    version = Version(customer=form['customer'],chip_num=form['chip_num'],ver_name=form['ver_name'], \
        git_node=form['git_node'],commit_time=float(form['commit_time']),file_path=file_path, comment=form['comment'])
    
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