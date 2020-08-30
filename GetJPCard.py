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
    progress = pyqtSignal(int)
    getfirst = False
    inputSeries = None
    hide = None
    pageNo = None
    prev_pageNo = None
    cardname = None
    cardtype = None
    BrowserRunning = False
    cardlist = []

    def run(self):
        self.mainpage = None
        self.driver = None
        self.CardType_DropDown = None
        self.SearchOptionSpan = None
        self.RequestURL = False
        self.RequestMsg = []
        self.IsStandard = None
        self.search_box = None
        self.progpercent = 0
        self.UpdateProgress(0) #0%
        while True: #Wait First signal  #cardname, cardtype, inputSeries, hide=False
            self.msleep(500)
            #print("QThread : Wait First Signal!!")
            if(self.getfirst):
                print("QTrhead : Rcv First Signal!!")
                break
        #Name,Type,Series is updated by First Signal
        self.UpdateProgress(5) #5%
        inputSeries = self.inputSeries
        cardtype = self.cardtype
        cardname = self.cardname 
        hide = self.hide
        pageNo = self.pageNo
        isok = True

        if (self.SeriesNameCheck(inputSeries, pageNo) == False): #Standard Series Check
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

            if(pageNo == 0):
                print("QThread : Init Standard Page !!!")
                self.mainpage = "https://www.pokemon-card.com/card-search"
                self.IsStandard = True
            else:
                print("QThread : Init None Standard Page !!!")
                self.mainpage = "https://www.pokemon-card.com/card-search/index.php?mode=statuslist&pg="+pageNo
                self.IsStandard = False
            self.UpdateProgress(10) #10%
            self.driver = webdriver.Chrome('chromedriver', chrome_options=options)
            self.driver.get(self.mainpage)
            self.driver.implicitly_wait(5)
            self.UpdateProgress(30) #30%
            self.prev_pageNo = pageNo ##IMPORTANT
            
            self.LoadBttn()
            
            self.currentType = cardtype
            self.SelectCardType(cardtype)
            self.UpdateProgress(30) #35% CardType Select Complete
            if self.IsStandard:
                self.SearchOptionSpan.click()
                while True:
                    if(self.SearchOptionSpan.find_element_by_tag_name("div").get_attribute("class") == "AddFilterButton js-active"):
                        print("QThread OptionSpan OK: ",self.SearchOptionSpan.find_element_by_tag_name("div").get_attribute("class"))  
                        break
                    else:
                        self.msleep(100)
                        print("QThread OptionSpan CHECK!!: ",self.SearchOptionSpan.find_element_by_tag_name("div").get_attribute("class"))
                #self.driver.implicitly_wait(5)
                
                self.StandardSeriesSlect(inputSeries,cardtype)
                print("-------------------------------------------")
                print("QThread Init", self.SeriesOptionSpan.get_attribute("class")) #groupSubList groupSubList-toggle
                print("-------------------------------------------")

            self.UpdateProgress(40) #40% SeriesSelect Complete
            self.driver.implicitly_wait(5)
            self.searchBoxWrite(cardname)
            self.UpdateProgress(50) #50% WriteSearchBox Complete
            
            self.init.emit(True) #Initiallize OK Send to Main
            self.BrowserRunning = True
            self.sendlist.emit(self.getCardLink()) # UrlList Send to MAIN
            self.UpdateProgress(100) #100%
        else:
            self.sendlist.emit([]) # UrlList Send to MAIN
            self.UpdateProgress(100) #100%

        while(True): #Request URL Wait Loop
            if(self.RequestURL): #Search Again Msg Get From Main
                linklist=self.SearchAgain(self.RequestMsg[0], self.RequestMsg[1], self.RequestMsg[2], self.RequestMsg[3])
                self.sendlist.emit(linklist)
                self.RequestURL = False
            self.msleep(100)


    def UpdateProgress(self, update):
        self.progpercent = update
        self.progress.emit(self.progpercent)
    
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

    def SearchAgain(self, cardname ,cardtype, inputSeries, pageNo):
        self.cardlist = []
        self.UpdateProgress(0)
        changed = False
        
        if (self.SeriesNameCheck(inputSeries, pageNo) == False): #Standard Series Check
            return []
                
        self.UpdateProgress(10)    
        #Check URL Change Standard <-> NoneStandard
        if(self.IsStandard): #Current Standard
            if (pageNo==0): #Standard
                print("Keep Current URL : Standard")
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

        self.UpdateProgress(20)    
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
        self.UpdateProgress(30)
        
        if self.IsStandard:
            self.StandardSeriesSlect(inputSeries, cardtype)

        self.UpdateProgress(40)
        self.searchBoxWrite(cardname)
        self.UpdateProgress(50)
        link = self.getCardLink()
        self.UpdateProgress(100)
        return link

    def StandardSeriesSlect(self, inputSeries, cardtype):
        self.SeriesOptionSpan = self.driver.find_element_by_xpath("//*[@id=\"CardSearchForm\"]/div/div[3]/div/div/div[4]/div[2]/div[2]")
        self.SeriesOptionSpan.click()
        while True:
            if(self.SeriesOptionSpan.get_attribute("class")=="groupSubList groupSubList-toggle js-open"):
                print("QThread SeriesSpan OK:", self.SeriesOptionSpan.get_attribute("class"))
                break
        self.driver.implicitly_wait(5)
        print(inputSeries,":",self.findSeriesXpath(inputSeries, cardtype))
        SeriesRadioBttn = self.driver.find_element_by_xpath( self.findSeriesXpath(inputSeries, cardtype) )
        print("QThread RadioButton Find!!:",SeriesRadioBttn.find_element_by_class_name("KSFormText").text)
        SeriesRadioBttn.click()
        self.driver.implicitly_wait(5)

    def LoadBttn(self):
        self.search_box = self.driver.find_element_by_xpath("/html/body/div/div[1]/div/form/div/div[1]/div/div/div[2]/label/input")
        self.CardType_DropDown = self.driver.find_element_by_xpath("//*[@id=\"CardSearchForm\"]/div/div[1]/div/div/div[3]/label")
        self.SearchOptionSpan = self.driver.find_element_by_xpath("//*[@id=\"AddFilterArea\"]")
        
        print("QThread LoadBttn : ", self.SearchOptionSpan.find_element_by_tag_name("div").get_attribute("class"))


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

    @pyqtSlot(list)
    def getFirstSigSlot(self, firstsig):
        print("QThread : GET FIRST SIGANL!!")
        self.cardname = firstsig[0]
        self.cardtype = firstsig[1]
        self.inputSeries = firstsig[2]
        self.pageNo = firstsig[3]
        self.hide = firstsig[4]
        self.getfirst = True
        print("QThread : Finish First Signal")

    @pyqtSlot(list)
    def getCardListSlot(self, getlist):
        print("QThread : GET Request URL List!!")
        #[jpname, CardType, Series]
        print("prevPage:",self.prev_pageNo) 
        self.RequestMsg = getlist
        print(getlist)
        self.RequestURL = True #run() Excute searchAgain

    def WaitText(self,txt_element):
        old_txt = "OLD"
        new_txt = "NEW"
        cnt = 0
        while (old_txt != new_txt):
            if(cnt<10):
                self.UpdateProgress(50+cnt*5) 
            old_txt = new_txt
            self.msleep(500)
            new_txt = txt_element.text    
            print("NEW:%s, OLD:%s"%(new_txt, old_txt))
            cnt+=1
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
        
    @pyqtSlot(bool)
    def closeBrowser(self, iskill):
        print("QThread : Kill Browser!!!")
        if iskill and self.BrowserRunning:
            self.driver.quit()
            

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