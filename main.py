import lxml.html
# scraper file is in my repository called "ScrapingTools"
# https://www.freelancer.com/projects/data-entry/vba-excel-website-data-scraping/
import scraper as sc


class Scraping:

    def __init__(self):
        self.url = 'http://www.livescore.com/soccer/australia/a-league/'
        self.data = []
        # JSHandle has sometimes troubles with getting site source. Please restart the program, error should be gone.
        self.source = sc.JSHandle(self.url)
        self.tree = lxml.html.fromstring(self.source)

    def get_matches_data(self):
        self.data = []
        mount = int(self.tree.xpath('count(//div[@data-type="container"]/div[@data-type="evt"])'))
        for i in range(1, mount+1):
            element = self.tree.xpath('//div[@data-type="container"]//div[@data-type="evt"]['+str(i)+']')[0]
            date = sc.get_text(element.xpath('.//preceding::div[@class="right fs11"][1]/text()'))
            time = sc.get_text(element.xpath('.//div[@class="min "]/span/text()'))
            home_name = sc.get_text(element.xpath('.//div[@class="ply tright name"]/span/text()'))
            away_name = sc.get_text(element.xpath('.//div[@class="ply name"]/span/text()'))
            score_home = sc.get_text(element.xpath('.//span[@class="hom"]/text()'))
            score_away = sc.get_text(element.xpath('.//span[@class="awy"]/text()'))
            print(date, time, home_name, score_home, score_away, away_name)
            self.data.append([date, time, home_name, score_home, away_name, score_away])
        sc.Database(('data', 'time', 'home_name', 'score_home', 'away_name', 'score_away'), 'matches.db').database(self.data)

    def get_table_data(self):
        self.data = []
        etree = self.tree.xpath('//div[@data-type="league-table-container"]/div[@data-type="table"]/div[@data-type="table-row"]')
        for element in etree:
            name = sc.get_text(element.xpath('./div[@class="team"]/text()'))
            place = sc.get_text(element.xpath('.//span[@data-type="rank"]/text()'))
            played = sc.get_text(element.xpath('.//div[@data-type="played"]/text()'))
            wins = sc.get_text(element.xpath('.//div[@data-type="wins"]/text()'))
            draws = sc.get_text(element.xpath('./div[@data-type="draws"]/text()'))
            losses = sc.get_text(element.xpath('./div[@data-type="losses"]/text()'))
            scored = sc.get_text(element.xpath('./div[@data-type="goals-scored"]/text()'))
            received = sc.get_text(element.xpath('./div[@data-type="goals-received"]/text()'))
            difference = sc.get_text(element.xpath('./div[@data-type="goal-difference"]/text()'))
            points = sc.get_text(element.xpath('./div[@data-type="points"]/text()'))
            print(name, place, played, wins, draws, losses, scored, received, difference, points)
            self.data.append([name, place, played, wins, draws, losses, scored, received, difference, points])
        sc.Database(('name', 'place', 'played', 'wins', 'draws', 'losses', 'scored', 'received', 'difference', 'points'), 'table.db').database(self.data)


Scraping = Scraping()
Scraping.get_table_data()
Scraping.get_matches_data()
