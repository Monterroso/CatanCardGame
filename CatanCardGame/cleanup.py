# Read in the file
with open('file.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('ram', 'abcd')

# Write the file out again
with open('file.txt', 'w') as file:
  file.write(filedata)
