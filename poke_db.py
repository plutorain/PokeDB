# -*- coding:utf-8 -*-
import mysql.connector

#QT GUI
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic 
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QSize
form_class = uic.loadUiType("PokeDBWindow.ui")[0]

#WEB BROWSER
import webbrowser

#Copy Clipboard
import io
import csv

#PokeCard Browser
import Poke_Card


try:
    from html import escape
except ImportError:
    from cgi import escape

#from html.parser import HTMLParser
from bs4 import BeautifulSoup


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


#DB 접속정보를 dict type 으로 준비한다.
config={
        "user":"root",
        "password":"1234",
        "host":"127.0.0.1",   
        "database":"pokecard",
        "port":3306
    }


'''    
gMarkTextColor = QColor("orange")
class HTMLDelegate(QStyledItemDelegate):
    def __init__(self, color ,parent=None):
        super(HTMLDelegate, self).__init__(parent)
        self.doc = QTextDocument(self)
        
    def paint(self, painter, option, index):
        substring = index.data(Qt.UserRole)
        painter.save()
        
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        res = ""
        global gMarkTextColor
        color = gMarkTextColor
        if(substring != None):
            doc = QTextDocument(self)
            doc.setHtml(options.text)
            html = doc.toHtml()
            print("------------------")
            print("option text %s"%options.text)
            
            
            print("-----------------------Original------------------------")
            print(html)
            print("--------------------------------------------------------")
            #parser = HTMLParser()
            #parser.feed(html)
            print("Take Text1:")
            soup = BeautifulSoup(html)
            print(soup.p) 
           
            
        if substring:
            substrings = options.text.split(substring)
            #print(substrings)
            res = """<font color="{}">{}</font>""".format(
                color.name(QColor.HexRgb), substring
            ).join(list(map(escape, substrings)))
        else:
            res = escape(options.text)
        if(substring != None):
            print("Res:")
            print(res)
            
            #print(self.doc.toHtml())
        self.doc.setHtml(res)
        if(substring != None):
            print("Final html:")
            print(self.doc.toHtml())
        

        options.text = ""
        style = (
            QApplication.style()
            if options.widget is None
            else options.widget.style()
        )
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        ctx = QAbstractTextDocumentLayout.PaintContext()
        if option.state & QStyle.State_Selected:
            ctx.palette.setColor(
                QPalette.Text,
                option.palette.color(
                    QPalette.Active, QPalette.HighlightedText
                ),
            )
        else:
            ctx.palette.setColor(
                QPalette.Text,
                option.palette.color(QPalette.Active, QPalette.Text),
            )

        textRect = style.subElementRect(QStyle.SE_ItemViewItemText, options)

        if index.column() != 0:
            textRect.adjust(5, 0, 0, 0)

        thefuckyourshitup_constant = 4
        margin = (option.rect.height() - options.fontMetrics.height()) // 2
        margin = margin - thefuckyourshitup_constant
        textRect.setTop(textRect.top() + margin)

        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        self.doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        #print("resize")
        return QSize(self.doc.idealWidth(), self.doc.size().height())
'''  
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
    
class PokeDBWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #QTable Initial Size
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(10)
        
        #DataBase
        self.conn = None
        self.cursor = None
        self.col_cnt = 10
        self.col_list = []

        #QTable
        self.initQTableAction()
        
        #copy_action.setShortcut('Ctrl+C')
        self.max_cnt = 0
        #self.tableWidget.setItemDelegate(HTMLDelegate(self.tableWidget))

        #Menu
        self.menuSearchCount = 0
        self.actionConnect_To_DataBase.triggered.connect(self.Connect_Clicked)
        self.actionSearch_Text.triggered.connect(self.Search_Text_Clicked)
        self.menuList = []
        self.menuActionList = []
        
        self.actionCell_Marking.triggered.connect(self.QTableCellMarking)
        self.actionClearCell_Marking.triggered.connect(self.QTableCellMarkingClear)
        self.actionText_Marking.triggered.connect(self.QTableTextMarking)
        self.actionClear_Text_Marking.triggered.connect(self.QTableTextMarkingClear)
        
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
        self.CardWindow.setWindowTitle("PokeCard Viewer")
        self.CardWindow.setWindowIcon(QIcon("Pokemon.ico"))
        
    
    
    def initQTableAction(self):
        #Url Open duble click!
        self.tableWidget.cellDoubleClicked.connect(self.QTable_CellDoubleClicked)
        
        #Table Right Button Menu
        self.tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        copy_action = QAction("Copy", self.tableWidget) 
        url_action = QAction("Open Current Row Card Page", self.tableWidget) 
        self.tableWidget.addAction(copy_action) 
        self.tableWidget.addAction(url_action)
        
        copy_action.triggered.connect(self.copySelection)
        url_action.triggered.connect(self.QTableRowOpenUrl)
        url_action.setShortcut('Ctrl+O')
        
        #Range Selection Event
        self.tableWidget.itemSelectionChanged.connect(self.QTableItemSelectionChanged)
        
        #Table Column Label Right Button Menu
        col_header = self.tableWidget.horizontalHeader()
        col_header.setContextMenuPolicy(Qt.ActionsContextMenu)
        colcopyAction       = QAction("Copy", col_header)
        abilityshow_action  = QAction("Hide ALL Column Except Ability", col_header) 
        abilitylabel_action = QAction("Hide ALL Column Except Ability_Label", col_header) 
        abilityshow_all     = QAction("Show ALL Column", col_header)
        
        col_header.addAction(colcopyAction)
        col_header.addAction(abilityshow_action)
        col_header.addAction(abilitylabel_action)
        col_header.addAction(abilityshow_all) 
        
        select_list = ["ability1", "ability2", "ability3", "ability4"]
        abilityshow_action.triggered.connect(lambda:self.QTableShowOnlySelected(select_list))
        select_list2 = ["ability_label1", "ability_label2", "ability_label3", "ability_label4"]
        abilitylabel_action.triggered.connect(lambda:self.QTableShowOnlySelected(select_list2))
        abilityshow_all.triggered.connect(self.QTableShowALLCol)
        colcopyAction.triggered.connect(self.copySelection)
        
        #Variable Action by QtableSelectionChanged
        self.HideColumnAction = QAction("Hide Selected Column", self.tableWidget)
        self.ShowColumnAction = QAction("Show Selected Column", self.tableWidget)
        self.HideColumnAction.triggered.connect(self.QTableHideSelected)#Prevent error first disconncet
        self.ShowColumnAction.triggered.connect(self.QTableShowSelected)#Prevent error first disconncet
    
        
    def onSectionClicked(self):
        print("section clicked")
    
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
            if ok:
                self.searchCountBox.setValue(1)
                self.treelist[0].setText(2, txt)
                self.QMenuCheckAll(0, Qt.Checked)
                
            #return False
        #Check EmptyText
        for i in range(self.searchCount):
            if(self.treelist[i].text(2) == ""):
                self.MessageBox("Search%d Text is Empty"%(i+1))
                return False
        #Checked item is not exist 
        first_col = None
        for num in range(self.searchCount):
            check_cnt = 0
            for i in range(self.col_cnt):
                if(self.treelist[num].child(i).checkState(1) == Qt.Checked): #Check Status
                    check_cnt+=1
                    if(check_cnt ==1):
                        first_col = i
            if(check_cnt == 0):
                self.MessageBox("Search%d Column is not Selected"%(num+1))
                return False
        #Get Operator
        operator_list = []
        for i in range(self.searchCount):
            if(i>0):
                print("%d : %s"%(i+1, self.bttnConditionlist[i].text() ))
                operator_list.append(self.bttnConditionlist[i].text())
        
        sql = "SELECT * FROM `pokecard`.`cardinfo` WHERE "
        
        for num in range(self.searchCount):
            txt = self.treelist[num].text(2)
            sql += "("
            for i in range(self.col_cnt):
                if(self.treelist[num].child(i).checkState(1) == Qt.Checked): #Check Status
                    sql+="%s LIKE \"%%%s%%\" OR "%(self.col_list[i],txt)
            sql = sql[:-3] + ")"
            if(num < self.searchCount-1): #Final loop don't need Operator
                sql += operator_list[num]
        
        print(sql)
        self.QTableUpdateList(self.DB_SendQuery(sql))
        self.tabWidget.setCurrentIndex(1)
        
        self.tableWidget.scrollToItem(self.tableWidget.item(0, first_col) , QAbstractItemView.PositionAtCenter)
        
        
    def Connect_Clicked(self):
        #self.MessageBox("Connect_Clicked!!")
        try:
            self.conn = mysql.connector.connect(**config)
            print(self.conn)
            self.cursor=self.conn.cursor()
            self.QTableUpdateColumn()
            #self.menuSearch.setEnabled(True)
            self.QTreeSearchCountEnable()
            self.treeWidget.setEnabled(True)
            self.QMenuEnableALL(self.menuTable ,True)
            self.QMenuEnableALL(self.menuSearch ,True)
            self.QMenuEnableALL(self.menuConnect ,False)
            
            self.MessageBox("Connected!!!")
            
            
            
        except mysql.connector.Error as err:
            print(err)
            
    
    def WordCounter():
        resultList = self.DB_SendQuery("SELECT * FROM `pokecard`.`cardinfo` LIMIT 100000;")
        self.max_cnt = len(resultList)
        input_string = ""
        for row in range(self.max_cnt):
            for col in range(self.col_cnt):
                input_string += resultList[row][col][1:-1] + " "
        wc = WordCounter(input_string)

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
        if(range_t == []):
            return False
        if(range_t[0].rowCount() == self.tableWidget.rowCount()): # column selected
            left = range_t[0].leftColumn()
            Right = range_t[0].rightColumn()
            self.tableWidget.horizontalHeader().addAction(self.HideColumnAction)
            self.tableWidget.horizontalHeader().addAction(self.ShowColumnAction)
            select = []
            for i in range(left, Right+1):
                select.append(self.col_list[i])
            self.HideColumnAction.triggered.disconnect()
            self.ShowColumnAction.triggered.disconnect()
            self.HideColumnAction.triggered.connect(lambda: self.QTableHideSelected(select))
            self.ShowColumnAction.triggered.connect(lambda: self.QTableShowSelected(select))
        else:
            self.tableWidget.horizontalHeader().removeAction(self.HideColumnAction)
            self.tableWidget.horizontalHeader().removeAction(self.ShowColumnAction)
        
        
    def QTable_CellDoubleClicked(self):
        if(self.tableWidget.currentItem() == None):
            return False
        if(self.tableWidget.horizontalHeaderItem(0).text() == "CardNum" and self.tableWidget.currentColumn() == 0):
            if(self.tableWidget.currentItem() != None):
                CardNum = self.tableWidget.currentItem().text()
                if(CardNum != ""):
                    print("Find CardNum!!! : %s "%CardNum)
                    self.CardWindow.setInputText(CardNum)
                    self.CardWindow.btn_clicked()
                    self.CardWindow.show()
                    self.CardWindow.activateWindow()
                    
                    #webbrowser.get(chrome_path).open('https://pokemoncard.co.kr/cards/detail/'+CardNum)
    
    def QTableRowOpenUrl(self):
        row=self.tableWidget.currentRow()
        if(self.tableWidget.item(row,0) != None):
            CardNum = self.tableWidget.item(row,0).text()
            if(CardNum != ""):
                print("Find CardNum!!! : %s "%CardNum)
                webbrowser.get(chrome_path).open('https://pokemoncard.co.kr/cards/detail/'+CardNum)
    
    
    def QTableCellMarking(self):
        txt, ok = QInputDialog.getText(self, 'InputWindow', 'Search Text')
        if ok:
            color = QColorDialog.getColor()
            color.setAlpha(100)
            allitems = self.tableWidget.findItems("", Qt.MatchContains)
            selected_items = self.tableWidget.findItems(txt, Qt.MatchContains)
            for item in allitems:
                if item in selected_items:
                    item.setBackground(color)
    
    def QTableTextMarking(self):
        txt, ok = QInputDialog.getText(self, 'InputWindow', 'Search Text')
        if ok:
            color = QColorDialog.getColor()
            global gMarkTextColor 
            gMarkTextColor = color
            allitems = self.tableWidget.findItems("", Qt.MatchContains)
            selected_items = self.tableWidget.findItems(txt, Qt.MatchContains)
            for item in allitems:
                if item in selected_items:
                    item.setForeground(color)
                    #item.setData(Qt.UserRole, txt if item in selected_items else None)
                
    def QTableCellMarkingClear(self):
        allitems = self.tableWidget.findItems("", Qt.MatchContains)
        for item in allitems:
            if(item != None):
                item.setBackground(QColor(255,255,255))
                
    def QTableTextMarkingClear(self):
        global gMarkTextColor 
        gMarkTextColor = QColor(0,0,0)
        allitems = self.tableWidget.findItems("", Qt.MatchContains)
        for item in allitems:
            if(item != None):
                item.setForeground(QColor(0,0,0))
    
    def QTableUpdateList(self,resultList):
        self.max_cnt = len(resultList)
        self.tableWidget.setRowCount(self.max_cnt)        
        for row in range(self.max_cnt):
            for col in range(self.col_cnt):
                self.tableWidget.setItem(row, col, QTableWidgetItem(resultList[row][col][1:-1]))
    
    def QTableUpdateColumn(self):
        sql="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='cardinfo'"
        resultList=self.DB_SendQuery(sql) # tuple 이 들어있는 list
        self.col_cnt = len(resultList)
        self.tableWidget.setColumnCount(self.col_cnt)        
        for i in range(self.col_cnt):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(resultList[i][0]))
            #self.tableWidget.sectionClicked(i).connect()
            self.col_list.append(resultList[i][0])
    
    def Search_Clicked(self):
        txt = self.lineEdit.text()
        print(txt)
        sql = "SELECT * FROM `pokecard`.`cardinfo` WHERE "
        #print(self.col_cnt)
        #print(self.col_list)
        for i in range(self.col_cnt):
            sql+="%s LIKE \"%%%s%%\" OR "%(self.col_list[i],txt)

        sql=sql[:-3]
        self.QTableUpdateList(self.DB_SendQuery(sql))
    
    def DB_SendQuery(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def MessageBox(self,msg):
        w = QWidget()
        Mbox=QMessageBox()
        w.move(self.pos().x()+(self.width()-Mbox.width())/2,self.pos().y()+(self.height()-Mbox.height())/2)
        Mbox.information(w, "Information", msg)
    
    def resizeEvent(self,event):
        h = self.height()
        w = self.width()
        self.tabWidget.resize(w-20,h-40)
        self.treeWidget.resize(w-26,h-80)
        self.tableWidget.resize(w-26,h-80) #Table Resize
    
    
    def keyPressEvent(self, ev):
        if(ev.key() == Qt.Key_C) and (ev.modifiers() & Qt.ControlModifier):
            self.copySelection()
    
    def copySelection(self):
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
            QApplication.clipboard().mimeData().setText(stream.getvalue())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = PokeDBWindow()
    demoWindow.setWindowTitle("PokeCard DataBase")
    demoWindow.setWindowIcon(QIcon("Pokemon.ico"))
    demoWindow.show() 
    app.exec_()
    
    
