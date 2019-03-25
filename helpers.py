from docx import Document
from datetime import datetime
import re
#######

# class HDoc acts as a layer over top the docx xml layout
# DOCX xml:
#   paragraph in paragraphs
#       run in paragraph.runs
# 
# Usage: 
#   takes docx file path, and delimeter
#   delimeter will always force return or cursor text
#   doc = HDoc(doc_file, "***") or doc = HDoc(doc_file)
# 
# class functions search_for_term and search_for_format will both: 
#   take: term | TextFormat (class included in this file)
#   return [[HDocRun], BOOL]
#       
#       1:  array of  result from search for term | TextFormat
#       2:  has the delimiter been found
class HDocRun:
    def __init__(self, fmt=None, text=None):
        self.fmt = fmt
        self.text = text

class HDoc:
    def __init__(self, file_path, delimeter=None):
        doc = Document(file_path)
        self.pgs = doc.paragraphs
        self.pgs_len = len(self.pgs)
        self.index = 0
        self.run_index = 0
        self.delimeter = delimeter
    
    def __str__(self):
        return "index: %s of %s" % (self.index, self.pgs_len)

    def delimeter_found(self, txt):
        if self.delimeter:
            if self.delimeter in txt:
                return True
        return False

    def not_done(self):
        return self.index < self.pgs_len

    def search_for(self, method, limit=False):
        delimeter_hit = False
        matched = False
        rns=[]
        run_count = 0
        pg_text = ""
        while self.not_done(): 
            pg = self.pgs[self.index]
            pg_text += pg.text
            runs = pg.runs
            runs_len = len(runs)
            run = runs[self.run_index]
            #print(show_run_details(run))
            while self.run_index < runs_len:               
                if run.text:
                    run_count += 1
                    rn = HDocRun(text=run.text)
                    rn.fmt = TextFormat(size=12.0)
                    if run.font.size:
                        rn.fmt.size=run.font.size.pt
                        rn.fmt.bold=run.font.bold
                        rn.fmt.italic=run.font.italic
                    rns.append(rn)
                if not matched:
                    matched = method(run)
                if not delimeter_hit:
                    delimeter_hit = self.delimeter_found(run.text)

                self.run_index += 1
            self.run_index = 0
            self.index += 1
            if matched or delimeter_hit or (limit and run_count >= limit):
                return [rns, pg_text, delimeter_hit]
            
            

    def get_next_paragraph(self):
        if self.not_done(): 
            pg = self.pgs[self.index]
            self.index += 1
            return pg
        return False


    def get_next_text(self, limit=False):
        def search_method(r):
            return True
        return self.search_for(method=search_method, limit=limit)

    # advance to next 
    def advance_to_delimeter(self):
        def search_method(r):
            return False
        return self.search_for(method=search_method)

    def search_for_term(self, term="", limit=False):
        def search_method(r):
            found = False
            if r.text:
                if term in r.text:
                    found = True
            return found
        return self.search_for(method=search_method, limit=limit)


    def search_for_fmt(self, fmt, limit=False):
        def search_method(r):
            found = False
            if r.font.size:
                curr_fmt = TextFormat(size=r.font.size.pt, bold=r.font.bold, italic=r.font.italic)
                if curr_fmt.is_equal_to(fmt):
                    found = True
            return found
        return self.search_for(method=search_method, limit=limit)

class TextFormat:
    def __init__(self, size=None, bold=None, italic=None, name=None):
        self.size = size
        self.bold = bold
        self.italic = italic
        self.name = name
    
    def __str__(self):
        return "size: %s    bold: %s    italic: %s" % (str(self.size), str(self.bold), str(self.italic))

    def is_set(self):
        return ( self.size!=None and self.bold!=None and self.italic!=None )

    def is_equal_to(self, new):
        return (self.size == new.size)and (self.bold == new.bold) and (self.italic == new.italic)

#######

# takes a run
def show_run_details(r):
    if r.text:
        if r.font.size:  
            return """ 
                size    bold    italic   
                ----    ----    ------ 
                %s    %s    %s 
                -------------------------
                text: 
                -----
                %s    
            """ % (str(int(r.font.size.pt)), str(r.font.bold), r.font.italic, r.text)
        else:
            return """
                no font info found
                ------------------
                text: %s
                -----
            """ % r.text
    return "No Run Text Found:: Line Break?"

def get_date(txt):
    p = re.compile('(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)(.+?)([1][9][0-9]{2})', re.IGNORECASE)
    qualifier = re.compile('^(late|early)$', re.IGNORECASE)
    m = p.search(txt)
    if m:
        date_string = m.group()
        d = parse_date_string(date_string)
        if d:
            r = txt.replace(date_string, '').strip(' ,:')
            if qualifier.search(r):
                r = ""
            return [d, r]
    #else:
    #    print("(get-date) match failed for: " + txt)
    return [None, txt]
        
    

def parse_date_string(d_str):
    # regex patterns for date formats
    # e.g. Jan 12, 1988
    pattern_short = re.compile('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ', re.IGNORECASE)
    # e.g. January 12, 1988
    pattern_long = re.compile('(January|February|March|April|May|June|July|August|September|October|November|December) ', re.IGNORECASE)
    # January 12, 1988 vs January 1988
    pattern_day = p = re.compile('.*((?:[1-3])?[0-9]) ')
    # e.g. Mar-Apr 1988
    pattern_date_range = re.compile('.*(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)[-](Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)', re.IGNORECASE)
    # e.g.March 14,15, 1989
    pattern_multi_day = re.compile('.*((?:[1-3])?[0-9])[,]((?:[1-3])?[0-9])')
    # match date string
    
    date_range = pattern_date_range.match(d_str)
    multi_day = pattern_multi_day.match(d_str)
    if date_range:
        months = date_range.group()
        year = d_str.split(months)[1].strip(' ,-')
        month = months.split('-')[0].strip(' ,-')
        date_string = "%s %s" % (month, year)
        #print("combo month: " + months)
        #print("new str: " + date_string)
    elif multi_day:
        days = multi_day.group()
        day = days.split(',')[0].strip(', ')
        date_string = d_str.replace(days, day).replace(',', '')
        #print("multi day: " + date_string)
    else:
        date_string = d_str.replace(',', '')
    
    short_month = pattern_short.search(date_string)
    long_month = pattern_long.search(date_string)
    day_match = pattern_day.match(date_string)
    # build strptime date format
    dt_pat = ""
    if short_month:
        #print("short month: " + date_string)
        dt_pat += "%b"
    elif long_month:
        #print("long month: " + date_string)
        dt_pat += "%B"
    if day_match:
        dt_pat += " %d"
    dt = None
    if short_month or long_month:
        dt_pat += " %Y"
        try:
            dt = datetime.strptime(date_string, dt_pat)
        except ValueError:
            print("problem date string : " + date_string )
            pass
    return dt
