import json
class Song:
    def __init__(self, 
                 title=None, 
                 artist=None, 
                 lyrics_by=None, 
                 music_by=None, 
                 arranged_by=None, 
                 lyrics=None, 
                 pub_date=None,
                 jacket=None
                 ):
        self.title = title
        self.artist = artist
        self.lyrics_by = lyrics_by
        self.music_by = music_by
        self.arranged_by =arranged_by
        self.lyrics = lyrics
        self.pub_date = pub_date
        self.jacket = jacket

    def __str__(self):
        return f'{self.title=}\n{self.artist=}\n{self.lyrics_by=}\n{self.music_by=}\n{self.arranged_by=}\n{self.pub_date=}\n{self.jacket=}\n'
    
    def to_textfile(self, savepath="./"):
        if not savepath[-1] == "/":
            savepath += "/"
        try:
            with open(f'{savepath}{self.title}.txt', 'w') as f:
                f.write(self.lyrics)
            return True
        except Exception as e:
            print(e)
            return False
        
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
