from bs4 import BeautifulSoup
import selenium 
from selenium import webdriver
#from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
import time

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal, pyqtSlot

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
    "sm9": ["ポケモンカードゲームサン&ムーン 拡張パック「タッグボルト」", "ポケモンカードゲームサン&ムーン 強化拡張パック「ダークオーダー」"],
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
"ポケモンカードゲームソード&シールド プロモカード", #0
"強化拡張パック「伝説の鼓動」", #1
"Vスタートデッキ草　フシギバナ", #2
"Vスタートデッキ炎　ガオガエン", #3
"Vスタートデッキ水　ホエルオー", #4
"Vスタートデッキ雷　ピカチュウ", #5
"Vスタートデッキ超　ミュウ", #6
"Vスタートデッキ闘　ルカリオ", #7
"Vスタートデッキ悪　ガラルヤドラン", #8
"Vスタートデッキ鋼　ジュラルドン", #9
"Vスタートデッキ無色　イーブイ", #10
"拡張パック「ムゲンゾーン」", #11
"強化拡張パック「爆炎ウォーカー」", #12
"スターターセットVMAX　リザードン", #13
"スターターセットVMAX　オーロンゲ", #14
"ザシアン＋ザマゼンタBOX", #15
"拡張パック「反逆クラッシュ」", #16
"強化拡張パック「VMAXライジング」", #17
"ポケモンカードゲームソード&シールド 拡張パック「シールド」", #18
"ポケモンカードゲームソード&シールド 拡張パック「ソード」", #19
"ポケモンカードゲームソード&シールド スターターセットV　草", #20
"ポケモンカードゲームソード&シールド スターターセットV　炎", #21
"ポケモンカードゲームソード&シールド スターターセットV　水", #22
"ポケモンカードゲームソード&シールド スターターセットV　雷", #23
"ポケモンカードゲームソード&シールド スターターセットV　闘", #24
"ポケモンカードゲームサン&ムーン ハイクラスパック「TAG TEAM GX タッグオールスターズ」", #25
"ポケモンカードゲームサン&ムーン 拡張パック「オルタージェネシス」", #26
"ポケモンカードゲームサン&ムーン 強化拡張パック「ドリームリーグ」", #27
"ポケモンカードゲームサン&ムーン 強化拡張パック「リミックスバウト」", #28
"ポケモンカードゲームサン&ムーン スターターセット TAG TEAM GX「ブラッキー&ダークライGX」", #29
"ポケモンカードゲームサン&ムーン スターターセット TAG TEAM GX 「エーフィ&デオキシスGX」", #30
"ポケモンカードゲームサン&ムーン 拡張パック「ミラクルツイン」", #31
"ポケモンカードゲームサン&ムーン ムービースペシャルパック「名探偵ピカチュウ」", #32
"ポケモンカードゲームサン&ムーン 強化拡張パック「スカイレジェンド」", #33
"ポケモンカードゲームサン&ムーン 強化拡張パック「ジージーエンド」", #34
"ポケモンカードゲームサン&ムーン 拡張パック「ダブルブレイズ」", #35
"ポケモンカードゲームサン&ムーン 強化拡張パック「フルメタルウォール」", #36
"ポケモンカードゲームサン&ムーン 強化拡張パック「ナイトユニゾン」", #37
"ポケモンカードゲームサン&ムーン 拡張パック「タッグボルト」", #38
"ポケモンカードゲームサン&ムーン スターターセット「炎のブースターGX」", #39
"ポケモンカードゲームサン&ムーン スターターセット「水のシャワーズGX」", #40
"ポケモンカードゲームサン&ムーン スターターセット「雷のサンダースGX」", #41
"ポケモンカードゲームサン&ムーン ハイクラスパック「GXウルトラシャイニー」", #42
"ポケモンカードゲームサン&ムーン 強化拡張パック「ダークオーダー」", #43
"ポケモンカードゲームサン&ムーン 拡張パック「超爆インパクト」", #44
"ポケモンカードゲームサン&ムーン 強化拡張パック「フェアリーライズ」", #45
"ポケモンカードゲームサン&ムーン 強化拡張パック「迅雷スパーク」", #46
"ポケモンカードゲームサン&ムーン 拡張パック「裂空のカリスマ」", #47
"ポケモンカードゲームサン&ムーン 強化拡張パック「チャンピオンロード」", #48
"ポケモンカードゲームサン&ムーン 強化拡張パック「ドラゴンストーム」", #49
"ポケモンカードゲームサン&ムーン 拡張パック「禁断の光」", #50
"ポケモンカードゲームサン&ムーン 強化拡張パック「ウルトラフォース」", #51
"ポケモンカードゲームサン&ムーン 拡張パック「ウルトラムーン」", #52
"ポケモンカードゲームサン&ムーン 拡張パック「ウルトラサン」", #53
"スターターセット伝説 ソルガレオGX ルナアーラGX", #54
"ポケモンカードゲームサン&ムーン ハイクラスパック「GXバトルブースト」", #55
"ポケモンカードゲームサン&ムーン 拡張パック「覚醒の勇者」", #56
"ポケモンカードゲームサン&ムーン 拡張パック「超次元の暴獣」", #57
"ポケモンカードゲームサン&ムーン 強化拡張パック「ひかる伝説」", #58
"ポケモンカードゲームサン&ムーン 拡張パック「闘う虹を見たか」", #59
"ポケモンカードゲームサン&ムーン 拡張パック「光を喰らう闇」", #60
"ポケモンカードゲーム サン＆ムーン 30枚デッキ対戦セット「サトシVSロケット団」", #61
"ポケモンカードゲームサン&ムーン 強化拡張パック「新たなる試練の向こう」", #62
"ポケモンカードゲームサン&ムーン スターターセット改造「カプ・ブルルGX」", #63
"ポケモンカードゲームサン&ムーン 拡張パック「アローラの月光」", #64
"ポケモンカードゲームサン&ムーン 拡張パック「キミを待つ島々」", #65
"ポケモンカードゲームサン&ムーン 強化拡張パック「サン&ムーン」", #66
"ポケモンカードゲームサン&ムーン 「スターターセット水 アシレーヌGX」", #67
"ポケモンカードゲームサン&ムーン 「スターターセット炎 ガオガエンGX」", #68
"ポケモンカードゲームサン&ムーン 「スターターセット草 ジュナイパーGX」", #69
"ポケモンカードゲームサン&ムーン 拡張パック「コレクション ムーン」", #70
"ポケモンカードゲームサン&ムーン 拡張パック「コレクション サン」", #71
"ポケモンカードゲームサン&ムーン プロモカード" #72
]


