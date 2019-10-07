"""
classes for Halfway To History documents
Each document (docx file) adheres to the following schema:
Chapter
  - Title
  - Year
  - Articles (array of Class Article)
    -- Article --
    -- headline (required)
    -- speakers (required)
      --- Speaker ---
      --- name
      --- affiliation
    -- date (required)
    -- info texts (optional)
      -- text ---
    -- content (array of paragraphs)
      --- Paragraph ---
      --- text (required)
      --- speaker :: <BOLD-Name>: (optional)
      --- Question :: <BOLD>Q: (optional)
      --- Comment (True|False)
    -- tags (array of tags)
"""
class Chapter:
    def __init__(self, title=None, year=None):
        self.title = title
        self.year = year
        self.articles = []
        self.art_index = 0
  
    def __str__(self):
        return "title: %s year: %s" % (self.title, self.year)

    def show_contents(self, debug=False):
        print(""" 
            title : %s 
            year  : %s
            -------------------
        """ % (self.title, self.year))
        for a in self.articles:
            print("\nNew Article\n---------------")
            print(a)
            if debug:
                for pg in a.paragraphs:
                    print(pg)

    def get_articles(self):
        return self.articles
            

class Article:
    def __init__(self, headline=None, speakers=[], info=[], date=None, paragraphs=[], tags=[]):
        self.headline = headline
        self.speakers = speakers
        self.info = info
        self.date = date
        self.paragraphs = paragraphs
        self.tags = tags
  
    def __str__(self):
        sps = ', '.join([str(sp) for sp in self.speakers if sp])
        return """
          -- headline : %s
          -- date     : %s
          -- speakers : [ %s ]
          -- info     : [ %s ]
          -- tags     : [ %s ]
        """ % (self.headline, self.date, sps, ', '.join(self.info), ', '.join(self.tags))


    def add_info(self, info_txt):
        if info_txt and info_txt!=' ':
            if info_txt not in self.info:
                self.info.append(info_txt)
                return True
        return False
    
    def json_object(self):
        dt = self.date.isoformat() if self.date else None
        result = {
            'headline': self.headline,
            'article_date': dt,
            'speakers': [],
            'info': self.info,
            'tags': self.tags,
            'paragraphs': []
        }
        for s in self.speakers:
            result['speakers'].append(s.json_object())
        for p in self.paragraphs:
            result['paragraphs'].append(p.json_object())
        return result

class Speaker:
    def __init__(self, name=None, affiliation=None):
        self.name = name
        self.affiliation = affiliation

    def __str__(self):
        return "%s -> %s" % (self.name, self.affiliation)

    def json_object(self):
        return {
            'speaker_name': self.name,
            'affiliation': self.affiliation
        } if self.name else {}

class Paragraph:
    def __init__(self, text=None, speaker=None, question=False, comment=False):
        self.text = text if text != '' else None
        self.speaker = speaker
        self.question = question
        self.comment = comment
    
    def __str__(self):
        return """
            --- speaker  : %s
            --- question : %s
            --- comment  : %s
            --- text     : %s
        """ % (self.speaker, str(self.question), str(self.comment), self.text)

    def json_object(self):
        return {
            'text': self.text,
            'speaker': self.speaker,
            'question': self.question,
            'comment': self.comment
        }