from datetime import datetime
from schema import Chapter, Article, Speaker, Paragraph
from hdoc import HDoc, TextFormat
import re, sys


def contains_question(s):
    p = re.compile('Q:', re.IGNORECASE)
    return True if p.match(s) else False

def contains_speaker(s):
    res = False
    t = s.strip(' ')
    p_simple = re.compile('\w{2,}:')
    p_info = re.compile('[a-zA-Z0-9, ]{2,}:\Z')
    m_name = p_simple.match(t)
    m_info = p_info.match(t)
    if m_name:
        res = m_name.group(0)
    elif m_info:
        res = m_info.group(0)
    return res

def match_speaker_name(s):
    t = s.strip(',')
    p = re.compile('(\w{2,}(?:\.)?\s){1,2}(\w{3,})\Z')
    m = p.match(t)
    return m.group(0) if m else False

def in_speakers(s, arr):
    res = False
    for sp in arr:
        if s in sp.name:
            res = True
            break
    return res

def get_date(txt):
    p = re.compile('(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)(.+?)([1][9][0-9]{2})', re.IGNORECASE)
    qualifier = re.compile('^(late|early)$', re.IGNORECASE)
    t = txt.replace('Sept', 'Sep')
    m = p.search(t)
    if m:
        date_string = m.group()
        d = parse_date_string(date_string)
        if d:
            r = txt.replace(date_string, '').strip(' ,:')
            if qualifier.search(r):
                r = ""
            return [d, r]
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
    elif multi_day:
        days = multi_day.group()
        day = days.split(',')[0].strip(', ')
        date_string = d_str.replace(days, day).replace(',', '')
    else:
        date_string = d_str.replace(',', '')
    
    short_month = pattern_short.search(date_string)
    long_month = pattern_long.search(date_string)
    day_match = pattern_day.match(date_string)
    # build strptime date format
    dt_pat = ""
    if short_month:
        dt_pat += "%b"
    elif long_month:
        
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
        "Brookings, May 10, 1988",
        "French Defense Minister, Sept 29, 1988"
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
    content_fmt = TextFormat(size=14, name="content")

    runmode = "start"
    new_article = False

    while doc.not_done():
 
        if runmode == "start":
            _, pg_text, new_article = doc.advance_to_delimeter()
            
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
                speakers = []
                infos = []
                tags = []
                pgs = []
                runmode = "speaker"
        
        if runmode == "speaker":
            content_detected = False
            r_text = ""
            s_res, pg_text, new_article = doc.get_next_text()
            if s_res:
                for r in s_res:    
                    if r.text:
                        r_text = r.text.strip(',: ')
                        if contains_speaker(r.text):
                            content_detected = True      
                        elif r.fmt.bold:
                            # parse for remainder of paragraph
                            info_text = pg_text.split(r_text)[1].strip(',: ')
                            # check to see if we found something
                            if info_text and info_text!=' ':
                                # does remaining string contain a date?
                                date_time, info_rem = get_date(info_text)
                                if  date_time:
                                    if info_rem and (info_rem!=' ') and (info_rem not in infos):
                                        infos.append(info_rem)
                                    # move to the next runmode
                                    runmode = "content"                                
                                else:
                                    # no date matched. Add as info string
                                    if not in_speakers(info_text, speakers):
                                        speakers.append(Speaker(name=r_text, affiliation=info_text))
                            # no extra text, just a speaker
                            else:
                                if match_speaker_name(r_text):
                                    if not in_speakers(r_text, speakers):
                                        speakers.append(Speaker(name=r_text))
                                else:
                                    if r_text not in infos:
                                        infos.append(r_text)
                                    
                        # have we reached the content yet?        
                        elif r.fmt.is_equal_to(content_fmt) or r.fmt.italic or r.fmt.size==14:
                            content_detected = True
                        # should be the last date paragraph 
                        else:
                            # is there a date in the string?
                            date_time, info_rem = get_date(r_text)
                            if date_time:
                                if info_rem and (info_rem!=' ') and (info_rem not in infos):
                                    infos.append(info_rem)
                                runmode = "content"
                            else:
                                # if no date in string. speaker or info
                                sp_string = match_speaker_name(r_text)
                                if sp_string:
                                    sp_text = sp_string.strip(',: ')
                                    sp_aff = pg_text.strip(sp_text).strip(',: ')
                                    if not in_speakers(sp_text, speakers):
                                        speakers.append(Speaker(name=sp_text, affiliation=sp_aff))
                                else:
                                    other_text = pg_text.strip(', ')
                                    if other_text not in infos:
                                        infos.append(other_text)
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
                        else:
                            if "tags:" not in pg.text:
                                append_pg = True
                            if not r.font.italic:
                                is_comment = False
                if append_pg:
                    has_speaker = contains_speaker(pg.text)
                    # does the pg have a speaker at the beginning
                    if has_speaker:
                        body_speaker_info = None
                        body_speaker_text = has_speaker.strip(':')
                        # does the speaker contain info as well as the name?
                        if ',' in body_speaker_text:
                            body_speaker_name = body_speaker_text.split(',')[0].strip(',: ')
                            body_speaker_info = body_speaker_text.split(',')[1].strip(',: ')
                        else:
                            body_speaker_name = body_speaker_text
                        speaker_pg_text = pg.text.strip(has_speaker+' ')
                        if not in_speakers(body_speaker_name, speakers):
                            speakers.append(Speaker(name=body_speaker_name, affiliation=body_speaker_info))
                        pgs.append(Paragraph(text=speaker_pg_text, speaker=Speaker(name=body_speaker_name, affiliation=body_speaker_info)))
                    elif contains_question(pg.text):
                        pgs.append(Paragraph(text=pg.text, question=True))
                    else:
                        pgs.append(Paragraph(text=pg.text, comment=is_comment))
                            
        if new_article:
            chapter.articles.append(Article(headline=headline_text, date=date_time, speakers=speakers, info=infos, paragraphs=pgs, tags=tags))
            runmode = "new_article"

    return chapter