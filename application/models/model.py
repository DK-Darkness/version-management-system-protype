from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Version(Base):
    
    __tablename__ = 'version'  # version表
    
    ver_id = Column(Integer, primary_key=True, autoincrement=True)  # 版本ID
    customer = Column(String(20))  # 客户名称
    chip_num = Column(String(20))  # 芯片方案
    ver_name = Column(String(20))  # 版本名称
    git_node = Column(String(32))  # git 节点
    git_url = Column(String(32))  # git 节点
    file_path = Column(String(256))  # 文件存放路径
    commit_time = Column(Float)  # commit 时间
    comment = Column(String(64))  # 备注

class TWVersion(Base):

    __tablename__ = 'twversions'

    ver_id = Column(Integer, primary_key=True, autoincrement=True)  # 版本ID
    customer = Column(String(20))  # 客户名称
    chip_num = Column(String(20))  # 芯片方案
    ver_name = Column(String(20))  # 版本名称
    release_date = Column(Integer)  # 发布时间
    file_path = Column(String(256))  # 文件存放路径
    comment = Column(String(64))  # 备注


if __name__ == "__main__":
    # 创建所有表
    engine = create_engine('sqlite:///db/sqlite3.db?check_same_thread=False', echo=True)
    Base.metadata.create_all(engine, checkfirst=True)

