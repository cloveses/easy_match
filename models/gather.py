import xlrd
from .mydb import *

@db_session
def clear_data():
    for o in (PlayGround,Games,Player,Team,PlayDate,Face,Group)[::-1]:
        select(r for r in o).delete()

def team_num2int(data):
    default = 1
    if isinstance(data,str) and data != '' and data.isdigt():
        default = int(data)
    if isinstance(data,float):
        default = int(data)
    return default if default>0 else 1

def age2int(data):
    if isinstance(data,str) and data != '' and data.isdigt():
        return int(data)
    if isinstance(data,float):
        return int(data)

def tel2str(data):
    if isinstance(data,str):
        return data
    if isinstance(data,float):
        return str(int(data))

@db_session
def load_data(fname):
    print(fname)
    names_objs = (('playground',PlayGround,('name','memo'),(None,None)),
        ('games',Games,('name','team_num','sex','memo'),(None,team_num2int,None,None)),
        ('players',Player,('name','idcode','sex','age','work_place','tel'),
                            (None,None,None,age2int,None,tel2str)))
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        wb = xlrd.open_workbook(fname)
        for sheetname,obj,keys,chg_funs in names_objs:
            datas = []
            ws = wb.sheet_by_name(sheetname)
            for i in range(1,ws.nrows):
                datas.append(ws.row_values(i))
            # print(datas)
            for index,data in enumerate(datas):
                data = [chgfun(d) if chgfun else d for d,chgfun in zip(data,chg_funs)]
                param = dict()
                for d,k in zip(data,keys):
                    if d:
                        param[k] = d
                try:
                    # print(param)
                    obj(**param)
                except:
                    rollback()
                    # print('error!')
                    info = '请检查{}表，第{}行数据。'.format(sheetname,index+1)
                    # print(info,param)
                    return info

@db_session
def get_games():
    games = select((g.name,g.team_num) for g in Games)
    games = {k:v for k,v in games}
    return games

@db_session
def get_games_sex():
    games = select((g.name,g.sex) for g in Games)
    games = {k:v for k,v in games}
    return games

@db_session
def get_players(sex=None):
    if sex:
        players = select(p for p in Player if p.sex==sex)[:]
    else:
        players = select(p for p in Player)[:]
    return players

@db_session
def get_playgrounds(using=None):
    if using is not None:
        pgs = select(p for p in PlayGround if p.using==using)[:]
    else:
        pgs = select(p for p in PlayGround)[:]
    return pgs

@db_session
def get_games():
    return select(g for g in Games)[:]

@db_session
def has_data():
    if exists(p for p in Player) and exists(g for g in Games):
        return True

@db_session
def save_cell(obj,key,data):
    obj[key].set(**data)

@db_session
def del_rowdb(obj,key):
    obj[key].delete()

@db_session
def new_team(gid,pids,flag=0):
    infos = []
    game = Games[gid]
    players = [Player[pid] for pid in pids]
    if flag:
        for player in players:
            if any([player in t.players for t in game.team]):
                infos.append(player.name)
            else:
                team = Team(name=player.name,game=game)
                team.players.add(player)
                game.team.add(team)
                player.team.add(team)
        if infos:
            infos = ' '.join(infos) + '不能多次参加一个项目！'
        else:
            infos = ''
    else:
        if any([set(players).intersection(set(t.players)) for t in game.team]):
            infos = '一个人不能多次参加一个项目！'
        else:
            team = Team(name='-'.join([player.name for player in players]),game=game)
            for p in players:
                team.players.add(p)
                p.team.add(team)
            game.team.add(team)
            
    return infos

@db_session
def get_team_datas(game_type=None):
    if game_type:
        Ts = select(t for t in Team if t.game==Games[game_type])
    else:
        Ts = select(t for t in Team)
    datas = []
    for team in Ts:
        data = []
        data.append(team.id)
        data.append('-'.join([p.name for p in team.players]))
        data.append(team.game.name)
        data.append(team.group.name if team.group else '')
        datas.append(data)
    if datas:
        datas.sort(key=lambda x:x[2])
    return datas

@db_session
def get_group_datas():
    datas = []
    for group in select(g for g in Group):
        data = []
        data.append(group.id)
        data.append(group.name)
        data.append(group.game.name)
        data.append(','.join((t.name for t in group.teams)))
        data.append(group.game.id)
        datas.append(data)
    if datas:
        datas.sort(key=lambda x:x[2])
    return datas

@db_session
def add_groupdb(name,gid):
    if exists(p for p in Group if p.name == name):
        return '不能重名！'
    else:
        g = Group(name=name,game=Games[gid])
        Games[gid].group.add(g)

@db_session
def add_team2group_db(gid,tids):
    g = Group[gid]
    for tid in tids:
        g.teams.add(Team[tid])

@db_session
def get_group_for_game(gid):
    groups = select(g for g in Group if g.game==Games[gid])
    return [(g.id,g.name,g.game.name) for g in groups]

@db_session
def get_teams_for_group(gid):
    teams = Group[gid].teams
    return [(t.id,t.name,','.join(p.name for p in t.players)) for t in teams]

@db_session
def add_face2db(tid1,tid2):
    print(tid1,tid2)
    teama = Team[tid1]
    teamb = Team[tid2]
    print(teama.name,teamb.name)
    face = Face(teama=teama,teamb=teamb)
    teama.facea = face
    teamb.faceb = face


@db_session
def get_faces(gid,ggid):
    faces = select(f for f in Face if f.teama.game.id == gid and f.teama.group.id == ggid)
    return [(f.id,' '.join(str(f.teama.id),f.teama.name),
        ' '.join(str(f.teamb.id),f.teamb.name)) for f in faces]
    # return [('1','aa','bb'),]