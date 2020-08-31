import sys
import urllib
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QUrl

form_class = uic.loadUiType("Poke_Card.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)
        self.SetEnableNextPrevBttn(False)

        self.pushButton_Prev.clicked.connect(self.Prev_clicked)
        self.pushButton_Next.clicked.connect(self.Next_clicked)

        self.imglist = []
        self.nowimg = 0

        self.ProgressBar = None

    def btn_clicked(self):
        detail_code = self.textEdit.toPlainText()
        if detail_code == "":
            QMessageBox.about(self, "Warning", "Please Input detail code!!!")
        
        else:
            card_link = "https://pokemonkorea.co.kr/cards/detail/" + detail_code.strip()
            print (card_link)
         
            webpage = urllib.request.urlopen(card_link) 
            source  = BeautifulSoup(webpage,'html.parser')
            
            img = source.find("div", {"id":"heaer_top"}).findAll("img")
            file_link = img[0].get("src").split('?w')[0] #first url is main image.. and remove width parameter
            self.LoadImage(file_link)

    def LoadImage(self, file_link):
        url=QUrl(file_link)
        self.webView.load(url)
        self.webView.show()

    def SetCountry(self, Country):
        if(Country == "JPN"):
            self.textEdit.deleteLater()
            self.pushButton.deleteLater()
            self.widgetProgress
            self.ProgressBar=QProgressBar(self.widgetProgress)
            self.ProgressBar.setRange(0,100)
            self.ProgressBar.resize(395,31)
            print("PokeCard Progress Bar(w:%d,h:%d)"%(self.ProgressBar.width(), self.ProgressBar.height()))
            

        elif(Country == "KOR"):
            self.pushButton_Next.deleteLater()
            self.pushButton_Prev.deleteLater()
    

    def LoadCurrentImage(self):
        if(len(self.imglist) == 0):
            return False
        self.LoadImage(self.imglist[self.nowimg])
        
    def SetImageList(self, ImgLinkList):
        self.imglist =[]
        
        self.imglist = ImgLinkList
        if(len(self.imglist)>1):
            self.SetEnableNextPrevBttn(True)
        else:
            self.SetEnableNextPrevBttn(False)
        self.nowimg = 0
        self.LoadCurrentImage()

    def Next_clicked(self):
        if(self.nowimg < len(self.imglist)-1):
            self.nowimg +=1
        self.LoadCurrentImage()

    def Prev_clicked(self):
        if(self.nowimg > 0):
            self.nowimg -=1
        self.LoadCurrentImage()

    def SetEnableNextPrevBttn(self, isEnable):
        self.pushButton_Prev.setEnabled(isEnable)
        self.pushButton_Next.setEnabled(isEnable)
        

    def setInputText(self,string):
        self.textEdit.setText(string)
        
    def webView_SaveImage(self):    
        print ("aaaa")
        
    def resizeEvent(self,event):
        h = self.height()
        w = self.width()
        self.webView.resize(w-25,h-110)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.SetCountry("JPN")
    myWindow.show()
    app.exec_()
