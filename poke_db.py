# -*- coding:utf-8 -*-
import mysql.connector
import time

#QT GUI
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic 
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QSize, QEvent, QThread, QObject
form_class = uic.loadUiType("PokeDBWindow.ui")[0]
#from PyQt5.QtCore import pyqtBoundSignal

#WEB BROWSER
import webbrowser

#Copy Clipboard
import io
import csv

#PokeCard Browser
import Poke_Card

#JP Search
import GetJPCard
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from pandas import read_excel
from pandas import DataFrame
from pandas import concat
from PyQt5 import QtTest

#PokeConverter
import Pokecard_Converter

#Reader 
# from gtts import gTTS
# from playsound import playsound
import os


try:
    from html import escape
except ImportError:
    from cgi import escape

#from html.parser import HTMLParser
#from bs4 import BeautifulSoup

import ctypes
#For Icon
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/'
HIDE_BROWSER = True

if(os.path.isdir(chrome_path)):
    chrome_path += 'chrome.exe %s'
    pass
else:
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'



#DB 접속정보를 dict type 으로 준비한다.
config={
        "user":"root",
        "password":"1234",
        "host":"127.0.0.1",   
        "database":"pokecard",
        "port":3306
    }

class WordCounter():
    def __init__(self, input_string):
        print("WordCountinit")
        self.d = {}
        words = input_string.split()
        for word in words:
            try:
                self.d[word] += 1
            except:
                self.d[word] = 1

        f = open("WordCheck.txt", 'w')        
        for k in self.d.keys():
            f.write("%s\t%d\n" % (k, self.d[k]))
        f.close()
        print("finish to write file")

class PokeScore():
    def __init__(self, input_string):
        print("PokeScoreinit")
        cards = input_string.split('\n')
        
        self.data = []
        for card in cards:
            self.data.append(card.split(','))
        #print(self.data)
        
        print("Finish Get ALL DATA")
        
    def CalcScore(self):
        #self.data[0][]
        print("clacscore")


class EXCEL_DATA(QThread):

    NonRedundantList=pyqtSignal(list)

    def __init__(self, f_name):
        print("JP_DATA INIT")
        try:
            namelist=f_name.split('.')
            
            ext = namelist[len(namelist)-1].strip()
            if(ext == 'xlsx' or ext == 'xlsm' or ext == 'xls' or ext == 'csv'):
                pass
            else:
                print("EXCEL DATA LOAD FAIL!!")
                return None
            self.xlsx = None
            self.key = None
            self.f_name = f_name
            #print(self.key)
            QThread.__init__(self)
        except:
            print("EXCEL DATA LOAD FAIL!!")
            return None
    
    def XLS_DATA( self , col , row ):
        return self.xlsx[self.key[col]][row]

    
    def SetRedundantData(self, col_cnt ,CompareData, fieldSeperator=False):
        self.DB_ColCnt = col_cnt
        self.fieldSeperator = fieldSeperator
        self.CompareData = CompareData
    
    def run(self):
        #init just check file extension
        self.xlsx = read_excel(self.f_name, encoding='utf-8', keep_default_na=False) #read dataframe
        self.key = self.xlsx.keys()

        #self.CompareData is Not Exist
        #print(self.CompareData)
        #print(self.key)
        print("[EXCEL QThread] DB Column size:",self.DB_ColCnt, "Excel Column Size:", len(self.key))

        if(self.DB_ColCnt != len(self.key)):
            self.NonRedundantList.emit(["WRONG_FILE"])
        else:
            res=self.GetNonRedundantData(self.CompareData, self.fieldSeperator)
            self.NonRedundantList.emit(res)


    def GetNonRedundantData(self, CompareData, fieldSeperator=False):
        ExlDataDf=DataFrame(self.xlsx[self.key[0]])
        if(fieldSeperator == True): #remove fieldSeperator("") to compare
            CopareDf = DataFrame( {self.key[0]: [ str(CompareData[i][0])[1:-1] for i in range(len(CompareData)) ]} )
        else:
            CopareDf = DataFrame( {self.key[0]: [ str(CompareData[i][0]) for i in range(len(CompareData)) ]} )
        
        #First Column of DataBase + FindTag(index-0) +First Column of Excel File 
        #Use Drop duplicates Delete duplicated rows
        df_diff = concat([ExlDataDf, DataFrame(["FIND_TAG"], columns=[self.key[0]]) ,CopareDf]).drop_duplicates(keep=False)
        
        #print(df_diff)
        res = None

        #Find Tag Position To seperate Original Data from Where (Excel or DataBase)
        tag_pos = 0
        for i in range(len(df_diff.index)):
            print(df_diff.iloc[i][0])
            if(df_diff.iloc[i][0] == "FIND_TAG"):
                tag_pos = i
                break
        print("TAG_POS : ",tag_pos)
        if(tag_pos == 0): #DB data = Excel Data or DB has more data
            idx_list = df_diff.index.to_list()
            FullCompareDF = DataFrame( CompareData ,  columns = self.key, dtype=str ) 
            print("---DataBase ORG Data--")
            res = DataFrame(FullCompareDF, index=idx_list[1:], dtype=str)
            print(res)
            res = DataFrame([])
        else: # DB data != Excel Data Seperate Data
            ExlDataOrgIndex = df_diff.index[:tag_pos]
            #print(ExlDataOrgIndex)
            CompDataOrgIndex = df_diff.index[tag_pos+1:]
            #print(CompDataOrgIndex)
            res1 = DataFrame(self.xlsx, index=ExlDataOrgIndex, dtype=str)
            print("---Excel ORG Data--")
            print(res1[self.key[0]])
            FullCompareDF = DataFrame( CompareData ,  columns = self.key, dtype=str ) 
            res2 = DataFrame(FullCompareDF, index=CompDataOrgIndex, dtype=str)
            print("---DataBase ORG Data--")
            print(res2)
            res = res1
        return res.values.tolist()

    def PrintExcelFile(self):
        print(self.xlsx)


class MyProgressBar(QProgressBar):
    def __init__(self, widget, min=0, max=0):
        super().__init__(widget)
        self.setRange(min, max)
        self.setAlignment(Qt.AlignCenter)
        self._text = None
    def setText(self, text):
        self._text = text
    def text(self):
        return self._text

class QProgressPopup(QThread):
    init = pyqtSignal(bool)
    progress = pyqtSignal(int)
    def __init__(self, min, max, hideTitle=False, pos = None, txt = None):
        QThread.__init__(self)
        self.w = QWidget()
        QProgressBar.__init__(self.w)
        self.ProgressBar = MyProgressBar(self.w, min, max)
        self.cnt = 0
        self.ProgressBar.setRange(min,max)
        self.ProgressBar.resize(420,31)
        self.w.resize(420,31)
        self._status = False
        

        if(hideTitle == True):
            self.w.setWindowFlag(Qt.FramelessWindowHint)

        if(txt):
            self.ProgressBar.setText(txt)
        if(pos):
            print("move")
            self.w.move( pos["x"]+(pos["width"]-self.w.width())/2 , pos["y"]+ (pos["height"]-self.w.height())/2 )
        self.w.show()

    def run(self):
        self._status = True
        while True:
            self.msleep(100)
            print("[QProgressThread] Running")
            if(self.ProgressBar.value == 100):
                break
        print("[QProgressThread] Finish")
        self._status = False
    
    def closeEvent(self, event):
        print("[QProgressThread]closeEvent!!!")
        self.w.close()
        self.terminate()

            

        
