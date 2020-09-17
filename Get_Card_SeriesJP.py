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


class JPSeriesInfo():

    def __init__(self, hide=False):
        
        options = webdriver.ChromeOptions()
        #https://www.whatismybrowser.com/detect/what-is-my-user-agent 
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36")
        #chrome Headless Mode
        if (hide == True):
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")

        self.mainpage = "https://www.pokemon-card.com/card-search"
        self.driver = webdriver.Chrome('chromedriver', chrome_options=options)
        self.driver.get(self.mainpage)

    def GetSeriesInfo(self, pagenum):
        self.mainpage = "https://www.pokemon-card.com/card-search/index.php?mode=statuslist&pg="+str(pagenum)
        self.driver.get(self.mainpage)

        JPname=self.driver.find_element_by_xpath("//*[@id=\"CardSearchForm\"]/div/div[2]/div[1]/div/div/div[2]/ul/li/div").text.strip()
        
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = self.driver.current_window_handle
        self.driver.find_element_by_xpath("//*[@id=\"card-show-id0\"]/img").click()
        signin_window_handle = None
        while not signin_window_handle:
            for handle in self.driver.window_handles:
                if handle != main_window_handle:
                    signin_window_handle = handle
                    break

        self.driver.switch_to.window(signin_window_handle)
        #Page From SeriesCode
        JPSeries=self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[1]/img").get_attribute("alt")
        print(pagenum,",",JPname,",",JPSeries)
        self.driver.close()
        self.driver.switch_to.window(main_window_handle)

    def closeBrowser(self):
        self.driver.close()


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

