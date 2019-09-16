import sys, argparse, os
from helpers import read_docx, exec_test
from bridge.api import post_new_article

desc = """ Parses docx file to Halfway To Home document db """
p = argparse.ArgumentParser(description=desc)
p.add_argument('-f', action='store', dest='file')
p.add_argument('-c', action='store', dest='chapter_title')
p.add_argument('-y', action='store', dest='chapter_year')
p.add_argument('-t', action='store_true', dest='run_test')

def run():
    args = p.parse_args()
    if not args.file:
        print("must provide a file name")
        sys.exit(1)

    f = args.file
    if os.path.isfile(f):
        chap = read_docx(f, args.chapter_title, args.chapter_year)
        if args.run_test:
            chap.show_contents(debug=False)
        else:
            articles = chap.get_articles()
            for article in articles:
                req = article.json_object()        
                res = post_new_article(req)
                print(res)

    sys.exit(0)

if __name__ == '__main__':
    run()