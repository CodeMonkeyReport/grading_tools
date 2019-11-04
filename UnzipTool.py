#!/usr/bin/python3
from pyunpack import Archive
from shutil import copy2
import zipfile
import sys
import os
import re

class UnzipTool():
    """
    This tool expects a zip file to extract and a destination to place it
        Dependencies:
            pyunpack    - This will most likely need to be installed: python -m pip install pyunpack
            patool      - This module is a dependency of pyunpack and will also need to be installed: python -m pip install patool
    """
    def __init__(self):
        self.name = 'unzip'

    @staticmethod
    def processFile(student_result_dir, name_and_extension, raw_path):
        accepted_compression_formats = set("7z ace a arj bz2 cab Z cpio deb dms gz lrz lha lzh lz lzma lzo rpm rar rz tar xz zip zoo".split(sep=' '))
        """
            Function to handle a single file, given the student's directory and the file itself in the form (filename, extension)
        """
        extension = name_and_extension[1]
        filename = name_and_extension[0]

        archive_full_path = os.path.join(raw_path, filename)

        if not os.path.exists(archive_full_path):
            print("File path error at: ", archive_full_path)
            return

        if extension is not None and extension in accepted_compression_formats:
            try:
                Archive(archive_full_path).extractall(student_result_dir)
            except ValueError:
                print("Unexpected error while extracting file ", archive_full_path, ", The file may be corrupted or in an unsuported format.")
        else:
            f = os.path.join(raw_path, filename)
            copy2(archive_full_path, student_result_dir)
            # This section could use a feature which cleans up filenames when not compressed TODO
    def Run(self, args):
        # Regex used to get the student id and file extension from file names
        regex = r".+([a-z]{3}\d{3})_attempt_[0-9-]{19}_{0,1}[^\.]*\.?(.+)?"
        if len(args) < 3:
            print("Usage:", args[0], "[zipfile] [destination]")
            exit(0)
        else:
            zip_file_name = args[1]                             # Zip file to be processed
            destination_path = args[2]                          # Root destination
            raw_path = destination_path + '/raw'                # Where the raw results will be saved
            results_path = destination_path + '/result'         # where the final results will be saved

            # Create Directories and sub directories at location
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            if not os.path.exists(raw_path):
                os.makedirs(raw_path)
            if not os.path.exists(results_path):
                os.makedirs(results_path)


            # Open and extract to the given location
            zip_file = zipfile.ZipFile(zip_file_name, 'r')
            zip_file.extractall(raw_path)
            zip_file.close()

            # Get file names and match student ids
            file_names = os.listdir(raw_path)
            # each student id will have a list of files associated with them
            file_lists_by_id = {}

            for file_name in file_names:
                match = re.search(regex, file_name)
                if match:
                    student_id = match.group(1)
                    extension = match.group(2)

                    if not student_id in file_lists_by_id:
                        file_lists_by_id[student_id] = []

                    file_lists_by_id[student_id].append((file_name, extension))

            # Create directories and extract zip files to destination
            for student_id in file_lists_by_id.keys():
                # Create student directory
                student_result_dir = results_path + '/' + student_id
                if not os.path.exists(student_result_dir):
                    os.makedirs(student_result_dir)

                # Copy files into the directory
                for file in file_lists_by_id[student_id]:
                    UnzipTool.processFile(student_result_dir, file, raw_path)
                


if __name__ == '__main__':
    UnzipTool().Run(sys.argv)
    