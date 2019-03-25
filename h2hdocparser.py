from docx import Document

class RunMode:
    modes = [
        'Title', 
        'Year',
        
        ]
    mode = 

def read_docx(doc_file):
    document = Document(doc_file)
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            if run.bold:
                print(run.text)

#def parse_doc_for_articles(**kwargs):


#def parse_article_for_headline(**kwargs)