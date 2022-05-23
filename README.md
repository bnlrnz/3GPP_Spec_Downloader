# 3GPP_Spec_Downloader
Python script to download 3GPP specs from https://www.3gpp.org/ftp/Specs/archive

usage: spec_downloader.py [-h] (-d DOCUMENT | -s SERIES | -l LIST)
                          [-v MAJOR_VERSION] [-e] [--latest]

Downloads 3GPP specs. If no version parameter is given all versions are
downloaded.

options:
  -h, --help            show this help message and exit
  -d DOCUMENT, --document DOCUMENT
                        comma separated list of documents to download with
                        format <series>.<document_number>.g. 33.117
  -s SERIES, --series SERIES
                        comma separated list of numbers representing a 3GPP
                        spec series
  -l LIST, --list LIST  textfile including document list (line based) -
                        document format e.g. 33.117
  -v MAJOR_VERSION, --major-version MAJOR_VERSION
                        comma separated list of numbers or characters
                        representing 3GPP spec major version(s)
  -e, --extract         extracts the downloaded zip archives
  --latest              only latest (or latest major version if given)
                        document version is downloaded
