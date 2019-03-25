
# classes for Halfway To History documents
# Each document (docx file) adheres to the following schema:
#
# Chapter
#   - Title
#   - Year
#   - Articles (array of Class Article)
#     -- Article --
#     -- headline (required)
#     -- speakers (required)
#       --- Speaker ---
#       --- name
#       --- affiliation
#     -- speaker affiliation (optional)
#     -- date (required)
#     -- location (optional)
#     -- intro text (optional)
#     -- content (array of paragraphs)
#       --- Paragraph ---
#       --- text (required)
#       --- speaker :: <BOLD-Name>: (optional)
#       --- Question :: <BOLD>Q: (optional)
#     -- tags :: [<UNDERLINE-tags>]:



class Chapter:
    #title = None
    #year = None
    #articles = []
    #art_index = 0
    def __init__(self, title=None, year=None):
        self.title = title
        self.year = year
        self.articles = []
        self.art_index = 0

    def next_article(self):
        return self.articles[self.art_index]
    def current_article(self):
        return self.articles[self.art_index-1]
    def is_set(self):
        return self.title and self.year
    
    def add_article(self, a):
        self.articles.append(a)
        self.art_index += 1
  
    # __str__ used in the print function
    # defining this makes it easy to print the object 
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
            

class Article:
    def __init__(self, headline=None, speakers=[], info=[], date=None, paragraphs=[], tags=[]):
        self.headline = headline
        self.speakers = speakers
        self.info = info
        self.date = date
        self.paragraphs = paragraphs
        self.tags = tags
  
    def __str__(self):
        #res = """
        #  -- headline : %s
        #""" % self.headline
        #for sp in self.speakers:
        #    res += str()
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

class Speaker:
    def __init__(self, name=None, affiliation=None):
        self.name = name
        self.affiliation = affiliation

    def __str__(self):
        return "%s -> %s" % (self.name, self.affiliation)

class Paragraph:
    def __init__(self, text=None, speaker=None, question=None, comment=False):
        self.text = text
        self.speaker = speaker
        self.question = question
        self.comment = comment
    
    def __str__(self):
        return """
            --- speaker  : %s
            --- question : %s
            --- comment  : %s
            --- text     : %s
        """ % (self.speaker, self.question, str(self.comment), self.text)