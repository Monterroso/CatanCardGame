import re
import sys

for fi in range(1, len(sys.argv)):
  # Read in the file
  with open(sys.argv[fi], 'r') as file :
    filedata = file.read()

  # Replace the target string
  filedata = re.sub('[a-zA-Z]*', '', filedata)
  print(filedata)

  # Write the file out again
  with open(sys.argv[fi], 'w') as file:
    file.write(filedata)
