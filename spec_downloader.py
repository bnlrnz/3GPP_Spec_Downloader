#!/usr/bin/python3

import argparse
import sys
import os
import ftplib as FTP
import zipfile
from collections import defaultdict

BASE_ADDRESS = 'www.3gpp.org'
BASE_PATH = '/Specs/archive'

# argument parsing
parser = argparse.ArgumentParser(description='Downloads 3GPP specs. If no version parameter is given all versions are downloaded.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--document', type=str, help='comma separated list of documents to download with format <series>.<document_number>.g. 33.117')
group.add_argument('-s', '--series', type=str, help='comma separated list of numbers representing a 3GPP spec series')
group.add_argument('-l', '--list', type=str, help='textfile including document list (line based) - document format e.g. 33.117')
parser.add_argument('-v', '--major-version', type=str, help='comma separated list of numbers or characters representing 3GPP spec major version(s)')
parser.add_argument('-e', '--extract', action="store_true", help='extracts the downloaded zip archives')
parser.add_argument('--latest', action="store_true", help='only latest (or latest major version if given) document version is downloaded')
args = parser.parse_args()

major_version_list = [] 

# key: series: value: document list
doc_list = defaultdict(list)

# get a comma separated list of documents (or single doc)
if args.document:
    docs = args.document.split(',')

    for d in docs:
        series_doc = d.split('.')
        doc_list[series_doc[0]].append(series_doc[1])
    

# get all documents from a series
if args.series:
    series_list = args.series.split(',')

    for series in series_list:
        doc_list[series] = []
    
# get all documents listed in a text file
if args.list:
    with open(args.list) as doc_list_file:
        lines = doc_list_file.readlines()
        docs = [l.strip() for l in lines]
        for d in docs:
            series_doc = d.split('.')
            doc_list[series_doc[0]].append(series_doc[1])
    
# get the major version(s)
if args.major_version:
    major_version_list.extend(args.major_version.split(','))

extract_after_download = args.extract
latest_only = args.latest
major_versions = len(major_version_list) != 0 

for series in doc_list.keys():
    ftp = FTP.FTP(BASE_ADDRESS)
    ftp.login()
    ftp.cwd(BASE_PATH + f"/{series}_series")
    
    download_all_docs = False

    if len(doc_list[series]) == 0:
        download_all_docs = True

    for d in ftp.nlst():
        ser_number = d.split('.')[0]
        doc_number = d.split('.')[1]

        if doc_number not in doc_list[ser_number] and download_all_docs is False:
            continue
        
        ftp.cwd(BASE_PATH + f"/{series}_series/{ser_number}.{doc_number}")

        filenames = ftp.nlst()
        filenames.sort()

        to_download = []
        
        # download all
        if major_versions is False and latest_only is False:
            to_download = filenames

        # download latest
        if major_versions is False and latest_only:
            to_download = [filenames[-1]]
        
        if major_versions:
            # key: major version value: list of minor versions
            versions_dict = defaultdict(list)

            for filename in filenames:
                for major_version in major_version_list:
                    if "-" in filename and filename.split('-')[1][0] is major_version:
                        versions_dict[major_version].append(filename)

            # download latest of major version(s)
            if latest_only:
                for major_version in major_version_list:
                    if len(versions_dict[major_version]) > 0:
                        to_download.append(versions_dict[major_version][-1])

            # download all of major version(s)
            if latest_only is False:
                for major_version in major_version_list:
                    to_download.extend(versions_dict[major_version])

        for filename in to_download:
            if ".zip" not in filename:
                continue

            with open(filename, "wb") as fp:
                ftp.retrbinary(f"RETR {filename}", fp.write)
                print(f"{filename} downloaded")

            if extract_after_download:
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall()
                    print(f"{filename} extracted")

                if os.path.exists(filename):
                    os.remove(filename)
