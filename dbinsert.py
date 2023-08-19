#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import *
import hashlib
from os import urandom
import datetime
engine = create_engine('sqlite:///scrape.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
words = ['automatic', 'bottom', 'bottom bitch', 'branding', 'caught a case', 
'choosing up', 'circuit', 'coercion', 'commercial sex act', 'cousin-in-law', 
'cousin in law', 'daddy', 'date', 'exit fee', 'facilitaor', 'family', 'folks', 
'finesse pimp', 'romeo pimp', 'force', 'fraud', 'gorilla pimp', 'guerilla pimp', 
'head cut', 'human smuggling', 'human traffick', 'in-pocket', 'in pocket', 'john', 
'trick', 'kiddie stroll', 'loose bitch', 'lot lizard', 'madam', 'out of pocket', 
'pimp', 'pimp circle', 'pimp partner', 'quota', 'eyeballing', 'renegade', 
'seasoning', 'serving a pimp', 'squaring up', 'stable', 'the game', 'the life', 
'track', 'stroll', 'blade', 'trade up', 'trade down', 'traficker', 'turn out', 
'the wire', 'wifey', 'wife-in-law', 'wife in law', 'sister wife']
for word in set(words):
    buzz = Buzzwords(word=word)
    session.add(buzz)
    session.commit()

password = "admin123"
salt = urandom(8)
hash_object = hashlib.sha256(password.encode() + salt)
admin = User(username="admin", password=hash_object.hexdigest(), salt=salt)
session.add(admin)
session.commit()