import lxml.html
# scraper file is in my repository called "ScrapingTools"
import scraper as sc


class Scraping:

    def __init__(self):
        self.url = 'http://www.livescore.com/soccer/australia/a-league/'
        self.data = []

    def get_data(self):
        # JSHandle has sometimes troubles with getting site source. Please restart the program, error should be gone.
        source = sc.JSHandle(self.url)
        tree = lxml.html.fromstring(source)
        etree = tree.xpath('//div[@data-type="container"]')[0]
        mount = int(tree.xpath('count(//div[@data-type="container"]/div[@data-type="evt"])'))
        for i in range(1, mount+1):
            element = etree.xpath('.//div[@data-type="evt"]['+str(i)+']')[0]
            date = sc.get_text(element.xpath('.//preceding::div[@class="right fs11"][1]/text()'))
            time = sc.get_text(element.xpath('.//div[@class="min "]/span/text()'))
            home_name = sc.get_text(element.xpath('.//div[@class="ply tright name"]/span/text()'))
            away_name = sc.get_text(element.xpath('.//div[@class="ply name"]/span/text()'))
            score_home = sc.get_text(element.xpath('.//span[@class="hom"]/text()'))
            score_away = sc.get_text(element.xpath('.//span[@class="awy"]/text()'))
            print(date, time, home_name, score_home, away_name, score_away)
            self.data.append([date, time, home_name, score_home, away_name, score_away])
        sc.Database(('data', 'time', 'home_name', 'score_home', 'away_name', 'score_away')).database(self.data)


Scraping = Scraping()
Scraping.get_data()
