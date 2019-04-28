"""
class HDoc acts as a layer over top the docx xml layout
DOCX xml:
  paragraph in paragraphs
      run in paragraph.runs 
Usage: 
  takes docx file path, and delimeter
  delimeter will always force return or cursor text
  doc = HDoc(doc_file, "***") or doc = HDoc(doc_file)
    
      1:  array of  result from search for term | TextFormat
      2:  has the delimiter been found
"""
from docx import Document
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

    def is_equal_to(self, new):
        return (self.size == new.size)and (self.bold == new.bold) and (self.italic == new.italic)

#######
# for testing purposes
# takes a run an prints text and format details
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