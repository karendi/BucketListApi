import datetime
from passlib.apps import custom_app_context as password_content
from sqlalchemy.orm import relationship
from . import db


class UserModel(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    bucket_list = db.relationship('BucketList', lazy='dynamic')

    def __repr__(self):
        # how the object will be printed helps in debugging
        return '< User %r>' % self.email

    def hash_password(self, password_hash):
        self.password = password_content.encrypt(password_hash)

    def verify_password(self, password_hash):  # returns true or false if the password is correct
        return password_content.verify(password_hash, self.password)

    @property
    def id(self):
        return self.user_id


class BucketList(db.Model):
    __tablename__ = 'bucket_list'
    bucket_list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    bucket_list_name = db.Column(db.String(25), index=True)
    items = relationship('Items', back_populates="bucket_list")
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime)

    def __repr__(self):
        return '<BucketList: %r>' % self.bucket_list_name


class Items(db.Model):
    __tablename__ = 'items'
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(64), index=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    bucket_list_items_id = db.Column(db.Integer, db.ForeignKey('bucket_list.bucket_list_id'))
    completed = db.Column(db.Boolean, default=False)
    bucket_list = relationship('BucketList', back_populates="items")

    def __repr__(self):
        return '<item_name %r>' % self.item_name
db.create_all(bind='__all__')