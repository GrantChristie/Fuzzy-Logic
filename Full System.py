import re

def main():
    filename = input("Enter file to be processed: ")
    file = read_file(filename)
    process(file['Rules'])

def read_file(filename):
    info = {}
    real_values = []
    f = open(filename, "r")
    file_contents = (re.split(r'\n\n',f.read()))#split text file by using every double whitespace

    rule_base =  file_contents[0]
    rules = file_contents[1]
    fuzzy_sets = []
    measurements = file_contents[len(file_contents)-1].split("\n") #last 'paragraph' will be the measurements

    #store real values 
    for i in range(0, len(measurements)):
        measurements[i] = measurements[i].split(" = ")
        if measurements[i] is not None:
            real_values.append(dict({"name":measurements[i][0], "value":measurements[i][1]}))
            
    for i in range(2,len(file_contents)-1,2): #Locate and group fuzzy set values
        fuzzy_sets.append(file_contents[i+1].split("\n"))

    f.close()

    info['Rule_Base'] = rule_base
    info['Rules'] = rules.split("\n")
    info['Fuzzy_Sets'] = fuzzy_sets
    info['Real_Values'] = real_values

    return info

def membership(a,b,alpha,beta,x):
    if x < a - alpha:
        print(0)
    elif x in range(a - alpha, a):
            print((x - a + alpha )/alpha)
    elif x in range(a, b):
        print(1)
    elif x in range(b, b + beta):
        print((b + beta - x)/beta)
    elif x > b + beta:
        print(0)

def read_rule(rule):
    new_rules = {}
    x = re.search("(Rule|rule) (?P<RuleID>[0-9]*) (if|If) the (?P<Variable1>[0-1A-Za-z_]+) is (?P<Value1>[0-1A-Za-z_]+) (?P<Operator>and|or) the (?P<Variable2>[0-1A-Za-z_]+) is (?P<Value2>[0-1A-Za-z_]+) then the (?P<Output>[0-1A-Za-z]+) will be (?P<Value>[0-1A-Za-z]+)" , rule)
    if x is None:
        print("Invalid rule")
    else:
        ID = x.group("RuleID")
        variables = [x.group("Variable1"), x.group("Variable2")]
        values = [x.group("Value1"),x.group("Value2")]
        operator = x.group("Operator")
        output = x.group("Output")
        value = x.group("Value")

        new_rules = {"ID": ID, "Variables":variables, "Values":values, "Operator":operator, "Output":{output, value}}
        return new_rules
    
def process(rules):
    for i in range(0, len(rules)):
        new_rule = read_rule(rules[i])
        print(new_rule)

if __name__ == '__main__':
    main()
