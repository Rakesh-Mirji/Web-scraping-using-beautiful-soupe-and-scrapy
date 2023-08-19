#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, LargeBinary,Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Buzzwords(Base):
    __tablename__ = 'buzzwords'
    word = Column(Text, primary_key = True)

    @property
    def serialise(self):
        return {'word': self.word}

class Catches(Base):
    __tablename__ = 'catches'
    catch_id = Column(Integer, primary_key = True)
    message = Column(Text)
    author = Column(Text)
    word = Column(Text, ForeignKey('buzzwords.word'))
    buzzwords = relationship(Buzzwords)
    catchdate = Column(Text)
    website = Column(Text)

    @property
    def serialise(self):
        return {
        'catch_id': self.catch_id,
        'message': self.message,
        'author': self.author,
        'word': self.word,
        'catchdate': self.catchdate,
        'website': self.website
        }
    
class Report(Base):
    __tablename__ = 'report'
    report_id = Column(Integer, primary_key = True)
    website = Column(Text)
    word = Column(Text, ForeignKey('buzzwords.word'))
    message = Column(Text)
    buzzwords = relationship(Buzzwords)

    @property
    def serialise(self):
        return {
        'report_id': self.report_id,
        'word': self.word,
        'message': self.message,
        'website': self.website
        }
    
class User(Base):
    __tablename__ = 'user'
    username = Column(String(20), primary_key = True)
    password = Column(String(20), nullable = False)
    salt = Column(LargeBinary)
engine = create_engine('sqlite:///scrape.db')
Base.metadata.create_all(engine)
