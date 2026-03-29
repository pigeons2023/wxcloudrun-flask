from datetime import datetime

from wxcloudrun import db


# 用户表
class User(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'User'

    # 设定结构体对应表格的字段
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False, unique=True)
    openid = db.Column(db.String(100), nullable=False)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())
