# grading_tools

These are simple tools to aid in grading, provided to UTSA TAs and Graders, they are still in a rudementary stage and contributors are welcome.

UnzipTool is used to help extract individual student files, TaskTool can be used to run scripts within student folders and compile all results into a single output file sorted by student id.

# Requirements

  python -m pip install pyunpack patool

# Usage
 
  python UnzipTool.py [zipfile] [destination]

  python TaskTool.py [ScriptToExecute] [StudentFileRegex] [OutputFile] [RequiredFilesDirectory]
  
  
