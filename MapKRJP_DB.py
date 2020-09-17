import selenium 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

#Database
import mysql.connector
import time
from PyQt5 import QtTest
from pandas import DataFrame, concat


JPNameDic = {
    "promo": ["ポケモンカードゲームソード&シールド プロモカード",
              "ポケモンカードゲームサン&ムーン プロモカード"],
    "S3a": ["強化拡張パック「伝説の鼓動」"],
    "SD" : ["Vスタートデッキ草　フシギバナ",
            "Vスタートデッキ炎　ガオガエン",
            "Vスタートデッキ水　ホエルオー",
            "Vスタートデッキ雷　ピカチュウ",
            "Vスタートデッキ超　ミュウ",
            "Vスタートデッキ闘　ルカリオ",
            "Vスタートデッキ悪　ガラルヤドラン",
            "Vスタートデッキ鋼　ジュラルドン",
            "Vスタートデッキ無色　イーブイ"],
    "S3": ["拡張パック「ムゲンゾーン」"],
    "S2a": ["強化拡張パック「爆炎ウォーカー」"],
    "SC_R": ["スターターセットVMAX　リザードン"],
    "SC_D": ["スターターセットVMAX　オーロンゲ"],
    "SP1": ["ザシアン＋ザマゼンタBOX"],
    "S2": ["拡張パック「反逆クラッシュ」"],
    "S1a": ["強化拡張パック「VMAXライジング」"],
    "S1H": ["ポケモンカードゲームソード&シールド 拡張パック「シールド」"],
    "S1W": ["ポケモンカードゲームソード&シールド 拡張パック「ソード」"],
    "SA_G": ["ポケモンカードゲームソード&シールド スターターセットV　草"],
    "SA_F": ["ポケモンカードゲームソード&シールド スターターセットV　炎"],
    "SA_W": ["ポケモンカードゲームソード&シールド スターターセットV　水"],
    "SA_L": ["ポケモンカードゲームソード&シールド スターターセットV　雷"],
    "SA_R": ["ポケモンカードゲームソード&シールド スターターセットV　闘"],
    "SM12a": ["ポケモンカードゲームサン&ムーン ハイクラスパック「TAG TEAM GX タッグオールスターズ」"],
    "SM12": ["ポケモンカードゲームサン&ムーン 拡張パック「オルタージェネシス」"],
    "SM11b": ["ポケモンカードゲームサン&ムーン 強化拡張パック「ドリームリーグ」"],
    "SM11a": ["ポケモンカードゲームサン&ムーン 強化拡張パック「リミックスバウト」"],
    "SMM": ["ポケモンカードゲームサン&ムーン スターターセット TAG TEAM GX「ブラッキー&ダークライGX」",
            "ポケモンカードゲームサン&ムーン スターターセット TAG TEAM GX 「エーフィ&デオキシスGX」"],
    "SM11": ["ポケモンカードゲームサン&ムーン 拡張パック「ミラクルツイン」"],
    "smp2": ["ポケモンカードゲームサン&ムーン ムービースペシャルパック「名探偵ピカチュウ」"],
    "sm10b": ["ポケモンカードゲームサン&ムーン 強化拡張パック「スカイレジェンド」"],
    "SM10a": ["ポケモンカードゲームサン&ムーン 強化拡張パック「ジージーエンド」"],
    "sm10": ["ポケモンカードゲームサン&ムーン 拡張パック「ダブルブレイズ」"],
    "sm9b": ["ポケモンカードゲームサン&ムーン 強化拡張パック「フルメタルウォール」"],
    "sm9a": ["ポケモンカードゲームサン&ムーン 強化拡張パック「ナイトユニゾン」"],
    "sm8a": ["ポケモンカードゲームサン&ムーン 強化拡張パック「ダークオーダー」"],
    "sm9": ["ポケモンカードゲームサン&ムーン 拡張パック「タッグボルト」"],
    "SMI": ["ポケモンカードゲームサン&ムーン スターターセット「炎のブースターGX」",
            "ポケモンカードゲームサン&ムーン スターターセット「水のシャワーズGX」",
            "ポケモンカードゲームサン&ムーン スターターセット「雷のサンダースGX」"],
    "sm8b": ["ポケモンカードゲームサン&ムーン ハイクラスパック「GXウルトラシャイニー」"],
    "sm8": ["ポケモンカードゲームサン&ムーン 拡張パック「超爆インパクト」"],
    "sm7b": ["ポケモンカードゲームサン&ムーン 強化拡張パック「フェアリーライズ」"],
    "sm7a": ["ポケモンカードゲームサン&ムーン 強化拡張パック「迅雷スパーク」"],
    "sm7": ["ポケモンカードゲームサン&ムーン 拡張パック「裂空のカリスマ」"],
    "sm6b": ["ポケモンカードゲームサン&ムーン 強化拡張パック「チャンピオンロード」"],
    "sm6a": ["ポケモンカードゲームサン&ムーン 強化拡張パック「ドラゴンストーム」"],
    "sm6": ["ポケモンカードゲームサン&ムーン 拡張パック「禁断の光」"],
    "sm5plus": ["ポケモンカードゲームサン&ムーン 強化拡張パック「ウルトラフォース」"],
    "sm5m": ["ポケモンカードゲームサン&ムーン 拡張パック「ウルトラムーン」"],
    "sm5s": ["ポケモンカードゲームサン&ムーン 拡張パック「ウルトラサン」"],
    "sme": ["スターターセット伝説 ソルガレオGX ルナアーラGX"],
    "sm4plus": ["ポケモンカードゲームサン&ムーン ハイクラスパック「GXバトルブースト」"],
    "sm4s": ["ポケモンカードゲームサン&ムーン 拡張パック「覚醒の勇者」"],
    "sm4a": ["ポケモンカードゲームサン&ムーン 拡張パック「超次元の暴獣」"],
    "sm3plus": ["ポケモンカードゲームサン&ムーン 強化拡張パック「ひかる伝説」"],
    "sm3n": ["ポケモンカードゲームサン&ムーン 拡張パック「闘う虹を見たか」"],
    "sm3h": ["ポケモンカードゲームサン&ムーン 拡張パック「光を喰らう闇」"],
    "smd": ["ポケモンカードゲーム サン＆ムーン 30枚デッキ対戦セット「サトシVSロケット団」"],
    "sm2plus": ["ポケモンカードゲームサン&ムーン 強化拡張パック「新たなる試練の向こう」"],
    "smc": ["ポケモンカードゲームサン&ムーン スターターセット改造「カプ・ブルルGX」"],
    "sm2l": ["ポケモンカードゲームサン&ムーン 拡張パック「アローラの月光」"],
    "sm2k": ["ポケモンカードゲームサン&ムーン 拡張パック「キミを待つ島々」"],
    "sm1plus": ["ポケモンカードゲームサン&ムーン 強化拡張パック「サン&ムーン」"],
    "sma": ["ポケモンカードゲームサン&ムーン 「スターターセット水 アシレーヌGX」","ポケモンカードゲームサン&ムーン 「スターターセット炎 ガオガエンGX」","ポケモンカードゲームサン&ムーン 「スターターセット草 ジュナイパーGX」"],
    "sm1m": ["ポケモンカードゲームサン&ムーン 拡張パック「コレクション ムーン」"],
    "sm1s": ["ポケモンカードゲームサン&ムーン 拡張パック「コレクション サン」"],
}

