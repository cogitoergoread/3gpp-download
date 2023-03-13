#!/home/muszi/gwork/3gpp-env/bin/python

import os
from ftplib import FTP 
import argparse
import pandas as pd
import zipfile


RENAMING_CONVENTION = "https://www.3gpp.org/DynaReport/{:02d}-series.htm"
BASE_3GPP_SERIES = "Specs/archive/{:02d}_series/{}"
BASE_3GPP_FTP = 'ftp.3gpp.org'

class Renamer:
    def get_renaming(self, series):
        data = pd.read_html(RENAMING_CONVENTION.format(series))
        spec_n = [i.replace("TS ", "") for i in list(data[0]['spec number'])]
        spec_title = [i.replace(" ", "_") for i in list(data[0]['title'])]

        ret = {}
        for document, title in zip(spec_n, spec_title):
            if "TS" in document:
                document = document.replace("TS ", "")
            if "TR" in document:
                document = document.replace("TR ", "")
            mytitle = title.replace(";", "")
            # print (f'Document: {document}, Document title:{mytitle}')
            ret[document] = mytitle
        return ret

class Downloader:
    def __init__(self):
        self.ftp = FTP('ftp.3gpp.org') 
        self.ftp.login()
        self.renamer = Renamer()

    def __del__(self):
        self.ftp.quit()

    def unzip(self, path_to_zip_file, directory_to_extract_to):
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)

    @classmethod
    def get_series(cls, document):
        if "." not in document:
            raise ValueError("Invalid document number")
        [series_number, _] = document.split(".")
        return int(series_number)

    def get(self, document):
        series_number = self.get_series(document)
        print("Gettting document ", document, "from series", series_number)

        versions_path = BASE_3GPP_SERIES.format(
            series_number, 
            document)
        print(f'Versions path:{versions_path}')

        try:
            # Download the latest file, latest is always the last
            document_versions = self.ftp.nlst(versions_path)
        except:
            print("Could not retrieve list of files")
            return
        
        # document_path = document_versions[-1]
        doc_select='0000'
        doc_req=document.replace('.','')
        for docelem in document_versions:
            target_file = docelem.split("/")[-1]
            if (target_file[:5] == doc_req) & (target_file[5:7] == '-g'):
                # Matches for Rel 16 format -g00
                if doc_select < target_file:
                    doc_select = target_file
                    document_path = docelem
        # target_file = document_path.split("/")[-1]
        target_file = doc_select
        print(f'Target File: {target_file}')
        print(f'3GPP path: {document_path}')


        try:
            destiny = "/tmp/{}.zip".format(document)
            print("Downloading file to {}".format(destiny))
            with open(destiny, "wb") as fp:
                self.ftp.retrbinary('RETR {}'.format(document_path), fp.write)
        except:
            print("Could not download the Specification")

	# Unzip in the local folder
        is_zip = ".zip" in document_path
        if is_zip:
            print("Unpacking file into localfolder from: ", destiny)
            self.unzip(destiny, ".")

	# Rename the downloaded file
        renaming = self.renamer.get_renaming(series_number)
        if os.path.isfile(target_file.replace(".zip", ".doc")):
            ext = ".doc"
        elif os.path.isfile(target_file.replace(".zip", ".docx")):
            ext = ".docx"
        else:
            print("Could not find valid extension, expected .doc or .docx")

        new_name = "{}-{}{}".format(document, renaming[document], ext)
        curr_name = target_file.replace(".zip", ext)
        print("Created file: {}".format(new_name))
        os.rename(curr_name, new_name)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download or list 3GPP specifications')

    parser.add_argument('document', metavar='S', type=str, nargs=1,
                   help='The document number, Ex: 21.978')
    parser.add_argument('-n', '--name', action='store_const', dest='only_name', const=True,
                   help='shown only the name of a document (Ex: 21.978)')


    args = parser.parse_args()
    document = args.document[0]
    only_name = args.only_name

    #print(args)
    if only_name:
        try:
            series = Downloader.get_series(document)
            naming_dict = Renamer().get_renaming(series)
            print("{}-{}".format(document, naming_dict[document]))
        except:
            print("Specification ID not found")
    else:
        Downloader().get(document)
