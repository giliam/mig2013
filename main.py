#!/usr/bin/python
# -*-coding:utf-8 -*

import sys
sys.path.append("db")
sys.path.append("recorder")

from db import Db
db = Db("db/")

from recorder import recorder
recorder(db)
