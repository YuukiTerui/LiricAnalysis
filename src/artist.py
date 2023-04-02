from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json, pickle, os

from song import Song

class Artist:
    BASE_URL = "https://www.uta-net.com/"

    def __init__(self):
        self.artist_name = None
        self.artist_url = None
        self.song_urls = {}
        self.songs = {}

    def __str__(self):
        return self.artist_name
        
    def init(self, keyword=None):
        while True:
            if keyword is None:
                keyword = input("artist's name?> ")
            html = self.__get_html(f"https://www.uta-net.com/search/?target=art&type=in&keyword={keyword}")
            bs = BeautifulSoup(html.read(), "html.parser")
            ls = bs.select("a.d-block")
            if ls is not None:
                for i, l in enumerate(ls):
                    print(f"{i}: {l.select('.fw-bold')[0].get_text()}")
                print(f"{i+1}: <retry input keyword>")
                idx = int(input("chose number> "))
                if not idx == i + 1:
                    keyword = None
                    break
            else:
                print(f"Not found. Try other keyword.[{keyword}]")
        self.artist_name = ls[idx].select('.fw-bold')[0].get_text()
        self.artist_url = self.BASE_URL + ls[idx]['href']
        self.__create_songs_urls()

    def create_song_datas(self):
        for k, v in self.song_urls.items():
            print(k)
            html = self.__get_html(self.BASE_URL + v)
            bs = BeautifulSoup(html.read(), "html.parser")
            title = bs.h2.get_text()

            tmp = bs.select("span[itemprop='byArtist name']")
            artist = tmp[0].get_text() if tmp else None
            
            tmp = bs.select("a[itemprop='lyricist']")
            lyrics_by = tmp[0].get_text() if tmp else None
            
            tmp = bs.select("a[itemprop='composer']")
            music_by = tmp[0].get_text() if tmp else None
            
            tmp = bs.select("a[itemprop='arranger']")
            arranged_by = tmp[0].get_text() if tmp else None
            
            tmp = bs.select(".detail")
            tmp = tmp[0].get_text() if tmp else None
            pub_date = tmp[tmp.find("発売日：")+4: tmp.find("発売日：")+14]
            
            tmp = bs.select(".img-fluid")
            jacket = tmp[0]["src"] if tmp else None
            
            self.songs[title] = Song(title=title, 
                                     artist=artist, 
                                     lyrics_by=lyrics_by, 
                                     music_by=music_by, 
                                     arranged_by=arranged_by, 
                                     pub_date=pub_date, 
                                     jacket=jacket)
            
    def to_dict(self):
        dict = {}
        for k, v in self.__dict__.items():
            try:
                json.dumps(v)
            except TypeError:
                if '__dict__' in dir(v):
                    v = v.__dict__
                else:
                    continue
            finally:
                dict[k] = v
        return dict
        
    def to_pickle(self):
        try:
            with open(f"{os.path.dirname(__file__)}/../data/pickle/{self.artist_name}.pkl", "wb") as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)

    def __create_songs_urls(self):
        html = self.__get_html(self.artist_url)
        bs = BeautifulSoup(html.read(), "html.parser")
        ls = bs.select(".py-lg-0")
        for l in ls:
            self.song_urls[l.select('.songlist-title')[0].getText()] = l['href']

    def __get_html(cls, url):
        try:
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        return html
