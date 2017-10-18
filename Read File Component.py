import re

filename = input("Enter file to be processed: ")
print(filename)
f = open(filename, "r")
file_contents = (re.split(r'\n\n',f.read()))#split text file by using every double whitespace
rule_base =  file_contents[0]
rules = file_contents[1]
fuzzy_sets = []
measurements = file_contents[len(file_contents)-1] #last 'paragraph' will be the measurements

for i in range(2,len(file_contents)-1,2): #Locate and group fuzzy set values
    fuzzy_sets.append(file_contents[i+1].split("\n"))
f.close()

print (rule_base)
print (rules)
print (fuzzy_sets)
print (measurements)
