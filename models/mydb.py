from pony.orm import *

db = Database()

class PlayGround(db.Entity):
    name = Required(str)
    using = Required(bool,sql_default=False,default=False)
    face = Optional('Face')
    memo = Optional(str)

class Games(db.Entity):
    name = Required(str)
    is_team = Required(bool,sql_default=False,default=False)
    memo = Optional(str)

class Player(db.Entity):
    name = Required(str)
    sex = Required(int)
    age = Required(int)
    work_place = Optional(str)
    tel = Required(str)
    team = set('Team')

class Team(db.Entity):
    name = Required(str)
    players = set('Player')
    facea = Optional('Face', reverse="teama")
    faceb = Optional('Face', reverse="teamb")

class PlayDate(db.Entity):
    flag = Required(str)

class Face(db.Entity):
    times = Required(int)
    teama = Required('Team', reverse="facea")
    teamb = Required('Team', reverse="faceb")
    scorea = Optional(int,nullable=True)
    scoreb = Optional(int,nullable=True)
    playground = Optional(PlayGround)

set_sql_debug(True)
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)