class JP_WebSearch():
    def __init__(self, hide=False):
        
        self.mainpage = None
        self.driver = None
        self.CardType_DropDown = None
        self.SearchOptionSpan = None
        self.RequestURL = False
        self.RequestMsg = []
        self.IsStandard = None
        self.search_box = None
        self.progpercent = 0
        self.prev_pageNo = None
        self.cardname = None
        self.cardtype = None
        self.BrowserRunning = False
        self.cardlist = []
        self.currentType = None
        
        options = webdriver.ChromeOptions()
        #https://www.whatismybrowser.com/detect/what-is-my-user-agent 
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36")
        #chrome Headless Mode
        if (hide == True):
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")

        self.mainpage = "https://www.pokemon-card.com/card-search"
        self.IsStandard = True
        self.driver = webdriver.Chrome('chromedriver', chrome_options=options)
        self.driver.get(self.mainpage)
        self.driver.implicitly_wait(5)
        self.BrowserRunning = True
        self.LoadBttn() #For FirstLoad Case

    def SeriesNameCheck(self, inputSeries, pageNo):
        if (pageNo==0):
            try:
                JPNameDic[inputSeries]
                print("QThread : KeyOK-",inputSeries)
            except KeyError:
                print("QThread : KeyError-",inputSeries)
                self.UpdateProgress(100)    
                return False
        return True

    def Search(self, cardname ,cardtype, inputSeries, pageNo):
        self.cardlist = []
        
        self.dic ={
            "CardNum"       : [""],
            "CollectionNum" : [""],
            "CardName"      : [""],
            "PokeNum"       : [""],
            "MonType"       : [""],
            "DoxInfo"       : [""],
            "AbilityLabel1" : [""],
            "Ability1"      : [""],
            "AbilityLabel2" : [""],
            "Ability2"      : [""],
            "AbilityLabel3" : [""],
            "Ability3"      : [""],
            "AbilityLabel4" : [""],
            "Ability4"      : [""],
            "GoodsName"     : [""]
        }
        
        changed = False
        link = []
        if (self.SeriesNameCheck(inputSeries, pageNo) == False): #Standard Series Check
            return self.dic
                
        JPSeriesCount = 1 #NonStandard Loop-1time
        if(pageNo == 0): #Standard Case Get Series Count
            JPSeriesCount = len(JPNameDic[inputSeries])
            print("Current KR Series incldue %d JP Series "%JPSeriesCount)

        for JPindex in range(JPSeriesCount):
            print("JPIndex-%d"%JPindex)
            #Check URL Change Standard <-> NoneStandard
            if(self.IsStandard): #Current Standard
                if (pageNo==0): #Standard
                    print("Keep Current URL : Standard")
                    self.prev_pageNo = pageNo
                    self.LoadBttn() #For FirstLoad Case
                    changed = False
                else:
                    print("Change URL : Standard->%s"%pageNo)
                    self.mainpage = "https://www.pokemon-card.com/card-search/index.php?mode=statuslist&pg="+pageNo
                    self.prev_pageNo = pageNo
                    self.driver.get(self.mainpage)
                    self.driver.implicitly_wait(5)
                    self.IsStandard = False
                    self.LoadBttn()
                    changed = True
            else: #Current NoneStandard
                if (pageNo==0): #Standard
                    print("Change URL : %s -> Standard"%self.prev_pageNo)
                    self.mainpage = "https://www.pokemon-card.com/card-search"
                    self.prev_pageNo = 0 ##IMPORTANT
                    self.driver.get(self.mainpage)
                    self.driver.implicitly_wait(5)
                    self.IsStandard = True
                    self.LoadBttn()
                    changed = True

                elif(self.prev_pageNo != pageNo):
                    print("Change URL : %s -> %s"%(self.prev_pageNo, pageNo))
                    self.prev_pageNo = pageNo ##IMPORTANT!!! 
                    self.mainpage = "https://www.pokemon-card.com/card-search/index.php?mode=statuslist&pg="+pageNo
                    self.driver.get(self.mainpage)
                    self.driver.implicitly_wait(5)
                    self.IsStandard = False
                    self.LoadBttn()
                    changed = True

            self.searchBoxWrite("\b\b\b\b\b\b\b\b\b\b\b\b\b")

            if((self.currentType != cardtype) or changed):
                self.SelectCardType(cardtype)
                self.SearchOptionSpan.click()
                print("QThread OptionSpan CLICK!!")
                while True:
                    if(self.SearchOptionSpan.find_element_by_tag_name("div").get_attribute("class") == "AddFilterButton js-active" ):
                        print("QThread OptionSpan OK: ",self.SearchOptionSpan.find_element_by_tag_name("div").get_attribute("class"))    
                        break
                    else:
                        self.msleep(100)
                        print("QThread OptionSpan CHECK!!: ",self.SearchOptionSpan.find_element_by_tag_name("div").get_attribute("class"))
                print("QThread OptionSpan OK!!")    
                self.driver.implicitly_wait(5)
                self.currentType = cardtype    
            
            if self.IsStandard:
                self.StandardSeriesSlect(inputSeries, cardtype, JPindex)
            self.searchBoxWrite(cardname)
            
            #link += self.getCardLink()
            count = int(self.GetTotalCount())
            if(count == 0):
                return self.dic
            elif(count >= 1): #Change To ==1
                print("FOUND CARD!!!")
                self.SearchOptionSpan.click()

                main_window_handle = None
                while not main_window_handle:
                    main_window_handle = self.driver.current_window_handle
                self.driver.find_element_by_xpath("//*[@id=\"card-show-id0\"]/img").click()
                signin_window_handle = None
                while not signin_window_handle:
                    for handle in self.driver.window_handles:
                        if handle != main_window_handle:
                            signin_window_handle = handle
                            break
                self.driver.switch_to.window(signin_window_handle)
                #Page From SeriesCode
                
                
                CardNum       = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/img").get_attribute("src")[61:]
                CollectionNum = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[1]").text
                CardName      = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/h1").text
                
                tmp           = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[2]/h4").text.split('\u3000')
                try:
                    PokeNum = tmp[0][3:]
                    MonType = tmp[1]
                    DoxInfo = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[2]/p[2]").text
                except IndexError: #EX Case
                    MonType = ""
                    DoxInfo = ""
                    PokeNum = ""

                #SkillName
                AbilityLabel = self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h4")#.text.split('\n')[0]
                #Skill Explanation
                Ability  = self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/p")#.text
                GoodsName = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[2]/div/ul/li/a").text
                JPSeries=self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[1]/img").get_attribute("alt")
                
                print("TEST", len(AbilityLabel)  , len(Ability))

                if(len(AbilityLabel) != len(Ability)): #GX EX Rule Exsist
                    AbilityLabel.append(self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h2["+str(len(AbilityLabel))+"]"))
                
                self.dic ={
                    "CardNum"       : [CardNum],
                    "CollectionNum" : [CollectionNum],
                    "CardName"      : [CardName],
                    "PokeNum"       : [PokeNum],
                    "MonType"       : [MonType],
                    "DoxInfo"       : [DoxInfo],
                    "AbilityLabel1" : [""],
                    "Ability1"      : [""],
                    "AbilityLabel2" : [""],
                    "Ability2"      : [""],
                    "AbilityLabel3" : [""],
                    "Ability3"      : [""],
                    "AbilityLabel4" : [""],
                    "Ability4"      : [""],
                    "GoodsName"     : [GoodsName]
                }
                Ability_length = len(Ability)
                for i in range(Ability_length):
                    self.dic["AbilityLabel%d"%(i+1)] = [ AbilityLabel[i].text.split('\n')[0].strip() ]
                    self.dic["Ability%d"%(i+1)]      = [ Ability[i].text.strip() ]
                    if(i==2 and ("ワザ" in AbilityLabel[i].text)):
                        print("2-Rules Case")
                        tmp = [self.dic["AbilityLabel2"], self.dic["Ability2"]]
                        self.dic["AbilityLabel2"] = ["特別なルール"]
                        self.dic["Ability2"]      = [ self.dic["Ability3"][0].split('\n')[0].strip() ]
                        self.dic["AbilityLabel4"] = ["特別なルール"]
                        self.dic["Ability4"]      = [ self.dic["Ability3"][0].split('\n')[1].strip() ]
                        self.dic["AbilityLabel3"] = tmp[0]
                        self.dic["Ability3"]      = tmp[1]
                        Ability_length = 4
               
                
                print("CardNum :", CardNum)
                print("CollectionNum :", CollectionNum)
                print("CardName:", CardName)
                print("MonType :", MonType)
                print("DoxInfo:", DoxInfo)
                for i in range(Ability_length):
                    print("AbilityLabel%d :"%(i+1), self.dic["AbilityLabel%d"%(i+1)])
                    print("Ability%d :"%(i+1),  self.dic["Ability%d"%(i+1)])
                print("GoodsName:", GoodsName)
 

                self.driver.close()
                self.driver.switch_to.window(main_window_handle)
                self.SearchOptionSpan.click() 

                return self.dic


    def TrainersCheck(self, txt):
        if("グッズ" in txt):
            return "グッズ"
        elif("サポート" in txt):
            return "サポート"
        elif("エネルギー" in txt):
            return "エネルギー"
        elif("スタジアム" in txt):
            return "スタジアム"
        elif("ポケモンのどうぐ" in txt):
            return "ポケモンのどうぐ"
        elif("トレーナー" in txt):
            return "トレーナー"
        else:
            return "POKEMON"


    def InitDic(self):
        self.dic ={
            "PageNo"        : [""],
            "CardNum"       : [""],
            "CollectionNum" : [""],
            "CardType"      : [""],
            "CardName"      : [""],
            "PokeNum"       : [""],
            "MonType"       : [""],
            "DoxInfo"       : [""],
            "AbilityLabel1" : [""],
            "Ability1"      : [""],
            "AbilityLabel2" : [""],
            "Ability2"      : [""],
            "AbilityLabel3" : [""],
            "Ability3"      : [""],
            "AbilityLabel4" : [""],
            "Ability4"      : [""],
            "GoodsName"     : [""]
        }

    def Search2(self, pageNo):
        #self.cardlist = []
        
        # 1) 
        # /html/body/div/div[1]/section[1]/h1 -> Text확인 (카드이름)  - 검색창뜨는경우 Exception처리
        # 트레이너스/에너지
        # /html/body/div/div[1]/section[1]/div/div[2]/div/h2  -> Text  (グッズ / サポート/エネルギー /スタジアム / ポケモンのどうぐ)
        # /html/body/div/div[1]/section[1]/div/div[2]/div/p[1] -> Text가져오기 
        # 실패시
        # 기본 풀/물/불/전기 에너지등 /html/body/div/div[1]/section[1]/div/div[1]/div[1] 에서 Text가져오기 GRA/WAT 등
        # 포켓몬
        # -> 기존대로 데이터 가져오기

        self.mainpage = "https://www.pokemon-card.com/card-search/details.php/card/"+str(pageNo)+"/regu/all"

        #https://www.pokemon-card.com/card-search/details.php/card/1/regu/all
        
        start = time.time()  # 시작 시간 저장
        self.driver.get(self.mainpage)
        self.InitDic()
        self.dic["PageNo"] = [ pageNo]
        self.driver.implicitly_wait(5)
        try:
            self.driver.find_elements_by_xpath("/html/head")
            print("[SEARCH] PAGE Load OK!! %d "%pageNo)
        except:
            print("[SEARCH] PAGE Load FAIL!! %d "%pageNo)
            return False

        
        self.driver.implicitly_wait(0.3) #Make Faster PageNo SKip
        try:
            CardName = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/h1").text.strip()
            #print("[SEARCH] TIME : ", (time.time()-start),"PageNo :", pageNo)
        except:
            print("[SEARCH] CardName GET FAIL!!")
            #print("[SEARCH] TIME : ", (time.time()-start),"PageNo :", pageNo)
            return False
        
        self.dic["CardName"] = [CardName]

        #GOODS INFO GET
        GoodsEle = self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[2]/div/ul/li/a")
        GoodsName = ""               
        if(len(GoodsEle) == 0):                             
            GoodsEle = self.driver.find_elements_by_xpath("/html/body/div[1]/section/div/ul/li[1]/a") #36020프테라 Case 대응 상품명 Xpath변경됨
        if(len(GoodsEle) == 0): #37197 Promo Eve 상품명 없음 대응    
            GoodsEle=self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[2]/div/ul")
            if(GoodsEle):
                GoodsEle = self.driver.find_elements_by_class_name("a")
                if(GoodsEle == []):
                    print("[SEARCH] Can't Find Goods Name at Final Condition Check!!!")
                    GoodsName = "N/A"    
        if(GoodsName != "N/A"):
            GoodsName = GoodsEle[0].text  
        self.dic["GoodsName"] = [GoodsName]
        #CARD NUMBER (FOR IMAGE LOAD)
        self.driver.implicitly_wait(5) #TO PREVENT READ ERROR
        CardNum       = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/img").get_attribute("src")[61:]
        self.dic["CardNum"] = [CardNum]
        CollectionNum = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[1]").text
        self.dic["CollectionNum"] = [CollectionNum]

        try:
            self.driver.implicitly_wait(0.5)
            others_ability_label = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h2").text.strip()
            self.dic["AbilityLabel1"] = others_ability_label
            
            others_ability = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/p").text.strip()    
            print("[SEARCH] Others Ability Label ", others_ability_label)
            self.dic["Ability1"] = others_ability
        except:
            print("[SEARCH] Ability Explanation Get FAIL!!!")
            if("エネルギー" in others_ability_label):
                self.dic["CardType"] = ["エネルギー"]
                print("[SEARCH] Default Energy!!")
                return self.dic
            else:
                raise "[SEARCH] Others Ability Get Fail -> Not Default Enegy %d"%pageNo 
                
        self.driver.implicitly_wait(5)
        print("[SEARCH] TYPE CHECK!!")
        Type = self.TrainersCheck(others_ability_label)
        self.dic["CardType"] = [Type]
        print("[SEARCH]", others_ability_label, "-> TYPE:", Type)
        if(Type != "POKEMON"):
            self.driver.implicitly_wait(1)
            EleAbility=self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/p")
            EleAbLabel=self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h2")
            EleAbSkillLabel=self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h4")
            self.driver.implicitly_wait(5)
            print("[SEARCH] A-Label:", len(EleAbLabel),"Ability:",len(EleAbility), "SkillLabel", len(EleAbSkillLabel))
            
            del_list = []
            isAceSpec = False
            if(len(EleAbility)==5): #ACE SPEC
                isAceSpec = True
                for i in range(len(EleAbility)):
                    txt = EleAbility[i].text.strip()
                    if("グッズは、自分の番に何枚でも使える" in txt):
                        del_list.append(i)

            for i in del_list:
                del EleAbility[i]           

            if(len(EleAbility)>1):
                for i in range(len(EleAbility)):
                    self.dic["Ability%d"%(i+1)] = EleAbility[i].text.strip()
                
                if(len(EleAbLabel)>1):
                    cnt = 0
                    space = 0
                    for i in range(len(EleAbLabel)):
                        txt = EleAbLabel[i].text.strip()
                        if("ワザ" in txt):
                            if(isAceSpec):
                                space = 1
                            self.dic["AbilityLabel%d"%(i+space+1)] = EleAbSkillLabel[cnt].text.strip()
                            cnt +=1
                        else:
                            self.dic["AbilityLabel%d"%(i+space+1)] = txt
            
            # Already Done update Ability Info / At check condition of default Energy 
            # self.dic["Ability1"] = [others_ability]
            # self.dic["AbilityLabel1"] = [others_ability_label]
            print("[SEARCH] TIME : ", (time.time()-start),"PageNo :", pageNo)
            return self.dic
            
        else:
            self.driver.implicitly_wait(5) #TO PREVENT READ ERROR
            #CardNum       = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/img").get_attribute("src")[61:]
            #CollectionNum = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[1]").text
            #CardName      = self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/h1").text
            
            try:
                tmp = []
                self.driver.implicitly_wait(1)
                tmpElem = self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[2]/h4")
                if(len(tmpElem) > 0):
                    tmp = tmpElem[0].text.split('\u3000')
                PokeNum = tmp[0][3:]
                MonType = tmp[1]
                DoxInfo = self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[2]/p[2]")
            except IndexError: # PokeNum, Montype, DoxInfo Get Fail
                MonType = ""
                PokeNum = ""
                DoxInfo = []
            if(len(DoxInfo) > 0):
                DoxInfo = DoxInfo[0].text
            else:
                print("[SEARCH] Get Dox Info Fail")
                DoxInfo = ""

            #SkillName
            self.driver.implicitly_wait(5)
            AbilityLabel = self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h4")#.text.split('\n')[0]
                                                               #/html/body/div/div[1]/section[1]/div/div[2]/div/h4[1]
            #Skill Explanation
            Ability  = self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/p")#.text

        
            
                                                         
            JPSeries=self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[1]/div[1]/img").get_attribute("alt")
            
            
                                                                       
            self.dic ={
                "PageNo"        : [pageNo],
                "CardNum"       : [CardNum],
                "CollectionNum" : [CollectionNum],
                "CardType"      : [Type],
                "CardName"      : [CardName],
                "PokeNum"       : [PokeNum],
                "MonType"       : [MonType],
                "DoxInfo"       : [DoxInfo],
                "AbilityLabel1" : [""],
                "Ability1"      : [""],
                "AbilityLabel2" : [""],
                "Ability2"      : [""],
                "AbilityLabel3" : [""],
                "Ability3"      : [""],
                "AbilityLabel4" : [""],
                "Ability4"      : [""],
                "GoodsName"     : [GoodsName]
            }

            print("AbilityCountCheck", len(AbilityLabel)  , len(Ability))

            if(len(AbilityLabel) < len(Ability)): #EX Rule Exsist #35794 가이오가 확인
                h2_list = self.driver.find_elements_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h2")
                print("H2 first : ", h2_list[0].text)
                if("ワザ"in h2_list[0].text ): #31821 지가르데 Case 
                    AbilityLabel.append(self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h2["+str(len(h2_list))+"]"))
                else:
                    AbilityLabel.append(self.driver.find_element_by_xpath("/html/body/div/div[1]/section[1]/div/div[2]/div/h2["+str(len(AbilityLabel))+"]"))
                                                                       
            Ability_length = len(AbilityLabel)
            
            # print("[SEARCH] BEFORE DICTIONARY")
            # for i in range(Ability_length):
            #     print("AbilityLabel%d :"%(i+1), AbilityLabel[i].text)
            #     print("Ability%d :"%(i+1),  Ability[i].text)
            
            for i in range(Ability_length):
                self.dic["AbilityLabel%d"%(i+1)] = [ AbilityLabel[i].text.split('\n')[0].strip() ] #'みずのはどう\n30' -> Remove Damage
                self.dic["Ability%d"%(i+1)]      = [ Ability[i].text.strip() ]
                if(i==2 and ("ワザ" in AbilityLabel[i].text)): #31241 원시가이오가 확인
                    print("[SEARCH] Found! ワザ Ability 3 / Need Check Rules Count" )
                    RuleCount=len(self.dic["Ability3"][0].split('\n'))
                    print("[SEARCH] Rule Count:", RuleCount)
                    if(RuleCount == 2):
                        print("2-Rules Case")
                        tmp = [self.dic["AbilityLabel2"], self.dic["Ability2"]]
                        self.dic["AbilityLabel2"] = ["特別なルール"]
                        self.dic["Ability2"]      = [self.dic["Ability3"][0].split('\n')[0].strip()]
                        self.dic["AbilityLabel4"] = ["特別なルール"]
                        self.dic["Ability4"]      = [self.dic["Ability3"][0].split('\n')[1].strip()]
                        self.dic["AbilityLabel3"] = tmp[0]
                        self.dic["Ability3"]      = tmp[1]
                        Ability_length = 4 #For Print
                        break
                    else:
                        print("1-Rules Case")
                        self.dic["AbilityLabel3"] = ["特別なルール"]
                    
            
            print("CardNum :", CardNum)
            print("CollectionNum :", CollectionNum)
            print("CardName:", CardName)
            print("MonType :", MonType)
            print("DoxInfo:", DoxInfo)
            for i in range(Ability_length):
                print("AbilityLabel%d :"%(i+1), self.dic["AbilityLabel%d"%(i+1)])
                print("Ability%d :"%(i+1),  self.dic["Ability%d"%(i+1)])
            print("GoodsName:", GoodsName)
            print("[SEARCH] TIME : ", (time.time()-start),"PageNo :", pageNo)
            return self.dic

        

    def StandardSeriesSlect(self, inputSeries, cardtype , JPindex):

        while True:
            try:
                if(cardtype == "POKEMON"):
                    self.SeriesOptionSpan = self.driver.find_element_by_xpath("//*[@id=\"CardSearchForm\"]/div/div[3]/div/div/div[4]/div[2]/div[2]")
                elif(cardtype == "TRAINERS" or cardtype == "ENERGY"):
                    self.SeriesOptionSpan = self.driver.find_element_by_xpath("//*[@id=\"CardSearchForm\"]/div/div[3]/div/div/div[2]/div[2]/div[2]")
                self.SeriesOptionSpan.click()
                break
            except:
                print("QThread Series OptionSpan click fail > Restart!! get element")
        while True:
            if(self.SeriesOptionSpan.get_attribute("class")=="groupSubList groupSubList-toggle js-open"):
                print("QThread SeriesSpan OK:", self.SeriesOptionSpan.get_attribute("class"))
                break
        self.driver.implicitly_wait(5)
        print(inputSeries,":",self.findSeriesXpath(inputSeries, cardtype, JPindex))
        SeriesRadioBttn = self.driver.find_element_by_xpath( self.findSeriesXpath(inputSeries, cardtype , JPindex) )
        print("QThread RadioButton Find!!:", SeriesRadioBttn.find_element_by_class_name("KSFormText").text)
        SeriesRadioBttn.click()
        self.driver.implicitly_wait(5)

    def LoadBttn(self):
        self.search_box = self.driver.find_element_by_xpath("/html/body/div/div[1]/div/form/div/div[1]/div/div/div[2]/label/input")
        self.CardType_DropDown = self.driver.find_element_by_xpath("//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label")
        self.SearchOptionSpan = self.driver.find_element_by_xpath("//*[@id=\"AddFilterArea\"]")
        
        print("LoadBttn : ", self.SearchOptionSpan.find_element_by_tag_name("div").get_attribute("class"))


    def SelectCardType(self, CardType): #DropDown And Select CardType
        self.CardType_DropDown.click()
        self.driver.implicitly_wait(5)
        PokeSelect = self.driver.find_element_by_xpath(self.findCardTypeXpath(CardType))
        self.driver.implicitly_wait(5)
        ActionChains(self.driver).move_to_element(PokeSelect).click(PokeSelect).perform()
        self.driver.implicitly_wait(5)

    def GetTotalCount(self):
        CountElemnet = self.driver.find_element_by_xpath("//*[@id=\"AllCountNum\"]")
        Count = self.WaitText(CountElemnet)
        print("Total :", Count)
        return int(Count)

    def searchBoxWrite(self, string):
        for i in string:
            self.search_box.send_keys(i)

    def prntCardList(self):
        self.cardlist
        for card in self.cardlist:
            print(card["src"])

    def getCardList(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")
        self.cardlist = soup.find("section", {'class':'Section'}).findAll('img')
        return self.cardlist

    def WaitText(self,txt_element):
        old_txt = "OLD"
        new_txt = "NEW"
        cnt = 0
        while (old_txt != new_txt):
            old_txt = new_txt
            QtTest.QTest.qWait(500)
            new_txt = txt_element.text    
            print("NEW:%s, OLD:%s"%(new_txt, old_txt))
            cnt+=1
        return new_txt

    def findSeriesXpath(self,SeriesString, cardtype, JPindex):
        SearchStr = JPNameDic[SeriesString][JPindex]
        print("Series:",SeriesString ,"/SearchStr:", SearchStr)
        index=SeriesRadioBttnList.index(SearchStr)
        if(cardtype == "POKEMON"):
            return "//*[@id=\"CardSearchForm\"]/div/div[3]/div/div/div[4]/div[2]/div[2]/div[2]/div/ul/li["+str(index+2)+"]/label"
        elif(cardtype == "TRAINERS" or cardtype == "ENERGY"): 
            return "//*[@id=\"CardSearchForm\"]/div/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div/ul/li["+str(index+2)+"]/label"
        return 0

    def findCardTypeXpath(self,cardtype):
        if(cardtype == "ALL"):
            return "//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label/div/ul/li[1]"
        elif(cardtype == "POKEMON"):
            return "//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label/div/ul/li[2]"
        elif(cardtype == "TRAINERS"): 
            return "//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label/div/ul/li[3]"
        elif(cardtype == "ENERGY"): 
            return  "//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label/div/ul/li[4]"

    def getCardLink(self):
        count = int(self.GetTotalCount())
        cardlist= self.getCardList()
        urllist = []
        if(count == 0):
            return urllist
        else: # Over Links
            for i in range(len(cardlist)):
                urllist.append("https://www.pokemon-card.com"+cardlist[i]["src"])
                #print (urllist[i])
            return urllist


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
    kor_name=kor_name.replace(" VMAX" ,"")
    kor_name=kor_name.replace(" EX","")
    kor_name=kor_name.replace(" GX","")
    kor_name=kor_name.replace("가라르","ガラル")
    kor_name=kor_name.replace("M","")
    kor_name=kor_name.replace(" LV.X","")
    kor_name=kor_name.replace("[s]프리즘스타[/s]" ,"◇")
    kor_name=kor_name.replace(" V" ,"")
    kor_name=kor_name.replace("[P]" ,"")
    return kor_name

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


if __name__ == "__main__":
    DB = DataBase('cardinfo')
    col_list = DB.GetColumnList()
    ALL_Table = DB.GetALLTable()
    TotalRow=len(ALL_Table)

    idx_CardName = col_list.index("CardName")
    idx_Series   = col_list.index("GoodsName_image")
    idx_CardType = col_list.index("CardTypeNum")
    idx_CollNum  = col_list.index("CollectionNum")
    
    #print(ALL_Table[9242])

    for index in range(9256 , 9258):
        print("[MAIN] No.%d | Name: %s "%(index+1 ,ALL_Table[index][idx_CardName][1:-1]))
        DB.ChangeTable('name') #Change to Name Table
        OrgName = GetOriginalName(ALL_Table[index][idx_CardName][1:-1])
        res = DB.SearcDB_UseColumnValue("KOR", OrgName ) #Get JP name

        if(len(res)>0):
            JPName = res[0][0]
            print("[MAIN] JP NAME: %s"%(JPName))
            cardtype    = GetCardType(int(ALL_Table[index][idx_CardType][1:2]))
            CardTypeJP  = CardTypeKorToJP(int(ALL_Table[index][idx_CardType][1:-1]))
            inputSeries = ALL_Table[index][idx_Series][1:-1]
            DB.ChangeTable('series')
            JPSeries = None
            KRSeries = None
            JPSeriesName = None
            res=DB.SearcDB_UseColumnValue("KRSeries", inputSeries)
            if(len(res)>0):
                JPSeries     = res[0][1].strip()
                KRSeries     = res[0][2].strip()
                JPSeriesName = res[0][3].strip()
                print("[MAIN] KOR_SERIES: %s -> JPN_SERIES: %s(%s)  "%(KRSeries,JPSeriesName,JPSeries))
                
                col = ["CardName"]
                txt = [JPName] 
                
                if(JPSeriesName == "スタンダード"): #Standard Case
                    JPSeriesName = JPNameDic[KRSeries]
                    if(CardTypeJP == "POKEMON"):
                        col.append("CollectionNum")
                        korCollectionNum = ALL_Table[index][idx_CollNum][1:-1]
                        jpCollectionNum = korCollectionNum.split('/')[0] + " / " + korCollectionNum.split('/')[1]
                        txt.append(jpCollectionNum)
                    
                else: #Non-Standard Case
                    JPSeriesName = [res[0][3].strip()]
                DB.ChangeTable('jpcardinfo')
                               
                for i in range(len(JPSeriesName)):
                    col.append("GoodsName") 
                    txt.append(JPSeriesName[i])
                    
                res=DB.SearcDB_UseColumnValue(col, txt)
                print("GET SUCCESS")
                print(res)

            else:
                
                print("[MAIN] SERIES FIND FAIL!!! (KOR_SERIES : %s)"%inputSeries)

        else:
            print("[MAIN] JP NAME FIND FAIL!!")
            df = concat([df, empty_df])

    #JP_NAME = None
    #jp = JP_WebSearch(hide=True)   
    
    # SEARCH1
    # for index in range(507 , 508):
    #     print("[MAIN] No.%d | Name: %s "%(index+1 ,ALL_Table[index][idx_CardName][1:-1]))
    #     DB.ChangeTable('name')
    #     res = DB.SearcDB_UseColumnValue("KOR", GetOriginalName(ALL_Table[index][idx_CardName][1:-1]))
    #     if(len(res)>0):
    #         cardname = res[0][0]
    #         print("[MAIN] JP NAME: %s"%(cardname))
    #         cardtype    = GetCardType(int(ALL_Table[index][idx_CardType][1:2]))
    #         inputSeries = ALL_Table[index][idx_Series][1:-1]

    #         DB.ChangeTable('series')
    #         res=DB.SearcDB_UseColumnValue("KRSeries", inputSeries)
    #         pageNo = 0
    #         if(len(res)>0):
    #             print("[MAIN]] MAIN PAGE NO: %s, JPN_SERIES: %s, KOR_SERIES: %s "%(res[0][0],res[0][1],res[0][2]))
    #             pageNo = res[0][0]
    #             df = concat([df, DataFrame(jp.Search(cardname , cardtype, inputSeries, pageNo))])
    #         else:
    #             print("[MAIN] SERIES FIND FAIL!!! (KOR_SERIES : %s)"%inputSeries)
    #             df = concat([df, empty_df])
    #     else:
    #         print("[MAIN] JP NAME FIND FAIL!!")
    #         df = concat([df, empty_df])
    #print(df)

    #SEARCH2
    # jp = JP_WebSearch(hide=True)

    # columns = ["PageNo","CardNum","CollectionNum" ,"CardType","CardName","PokeNum","MonType","DoxInfo","AbilityLabel1" ,"Ability1","AbilityLabel2" ,"Ability2","AbilityLabel3" ,"Ability3","AbilityLabel4" ,"Ability4","GoodsName"]
    # df = DataFrame(columns = columns)

    #DEBUG
    #DataFrame(jp.Search2(31241)).to_excel("debug.xlsx") #원시가이오가eX
    #DataFrame(jp.Search2(35794)).to_excel("debug2.xlsx") #가이오가ex
    #DataFrame(jp.Search2(4010)).to_excel("debug2.xlsx") #부스타
    #DataFrame(jp.Search2(4086)).to_excel("debug2.xlsx") #트레이너카드
    #DataFrame(jp.Search2(8003)).to_excel("debug2.xlsx") #포켓바디, 마자
    #DataFrame(jp.Search2(38409)).to_excel("debug2.xlsx") #특성, 독침붕
    #DataFrame(jp.Search2(28417)).to_excel("debug2.xlsx") #기라티나 
    #DataFrame(jp.Search2(31821)).to_excel("debug2.xlsx")#31821 지가르데
    #DataFrame(jp.Search2(37197)).to_excel("debug2.xlsx")# #36020
    #DataFrame(jp.Search2(28745)).to_excel("debug2.xlsx")# ACE SPEC BW

    #GET TRAINERS & ENERGY INFO AGAIN
    #card_list = []
    # cnt = 0
    # file_cnt = 1
    # df = DataFrame(columns = columns)
    # for index in card_list:
    #     res = jp.Search2(index)
    #     if(res != False):
    #         df = concat([df,DataFrame(res)])
    #     cnt +=1
    #     if(cnt == 200):
    #         df.to_excel("trainers%d.xlsx"%file_cnt)
    #         file_cnt +=1
    #         cnt = 0
    #         df = DataFrame(columns = columns)
    # df.to_excel("trainers_last.xlsx")
    
    
    # GET Series NO
    # for seriesNo in range (270, 280):
    #     df = DataFrame(columns = columns)
    #     No = seriesNo*100
    #     start = No
    #     FailCount = 0
    #     res = True
    #     while True:
    #         res = jp.Search2(No)
    #         if(res != False):
    #             df = concat([df,DataFrame(res)])
    #         else:
    #             FailCount+=1
    #             print("FailCount : ",FailCount)
    #         if( (FailCount > 10) or (No-start >= 99) ):
    #             print("FailCount :", FailCount, "Write Excel!!: ")
    #             df.to_excel("%d-%s-%s.xlsx"%(seriesNo,start,No))
    #             break
    #         No+=1  
    #print(df)
    
