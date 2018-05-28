from pony.orm import *

db = Database()

class PlayGround(db.Entity):
    name = Required(str)
    using = Required(bool,sql_default=False,default=False)
    face = Optional('Face')
    memo = Optional(str,nullable=True)

class Games(db.Entity):
    name = Required(str)
    team_num = Required(int,sql_default=1,default=1)
    memo = Optional(str,nullable=True)
    team = Set('Team')

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
    facea = Optional('Face', reverse="teama")
    faceb = Optional('Face', reverse="teamb")
    game = Required('Games')
    group = Optional('Group')

class PlayDate(db.Entity):
    flag = Required(str)

class Face(db.Entity):
    times = Required(int)
    teama = Required('Team', reverse="facea")
    teamb = Required('Team', reverse="faceb")
    scorea = Optional(int,nullable=True)
    scoreb = Optional(int,nullable=True)
    playground = Optional(PlayGround)

class Group(db.Entity):
    name = Required(str)
    teams = Set(Team)

# set_sql_debug(True)
db.bind(provider='sqlite', filename='dbs', create_db=True)
db.generate_mapping(create_tables=True)