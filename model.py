from peewee import Model, PostgresqlDatabase, CharField,\
    IntegerField, TextField, BigIntegerField, BooleanField,\
    ForeignKeyField
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict

import os
import settings

if os.environ.get('DATABASE_URL'):
    database = connect(os.environ.get('DATABASE_URL'))
else:
    database = PostgresqlDatabase(
        settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
    )


class BaseModel(Model):
    class Meta:
        database = database

    def to_dict(self, exclude=[]):
        return model_to_dict(self, recurse=False, exclude=exclude)


class User(BaseModel):
    userId = TextField()
    email = CharField(default='test@mail.com')
