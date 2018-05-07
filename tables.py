tables = {'mkb':
              {'path':'REGIONAL/MKB.xml',
               'charset':'cp1251',
               'query':'''(CODE, NAME, KSG_CODE1, KSG_CODE2, KSG_CODE3, KSG_CODE4, KSG_CODE5, KSG_USED, KSG_CODE_C1, KSG_CODE_C2,  KSG_CODE_C3, KSG_CODE_C4, KSG_CODE_C5, KSG_USED_C, @START_DATE, @FINAL_DATE, @ADD_DATE)'''},
          'ksg_g':
              {'path':'REGIONAL/KSG_G.xml',
               'charset':'cp1251',
               'query':'''(MKB_CODE, MKB_CODE2, KSGN_CODE, AGE, SEX, DURATION, KSG_CODE, @START_DATE, @FINAL_DATE, @ADD_DATE)'''},
          'ksg_g_c':
              {'path':'REGIONAL/KSG_G_C.xml',
               'charset':'cp1251',
               'query':'''(MKB_CODE, MKB_CODE2, KSGN_CODE, AGE, SEX, DURATION, KSG_CODE, @START_DATE, @FINAL_DATE, @ADD_DATE)'''},
          'depart':
              {'path':'REGIONAL/DEPART.xml',
               'charset':'cp1251',
               'query':'''(CODE_D, NAME_D, MO_CODE, LEVEL_D, PROF_CODE, KSG_YES, KSG_NO, USL_OK, @START_DATE, @FINAL_DATE, @ADD_DATE)'''},
          'v002':
              {'path':'FEDERAL/V002.xml',
               'charset':'utf8',
               'query':'''(IDPR, PRNAME, @DATEBEG, @DATEEND) SET DATEBEG = STR_TO_DATE(@DATEBEG, '%d.%m.%Y'), DATEEND = STR_TO_DATE(@DATEEND, '%d.%m.%Y');'''}
         }

def getquery(rootdir,table):
    # шаблон для загрузки в базу
    sql = '''LOAD XML LOCAL INFILE "'''+rootdir+tables[table]['path']+'''" INTO TABLE ''' + table + '''
    CHARACTER SET '''+tables[table]['charset']+''' ROWS IDENTIFIED BY '<zap>' ''' + tables[table]['query']
    if table != 'v002':
        sql += '''    SET START_DATE = STR_TO_DATE(@START_DATE, '%d.%m.%Y'),
        FINAL_DATE = STR_TO_DATE(@FINAL_DATE, '%d.%m.%Y'),
        ADD_DATE = STR_TO_DATE(@ADD_DATE, '%d.%m.%Y');'''
    return sql
