import scrapy
import re
from bs4 import BeautifulSoup


class AtCoderSpider(scrapy.Spider):
    name = 'atcoder'

    allowed_domains = ['atcoder.jp']
    start_urls = ['https://atcoder.jp/']

    contestant_arr = ["purple_ghost"]

    def start_requests(self):
        for contestant in self.contestant_arr:
            history_url = "https://atcoder.jp/users/" + contestant + "/history"
            yield scrapy.Request(url=history_url, callback=self.parse_individul_history, meta={'user': contestant})


    def parse_individul_history(self, response):
        table = response.xpath('//*[@id="history"]')[0]
        contest_arr = table.css('tbody > tr')

        print(contest_arr)

        history = []
        for contest in contest_arr:
            info_arr = contest.css('td')

            # time
            soup = BeautifulSoup(info_arr[0].extract())
            contest_date = soup.get_text()

            #contest name and link
            soup = BeautifulSoup(info_arr[1].extract())
            contest_name = soup.get_text()
            links = []
            for a in soup.find_all('a', href=True):
                links.append(a['href'])

            # rank
            soup = BeautifulSoup(info_arr[2].extract())
            rank = soup.get_text()

            # performance
            soup = BeautifulSoup(info_arr[3].extract())
            performance = soup.get_text()

            # new_rating
            soup = BeautifulSoup(info_arr[4].extract())
            new_rating = soup.get_text()

            # difference
            soup = BeautifulSoup(info_arr[5].extract())
            difference = soup.get_text()

            contest_data = {
                'contest_date'  : contest_date,
                'contest_name'  : contest_name,
                'links'         : links,
                'rank'          : rank,
                'performance'   : performance,
                'new_rating'    : new_rating,
                'difference'    : difference
            }

            # print(contest_data)
            # yield contest_data
            history.append(contest_data)
        
        yield {
            'contestant': response.meta.get('user'),
            'history': history
        }







