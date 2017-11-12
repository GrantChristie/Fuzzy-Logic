import re
from FileReader import read_file
from MembershipCalculator import membership
from RuleReader import read_rule

def main():
    filename = input("Enter file to be processed: ")
    file = read_file(filename)  
    group = {}
    groups = {}
    for i in range(0,len(file['Real_Values'])):
        name = file['Real_Values'][i]['name']
        real_value = file['Real_Values'][i]['value']
        for key, value in file['Sets'].items():
            if key == name:
                for x in value:
                    group[x[0]] = membership(x[1], x[2], x[3], x[4], real_value)
        groups[name] = group
    print(fire(file['Rules'], groups)[0])

def fire(rules,memberships):
    fired_values = {}
    conditions = {}
    
    for i in range(0, len(rules)):
        condition_ints = []
        rule = read_rule(rules[i])

        for x in range(0,2):
            conditions.update({rule["Variables"][x] : rule["Values"][x]})

        for key, value in conditions.items():
            condition_ints.append(memberships[key][value])

        for x in condition_ints:
            if x == None:
                condition_ints.remove(x)

        if rule['Operator'] == "and":
            operator_value = min(condition_ints)
        else:
            operator_value = max(condition_ints)

        output_value = list(rule["Output"].values())[0]
        output_key = list(rule["Output"].keys())[0]

        if output_value in fired_values:
           fired_values[output_value].append(operator_value)
        else:
           fired_values[output_value] = [operator_value]
           
    sorted_fired_values = {}
    for key, value in fired_values.items():

        for x in value:
            if x == None:
                value.remove(x)
        if value == []:
            continue
        max_value = max(value)
        if max_value !=0:
            sorted_fired_values[key] = max_value

    return sorted_fired_values, output_key
            
if __name__ == '__main__':
    main()