SeriesRadioBttnList = [
"ポケモンカードゲームソード&シールド プロモカード",	#0
"強化拡張パック「伝説の鼓動」",	#1
"Vスタートデッキ草　フシギバナ",	#2
"Vスタートデッキ炎　ガオガエン",	#3
"Vスタートデッキ水　ホエルオー",	#4
"Vスタートデッキ雷　ピカチュウ",	#5
"Vスタートデッキ超　ミュウ",	#6
"Vスタートデッキ闘　ルカリオ",	#7
"Vスタートデッキ悪　ガラルヤドラン",	#8
"Vスタートデッキ鋼　ジュラルドン",	#9
"Vスタートデッキ無色　イーブイ",	#10
"拡張パック「ムゲンゾーン」",	#11
"強化拡張パック「爆炎ウォーカー」",	#12
"スターターセットVMAX　リザードン",	#13
"スターターセットVMAX　オーロンゲ",	#14
"ザシアン＋ザマゼンタBOX",	#15
"拡張パック「反逆クラッシュ」",	#16
"強化拡張パック「VMAXライジング」",	#17
"ポケモンカードゲームソード&シールド 拡張パック「シールド」",	#18
"ポケモンカードゲームソード&シールド 拡張パック「ソード」",	#19
"ポケモンカードゲームソード&シールド スターターセットV　草",	#20
"ポケモンカードゲームソード&シールド スターターセットV　炎",	#21
"ポケモンカードゲームソード&シールド スターターセットV　水",	#22
"ポケモンカードゲームソード&シールド スターターセットV　雷",	#23
"ポケモンカードゲームソード&シールド スターターセットV　闘",	#24
"ポケモンカードゲームサン&ムーン ハイクラスパック「TAG TEAM GX タッグオールスターズ」",	#25
"ポケモンカードゲームサン&ムーン 拡張パック「オルタージェネシス」",	#26
"ポケモンカードゲームサン&ムーン 強化拡張パック「ドリームリーグ」",	#27
"ポケモンカードゲームサン&ムーン 強化拡張パック「リミックスバウト」",	#28
"ポケモンカードゲームサン&ムーン スターターセット TAG TEAM GX「ブラッキー&ダークライGX」",	#29
"ポケモンカードゲームサン&ムーン スターターセット TAG TEAM GX 「エーフィ&デオキシスGX」",	#30
"ポケモンカードゲームサン&ムーン 拡張パック「ミラクルツイン」",	#31
"ポケモンカードゲームサン&ムーン ムービースペシャルパック「名探偵ピカチュウ」",	#32
"ポケモンカードゲームサン&ムーン 強化拡張パック「スカイレジェンド」",	#33
"ポケモンカードゲームサン&ムーン 強化拡張パック「ジージーエンド」",	#34
"ポケモンカードゲームサン&ムーン 拡張パック「ダブルブレイズ」",	#35
"ポケモンカードゲームサン&ムーン 強化拡張パック「フルメタルウォール」",	#36
"ポケモンカードゲームサン&ムーン 強化拡張パック「ナイトユニゾン」",	#37
"トレーナーバトルデッキ：ニビシティジムのタケシ",	#38
"トレーナーバトルデッキ：ハナダシティジムのカスミ",	#39
"ポケモンカードゲームサン&ムーン 拡張パック「タッグボルト」",	#40
"ポケモンカードゲームサン&ムーン スターターセット「炎のブースターGX」",	#41
"ポケモンカードゲームサン&ムーン スターターセット「水のシャワーズGX」",	#42
"ポケモンカードゲームサン&ムーン スターターセット「雷のサンダースGX」",	#43
"ポケモンカードゲームサン&ムーン ハイクラスパック「GXウルトラシャイニー」",	#44
"ポケモンカードゲームサン&ムーン 強化拡張パック「ダークオーダー」",	#45
"ポケモンカードゲームサン&ムーン 拡張パック「超爆インパクト」",	#46
"ポケモンカードゲームサン&ムーン 強化拡張パック「フェアリーライズ」",	#47
"ポケモンカードゲームサン&ムーン 強化拡張パック「迅雷スパーク」",	#48
"ポケモンカードゲームサン&ムーン 拡張パック「裂空のカリスマ」",	#49
"ポケモンカードゲームサン&ムーン 強化拡張パック「チャンピオンロード」",	#50
"ポケモンカードゲームサン&ムーン 強化拡張パック「ドラゴンストーム」",	#51
"ポケモンカードゲームサン&ムーン 拡張パック「禁断の光」",	#52
"ポケモンカードゲームサン&ムーン 強化拡張パック「ウルトラフォース」",	#53
"ポケモンカードゲームサン&ムーン 拡張パック「ウルトラムーン」",	#54
"ポケモンカードゲームサン&ムーン 拡張パック「ウルトラサン」",	#55
"スターターセット伝説 ソルガレオGX ルナアーラGX",	#56
"ポケモンカードゲームサン&ムーン ハイクラスパック「GXバトルブースト」",	#57
"ポケモンカードゲームサン&ムーン 拡張パック「覚醒の勇者」",	#58
"ポケモンカードゲームサン&ムーン 拡張パック「超次元の暴獣」",	#59
"ポケモンカードゲームサン&ムーン 強化拡張パック「ひかる伝説」",	#60
"ポケモンカードゲームサン&ムーン 拡張パック「闘う虹を見たか」",	#61
"ポケモンカードゲームサン&ムーン 拡張パック「光を喰らう闇」",	#62
"ポケモンカードゲーム サン＆ムーン 30枚デッキ対戦セット「サトシVSロケット団」",	#63
"ポケモンカードゲームサン&ムーン 強化拡張パック「新たなる試練の向こう」",	#64
"ポケモンカードゲームサン&ムーン スターターセット改造「カプ・ブルルGX」",	#65
"ポケモンカードゲームサン&ムーン 拡張パック「アローラの月光」",	#66
"ポケモンカードゲームサン&ムーン 拡張パック「キミを待つ島々」",	#67
"ポケモンカードゲームサン&ムーン 強化拡張パック「サン&ムーン」",	#68
"ポケモンカードゲームサン&ムーン 「スターターセット水 アシレーヌGX」",	#69
"ポケモンカードゲームサン&ムーン 「スターターセット炎 ガオガエンGX」",	#70
"ポケモンカードゲームサン&ムーン 「スターターセット草 ジュナイパーGX」",	#71
"ポケモンカードゲームサン&ムーン 拡張パック「コレクション ムーン」",	#72
"ポケモンカードゲームサン&ムーン 拡張パック「コレクション サン」",	#73
"ポケモンカードゲームサン&ムーン プロモカード",	#74
]


