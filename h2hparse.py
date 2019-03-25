#!/usr/bin/env python3.7

import sys, argparse, os
from h2hschema import *
from helpers import *

desc = """ Parses docx file to Halfway To Home document db """
p = argparse.ArgumentParser(description=desc)
p.add_argument('-f', action='append', dest='files')
p.add_argument('-c', action='store', dest='chapter_title')
p.add_argument('-y', action='store', dest='chapter_year')
p.add_argument('-t', action='store_true', dest='run_test')


def exec_test():

    txts = [
        "Dec 16, 1988, Foreign Press Center",
        "Defense Intelligence Agency, winter 1988",
        "december 1, 1988, Foreign Press Center",
        "December 01, 1988, Foreign Press Center",
        "January 1988, Foreign Press Center",
        "january 1988",
        "jan 1988",
        "Feb-Mar, 1988, Wilson Center",
        "June-July 1988",
        "March 14,15, 1989, House of Representatives",
        "Late January, 1988",
        "Brookings, May 10, 1988"
    ]
    for txt in txts:
        print("-----------\n%s\n--------\n" % txt)
        d, r = get_date(txt)
        if d:
            print(d)
            print(r)
        else:
            print("no date in line")

    sys.exit(0)

def read_docx(doc_file, c_title, c_year):

    chapter = Chapter(title=c_title, year=c_year)

    doc = HDoc(doc_file, "***")

    # different search formats 
    headline_fmt = TextFormat(size=16, bold=True, italic=None, name="headline")
    speaker_fmt = TextFormat(size=16, bold=True, name="speaker")    
    def_fmt = TextFormat(size=12, name="default")
    comment_fmt = TextFormat(italic=True, name="commentary")
    content_fmt = TextFormat(size=14, name="content")

    runmode = "start"
    new_article = False

    i=0
    doc
    while doc.not_done():
 
        if runmode == "start":
            res, pg_text, new_article = doc.advance_to_delimeter()
            #for r in res:
            #    if r.text:
            #        print("ignoring text: " + r.text)
            
            runmode = "new_article"
                    
        if runmode ==  "new_article":
            try:
                h_res, headline_text, new_article = doc.search_for_fmt(fmt=headline_fmt)
            except TypeError:
                pass
            h_done = False
            for r in h_res:
                if r.text:
                    if r.fmt.is_equal_to(headline_fmt):
                        h_done = True
            if h_done:          
                #new_article = Article(headline=headline_text)
                #chapter.add_article(new_article)
                #print("headline: " + headline_text)
                speakers = []
                speaker_names = []
                date = None
                infos = []
                tags = []
                pgs = []
                runmode = "speaker"
        
        if runmode == "speaker":
            content_detected = False
            r_text = ""
            s_res, pg_text, new_article = doc.search_for_fmt(fmt=speaker_fmt, limit=1)
            if s_res:
                for r in s_res:    
                    if r.text:
                        r_text = r.text.strip(',: ')              
                        # does run match speaker format?
                        #if r.fmt.is_equal_to(speaker_fmt):
                        if r.fmt.is_equal_to(speaker_fmt) and ":" in r.text:
                            content_detected = True
                        elif r.fmt.bold:
                            if r_text not in speaker_names:
                                # set speaker
                                speaker_names.append(r_text)
                                # parse for remainder of paragraph
                                info_text = pg_text.split(r_text)[1].strip(',: ')
                                # check to see if we found something
                                if info_text and info_text!=' ':
                                    # does remaining string contain a date?
                                    date_time, info_rem = get_date(info_text)
                                    if  date_time:
                                        date = date_time
                                        if info_rem and (info_rem!=' ') and (info_rem not in infos):
                                            #infos.append(info_rem+'(1)')
                                            speakers.append(Speaker(name=r_text, affiliation=info_rem))
                                        # move to the next runmode
                                        runmode = "content"
                                        #content_detected = True                                      
                                    else:
                                        # no date matched. Add as info string
                                        if info_text not in infos:
                                            #infos.append(info_text+'(1)')
                                            speakers.append(Speaker(name=r_text, affiliation=info_text))
                                # no extra text
                                else:
                                    speakers.append(Speaker(name=r_text))
                                    
                        # have we reached the content yet?        
                        elif r.fmt.is_equal_to(content_fmt) or r.fmt.italic or "(" in r.text or r.fmt.size==14:
                            content_detected = True
                        # should be the last date paragraph 
                        else:
                            # is there a date in the string?
                            date_time, info_rem = get_date(r_text)
                            if date_time:
                                date = date_time
                                if info_rem and (info_rem!=' ') and (info_rem not in infos):
                                    infos.append(info_rem+'(2)')
                                runmode = "content"
                                #content_detected = True
                            else:
                                if r_text not in infos:
                                    infos.append(r_text+'(2)')     
                # after runs are checked
                # if we reached the content already. Back up one pg and proceed. 
                if content_detected:
                    doc.index -= 1
                    runmode = "content"
            
            
        if runmode == "content":
            pg = doc.get_next_paragraph()

            if pg and pg.text: 
                is_comment = True
                append_pg = False
                for r in pg.runs:
                    if r.text:
                        if "***" in r.text:
                            new_article = True
                        elif "tags:" in r.text:
                            tags = [tag.strip() for tag in pg.text.strip('[]tags:').split(',') if (tag and tag!=' ')]
                            #break
                        else:
                            if "tags:" not in pg.text:
                                append_pg = True
                            if not r.font.italic:
                                is_comment = False
                if append_pg:
                    pgs.append(Paragraph(text=pg.text, comment=is_comment))
                            
        if new_article:
            chapter.articles.append(Article(headline=headline_text, date=date, speakers=speakers, info=infos, paragraphs=pgs, tags=tags))
            runmode = "new_article"

        #if i > 800:
        #    print(chapter)
        #    break
        #i += 1
    # While loop done
    chapter.show_contents(debug=True)

        
        

def run():
    args = p.parse_args()
    if args.run_test:
        exec_test()
    if not args.files:
        print("must provide a file name")
        sys.exit(1)


    for f in args.files:
        if os.path.isfile(f):
            #get_docx_text(f)
            read_docx(f, args.chapter_title, args.chapter_year)
    # open file
    # parse file into documents
    # parse documents into data structure
    # convert data to db schema
    # connect to cloud data store
    # upload documents

    sys.exit(0)

if __name__ == '__main__':
    run()