class JPCard(QThread):

    init = pyqtSignal(bool)
    sendlist = pyqtSignal(list)

    def run(self):
        self.getfirst = False
        self.cardname = None
        self.cardtype = None
        self.inputSeries = None
        self.hide = None
        self.BrowserRunning = False
        self.mainpage = "https://www.pokemon-card.com/card-search"
        self.driver = None
        self.CardType_DropDown = None
        self.SearchOptionSpan = None
        
        self.search_box = None
        while True: #Wait First signal  #cardname, cardtype, inputSeries, hide=False
            self.msleep(500)
            print("QThread : Wait First Signal!!")
            if(self.getfirst):
                print("QTrhead : Rcv First Signal!!")
                break
        #Name,Type,Series is updated by First Signal
        inputSeries = self.inputSeries
        cardtype = self.cardtype
        cardname = self.cardname 
        hide = self.hide

        try:
            JPNameDic[inputSeries][0]
            print("Key Check OK!!")
            isok = True
        except KeyError:
            print("KeyError:",inputSeries)
            self.init.emit(False)
            isok = False
        
        if isok:
            options = webdriver.ChromeOptions()
            #https://www.whatismybrowser.com/detect/what-is-my-user-agent 
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36")
            #chrome Headless Mode
            if (hide == True):
                options.add_argument('headless')
                options.add_argument('window-size=1920x1080')
                options.add_argument("disable-gpu")

            

            self.driver = webdriver.Chrome('chromedriver', chrome_options=options)
            self.driver.get(self.mainpage)

            
            self.CardType_DropDown = self.driver.find_element_by_xpath("//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label")
            self.SearchOptionSpan = self.driver.find_element_by_xpath("//*[@id=\"AddFilterArea\"]")
            

            self.CardTypeXpath = {
            "ALL"      : "//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label/div/ul/li[1]",
            "POKEMON"  : "//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label/div/ul/li[2]",
            "TRAINERS" : "//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label/div/ul/li[3]",
            "ENERGY"   : "//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label/div/ul/li[4]"
            }

            self.cardlist = []
            self.currentType = cardtype
            self.CardType_DropDown.click()
            self.SelectCardType(cardtype)
            self.SearchOptionSpan.click()
            self.SeriesOptionSpan = self.driver.find_element_by_xpath("//*[@id=\"CardSearchForm\"]/div/div[3]/div/div/div[4]/div[2]/div[2]")
            self.search_box = self.driver.find_element_by_xpath("/html/body/div/div[1]/div/form/div/div[1]/div/div/div[2]/label/input")
            self.driver.implicitly_wait(5)
            
            print()
            print("-------------------------------------------")
            print(self.SeriesOptionSpan.get_attribute("class")) #groupSubList groupSubList-toggle
            print("-------------------------------------------")
            print()
            self.SeriesOptionSpan.click()
            self.driver.implicitly_wait(5)
            #0.3sec
            #self.RadioElemnetRoot = self.driver.find_element_by_class_name("ListColumn2")
            #SeriesRadioBttn=self.RadioElemnetRoot.find_elements_by_tag_name("label")[SeriesRadioBttnList.index(JPNameDic[inputSeries][0])+1]
            
            #0.08sec
            SeriesRadioBttn = self.driver.find_element_by_xpath( self.findSeriesXpath(inputSeries, cardtype) )
            SeriesRadioBttn.click()
            self.driver.implicitly_wait(5)
            #print(self.search_box)
            self.searchBoxWrite(cardname)
            self.init.emit(True)
            self.BrowserRunning = True
            self.sendlist.emit(self.getCardLink())
        else:
            self.sendlist.emit([])

        while(True):
            #print("Thread Running")
            self.msleep(100)
            a = 1

    #def IsInitOK(self):
    #    return self.init

    def SearchAgain(self, cardname ,cardtype, inputSeries):
        
        self.cardlist = []
        try:
            JPNameDic[inputSeries]
        except KeyError:
            print("KeyError:",inputSeries)
            return None

        self.searchBoxWrite("\b\b\b\b\b\b\b\b\b\b\b\b\b")

        if(self.currentType != cardtype):
            self.CardType_DropDown.click()
            self.driver.implicitly_wait(5)
            self.SelectCardType(cardtype)
            self.driver.implicitly_wait(5)
            self.SearchOptionSpan.click()
            self.driver.implicitly_wait(5)
            self.currentType = cardtype    
        
        #self.SeriesOptionSpan.click()
        self.driver.implicitly_wait(5)
        
        print(inputSeries,":",self.findSeriesXpath(inputSeries, cardtype))
        SeriesRadioBttn = self.driver.find_element_by_xpath( self.findSeriesXpath(inputSeries, cardtype) )

        SeriesRadioBttn.click()
        self.driver.implicitly_wait(5)
        print(self.search_box)
        
        self.searchBoxWrite(cardname)
        return self.getCardLink()

        


    def SelectCardType(self, CardType):
        PokeSelect = self.driver.find_element_by_xpath(self.CardTypeXpath[CardType])
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

    @pyqtSlot(dict)
    def getFirstSigSlot(self, firstsig):
        print("QThread : GET FIRST SIGANL!!")
        self.cardname = firstsig["cardname"]
        self.cardtype = firstsig["cardtype"]
        self.inputSeries = firstsig["inputSeries"]
        self.hide = firstsig["hide"]
        self.getfirst = True

    @pyqtSlot(list)
    def getCardListSlot(self, getlist):
        print("QThread : GET Request URL List!!")
        #[jpname, CardType, Series]
        cardname = getlist[0]
        cardtype = getlist[1]
        inputSeries = getlist[2]
        self.cardlist = []
        try:
            JPNameDic[inputSeries][0]
            print("Key Check OK!!")
            isok = True
        except KeyError:
            print("KeyError:",inputSeries)
            isok = False
        
        if isok:
            self.searchBoxWrite("\b\b\b\b\b\b\b\b\b\b\b\b\b")
            if(self.currentType != cardtype):
                self.CardType_DropDown.click()
                self.driver.implicitly_wait(5)
                self.SelectCardType(cardtype)
                self.driver.implicitly_wait(5)
                self.SearchOptionSpan.click()
                self.driver.implicitly_wait(5)
                self.currentType = cardtype    
            #self.SeriesOptionSpan.click()
            self.driver.implicitly_wait(5)
            
            print(inputSeries,":",self.findSeriesXpath(inputSeries, cardtype))
            SeriesRadioBttn = self.driver.find_element_by_xpath( self.findSeriesXpath(inputSeries, cardtype) )

            SeriesRadioBttn.click()
            self.driver.implicitly_wait(5)
            print(self.search_box)
            
            self.searchBoxWrite(cardname)
            self.sendlist.emit(self.getCardLink())
        else: #KeyError Send Empty List
            self.sendlist.emit([])

    def WaitText(self,txt_element):
        old_txt = "OLD"
        new_txt = "NEW"
        while (old_txt != new_txt):
            old_txt = new_txt
            self.msleep(500)
            new_txt = txt_element.text    
            print("NEW:%s, OLD:%s"%(new_txt, old_txt))
        return new_txt

    def findSeriesXpath(self,SeriesString, cardtype):
        SearchStr = JPNameDic[SeriesString][0]
        print("Series:",SeriesString ,"/SearchStr:", SearchStr)
        index=SeriesRadioBttnList.index(SearchStr)
        if(cardtype == "POKEMON"):
            return "//*[@id=\"CardSearchForm\"]/div/div[3]/div/div/div[4]/div[2]/div[2]/div[2]/div/ul/li["+str(index+2)+"]/label"
        elif(cardtype == "TRAINERS"): 
            return "//*[@id=\"CardSearchForm\"]/div/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div/ul/li["+str(index+2)+"]/label"
        return 0

    def getCardLink(self):
        count = int(self.GetTotalCount())
        cardlist= self.getCardList()
        urllist = []
        if(count == 0):
            return None
        else: # Over Links
            for i in range(len(cardlist)):
                urllist.append("https://www.pokemon-card.com"+cardlist[i]["src"])
                #print (urllist[i])
            return urllist
        
    @pyqtSlot(bool)
    def closeBrowser(self, iskill):
        print("QThread : Kill Browser!!!")
        if iskill and self.BrowserRunning:
            self.driver.close()

if __name__ == "__main__":
    print("Main")
    #card = JPCard("フーパ", "POKEMON" ,"sm3plus")
    #link = card.getCardLink()
    #if link:
    #    print("GET SUCCESS : ", link)

    #link =card.SearchAgain("スーパーボール",  "TRAINERS" ,"SA_L")
    #if link:
    #    print("GET SUCCESS : ", link)

    #link =card.SearchAgain("ピカチュウ",  "POKEMON" ,"SA_L")
    #if link:
    #    print("GET SUCCESS : ", link)

#ENERGY TEST필요


    #card.close()