#DB 접속정보를 dict type 으로 준비한다.
config={
        "user":"root",
        "password":"1234",
        "host":"127.0.0.1",   
        "database":"pokecard",
        "port":3306
    }

class DataBase ():
    def __init__(self, table_name):
        try:
            self.conn = mysql.connector.connect(**config)
            print(self.conn)
            self.cursor=self.conn.cursor()
            self.table = table_name
        except mysql.connector.Error as err:
            print(err)

    def SendQuery(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def ChangeTable(self, table_name):
        self.table = table_name

    def GetColumnList(self):
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='%s'"%self.table
        resultList=self.SendQuery(sql) # return : list [ tuple() ] 
        col_cnt = len(resultList)
        col_list = []  
        for i in range(col_cnt):
            col_list.append(resultList[i][0])
        return col_list

    def GetALLTable(self):
        sql = "SELECT * FROM `pokecard`.`%s` LIMIT 100000"%self.table
        resultList=self.SendQuery(sql)
        return resultList

    def SearcDB_UseColumnValue(self, col_name , search):
        sql = "SELECT * FROM `pokecard`.`%s` WHERE "%(self.table)
        if(isinstance(col_name, list)):
            col_len  = len(col_name)
            print("col_name list",col_name)
            print("searchlist",search)
            for i in range(col_len):
                sql += "`%s` LIKE \"%s\" AND "%(col_name[i] , search[i])
            sql = sql[:-4]
            print("[DB_SEARCH]",sql)
            res = self.SendQuery(sql)
            return res
            
        elif(isinstance(col_name, str)):
            sql += "`%s` LIKE \"%s\""%(col_name , search)
            print("[DB_SEARCH]",sql)
            return self.SendQuery(sql)
        else:
            return False


def GetCardType(num):
    typelist = ["ALL","POKEMON", "TRAINERS", "ENERGY"]
    return (typelist[num])


def GetOriginalName(kor_name):
    changeType = []
    if(" VMAX" in kor_name):
        kor_name=kor_name.replace(" VMAX" ,"")
        changeType.append(1)
    if(" EX" in kor_name):
        kor_name=kor_name.replace(" EX","")
        changeType.append(2)
    if(" GX" in kor_name):
        kor_name=kor_name.replace(" GX","")
        changeType.append(3)
    if("가라르 " in kor_name):
        kor_name=kor_name.replace("가라르 ","")
        changeType.append(4)
    if("M" in kor_name):
        kor_name=kor_name.replace("M","")
        changeType.append(5)
    if(" LV.X" in kor_name):
        kor_name=kor_name.replace(" LV.X","")
        changeType.append(6)
    if("[s]프리즘스타[/s]" in kor_name):
        kor_name=kor_name.replace("[s]프리즘스타[/s]" ,"◇")
        changeType.append(7)
    if(" V" in kor_name):
        kor_name=kor_name.replace(" V" ,"")
        changeType.append(8)
    if("[P]" in kor_name):
        kor_name=kor_name.replace("[P]" ,"")
        changeType.append(9)
    if("마그마단의" in kor_name):
        kor_name=kor_name.replace("마그마단의 " ,"")
        changeType.append(10)
    if(" 소울링크" in kor_name):
        kor_name=kor_name.replace(" 소울링크" ,"")
        changeType.append(11)
    if("아쿠아단의" in kor_name):
        kor_name=kor_name.replace("아쿠아단의 " ,"")
        changeType.append(12)
    if("알로라" in kor_name):
        kor_name=kor_name.replace("알로라" ,"")
        changeType.append(13)
    if("울트라" in kor_name):
        kor_name=kor_name.replace("울트라","")
        changeType.append(14)
    if("가라르" in kor_name):
        kor_name=kor_name.replace("가라르","")
        changeType.append(15)
    return kor_name, changeType

def AddMarkChangeType(name, changeType):

    for i in changeType:
        if(i == 1):
            name=name+"VMAX"
        elif(i == 2):
            name=name+"EX"
        elif(i == 3):
            name=name+"GX"
        elif(i == 4):
            name="ガラル "+name
        elif(i == 5):
            name="メガ"+name
        elif(i == 6):
            name = name + " LV.X"
        elif(i == 7):#프리즘스타
            pass
        elif(i == 8):
            name=name+"V"
        elif(i == 9):
            name=name
        elif(i == 10):
            name="マグマ団の"+name
        elif(i == 11):
            name= name +"ソウルリンク"
        elif(i == 12):
            name = "アクア団の"+name
        elif(i == 13):
            name = "アローラ"+name
        elif(i == 14):
            name = "ウルトラ"+name
        elif(i == 15):
            name = "ガラル"+name
    
    return name

def CardTypeKorToJP(kor_type):

    if(int(kor_type/10) == 1):
        jp_type = "POKEMON"
    elif(kor_type == 21):
        jp_type = "グッズ"
    elif(kor_type == 22):
        jp_type = "サポート"
    elif(kor_type == 23):
        jp_type = "スタジアム"
    elif(kor_type == 23):
        jp_type = "スタジアム"
    elif(int(kor_type/10) == 3):
        jp_type = "エネルギー"
    return jp_type


def GoodsNameConverter( name):

    changed = name
    
    if("ポケモンカードゲームサン&ムーン 拡張パック「コレクション サン」" in name): #Full Sentence Check Series
        changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「コレクション サン」","拡張パック「コレクション サン」")
    elif("ポケモンカードゲームサン&ムーン 拡張パック「コレクション ムーン」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「コレクション ムーン」","ポケモンカードゲーム サン&ムーン 拡張パック「コレクション ムーン」" )
    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「サン&ムーン」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「サン&ムーン」","強化拡張パック「サン＆ムーン」" )

    elif("ポケモンカードゲームサン&ムーン 拡張パック「アローラの月光」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「アローラの月光」","拡張パック「アローラの月光」" )
    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「新たなる試練の向こう」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「新たなる試練の向こう」","強化拡張パック「新たなる試練の向こう」")
    
    elif("ポケモンカードゲームサン&ムーン 拡張パック「光を喰らう闇」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「光を喰らう闇」","拡張パック「闘う虹を見たか」")
    elif("ポケモンカードゲームBW 拡張パック「リューズブラスト」" in name):
        changed = name.replace("ポケモンカードゲームBW 拡張パック「リューズブラスト」","ポケモンカードゲームBW　拡張パック「リューズブラスト」")
    
    elif("ポケモンカードゲームサン&ムーン 拡張パック「キミを待つ島々」" in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「キミを待つ島々」","拡張パック「キミを待つ島々」")

    elif("ポケモンカードゲームサン&ムーン 拡張パック「闘う虹を見たか」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「闘う虹を見たか」","拡張パック「光を喰らう闇」")

    elif( "ポケモンカードゲームサン&ムーン 強化拡張パック「ひかる伝説」"in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「ひかる伝説」", "強化拡張パック「ひかる伝説」")
    

    elif( "ポケモンカードゲームサン&ムーン 拡張パック「覚醒の勇者」"in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「覚醒の勇者」","拡張パック「覚醒の勇者」")

    elif( "ポケモンカードゲームサン&ムーン 拡張パック「超次元の暴獣」"in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「超次元の暴獣」","拡張パック「超次元の暴獣」")
    
    elif( "ポケモンカードゲームサン&ムーン ハイクラスパック「GXバトルブースト」"in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン ハイクラスパック「GXバトルブースト」","ハイクラスパック「GXバトルブースト」")

    elif("ポケモンカードゲームBW 「プラズマ団パワードデッキ」"  in name):
        changed = name.replace("ポケモンカードゲームBW 「プラズマ団パワードデッキ」" , "ポケモンカードゲームBW 「プラズマ団パワードデッキ30」")

    elif("ポケモンカードゲームXY 「ゼルネアス30」" in name):
        changed = name.replace("ポケモンカードゲームXY 「ゼルネアス30」","ポケモンカードゲームXY 「ゼルネアスデッキ30」")

    elif("ポケモンカードゲームXY メガバトルデッキ60「【M】リザードンEX」" in name):
        changed = name.replace("ポケモンカードゲームXY メガバトルデッキ60「【M】リザードンEX」","ポケモンカードゲームXY メガバトルデッキ60「リザードンEX」")
    
    elif("ポケモンカードゲームXY メガバトルデッキ60「【M】レックウザEX」" in name):
        changed = name.replace("ポケモンカードゲームXY メガバトルデッキ60「【M】レックウザEX」","ポケモンカードゲームXY メガバトルデッキ60「レックウザEX」")

    elif("スターターセット伝説 ソルガレオGX ルナアーラGX" in name):
        changed = name.replace("スターターセット伝説 ソルガレオGX ルナアーラGX","ポケモンカードゲーム サン＆ムーン スターターセット伝説「ソルガレオGX ルナアーラGX」")
    
    elif("ポケモンカードゲームサン&ムーン スターターセット改造「カプ・ブルルGX」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン スターターセット改造「カプ・ブルルGX」","ポケモンカードゲーム サン&ムーン「スターターセット改造「カプ・ブルルGX」」")
    
    elif("ポケモンカードゲーム サン＆ムーン スターターセット伝説「ソルガレオGX ルナアーラGX」" in name):
        changed = name.replace("ポケモンカードゲーム サン＆ムーン スターターセット伝説「ソルガレオGX ルナアーラGX」","ポケモンカードゲーム サン＆ムーン スターターセット伝説「ソルガレオGX ルナアーラGX」")
    
    elif("ポケモンカードゲームサン&ムーン 拡張パック「ウルトラサン」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「ウルトラサン」","拡張パック「ウルトラサン」")


    elif("ポケモンカードゲームサン&ムーン 拡張パック「ウルトラムーン」" in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「ウルトラムーン」","拡張パック「ウルトラムーン」")

    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「ウルトラフォース」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「ウルトラフォース」","強化拡張パック「ウルトラフォース」")
        
    elif("ポケモンカードゲーム ハイクラスパック「THE BEST OF XY」" in name):
        changed = name.replace("ポケモンカードゲーム ハイクラスパック「THE BEST OF XY」","ハイクラスパック「THE BEST OF XY」")

    elif("ポケモンカードゲームサン&ムーン 拡張パック「禁断の光」" in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「禁断の光」","拡張パック「禁断の光」")

    
    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「ドラゴンストーム」" in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「ドラゴンストーム」","強化拡張パック「ドラゴンストーム」")
    
    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「チャンピオンロード」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「チャンピオンロード」","強化拡張パック「チャンピオンロード」")

    elif("ポケモンカードゲームサン&ムーン 拡張パック「裂空のカリスマ」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「裂空のカリスマ」","拡張パック「裂空のカリスマ」")
    
    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「フェアリーライズ」" in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「フェアリーライズ」","強化拡張パック「フェアリーライズ」")

    elif( "ポケモンカードゲームサン&ムーン 拡張パック「超爆インパクト」"in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「超爆インパクト」","拡張パック「超爆インパクト」")

    elif( "ポケモンカードゲームサン&ムーン 強化拡張パック「迅雷スパーク」"in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「迅雷スパーク」","強化拡張パック「迅雷スパーク」")

    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「ダークオーダー」" in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「ダークオーダー」","強化拡張パック「ダークオーダー」")
       
    elif("ポケモンカードゲームサン&ムーン 拡張パック「タッグボルト」"  in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン 拡張パック「タッグボルト」" ,"拡張パック「タッグボルト」")

    elif( "ポケモンカードゲームサン&ムーン スターターセット「"  in name):
       changed = name.replace( "ポケモンカードゲームサン&ムーン スターターセット「" ,"スターターセット「")
       
    elif("ポケモンカードゲームサン&ムーン ハイクラスパック「GXウルトラシャイニー」" in name):
       changed = name.replace("ポケモンカードゲームサン&ムーン ハイクラスパック「GXウルトラシャイニー」","ハイクラスパック「GXウルトラシャイニー」")
    
    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「ナイトユニゾン」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「ナイトユニゾン」", "ポケモンカードゲーム サン&ムーン 強化拡張パック「ナイトユニゾン」")

    elif("ポケモンカードゲームサン&ムーン 強化拡張パック「フルメタルウォール」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン 強化拡張パック「フルメタルウォール」","強化拡張パック「フルメタルウォール」")

    elif("ポケモンカードゲームサン&ムーン スターターセット TAG TEAM GX「ブラッキー&ダークライGX」" in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン スターターセット TAG TEAM GX「ブラッキー&ダークライGX」","スターターセット TAG TEAM GX 「ブラッキー&ダークライGX」")
    
    elif("ポケモンカードゲームソード&シールド スターターセットV" in name):
        changed = name.replace("ポケモンカードゲームソード&シールド ", "")
    
    elif("ポケモンカードゲームサン&ムーン " in name):
        changed = name.replace("ポケモンカードゲームサン&ムーン ","")

    elif("ポケモンカードゲームソード&シールド 拡張パック" in name):
        changed = name.replace("ポケモンカードゲームソード&シールド 拡張パック","拡張パック")
    

    # elif("" in name):
    #     changed = name.replace("","スターターセットV　炎")
    

    # elif("ポケモンカードゲームソード&シールド " in name):
    #     changed = name.replace("ポケモンカードゲームソード&シールド ","")

    # elif( in name):
    #    changed = name.replace(,)

    # elif( in name):
    #    changed = name.replace(,)


    #elif( in name):
    #    changed = name.replace(,)

    # elif(u' ' in name):
    #     print("[MAIN] CHANGE SPACE TYPE!!")
    #     changed = name.replace(u' ',u'\u3000') 
    return changed

if __name__ == "__main__":
    DB = DataBase('cardinfo')
    col_list = DB.GetColumnList()
    ALL_Table = DB.GetALLTable()
    TotalRow=len(ALL_Table)

    idx_CardName = col_list.index("CardName")
    idx_Series   = col_list.index("GoodsName_image")
    idx_CardType = col_list.index("CardTypeNum")
    idx_CollNum  = col_list.index("CollectionNum")


    DB.ChangeTable('jpcardinfo')
    jpcolumnlist = DB.GetColumnList()
    df = DataFrame(columns = jpcolumnlist)
    Write=True

    debugNo = 9156
    Write = False
    for index in range(debugNo , debugNo+1):
    #for index in range(9242 , 9246):
        print("[MAIN] No.%d | Name: %s "%(index+1 ,ALL_Table[index][idx_CardName][1:-1]))
        if(ALL_Table[index][idx_CardName][1:-1]==""):
            print("[MAIN] Empty ROW")
            empty_df= DataFrame( [["Empty"]*len(jpcolumnlist)] ,columns=jpcolumnlist, index=[index])
            df = concat([df, empty_df])
            continue

        DB.ChangeTable('name') #Change to Name Table
        ChangeType = []
        tmp_name = ALL_Table[index][idx_CardName][1:-1].strip()

        if('\n['in tmp_name):
            print("[MAIN] KR DB Name Exception!! Before : (%s)"% tmp_name)
            tmp_name = tmp_name[ : tmp_name.find('\n[') ]
            print("[MAIN] KR DB Name Exception!! After : (%s)"%tmp_name)
            

        res = DB.SearcDB_UseColumnValue("KOR", tmp_name ) #Firstly, Original String Search from DB
        if(len(res)==0):
            OrgName, ChangeType = GetOriginalName(tmp_name)
            res = DB.SearcDB_UseColumnValue("KOR", OrgName ) #Get JP name
        name_concat = ""
        if(len(res)==0): 
            print("[MAIN] Exception NAME CASE")
            if("블렌드 에너지" in OrgName ):
                temp = OrgName.split('블렌드 에너지')[1].replace(' ','') #removeSpce
                temp = temp.replace('풀','{G}')
                temp = temp.replace('물','{W}')
                temp = temp.replace('불꽃','{R}')
                temp = temp.replace('초','{P}')
                temp = temp.replace('악','{D}')
                temp = temp.replace('번개','{L}')
                temp = temp.replace('격투','{F}')
                temp = temp.replace('강철','{M}')
                OrgName = '블렌드 에너지 '+temp
            elif("유닛 에너지" in OrgName):
                temp = OrgName.replace('[s]','')
                temp = temp.replace('[/s]','')
                temp = temp.replace('풀','{G}')
                temp = temp.replace('물','{W}')
                temp = temp.replace('불꽃','{R}')
                temp = temp.replace('초','{P}')
                temp = temp.replace('악','{D}')
                temp = temp.replace('번개','{L}')
                temp = temp.replace('격투','{F}')
                temp = temp.replace('강철','{M}')
                OrgName = temp
                
            elif("특수" in OrgName and "에너지" in OrgName):
                temp = OrgName.replace('악 ', '[악]')
                temp = temp.replace('강철 ', '[강철]')
                OrgName = temp
            elif("페어리참" in OrgName):
                temp = OrgName.replace('[s]',' ')
                temp = temp.replace('[/s]','')
                temp = temp.replace('초','{P}')
                temp = temp.replace('격투','{F}')
                temp = temp.replace('드래곤','{Y}')
                temp = temp.replace('풀','{G}')
                temp = temp.replace('울트라비스트','UB')
                temp = temp.replace('번개','{L}')
                OrgName = temp
                
            
            print("[MAIN CHANGED ORGNAME]",OrgName)

            
            if("&" in OrgName): # Name1 & Name2 Type
                for name in OrgName.split('&'):
                    res=DB.SearcDB_UseColumnValue("KOR", name) 
                    if(len(res)>0):
                        name_concat += (res[0][0]+"&")
                name_concat = name_concat[:-1]
                print("ORG NAME:",OrgName)
            else:
                res = DB.SearcDB_UseColumnValue("KOR", OrgName ) #Get JP name
                if(len(res)>0):
                    name_concat = res[0][0]
        else:
            name_concat = res[0][0]

        JPNameBeforeMark = name_concat   


        if(len(res)>0):
            JPName = AddMarkChangeType(JPNameBeforeMark , ChangeType)
            if('◇' in JPName):
                JPName=JPName.replace('◇','')
            if("フェアリーチャーム竜" in JPName):
                JPName = "フェアリーチャームドラゴン"
            if('２' in JPName):
                JPName = JPName.replace('２','2')
            if('Ｚ' in JPName):
                JPName = JPName.replace('Ｚ','Z')
            print("[MAIN] JP NAME: %s"%(JPName))
            cardtype    = GetCardType(int(ALL_Table[index][idx_CardType][1:2]))
            CardTypeJP  = CardTypeKorToJP(int(ALL_Table[index][idx_CardType][1:-1]))
            inputSeries = ALL_Table[index][idx_Series][1:-1]
            DB.ChangeTable('series')
            JPSeries = None
            KRSeries = None
            JPSeriesName = None
            isStandard = False
            res=DB.SearcDB_UseColumnValue("KRSeries", inputSeries)
            if(len(res)==0):
                print("[MAIN] SERIES FIND FAIL!!! (KOR_SERIES : %s)"%inputSeries)
                print("[MAIN] TRY TO FIND STANDARD SERIES!!")
                
                try:
                    temp = JPNameDic[inputSeries]
                except:
                    print("[MAIN] FIND FAIL FROM STANDARD DICTIONARY")
                    empty_df= DataFrame( [["Series"]*len(jpcolumnlist)] ,columns=jpcolumnlist, index=[index])
                    df = concat([df, empty_df])
                    continue
                
                if(isinstance(temp, list)):
                    print("[MAIN] GET STANDARD LIST ")
                    JPSeriesName=temp
                else:
                    print("[MAIN] MATCHED ONE PRODUCT")
                    JPSeriesName=[temp]

                KRSeries = inputSeries
                isStandard = True
            else:
                print("[MAIN] FIND JP SERIES FROM DB")
                JPSeriesName = []
                for i in range(len(res)):
                    JPSeriesName.append(res[i][3].strip())
                JPSeries     = res[0][1].strip()
                KRSeries     = res[0][2].strip()
            
            print("[MAIN] KOR_SERIES: %s -> JPN_SERIES: %s(%s)  "%(KRSeries,JPSeriesName,JPSeries))
            col = ["CardName"]
            txt = [JPName] 

            if(isStandard):
                if(CardTypeJP == "POKEMON"):
                    korCollectionNum = ALL_Table[index][idx_CollNum][1:-1]
                    if('/' in korCollectionNum):
                        col.append("CollectionNum")
                        if("SM-P" in korCollectionNum.split('/')[1]):
                            jpCollectionNum = '%'+korCollectionNum.split('/')[1]+'%'
                        else:
                            jpCollectionNum = korCollectionNum.split('/')[0] + " / " + korCollectionNum.split('/')[1]
                        txt.append(jpCollectionNum)
            else: #Non-Standard Case
                JPSeriesName = []
                for i in range(len(res)):
                    JPSeriesName.append(res[i][3].strip())
            
            DB.ChangeTable('jpcardinfo') #GoodsName more than two
            JPSeriesCnt = len(JPSeriesName)
            
            
            #ADD GOODS NAME
            if(KRSeries == 'promo'):
                print("[MAIN] PROMO EXCEPTION -> Don't Add GoodsName ")
            else:
                res_accumulation = []
                col.append("GoodsName") 
                for i in range(JPSeriesCnt):
                    if(i==0):
                        txt.append(JPSeriesName[i])
                    else:
                        txt[col.index("GoodsName")] = JPSeriesName[i]
                    get=DB.SearcDB_UseColumnValue(col, txt)
                    for index in range(len(get)):
                        res_accumulation.append(get[index])
                res=res_accumulation
            print("GET SUCCESS")
            
            if(len(res)==1):
            #print(DataFrame(res, columns=jpcolumnlist, index=[index]))
                df = concat([df,  DataFrame(res, columns=jpcolumnlist, index=[index]) ])
            else:
                #Poke mon Case Add Collection Number
                if(CardTypeJP == "POKEMON" and isStandard==False):
                    korCollectionNum = ALL_Table[index][idx_CollNum][1:-1]
                    if('/' in korCollectionNum):
                        col.append("CollectionNum")
                        jpCollectionNum = korCollectionNum.split('/')[0] + " / " + korCollectionNum.split('/')[1]
                        txt.append(jpCollectionNum)

                #NO 844~892
                if(len(res)==0): #Change Space Type GoodsName
                    for i in range(len(col)):
                        if(col[i] == "GoodsName"): 
                            txt[i] = GoodsNameConverter(txt[i])

                            
                    res=DB.SearcDB_UseColumnValue(col, txt)

                if(len(res)==1):
                    empty_df= DataFrame( res , columns = jpcolumnlist, index=[index])
                if(len(res)==0):
                    empty_df= DataFrame( [[str(len(res))]*len(jpcolumnlist)] ,columns = jpcolumnlist, index=[index])
                else:
                    empty_df= DataFrame( [res[0]] , columns = jpcolumnlist, index=[index])
                    #empty_df= DataFrame( [[str(len(res))]*len(jpcolumnlist)] ,columns = jpcolumnlist, index=[index])
                
                df = concat([df, empty_df])

            

        else:
            print("[MAIN] JP NAME FIND FAIL!!")
            empty_df= DataFrame( [["Name"]*len(jpcolumnlist)] ,columns = jpcolumnlist, index=[index])
            df = concat([df, empty_df])
        print("[MAIN] INDEX : %d"%index)


    print(df)
    if(Write):
        df.to_excel("Mapped-JP-List.xlsx")
