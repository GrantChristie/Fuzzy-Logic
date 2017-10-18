import re

rule = input("Enter rule: ")

x = re.search("Rule|rule (?P<RuleID>[0-9]*) if the (?P<Variable>[0-1A-Za-z_]+) is (?P<Value>[0-1A-Za-z_]+)", rule)

if x is None:
    print("Invalid rule")
else:
    ID = x.group("RuleID")
    print(ID)#remove when done
    variable = x.group("Variable")
    print(variable)#remove when done
    value = x.group("Value")
    print(value)#remove when done
