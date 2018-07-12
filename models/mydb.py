import os
from pony.orm import *

db = Database()

class PlayGround(db.Entity):
    name = Required(str)
    using = Required(bool,sql_default=False,default=False)
    face = Optional('Face', cascade_delete=True)
    memo = Optional(str,nullable=True)

class Games(db.Entity):
    name = Required(str)
    team_num = Required(int,sql_default=1,default=1)
    sex = Optional(str,nullable=True)
    memo = Optional(str,nullable=True)
    team = Set('Team')
    group = Set('Group')

class Player(db.Entity):
    name = Required(str)
    idcode = Required(str, unique=True)
    sex = Required(str)
    age = Optional(int,nullable=True)
    work_place = Optional(str,nullable=True)
    tel = Required(str)
    team = Set('Team')

class Team(db.Entity):
    name = Required(str)
    players = Set('Player')
    # facea = Optional('Face', reverse="teama")
    # faceb = Optional('Face', reverse="teamb")
    game = Required('Games')
    group = Optional('Group')

class PlayDate(db.Entity):
    flag = Required(str)

class Face(db.Entity):
    teama = Required(Team)
    teamb = Required(Team)
    times = Optional(int,default=0)
    scorea = Optional(int,nullable=True)
    scoreb = Optional(int,nullable=True)
    playground = Optional(PlayGround)

class Group(db.Entity):
    name = Required(str)
    game = Required(Games,reverse="group")
    teams = Set(Team)

# 测试用
class TObj(db.Entity):
    name = Required(str)
    age = Required(int)
    tel = Optional(str)

# set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'dbs')

db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)