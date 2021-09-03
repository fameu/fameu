# -*- coding: utf-8 -*-

from mongoengine import Document, StringField, ReferenceField


class GuPiao(Document):
    no = StringField(required=True)
    name = StringField(required=True)
    details = StringField()


class Zhousi(Document):
