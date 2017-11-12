import re

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

    fired_values = fire(file['Rules'], groups)[0]
    output_key = fire(file['Rules'], groups)[1]

    print(defuzzification(fired_values, file['Sets'], output_key))
    
def read_file(filename):
    info = {}
    real_values = []
    sets = {}
    
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
        temp_fuzzy = []
        fuzzy_sets = (file_contents[i+1].split("\n"))
        for x in range (0, len(fuzzy_sets)):
            y = fuzzy_sets[x].split(" ")
            temp_fuzzy.append(y)

        sets[file_contents[i].strip()] = temp_fuzzy

    f.close()
    
    #Populate dictionary with split rule base values
    info['Rule_Base'] = rule_base
    info['Rules'] = rules.split("\n")
    info['Sets'] = sets
    info['Real_Values'] = real_values

    return info

def membership(a,b,alpha,beta,x):
    a = int(a)
    b = int(b)
    alpha = int(alpha)
    beta = int(beta)
    x = int(x)
    
    if x < a - alpha:
        return 0
    elif x in range(a - alpha, a):
            return (x - a + alpha )/alpha
    elif x in range(a, b):
        return 1
    elif x in range(b, b + beta):
        return(b + beta - x)/beta
    elif x > b + beta:
        return 0

def read_rule(rule):
    new_rules = {}
    
    #Use regular expression to match parts of rule with inputted rule
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
        
        #Create dictionary with matched values
        new_rules = {"ID": ID, "Variables":variables, "Values":values, "Operator":operator, "Output":{output: value}}

        return new_rules
    
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
                
        #MIN the values if AND is used, MAX if OR is used
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
           
    sorted_fired_values = {} #required to avoid runtime error when removing 0 values
    for key, value in fired_values.items():
        #Remove None and empty lists so max operation can be performed
        for x in value:
            if x == None:
                value.remove(x)
        if value == []:
            continue
        max_value = max(value)
        #Discard if 0
        if max_value !=0:
            sorted_fired_values[key] = max_value

    return sorted_fired_values, output_key

def defuzzification(fired_values, fuzzy_sets, output_key):
    numerator_values = []
    denominator_values = []
    
    #calculate offset, required when sets have negative values (temperature example in lectures for instance), default value is 0
    offset = 0
    for i in range(0, len(fuzzy_sets)):
        x = fuzzy_sets[output_key][i]
        temp_offset = (float(fuzzy_sets[output_key][i][1]) - float(fuzzy_sets[output_key][i][3]))
        if (temp_offset < offset):
            offset = temp_offset

    for i in range(0, len(fuzzy_sets)):
        if fuzzy_sets[output_key][i][0] in fired_values:
            a = float(fuzzy_sets[output_key][i][1])
            b = float(fuzzy_sets[output_key][i][2])
            alpha = float(fuzzy_sets[output_key][i][3])
            beta = float(fuzzy_sets[output_key][i][4])

            #calculate area
            base = abs((b + beta) - (a - alpha))
            area = (0.5 * fired_values[fuzzy_sets[output_key][i][0]] * base)
            if (a-alpha) == offset:
                center = abs(((a - alpha) + base/2))
            else:
                center = abs(((a - alpha) + base/2) + offset)

            numerator_values.append(area * center)
            denominator_values.append(area)

    solution = sum(numerator_values)/sum(denominator_values)

    return solution

if __name__ == '__main__':
    main()
