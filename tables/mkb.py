# таблица в базе : путь к файлу
name = {'mkb':'REGIONAL/MKB.xml'}
def getquery(file):
    # шаблон для загрузки в базу
    sql = '''LOAD XML LOCAL INFILE ''' + file + ''' INTO TABLE mkb
    CHARACTER SET cp1251
    ROWS IDENTIFIED BY '<zap>'
    (CODE, NAME, KSG_CODE1, KSG_CODE2, KSG_CODE3, KSG_CODE4, KSG_CODE5, KSG_USED, KSG_CODE_C1, KSG_CODE_C2,  KSG_CODE_C3, KSG_CODE_C4, KSG_CODE_C5, KSG_USED_C, @START_DATE, @FINAL_DATE, @ADD_DATE)
    SET START_DATE = STR_TO_DATE(@START_DATE, '%d.%m.%Y'),
    FINAL_DATE = STR_TO_DATE(@FINAL_DATE, '%d.%m.%Y'),
    ADD_DATE = STR_TO_DATE(@ADD_DATE, '%d.%m.%Y');'''
    print(sql)
