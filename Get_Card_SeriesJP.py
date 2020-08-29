import selenium 
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

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

if __name__ == "__main__":
    card = JPSeriesInfo(hide=False)
    start = 1
    end = 10
    for i in range(start,end+1):
        card.GetSeriesInfo(i)
    card.closeBrowser()
