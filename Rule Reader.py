import re

rule = input("Enter rule: ")

x = re.search("(Rule|rule) (?P<RuleID>[0-9]*) if the (?P<Variable1>[0-1A-Za-z_]+) is (?P<Value1>[0-1A-Za-z_]+) (?P<Operator>and|or) the (?P<Variable2>[0-1A-Za-z_]+) is (?P<Value2>[0-1A-Za-z_]+) then the (?P<Output>[0-1A-Za-z]+) will be (?P<Value>[0-1A-Za-z]+)" , rule)

if x is None:
    print("Invalid rule")
else:
    ID = x.group("RuleID")
    print(ID)#remove when done
    variables = [x.group("Variable1"), x.group("Variable2")]
    print(variables)
    values = [x.group("Value1"),x.group("Value2")]
    print (values)
    operator = x.group("Operator")
    print(operator)
    output = x.group("Output")
    print(output)
    value = x.group("Value")
    print(value)
    
