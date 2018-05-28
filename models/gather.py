import xlrd
from .mydb import *

@db_session
def clear_data():
    for o in (PlayGround,Games,Player,Team,PlayDate,Face,Group)[::-1]:
        select(r for r in o).delete(bulk=True)

# def exvl2int(data):
    

@db_session
def load_data(fname):
    print(fname)
    names_objs = (('playground',PlayGround,('name','memo')),
        ('games',Games,('name','team_num','memo')),
        ('players',Player,('name','idcode','sex','age','work_place','tel')))
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        wb = xlrd.open_workbook(fname)
        for sheetname,obj,keys in names_objs:
            datas = []
            ws = wb.sheet_by_name(sheetname)
            for i in range(1,ws.nrows):
                datas.append(ws.row_values(i))
            print(datas)
            for data in datas:
                param = dict()
                for d,k in zip(data,keys):
                    if d:
                        param[k] = d
                obj(**param)


