#!/usr/bin/python3
from subprocess import CalledProcessError, Popen, PIPE, TimeoutExpired
from sys import argv
from sys import stdout
import os
import re
from distutils.dir_util import copy_tree
import shutil


class Student:
    """
    This class handles storing all of the students information
    """
    def __init__(self, student_id):
        self.student_id = student_id
        self.script_name = ""
        self.dir_path = ""
        self.script_dir = ""


class TaskTool:

    @staticmethod
    def usage(arguments):
        print("Usage:", arguments[0], "[ScriptToExecute] [StudentFileRegex] [OutputFile] [RequiredFilesDirectory]")
        exit(0)

    def __init__(self, arguments):
        self.student_list = []
        self.script_name = arguments[0]
        self.student_file_regex = arguments[1]
        self.required_files_dir = ""
        self.output_file = open(arguments[2], 'w')
        if len(arguments) > 3:
            self.required_files_dir = arguments[3]

        self.student_flag = False
        if self.script_name == "-s":
            self.student_flag = True

    def get_students(self):
        
        id_list = next(os.walk("result"))[1]
        # Create student objects for each id found
        for student_id in id_list:
            student = Student(student_id)
            student.dir_path = "result" + "/" + student_id

            # Find the script file in all sub directories of each student
            for dir_name, subdir_name, file_list in os.walk(student.dir_path):
                # Check each file
                for file in file_list:
                    match = re.search(self.student_file_regex, file)
                    if match is not None:  # This means we found the script
                        if self.student_flag:
                            student.script_name = file
                        else:
                            student.script_name = self.script_name
                        student.script_dir = os.path.abspath(dir_name)

            self.student_list.append(student)
        self.student_list.sort(key=lambda x: x.student_id, reverse=False)

    def copy_files(self):
        # If the files dir argument isn't specified we dont need to copy files
        if self.required_files_dir == "":
            return
        # Get correct data folder
        if not os.path.exists(self.required_files_dir):
            print("Directory \'" + self.required_files_dir + "\' not found.")
            exit(1)

        self.required_files_dir

        # For all students
        for student in self.student_list:
            # Copy the directory into their folder
            copy_tree(self.required_files_dir, student.script_dir)

    def run(self):

        for student in self.student_list:

            self.output_file.write("<c>*******************************************************************************</c>\n")
            self.output_file.write("<p>\n")
            self.output_file.write("\t---- " + student.student_id + " ----\n")
            
            print(student.student_id + " .", end='')
            stdout.flush()
            self.output_file.flush()
            TaskTool.call_script(student, self.output_file)
            print(" . . Done")

            self.output_file.write("</p>\n")
            self.output_file.write("<c>*******************************************************************************</c>\n")

    @staticmethod
    def call_script(student, output_file):
        if student.script_name == '':
            output_file.write("\tERROR: " + student.script_name +  " missing\n")
            return
        try:
            call_args = ["/bin/bash", os.path.join(student.script_dir, student.script_name)]
            process = Popen(call_args,
                            stdout=PIPE,
                            stderr=PIPE,
                            cwd=student.script_dir
                            )
            res = process.communicate(None, 5)

            output_file.write("\t**** STDERR ****\n\n\t\t")
            output_file.write(res[1].decode("utf-8").replace("\n", "\n\t\t"))
            output_file.write("\n\t\n")

            output_file.write("\t**** STDOUT ****\n\n\t\t")
            output_file.write(res[0].decode("utf-8").replace("\n", "\n\t\t"))
            output_file.write("\n\t\n")

        except (PermissionError, CalledProcessError, UnicodeDecodeError, TimeoutExpired) as e:
            print(call_args)
            print("An Error occured while processing", end='')
            output_file.write("\tProcess ended with error\n")

if __name__ == "__main__":
    if len(argv) < 3:
        TaskTool.usage(argv)
    this = TaskTool(argv[1:])
    this.get_students()
    this.copy_files()
    this.run()