class PokeDBWindow(QMainWindow, form_class):
    
    #JP Card Search Signal
    request_url = pyqtSignal(list) #Request URL Again (Browser Already Opened)
    firstsig = pyqtSignal(list) #Browser Open, Request URL
    sig_killbrowser = pyqtSignal(bool) #kill Browser

    #ProgWindow Close Signal
    ProgCloseSig=pyqtSignal(QEvent)

    #Converter Signal
    ConvertMsg=pyqtSignal(list)

    #update progressvalue
    progvalue=pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)        
        self.conn = None
        self.cursor = None
        self.DBtablelist = [] #DB Table List
        self.DBTableNow = None
        self.col_cnt = 10
        self.col_list = []
        
        #QTable
        self.initQTableAction()
        #Table Action Connect
        self.actionCell_Marking.triggered.connect(self.QTableCellMarking)
        self.actionClearCell_Marking.triggered.connect(self.QTableCellMarkingClear)
        self.actionText_Marking.triggered.connect(self.QTableTextMarking)
        self.actionClear_Text_Marking.triggered.connect(self.QTableTextMarkingClear)
        self.actionSearch_Japan_Name.triggered.connect(self.QMenuSearchJPName)
        self.tableAddList = []
        self.tableUpdateList = []
        self.max_cnt = 0
        #self.tableWidget.setItemDelegate(HTMLDelegate(self.tableWidget))

        #Menu
        self.menuSearchCount = 0
        self.actionConnect_To_DataBase.triggered.connect(self.Connect_Clicked)
        self.actionSearch_Text.triggered.connect(self.Search_Text_Clicked)
        self.menuList = []
        self.menuActionList = []
        
        #DB Action Connect
        self.actionSelect_Table.triggered.connect(lambda:self.DBTableSelect(Select=True))
        self.actionLoad_Table_For_Update.triggered.connect(self.DBUpdateFromExcel)
        self.RedundantList = None #List Get From Thread
        self.r_data = None

        #ALL Menu item Enable Init
        self.QMenuEnableALL(self.menuTable ,False)
        self.QMenuEnableALL(self.menuSearch ,False)
        self.menuSearch_Select.setEnabled(True)
        
        #QTree
        self.treeWidget.setEnabled(False)
        self.treeWidget.itemChanged.connect(self.QTreeWidgetItemChanged)
        self.searchCountBox = None
        self.searchCount = 0
        self.treelist = []
        self.bttnTextlist = []
        self.bttnConditionlist = []
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.QTreeMenu)
        
        #PokeCard Window
        self.CardWindow = Poke_Card.MyWindow()
        self.CardWindow.SetCountry("KOR")
        self.CardWindow.setWindowTitle("PokeCard Viewer")
        self.CardWindow.setWindowIcon(QIcon("Pokemon.ico"))

        #Converter Tab
        self.pushButton_Load_JP.clicked.connect(self.Convert_Load_JP_Clicked)
        self.pushButton_Cvt_KR.clicked.connect(self.Convert_KR_Clicked)
        self.pushButton_Cvt_Txt.clicked.connect(self.Convert_Txt_Clicked)
        self.pushButton_Cvt_KR.setEnabled(False)
        self.pushButton_Cvt_Txt.setEnabled(False)
        self.r_JPfileName = None #read data (JP Excel file)
        self.Converter  = None
        self.isFinish = False
        self.r_JPdata = None #Get JP_DATA()
        
        #Log Text Viewer
        self.searchExeCnt = 0
        self.textBrowser.setEnabled(False)
        self.textBrowser.setReadOnly(True)

        #JP Card Search
        self.jpCard = None
        self.jpCardWindow = Poke_Card.MyWindow()
        self.jpCardWindow.SetCountry("JPN")
        self.jpCardWindow.setWindowTitle("JP Card Viewer")
        self.jpCardWindow.setWindowIcon(QIcon("Pokemon.ico"))
        self.BrowserRunning = False

        #ProgressBar
        self.ProgWindow = None

        #Text Reader
        self.tts = None

    
    def QProgressStart(self, getText, min=0, max=0):
        my_pos = {
            "x"     : self.pos().x(),
            "width" : self.width(), 
            "y"     : self.pos().y(),
            "height": self.height()
        }
        if(min ==0 and max ==0):
            self.ProgWindow = QProgressPopup(0,0, hideTitle=True, pos=my_pos, txt=getText)
        else:
            self.ProgWindow = QProgressPopup(min,max,  hideTitle=True, pos=my_pos)
        self.ProgCloseSig.connect(self.ProgWindow.closeEvent)
    
    def QProgressClose(self):
        self.ProgWindow.terminate()
        self.ProgCloseSig.emit(QEvent(QEvent.Close))

    def closeEvent(self, event):
        print("[MainWindow]closeEvent!!!")
        
        #DB Update Load table
        if(self.r_data != None):
            self.r_data.terminate()
            print("[MainWindow]DB Update Close Finish!!!")
        #Converter 
        if(self.r_JPfileName != None):
            self.ConvertMsg.emit(["FINISH"])
            self.ConverterFinishCheck()
            self.Converter.terminate()
            print("[MainWindow]Converter Close Finish!!!")
        if(self.BrowserRunning):
            #self.jpCard.closeBrowser()
            self.sig_killbrowser.emit(True)
            self.jpCard.terminate()
            self.jpCardWindow.close()
        self.CardWindow.close()
        self.jpCardWindow.close()
        self.CardWindow.close()
        print("[MainWindow]Browser Close Finish!!!")

    
    def initQTableAction(self):
        #Table Right Button Menu
        #Delete all Actions
        for action in self.tableWidget.actions():
            action.deleteLater()
        for action in self.tableWidget.horizontalHeader().actions():
            action.deleteLater()

        self.tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        #Copy Action (Common)
        self.copy_action = QAction("Copy Select Area", self.tableWidget)
        self.copy_action.triggered.connect(self.copySelection)
        self.copy_action.setShortcut('Ctrl+C')
        self.tableWidget.addAction(self.copy_action)
        
        #ADD Row Action (Common)
        add_action = QAction("ADD Row", self.tableWidget)
        add_action.triggered.connect(lambda:self.QTableAddRow(1))
        self.tableWidget.addAction(add_action)

        #Update to DB Action (Common)
        update_action = QAction("Update Current Row to Database", self.tableWidget)
        update_action.triggered.connect(self.QTableUpdateDataBase)
        self.tableWidget.addAction(update_action)

        #Only Cardinfo table Use below Action
        if(self.DBTableNow == 'cardinfo'):
            kr_url_action = QAction("Open Current Row Korea Card Page", self.tableWidget)
            jp_url_action = QAction("Open Current Row Japan Card Page", self.tableWidget)
            kr_action = QAction("Show Current Row Korea Card", self.tableWidget)
            jp_action = QAction("Search Current Row Japan Card", self.tableWidget)
            findname_action = QAction("Search Current Row Japan Name", self.tableWidget)
            #read_action = QAction("Read Current Row", self.tableWidget)
            
            self.tableWidget.addAction(kr_url_action)
            self.tableWidget.addAction(jp_url_action)
            self.tableWidget.addAction(kr_action)
            self.tableWidget.addAction(jp_action)
            self.tableWidget.addAction(findname_action)
            #self.tableWidget.addAction(read_action)
            
            kr_url_action.triggered.connect(self.QTableRowOpenUrl)
            kr_url_action.setShortcut('Ctrl+O')
            jp_url_action.triggered.connect(self.QTableRowOpenJPUrl)
            jp_url_action.setShortcut('Ctrl+I')
            kr_action.triggered.connect(self.QTableShowCurrentRow)
            kr_action.setShortcut('Ctrl+K')
            jp_action.triggered.connect(self.QTableSearchJPCard2)
            jp_action.setShortcut('Ctrl+J')
            findname_action.triggered.connect(self.QTableSearchJPName)
            """read_action.triggered.connect(self.QTableRowTTS)
            read_action.setShortcut('Ctrl+R') """
        
        #Range Selection Event
        self.tableWidget.itemSelectionChanged.connect(self.QTableItemSelectionChanged)
        
        #Table Column Label Right Button Menu
        col_header = self.tableWidget.horizontalHeader()
        col_header.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        if(self.DBTableNow == 'cardinfo'):
            abilityshow_action  = QAction("Hide ALL Column Except Ability", col_header) 
            abilitylabel_action = QAction("Hide ALL Column Except Ability_Label", col_header) 
            
            col_header.addAction(abilityshow_action)
            col_header.addAction(abilitylabel_action)
            
            select_list = ["ability1", "ability2", "ability3", "ability4"]
            abilityshow_action.triggered.connect(lambda:self.QTableShowOnlySelected(select_list))
            select_list2 = ["ability_label1", "ability_label2", "ability_label3", "ability_label4"]
            abilitylabel_action.triggered.connect(lambda:self.QTableShowOnlySelected(select_list2))
        
        self.colcopyAction  = QAction("Copy Selected Column", col_header)
        colShowAll          = QAction("Show ALL Column", col_header)
        col_header.addAction(self.colcopyAction)
        col_header.addAction(colShowAll) 
        self.colcopyAction.triggered.connect(self.copySelection)
        colShowAll.triggered.connect(self.QTableShowALLCol)
        
    
        #Table Raw Label Right Button Menu
        row_header = self.tableWidget.verticalHeader()
        row_header.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.rowcopyAction  = QAction("Copy Selected Row", row_header)
        self.rowUpdateDbAction = QAction("Update Selected Row to DataBase")
        row_header.addAction(self.colcopyAction)
        row_header.addAction(self.rowUpdateDbAction)
        self.rowUpdateDbAction.triggered.connect(self.QTableSelRowUpdateDB)
        
        
        #Variable Action by QtableSelectionChanged
        self.HideColumnAction = QAction("Hide Selected Column", self.tableWidget)
        self.ShowColumnAction = QAction("Show Selected Column", self.tableWidget)
        
    def onSectionClicked(self):
        print("section clicked")
    
    def QTableAddRow(self, cnt=1):
        print("AddRow : %d row"%cnt)
        for i in range(cnt):
            #print("QTableAddRow : %d"%(i+1))
            rowcnt=self.tableWidget.rowCount()
            #self.tableWidget.setRowCount(rowcnt+1)
            self.tableWidget.insertRow(rowcnt)
            self.tableWidget.setCurrentCell(rowcnt, 0)
            self.tableAddList.append(rowcnt)
            #print("AddedList : ", self.tableAddList)
            #self.tableWidget.scrollToItem(self.tableWidget.item(rowcnt,0), QAbstractItemView.PositionAtCenter)
        print("Added Row Update to List Finish!!")
        print(self.tableAddList)

    def QTableSelRowUpdateDB(self):
        print("QTableUpdateDataBase")
        rangelist = self.tableWidget.selectedRanges()

        selectedRowList = []
        for now_range in rangelist: #QTableWidgetSelectionRange Loop 
            if (now_range.columnCount() == self.tableWidget.columnCount()): #row Selected
                #print("Bottom:", now_range.bottomRow() ,"Top:", now_range.topRow())
                for i in range(now_range.topRow(), now_range.bottomRow()+1): selectedRowList.append(i) 

        print("Slected Rows",selectedRowList)


        
        self.QProgressStart("!!", min=0, max=len(selectedRowList))

        self.progvalue.connect(self.ProgWindow.ProgressBar.setValue)

        for row in selectedRowList:
            print("Row in Selected RowList:", row)
            self.QTableUpdateDataBase(row, disableMessage=True)
            self.progvalue.emit(row)
            QtTest.QTest.qWait(1) #Wait 1ms
        
        self.QProgressClose()
        self.MessageBox("Upate Finish!!!\nSelected Rows")

  
    """ def QTableRowTTS(self):
        currentRow = self.tableWidget.currentRow()
        currentCol = self.tableWidget.currentColumn()
        #for index in range(self.col_cnt):
        
        print(self.tableWidget.item(currentRow, currentCol).text())
        self.speak(self.tableWidget.item(currentRow, currentCol).text())
        print("END READ!!") """
            

    """ def speak(self, my_text):
        f = open("temp.mp3", "wb+")
        gTTS(text=my_text, lang='ko').write_to_fp(f)
        f.seek(0)
        f.close()
        playsound("temp.mp3")
        os.remove("temp.mp3") """

    def QTableUpdateDataBase(self, row=-1 , disableMessage=False):
        print("QTableUpdateDataBase")
        print("row : ", row)
        sql = 'INSERT INTO `pokecard`.`%s` ('%self.DBTableNow
        if(row == -1):
            currentRow = self.tableWidget.currentRow()
        else:
            currentRow =row
        print("CurrentRow : ", currentRow)
        #print("AddedList :: " ,self.tableAddList)
        try:
            self.tableAddList.index(currentRow)
            isAdd = True
            print("Find Index From AddedRowList", currentRow)
        except ValueError as e:
            UpdateInfo = None
            for table in self.tableUpdateList: #Searched Data was Changed
                if(table[0] == currentRow):
                    UpdateInfo = table            
            if(UpdateInfo == None):
                self.MessageBox("Update ERROR!!!\nCan't Find Change")
                print(self.tableAddList)
                return False
            #UPDATE EX)UPDATE `pokecard`.`name` SET `KOR`='3',`JP`='4' WHERE  `JP`='1' AND `KOR`='2' LIMIT 1;
            sql_f = 'UPDATE `pokecard`.`%s` SET '%self.DBTableNow
            sql_b = "WHERE "
            for i in range(self.col_cnt):
                print(self.col_list[i] ,":", UpdateInfo[1][i],"->",UpdateInfo[2][i])
                sql_f+="`%s`='%s' ,"%(self.col_list[i], UpdateInfo[2][i])
                sql_b+="`%s`='%s' AND "%(self.col_list[i], UpdateInfo[1][i])
            self.DB_UpdateQuery(sql_f[:-1]+sql_b[:-4]+"LIMIT 1;")
            self.textBrowser.append("OLD : %s\nNEW :%s\n"%(UpdateInfo[1],UpdateInfo[2]))
            self.tableUpdateList.remove(UpdateInfo) #Item Delete From UpdateList
            print("DB Update Finish!!!")
            return True

        #Added Row Data Update 
        for col in self.col_list:
            sql+='`%s`,'%col
        sql = sql[:-1] + ") VALUES ("
        log = []
        for index in range(self.col_cnt):
            if(self.tableWidget.item(currentRow, index) == None):
                sql+='"",'
            else:
                if(self.DBTableNow == 'cardinfo'):
                    sql+='"""%s""",'%self.tableWidget.item(currentRow, index).text()
                else:
                    sql+='"%s",'%self.tableWidget.item(currentRow, index).text()
                log.append(self.tableWidget.item(currentRow, index).text())
        sql = sql[:-1] + ")"
        #print(sql)
        #INSERT EX)INSERT INTO `pokecard`.`name` (`JP`, `KOR`) VALUES ('aaaa', 'bbb') LIMIT 1;
        self.textBrowser.append("NEW ROW :%s\n"%(log))
        self.DB_UpdateQuery(sql , disableMessage)
        self.tableAddList.remove(currentRow)
        print("DB ADD Finish!!!")
        
        

    def QTableCellChanged(self, row, col):
        print("QTableCellChanged (%d,%d)"%(row, col))
        try : 
            self.tableAddList.index(row)
        except ValueError:
            newRow = [row] # newRow = [RowNum, tuple(before col list), list[after col list]] 
            #Update Again
            for table in self.tableUpdateList:
                if(table[0] == row):
                    print("ROW: %d (COL %s:%s-%s)>"%(row ,self.col_list[col], table[2][col], self.tableWidget.item(row,col).text()))
                    table[2][col] = self.tableWidget.item(row,col).text()
                    print("Updated!!:%s"%table[2][col])
                    return True

            #First Update Need to check Original Data From DB
            sql = "SELECT * FROM `pokecard`.`%s` WHERE "%self.DBTableNow 
            for i in range(self.col_cnt):
                if( i != col): #Current Colum is changed so don't add to sql query
                    if(self.DBTableNow == 'cardinfo'):
                        sql+="`%s`=\'\"%s\"\' AND "%(self.col_list[i], self.tableWidget.item(row,i).text())
                    else:
                        sql+="`%s`='%s' AND "%(self.col_list[i], self.tableWidget.item(row,i).text())
            sql = sql[:-4]
            print(sql)
            res=self.DB_SendQuery(sql)
            if(len(res)!=1): #Can't Find Original-Data
                self.MessageBox("Can't Find Original Data\nMatched DB Data Found : %dEA"%len(res))
                return False

            newRow.append(res[0])
            newRow.append([])
            #Updated data to newRow[2]
            for i in range(self.col_cnt):
                if(self.DBTableNow == 'cardinfo'):
                    newRow[2].append('"'+self.tableWidget.item(row,i).text()+'"')
                else:
                    newRow[2].append(self.tableWidget.item(row,i).text())
            #print(newRow)
            print("Update New Row:%d!!!"%newRow[0])
            self.tableUpdateList.append(newRow)

        

    def QTableShowOnlySelected(self, select_list):
        print("QTableShowOnlySelected")
        for i in range(self.col_cnt):
            if(not(self.col_list[i] in select_list)):
                self.tableWidget.hideColumn(i)
            else:
                self.tableWidget.showColumn(i)
                
    def QTableHideSelected(self, select_list):
        print("QTableHideSelected")
        for i in range(self.col_cnt):
            if(self.col_list[i] in select_list):
                self.tableWidget.hideColumn(i)
    def QTableShowSelected(self, select_list):
        print("QTableShowSelected")
        for i in range(self.col_cnt):
            if(self.col_list[i] in select_list):
                self.tableWidget.showColumn(i)

    def QTableShowALLCol(self, select_list):
        print("QTableShowALLCol")
        for i in range(self.col_cnt):
            self.tableWidget.showColumn(i)
        
    
    def QTreeMenu(self, pos):
        menu = QMenu()
        menu.move(pos.x()+self.pos().x(), pos.y()+self.pos().y()+100) #???
        WigetList = self.treeWidget.selectedItems()
        if(len(WigetList) == 1):
            WidgetItem=self.treeWidget.selectedItems()[0]
            if(WidgetItem.parent() == None):#TopLevel Item
                menu.addAction("Search", self.Search_Text_Clicked)
                if("Search" in WidgetItem.text(0) and not("Count" in WidgetItem.text(0))): #Seach 1-10
                    menu.addAction("Check ALL", lambda:self.QMenuCheckAll(int(WidgetItem.text(0)[6:])-1, Qt.Checked))
                    menu.addAction("UnCheck ALL", lambda:self.QMenuCheckAll(int(WidgetItem.text(0)[6:])-1, Qt.Unchecked))
                    if(self.DBTableNow == 'cardinfo'):
                        select_list1 = ["ability_label1", "ability_label2", "ability_label3", "ability_label4"]
                        menu.addAction("Check Only Ability Label", lambda:self.QMenuCheckSelected(int(WidgetItem.text(0)[6:])-1, select_list1))
                        select_list2 = ["ability1", "ability2", "ability3", "ability4"]
                        menu.addAction("Check Only Ability", lambda:self.QMenuCheckSelected(int(WidgetItem.text(0)[6:])-1, select_list2))
                menu.exec()
                
            else:
                menu.addAction("Check", lambda:self.QMenuCheckOne(WidgetItem, Qt.Checked))
                menu.addAction("UnCheck", lambda:self.QMenuCheckOne(WidgetItem, Qt.Unchecked))
                menu.exec()
                    
        elif(len(self.treeWidget.selectedItems()) > 1):
            for item in WigetList: #TopLevel Item Exsist??
                if(item.parent() == None): 
                    return False
            
            menu.addAction("Check", lambda:self.QMenuCheckList(WigetList, Qt.Checked))
            menu.addAction("UnCheck", lambda:self.QMenuCheckList(WigetList, Qt.Unchecked))
            menu.exec()
        else:
            return False
        
    def QMenuCheckSelected(self, search_num, select_list):
        for i in range(self.col_cnt):
            if(self.treelist[search_num].child(i).text(0) in select_list):
                self.treelist[search_num].child(i).setCheckState(1, Qt.Checked)
            else:
                self.treelist[search_num].child(i).setCheckState(1, Qt.Unchecked)
            
    def clearSelection(self):
        print("clearSelection")
    
    def QTreeWidgetItemChanged(self, WidgetItem, col):
        #print("col : %d"% col)
        if (col == 1):
            if(WidgetItem.checkState(col) == Qt.Checked):
                WidgetItem.setBackground(0, QColor(255, 255, 0, 100))
                WidgetItem.setBackground(1, QColor(255, 255, 0, 100))
            else:
                WidgetItem.setBackground(0, QColor(255, 255, 255))
                WidgetItem.setBackground(1, QColor(255, 255, 255))

    def Search_Text_Clicked(self):
        print( "SearchCnt : %d\nColumn Cnt : %d"%(self.searchCount, self.col_cnt))
        #Search Cnt 0 case
        if(self.searchCount == 0):
            print("default search Mode")
            txt, ok = QInputDialog.getText(self, 'InputWindow', 'Search Text')
            if ok and txt!=None:
                self.searchCountBox.setValue(1)
                self.treelist[0].setText(2, txt)
                self.QMenuCheckAll(0, Qt.Checked)
            else:
                return False
                
            #return False
        #Check EmptyText
        for i in range(self.searchCount):
            if(self.treelist[i].text(2) == ""):
                self.MessageBox("Search%d Text is Empty"%(i+1))
                return False
        #Checked item is not exist 
        first_col = None
        log = "Search Sequence"+str(self.searchExeCnt+1)+"\n"
        for num in range(self.searchCount):
            check_cnt = 0
            log = log+self.treelist[num].text(2)+"("
            for i in range(self.col_cnt):
                if(self.treelist[num].child(i).checkState(1) == Qt.Checked): #Check Status
                    check_cnt+=1
                    log += str(i+1)+","
                    if(check_cnt ==1):
                        first_col = i
            log += ") TOTAL: "
            if(check_cnt == 0):
                self.MessageBox("Search%d Column is not Selected"%(num+1))
                return False
                
        #Get Operator
        operator_list = []
        for i in range(self.searchCount):
            if(i>0):
                print("%d : %s"%(i+1, self.bttnConditionlist[i].text() ))
                operator_list.append(self.bttnConditionlist[i].text())
                log=log.replace("TOTAL:", self.bttnConditionlist[i].text(),1)
        
        sql = "SELECT * FROM `pokecard`.`%s` WHERE "%self.DBTableNow
        
        for num in range(self.searchCount):
            txt = self.treelist[num].text(2)
            sql += "("
            for i in range(self.col_cnt):
                if(self.treelist[num].child(i).checkState(1) == Qt.Checked): #Check Status
                    sql+="%s LIKE \"%%%s%%\" OR "%(self.col_list[i],txt)
            sql = sql[:-3] + ")"
            if(num < self.searchCount-1): #Final loop don't need Operator
                sql += operator_list[num]
        
        #print(sql)
        res = self.DB_SendQuery(sql)
        self.QTableUpdateList(res)
        
        log += str(len(res))+"\n"
        log = log.replace(",)",")")
        #print(log)
        self.textBrowser.append(log)
        self.searchExeCnt += 1
        
        self.tabWidget.setCurrentIndex(1)
        
        self.tableWidget.scrollToItem(self.tableWidget.item(0, first_col) , QAbstractItemView.PositionAtCenter)
    

    #def QTextBrowserAddLog(self, ResultCount):
        #str = 
        #self.textBrowser.append()
        
    def Connect_Clicked(self):
        #self.MessageBox("Connect_Clicked!!")
        try:
            self.conn = mysql.connector.connect(**config)
            print(self.conn)
            self.cursor=self.conn.cursor()
            self.DBGetTableList() # Update DB List
            self.DBTableSelect()
            #PokeScore(self.SendALL_DB())
            
        except mysql.connector.Error as err:
            print(err)
            self.MessageBox(err)

    def DBUpdateFromExcel(self):
        print ("LOAD_JP")
        self.r_fileName = QFileDialog.getOpenFileName(self, self.tr("Open Data files"), ",/", self.tr("Data Files (*.csv *.xls *.xlsx);; All Files(*.*)"))
        print(self.r_fileName[0])
        if(self.r_fileName[0] == ""): #Cancel Select case
            self.MessageBox('Please Select Excel File Again')
            return False

        self.QProgressStart("Now Loading...")

        #TODO RUN THREAD
        self.r_data = EXCEL_DATA(self.r_fileName[0]) #Excel Load Fail Case
        if(self.r_data == None):
            self.MessageBox("Load Fail!!\nPlease check the file")
            self.QProgressClose()
            return False

        sql = "SELECT * FROM `pokecard`.`%s`"%(self.DBTableNow) 
        DB_DATA = self.DB_SendQuery(sql) # Return List[Tuple()]
        
        Seperator = False
        if(self.DBTableNow == "cardinfo"):
            Seperator = True
        #res=self.r_data.GetNonRedundantData(DB_DATA, fieldSeperator=Seperator)
        self.r_data.SetRedundantData(self.col_cnt , DB_DATA, fieldSeperator=Seperator)
        self.r_data.NonRedundantList.connect(self.DBGetRedundantList)
        self.r_data.start()
        #CHECK MSG FROM THREAD
        while (self.RedundantList == None):
            QtTest.QTest.qWait(100) #Wait 100ms
        
        res = self.RedundantList
        self.RedundantList = None

        if(res[0] == "WRONG_FILE"):
            #LIST FAIL
            self.MessageBox("Column Size is not Matched to DataBase!!!")
        else:
            #LIST OK
            self.QTableAddRow(cnt=len(res))
            self.QTableUpdateList(res, ClearList=False, DeleteSeperator=False)
            self.tabWidget.setCurrentIndex(1)
        
        self.ProgWindow.terminate()
        self.ProgCloseSig.emit(QEvent(QEvent.Close))
        
        self.r_data.terminate()
        self.r_data = None

    @pyqtSlot(list)
    def DBGetRedundantList(self, getlist):
        self.RedundantList = getlist

    def DBGetTableList(self):
        sql = 'SELECT * FROM `information_schema`.`TABLES` WHERE TABLE_SCHEMA = "pokecard"'
        resultList=self.DB_SendQuery(sql)
        for row in range(len(resultList)):
            self.DBtablelist.append(resultList[row][2])

    def DBTableSelect(self, Select=False):
        if(Select==False):
            ok = True
            select = "cardinfo"
        else:
            select, ok = QInputDialog.getItem(self, "Table Select", "Please Select DataBase", self.DBtablelist, 0, False)
        if ok:
            self.DBTableNow = select
            self.initQTableAction()
            self.QTableUpdateColumn()
            self.QTreeSearchCountEnable()
            self.treeWidget.setEnabled(True)
            self.QMenuEnableALL(self.menuTable ,True)
            self.QMenuEnableALL(self.menuSearch ,True)
            self.actionConnect_To_DataBase.setEnabled(False)
            self.actionLoad_Table_For_Update.setEnabled(True)
            self.actionSelect_Table.setEnabled(True)
            self.textBrowser.setEnabled(True)
            
            print("Connect OK")
            self.MessageBox("Connected!!!")
        #DB Select Case AddList Initialize
        self.tableAddList = []
        self.tableUpdateList = []
        
    def SendALL_DB(self):
        print("SendALLDB")
        resultList = self.DB_SendQuery("SELECT * FROM `pokecard`.`%s` LIMIT 100000;")%self.DBTableNow
        self.max_cnt = len(resultList)
        input_string = ""
        
        #CSV OUT
        for row in range(self.max_cnt):
            for col in range(self.col_cnt):
                input_string += resultList[row][col][1:-1] + ","
            input_string += "\n"
        
        return input_string

    def QMenuUpdate(self, SearchCnt):
        start = self.menuSearchCount
        update = SearchCnt
        if(start == update):
            return False
        
        #print("Start:%d , Update:%d"%(start,update))
        if(abs(start-update)!=1):
            if(update>start):#add
                for i in range(start+1, update):
                    #print(i)
                    self.QMenuUpdate(i)
                start = update-1
            else:#delete
                for i in range(start-1, update, -1):
                    #print(i)
                    self.QMenuUpdate(i)
                start = update+1
        
        #print("start : %d , update : %d "%(start,update))
        self.menuSearchCount = update
        
        if(update > start):
            self.menuList.append(self.menuSearch_Select.addMenu("Search"+str(SearchCnt)))
            self.menuList[update-1].addAction("Select ALL").triggered.connect(lambda:self.QMenuCheckAll(update-1, Qt.Checked))
            self.menuList[update-1].addAction("UnSelect ALL").triggered.connect(lambda:self.QMenuCheckAll(update-1, Qt.Unchecked))
        else:
            self.menuList[start-1].clear()
            self.menuList[start-1].setEnabled(False)
            self.menuList[start-1].deleteLater()
            del self.menuList[start-1]
        
            
    def QMenuCheckAll(self, search_num, Check):
        print("Search : %d , Check : %d"%(search_num, Check))
        for i in range(self.col_cnt):
            self.treelist[search_num].child(i).setCheckState(1, Check)
    
    def QMenuCheckOne(self, WidgetItem, Check):
        WidgetItem.setCheckState(1, Check)
    
    def QMenuCheckList(self, WidgetList, Check):
        for item in WidgetList:
            item.setCheckState(1, Check)

    def QTreeSearchCountEnable(self):
        if(self.searchCount != 0):
            print("SearchCount : ", self.searchCount)
            for cnt in range (self.searchCount, -1,-1):
                print("TreeWidgetUpdate:", cnt)
                self.QTreeWidgetUpdate(cnt)
        self.treeWidget.clear()
        WidgetItem = QTreeWidgetItem(self.treeWidget)
        WidgetItem.setText(0, "Search Count")
        self.searchCountBox = QSpinBox()
        self.searchCountBox.setAlignment(Qt.AlignHCenter)
        self.searchCountBox.valueChanged.connect(self.QTreeWidgetUpdate)
        self.searchCountBox.valueChanged.connect(self.QMenuUpdate)
        self.searchCountBox.setRange(0, 10) #Min 0 Max 10
        self.treeWidget.setItemWidget(WidgetItem,1,self.searchCountBox)
        self.treeWidget.addTopLevelItem(WidgetItem)
    
    def QTreeSetTextBttnClicked(self, index):
        txt, ok = QInputDialog.getText(self, 'InputWindow', 'Search Text', QLineEdit.Normal,self.treelist[index-1].text(2))
        if ok:
            self.treelist[index-1].setText(2, txt)
    
    def QMenuEnableALL(self, qmenu ,on_off):
        qmenu.setEnabled(on_off)
        action_list=qmenu.actions()
        for action in action_list:
            action.setEnabled(on_off)
    
    def QTreeWidgetUpdate(self, SearchCnt):
        start = self.searchCount 
        update = SearchCnt
        if(start == update):
            return False
        
        #print("Start:%d , Update:%d"%(start,update))
        if(abs(start-update)!=1):
            if(update>start):#add
                for i in range(start+1, update):
                    #print(i)
                    self.QTreeWidgetUpdate(i)
                start = update-1
            else:#delete
                for i in range(start-1, update, -1):
                    #print(i)
                    self.QTreeWidgetUpdate(i)
                start = update+1
                
        
        self.searchCount = update
        #print("start : %d , update : %d "%(start,update))
        if(start > update): #Remove 
            #print("remove")
            self.treeWidget.takeTopLevelItem(start)
            #print(self.treelist)
            #print("Delete : %d"% (start-1))
            del self.treelist[start-1]
            del self.bttnTextlist[start-1]
            del self.bttnConditionlist[start-1]
        else: #ADD
            WidgetItem = QTreeWidgetItem(self.treeWidget)
            WidgetItem.setText(0, "Search"+str(update))
            
            parent=QWidget()
            layout=QHBoxLayout(parent)
            layout.setContentsMargins(0,0,0,0)
            layout.setSpacing(0)
            
            btn = QPushButton("AND")
            if(update > 1): #Search 1 don't need AND OR Button
                layout.addWidget(btn)                
            self.bttnConditionlist.append(btn)
            self.bttnTextlist.append(QPushButton("Set Text"))

            layout.addWidget(self.bttnTextlist[update-1])
            self.bttnConditionlist[update-1].clicked.connect(lambda:self.QTreeSetConditionBttnClicked(self.bttnConditionlist[update-1]))
            self.bttnTextlist[update-1].clicked.connect(lambda:self.QTreeSetTextBttnClicked(update))
            self.treeWidget.setItemWidget(WidgetItem,1, parent)
            self.treeWidget.insertTopLevelItem(update,WidgetItem)
            self.treelist.append(WidgetItem)
            
            for item in self.col_list:
                Child = QTreeWidgetItem(self.treeWidget.topLevelItem(update))
                Child.setText(0, item)
                Child.setCheckState(1, Qt.Unchecked)
                self.treeWidget.topLevelItem(0).addChild(Child)
        
    def QTreeSetConditionBttnClicked(self, bttn):
        text = bttn.text()
        if(text == "AND"):
            bttn.setText("OR")
        else:
            bttn.setText("AND")
    def QTableItemSelectionChanged(self):
        range_t = self.tableWidget.selectedRanges()
        #print(range_t)
        #print(range_t[0].rowCount(), range_t[0].columnCount())
        if(range_t == []):
            return False
        RowCnt = range_t[0].rowCount()
        ColCnt = range_t[0].columnCount()
        
        if(RowCnt < self.tableWidget.rowCount() and ColCnt < self.tableWidget.columnCount()): #select item Case
            #print("Select Item")
            if(self.HideColumnAction in self.tableWidget.horizontalHeader().actions()):
                self.tableWidget.horizontalHeader().removeAction(self.HideColumnAction)
                self.tableWidget.horizontalHeader().removeAction(self.ShowColumnAction)
            if(self.rowUpdateDbAction in self.tableWidget.verticalHeader().actions()):
                self.tableWidget.verticalHeader().removeAction(self.rowUpdateDbAction)
            #Chnage Ctrl+C Action (Column -> item)
            self.QTableCopyActionShortCutInit()
            self.copy_action.setShortcut('Ctrl+C')
        elif(RowCnt == self.tableWidget.rowCount() and ColCnt == self.tableWidget.columnCount()): #select ALL Case
            #print("Select ALL")
            if(self.HideColumnAction in self.tableWidget.horizontalHeader().actions()):
                self.tableWidget.horizontalHeader().removeAction(self.HideColumnAction)
                self.tableWidget.horizontalHeader().removeAction(self.ShowColumnAction)
            if(not(self.rowUpdateDbAction in self.tableWidget.verticalHeader().actions())): #DB update Action ADD 
                self.tableWidget.verticalHeader().addAction(self.rowUpdateDbAction)
            self.QTableCopyActionShortCutInit()
            self.copy_action.setShortcut('Ctrl+C') #Cell Right Button
        elif(RowCnt == self.tableWidget.rowCount()): # column selected
            if(self.rowUpdateDbAction in self.tableWidget.verticalHeader().actions()):
                self.tableWidget.verticalHeader().removeAction(self.rowUpdateDbAction)
            left = range_t[0].leftColumn()
            Right = range_t[0].rightColumn()
            self.tableWidget.horizontalHeader().addAction(self.HideColumnAction)
            self.tableWidget.horizontalHeader().addAction(self.ShowColumnAction)
            select = []
            for i in range(left, Right+1):
                select.append(self.col_list[i])
            receiversCount = self.HideColumnAction.receivers(self.HideColumnAction.triggered)
            if(receiversCount > 0):
                self.HideColumnAction.triggered.disconnect()
                self.ShowColumnAction.triggered.disconnect()
            self.HideColumnAction.triggered.connect(lambda: self.QTableHideSelected(select))
            self.ShowColumnAction.triggered.connect(lambda: self.QTableShowSelected(select))
            self.QTableCopyActionShortCutInit()
            self.colcopyAction.setShortcut('Ctrl+C')
        elif(ColCnt == self.tableWidget.columnCount()): # Row Selected
            self.tableWidget.verticalHeader().addAction(self.rowUpdateDbAction)
            self.QTableCopyActionShortCutInit()
            self.rowcopyAction.setShortcut('Ctrl+C')
            

    def QTableCopyActionShortCutInit(self):
        self.copy_action.setShortcut(QKeySequence())
        self.rowcopyAction.setShortcut(QKeySequence())
        self.colcopyAction.setShortcut(QKeySequence())
    
    def QTableShowCurrentRow(self):
        row=self.tableWidget.currentRow()
        if(self.tableWidget.horizontalHeaderItem(0).text() == "CardNum"):
            if(self.tableWidget.item(row,0) != None):
                CardNum = self.tableWidget.item(row,0).text()
                if(CardNum != ""):
                    print("Find CardNum!!! : %s "%CardNum)
                    self.CardWindow.setInputText(CardNum)
                    self.CardWindow.btn_clicked()                    
                    self.CardWindow.show()
                    self.CardWindow.activateWindow()

    def QTableRowOpenJPUrl(self):
        row=self.tableWidget.currentRow()
        if(self.tableWidget.item(row,53) != None ):
            CardNum = self.tableWidget.item(row,53).text()
            if(CardNum != "" and CardNum != "0" and CardNum != "Series" and CardNum != "empty"):
                print("Find CardNum!!! : %s "%CardNum)
                webbrowser.get(chrome_path).open('https://www.pokemon-card.com/card-search/details.php/card/'+CardNum+'/regu/alL')


    def QTableRowOpenUrl(self):
        row=self.tableWidget.currentRow()
        if(self.tableWidget.item(row,0) != None):
            CardNum = self.tableWidget.item(row,0).text()
            if(CardNum != ""):
                print("Find CardNum!!! : %s "%CardNum)
                webbrowser.get(chrome_path).open('https://pokemoncard.co.kr/cards/detail/'+CardNum)
            
    
    def QTableSearchJPCard2(self):
        print("Search JP Card!!")
        #start = time.time()  # 시작 시간 저장
        row=self.tableWidget.currentRow()
        Series = self.tableWidget.item(row,45).text()

        JPPageNo = self.tableWidget.item(row,53).text()
        IsHaveJPNo = True
        print("JPPageNo:", JPPageNo)
        for i in JPPageNo:
            if(ord(i) >= ord('0') and ord(i) <= ord('9')):
                pass
            else:
                print("JP PAGE No ss not exist in DataBase!!")
                IsHaveJPNo = False
                break
        if( JPPageNo == "0"):
            IsHaveJPNo = False
        if IsHaveJPNo:
            link = "https://www.pokemon-card.com/assets/images/card_images/large/"+self.tableWidget.item(row,54).text()
            print(link)
            self.jpCardWindow.LoadImage(link)
            self.jpCardWindow.show()
            return True
        print("333")

        sql = 'SELECT * FROM `pokecard`.`series` WHERE KRSeries LIKE "'+Series+'"'
        res=self.DB_SendQuery(sql)
        pageNo = 0
        if(len(res)>0):
            print("MAIN PAGE NO: %s, JPN: %s, KOR: %s "%(res[0][0],res[0][1],res[0][2]))
            pageNo = res[0][0]

        typelist = ["ALL","POKEMON", "TRAINERS", "ENERGY"]
        CardType = typelist[int(self.tableWidget.item(row,5).text()[0])]
        print("CardType:%s\nSeries : %s\n"%(CardType,Series))       

        kor_name = self.tableWidget.item(row,7).text()
        print("MAIN", kor_name)
        jpname=self.SearchJPNameFromDB(self.GetOriginalName(kor_name)) # GET JPNAME From DataBase

        print("jpname :", jpname)
        if(jpname == None): #Find JP name Fail
            msg = "Can't Find JP Name\n"
            msg+= ("KOR:%s , JP:%s, SERIES:%s"%(kor_name, jpname, Series))
            self.MessageBox(msg)
            print("MAIN : FAIL FOUND JP NAME\n")
            return None
        
        if(self.BrowserRunning == False): #CurrentCard is Not Exsist - Need to luanch WebBrowser
            self.jpCard = GetJPCard.JPCard()
            self.jpCard.progress.connect(self.jpCardWindow.ProgressBar.setValue)
            self.jpCard.sendlist.connect(self.JPBrowserUrlListSignalSlot) #QThread -> Main (Search Result Msg)
            self.jpCard.init.connect(self.JPBrowserInitSignalSlot) #QThread -> Main (Browser Init Msg)
            self.firstsig.connect(self.jpCard.getFirstSigSlot) #Main -> QThread (First Search Msg)
            self.sig_killbrowser.connect(self.jpCard.closeBrowser) #Main -> QThread (Kill Brower Msg)
            self.request_url.connect(self.jpCard.getCardListSlot) #Main -> QThread (Search Again Msg)
            print("Main : Thread Start")
            self.jpCardWindow.show()#For ProgressBar Show First
            self.jpCard.start()
            firstsig = [jpname,CardType, Series, pageNo, HIDE_BROWSER] # [CARDNAME, CARDTYPE, SERIES, PageNo ,HIDE_BROWSER]
            print("MAIN : SEND First SIGNAL!!")
            self.firstsig.emit(firstsig) 
            #self.firstsig.emit(firstsig) #Prevent to RcvFail
        else: #Search Again (WebBrowser Already Loaded)
            print("Main : Send Signal List")
            self.request_url.emit([jpname, CardType, Series, pageNo])
        print("MAIN : FINISH REQUEST\n")
        
    @pyqtSlot(bool)
    def JPBrowserInitSignalSlot(self, isinit):
        print("Main : Get Init Signal ")
        if isinit: #QThread Running
            print("Main : Init OK")
            self.BrowserRunning = True
        else: #Fail to Load
            print("Init Fail")
            self.jpCard.terminate()
            self.jpCard = None
            self.BrowserRunning = False
            
    
    @pyqtSlot(list)
    def JPBrowserUrlListSignalSlot(self, link):
        print("Main : Get URL List ")
        if (len(link)>0):
            if(len(link) == 1):
                self.jpCardWindow.SetImageList(link)
                
            else: #More than 2
                msg = "Please Check Card List!!"
                self.MessageBox(msg)
                self.jpCardWindow.SetImageList(link)
            self.jpCardWindow.show()
            self.jpCardWindow.activateWindow()
        else:
            msg = "Can't Find Proper Link!\n"
            row=self.tableWidget.currentRow()
            msg += "Series: %s"%self.tableWidget.item(row,45).text()
            self.MessageBox(msg)

    def QTableSearchJPName(self):
        print("QTableSearchJPName")
        row=self.tableWidget.currentRow()
        kor_name = self.tableWidget.item(row,7).text()
        #print(kor_name) 
        print(self.GetOriginalName(kor_name))
        jpname=self.SearchJPNameFromDB(self.GetOriginalName(kor_name))
        self.MessageBox(jpname)

    def GetOriginalName(self,kor_name):
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

    def QMenuSearchJPName(self):
        print("QMenuSearchJPName")
        kor_name, ok = QInputDialog.getText(self, 'InputWindow', 'Search Text')
        if ok:
            jpname=self.SearchJPNameFromDB(self.GetOriginalName(kor_name))
            self.MessageBox(jpname)

    def SearchJPNameFromDB(self, kor_name):
        sql = "SELECT * FROM `pokecard`.`name` WHERE KOR LIKE \"" + kor_name +'"'
        res = self.DB_SendQuery(sql)
        
        if(len(res)>0):
            print("JP : %s, KOR: %s"%(res[0][0],res[0][1]))
            return res[0][0]
        else:
            return None

    def QTableCellMarking(self):
        txt, ok = QInputDialog.getText(self, 'InputWindow', 'Search Text')
        if ok:
            self.QTableCellChangeSetEnable(False)
            color = QColorDialog.getColor()
            color.setAlpha(100)
            allitems = self.tableWidget.findItems("", Qt.MatchContains)
            selected_items = self.tableWidget.findItems(txt, Qt.MatchContains)
            for item in allitems:
                if item in selected_items:
                    item.setBackground(color)
            self.QTableCellChangeSetEnable(True)
    
    def QTableCellChangeSetEnable(self, isOn):
        if isOn:
            self.tableWidget.cellChanged.connect(self.QTableCellChanged)
        else:
            receiversCount = self.tableWidget.receivers(self.tableWidget.cellChanged)
            if receiversCount > 0:
                self.tableWidget.cellChanged.disconnect()


    def QTableTextMarking(self):
        txt, ok = QInputDialog.getText(self, 'InputWindow', 'Search Text')
        if ok:
            self.QTableCellChangeSetEnable(False)
            color = QColorDialog.getColor()
            global gMarkTextColor 
            gMarkTextColor = color
            allitems = self.tableWidget.findItems("", Qt.MatchContains)
            selected_items = self.tableWidget.findItems(txt, Qt.MatchContains)
            for item in allitems:
                if item in selected_items:
                    item.setForeground(color)
                    #item.setData(Qt.UserRole, txt if item in selected_items else None)
            self.QTableCellChangeSetEnable(True)
                
    def QTableCellMarkingClear(self):
        allitems = self.tableWidget.findItems("", Qt.MatchContains)
        self.QTableCellChangeSetEnable(False)
        for item in allitems:
            if(item != None):
                item.setBackground(QColor(255,255,255))
        self.QTableCellChangeSetEnable(True)
                
    def QTableTextMarkingClear(self):
        global gMarkTextColor 
        gMarkTextColor = QColor(0,0,0)
        allitems = self.tableWidget.findItems("", Qt.MatchContains)
        self.QTableCellChangeSetEnable(False)
        for item in allitems:
            if(item != None):
                item.setForeground(QColor(0,0,0))
        self.QTableCellChangeSetEnable(True)
    
    def QTableUpdateList(self,resultList, UpdateEvent=False, ClearList=True, DeleteSeperator=True):
        self.max_cnt = len(resultList)
        self.tableWidget.setRowCount(self.max_cnt)        
        self.QTableCellChangeSetEnable(UpdateEvent)
        for row in range(self.max_cnt):
            for col in range(self.col_cnt):
                #cardinfo data from Excelfile don't need to delete ""
                if (self.DBTableNow == "cardinfo" and DeleteSeperator == True): 
                    self.tableWidget.setItem(row, col, QTableWidgetItem(resultList[row][col][1:-1]))
                else:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(resultList[row][col]))
        self.QTableCellChangeSetEnable(not(UpdateEvent))
        if(ClearList == True):
            self.tableAddList = [] #Init Added List 
            self.tableUpdateList = [] #Init Update List
    
    def QTableUpdateColumn(self):
        sql="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='%s'"%self.DBTableNow
        resultList=self.DB_SendQuery(sql) # return : list [ tuple() ] 
        self.col_cnt = len(resultList)
        self.col_list = []
        self.tableWidget.setColumnCount(self.col_cnt)        
        for i in range(self.col_cnt):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(resultList[i][0]))
            self.col_list.append(resultList[i][0])
        self.tableWidget.setRowCount(0)    
    
    def Search_Clicked(self):
        txt = self.lineEdit.text()
        print(txt)
        sql = "SELECT * FROM `pokecard`.`%s` WHERE "%self.DBTableNow
        #print(self.col_cnt)
        #print(self.col_list)
        for i in range(self.col_cnt):
            sql+="%s LIKE \"%%%s%%\" OR "%(self.col_list[i],txt)

        sql=sql[:-3]
        self.QTableUpdateList(self.DB_SendQuery(sql))
    
    def DB_SendQuery(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def DB_UpdateQuery(self, sql, disableMessage=False):
        self.cursor.execute(sql)
        self.conn.commit()
        if(disableMessage == False):
            self.MessageBox("Update Finish!!")

    
    def ConverterFinishCheck(self):
        while True:
            QtTest.QTest.qWait(200)
            if(self.isFinish == True):
                break
        
        self.isFinish = False
        if(self.r_JPdata == None):
            return False
            print("[MainWindow] Get Load Fail Msg!!")
        print("[MainWindow] Get Finish Msg!!")
        return True
    
    def Convert_Load_JP_Clicked(self):
        print ("LOAD_JP")
        self.r_JPfileName = QFileDialog.getOpenFileName(self, self.tr("Open Data files"), ",/", self.tr("Data Files (*.csv *.xls *.xlsx);; All Files(*.*)"))
        print(self.r_JPfileName[0])
        if(self.r_JPfileName[0]==""):
            return False
        
        self.Converter  = Pokecard_Converter.ConverterThread()
        self.ConvertMsg.connect(self.Converter.ConvertMsgSlot) #Mainwindow -> Thread
        self.Converter.isFinish.connect(self.ConvertGetMsg) #Thread -> Mainwindow
        self.Converter.start()
        if(self.ConvertSendMsgProgressWait("Now Loading...", ["LOAD", self.r_JPfileName[0]]) == False):
            self.ConvertMsg.emit(["FINISH"])
            self.ConverterFinishCheck()
            self.Converter.terminate()
            self.r_JPfileName = None
            self.MessageBox("Wrong JP-File Format!!")
            return False
        self.pushButton_Cvt_KR.setEnabled(True)
        self.pushButton_Cvt_Txt.setEnabled(True)
        print("[MainWindow] Load JP Finish!!")

    
    def Convert_KR_Clicked(self):
        self.ConvertSendMsgProgressWait("Converting Now...", ["CVT_KR"])
        print("[MainWindow] Convert KR Finish!!")
        self.MessageBox("Please Check [ORG_NAME]_KOR.xlsx")
    
    def Convert_Txt_Clicked(self):
        self.ConvertSendMsgProgressWait("Converting Now...", ["CVT_TXT"])
        print("[MainWindow] Convert TXT Finish!!")
        self.MessageBox("Convert Finish!!\nPlease Check Txt File")

    def ConvertSendMsgProgressWait(self,txtSet, Msg):
        self.QProgressStart(txtSet)
        self.ConvertMsg.emit(Msg)
        if(self.ConverterFinishCheck() == False):
            self.QProgressClose()
            return False
        self.QProgressClose()
        return True
    
    @pyqtSlot(list)
    def ConvertGetMsg(self, finishMsg):
        print("[MainWindow] GET Finish Msg", finishMsg)
        self.isFinish = finishMsg[0]
        if(len(finishMsg)>1):
            self.r_JPdata = finishMsg[1]  #After Load get read data
        

    def MessageBox(self,msg):
        w = QWidget()
        Mbox=QMessageBox(w)
        Mbox.setWindowTitle("Message")
        Mbox.setWindowIcon(QIcon("Pokemon.ico"))
        Mbox.setStyleSheet("messagebox-text-interaction-flags : 5;")
        Mbox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        Mbox.setText(msg)
        w.move(self.pos().x()+(self.width()-w.width())/2,self.pos().y()+(self.height()-w.height())/2)
        Mbox.exec()

    
    def resizeEvent(self,event):
        h = self.height()
        w = self.width()
        self.tabWidget.resize(w-20,h-40)
        self.treeWidget.resize(w-26,h-80)
        self.tableWidget.resize(w-26,h-80) #Table Resize
        self.textBrowser.resize(w-26,h-80) #Table Resize        
    
    def copySelection(self):
        print("copySelection!!!!")
        print("Thread Info: %s, %s"%(QThread.currentThread(), QThread.currentThreadId()))
        selection = self.tableWidget.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [['']*colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            cb = QApplication.clipboard()
            #IMPORTANT!!! ToAcCess Clipboard Write From MainWindow 
            cb.clear(mode=cb.Clipboard )
            cb.setText(stream.getvalue(), mode=cb.Clipboard)
            #print("---------------Clipboard Data--------------")
            #print(cb.mimeData().text())
            #print("--------------------END---------------------")
            

class QSignalSender(QObject):
    sigmain = pyqtSignal(int)
    def __init__(self,name):
        QObject.__init__(self) 
        self.name = name #
        self.alive = True
    def ConnectSlot(self, slot):
        self.sigmain.connect(slot)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = PokeDBWindow()
    demoWindow.setWindowTitle("PokeCard DataBase")
    demoWindow.setWindowIcon(QIcon('Pokemon.ico'))
    demoWindow.show() 
    # w = QProgressPopup(0,0, txt = "Now Loading")
    # w.start()
    # main = QSignalSender("MAIN")
    # main.ConnectSlot(w.ProgressBar.setValue)
    # cnt = 0

    # while True:
    #     #main.sigmain.emit(cnt)
    #     QtTest.QTest.qWait(15)
    #     print("MainLoop : ", cnt)
    #     cnt+=1
    #     if(cnt == 101):
    #         w.terminate()
    #         break


    
    app.exec_()
    
