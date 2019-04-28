#!/usr/bin/env python3.7

import sys, argparse, os
#from h2hschema import *
from helpers import read_docx, exec_test

desc = """ Parses docx file to Halfway To Home document db """
p = argparse.ArgumentParser(description=desc)
p.add_argument('-f', action='append', dest='files')
p.add_argument('-c', action='store', dest='chapter_title')
p.add_argument('-y', action='store', dest='chapter_year')
p.add_argument('-t', action='store_true', dest='run_test')

def run():
    args = p.parse_args()
    if args.run_test:
        exec_test()
    if not args.files:
        print("must provide a file name")
        sys.exit(1)


    for f in args.files:
        if os.path.isfile(f):
            chap = read_docx(f, args.chapter_title, args.chapter_year)
            chap.show_contents(debug=False)
    # open file
    # parse file into documents
    # parse documents into data structure
    # convert data to db schema
    # connect to cloud data store
    # upload documents

    sys.exit(0)

if __name__ == '__main__':
    run()