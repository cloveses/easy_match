import xlrd
from .mydb import *

@db_session
def clear_data():
    for o in (PlayGround,Games,Player,Team,PlayDate,Face,Group)[::-1]:
        select(r for r in o).delete(bulk=True)

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
def has_data():
    if exists(p for p in Player) and exists(g for g in Games):
        return True