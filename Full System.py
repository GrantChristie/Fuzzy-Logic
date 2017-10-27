import re

def main():
    filename = input("Enter file to be processed: ")
    file = read_file(filename)
    print(file)
    group = {}
    groups = {}
    for i in range(0,len(file['Real_Values'])):
        name = file['Real_Values'][i]['name']
        real_value = file['Real_Values'][i]['value']
        #print (name)
        #print (value)

        for key, value in file['Sets'].items():
            if key == name:
                for x in value:
                    #print(x[0])          
                    #{x[0], membership(x[1], x[2], x[3], x[4], real_value)}
                    group[x[0]] = membership(x[1], x[2], x[3], x[4], real_value)
        groups[name] = group

    #print (groups)
    #print (file['Fuzzy_Sets'])
    fired_values = process(file['Rules'], groups)[0]
    output_key = process(file['Rules'], groups)[1]#revise this if time permits
    #print (output_key)
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
            #print (y)
            temp_fuzzy.append(y)

        sets[file_contents[i].strip()] = temp_fuzzy

    f.close()

    info['Rule_Base'] = rule_base
    info['Rules'] = rules.split("\n")
    info['Sets'] = sets
    info['Real_Values'] = real_values

    return info

def membership(a,b,alpha,beta,x):
    #MAYBE THESE SHOULD BE CHANGED TO FLOATS TO SO MORE VALUES CAN BE ACCEPTED
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

        new_rules = {"ID": ID, "Variables":variables, "Values":values, "Operator":operator, "Output":{output: value}}
        return new_rules
    
def process(rules,memberships):
    fired_values = {}
    conditions = {}
    for i in range(0, len(rules)):
        condition_ints = []
        rule = read_rule(rules[i])
        for x in range(0,2):
            conditions.update({rule["Variables"][x] : rule["Values"][x]})

        for key, value in conditions.items():
            condition_ints.append(memberships[key][value])

        #print(conditions)
        #print(condition_ints)

        #SEE SLIDE 28
        if rule['Operator'] == "and":
            operator_value = min(condition_ints)
        else:
            operator_value = max(condition_ints)
        #print (operator_value)

        #print(list(rule["Output"].values())[0])
        output_value = list(rule["Output"].values())[0]
        output_key = list(rule["Output"].keys())[0]#revise...
        #print (output_value)

        if output_value in fired_values:
           fired_values[output_value].append(operator_value)
        else:
           fired_values[output_value] = [operator_value]
           
    sorted_fired_values = {} #required to avoid runtime error when removing 0 values
    for key, value in fired_values.items():
        max_value = max(value)
        #print(max_value)
        if max_value !=0:
            sorted_fired_values[key] = max_value

    return sorted_fired_values, output_key

def defuzzification(fired_values, fuzzy_sets, output_key):
    numerator_values = []
    denominator_values = []
    #print(fired_values)
    #print(fired_values.values())
    #for i in fired_values:
     #   defuzz_fired_values.append(fired_values.key())
    #print(fuzzy_sets[output_key])
    offset = 0 
    for i in range(0, len(fuzzy_sets)):
        x = fuzzy_sets[output_key][i]
        temp_offset = (float(fuzzy_sets[output_key][i][1]) - float(fuzzy_sets[output_key][i][3]))
        if (temp_offset < offset):
            offset = temp_offset
    print("offset: ", offset)

    for i in range(0, len(fuzzy_sets)):
        #print(fuzzy_sets[output_key][i])
        if fuzzy_sets[output_key][i][0] in fired_values:
            a = float(fuzzy_sets[output_key][i][1])
            b = float(fuzzy_sets[output_key][i][2])
            alpha = float(fuzzy_sets[output_key][i][3])
            beta = float(fuzzy_sets[output_key][i][4])

            #print(a,b,alpha,beta)
            #calculate base of fuzzy sets (found with sketches in tutorial)
            print (b," + ",beta," - ",a," - ",alpha)
            base = abs((b + beta) - (a - alpha))
            print("Base: ",base)
            print("Value: ",fired_values[fuzzy_sets[output_key][i][0]])
            #area = 0.5 * value of results from rule firing * base
            area = (0.5 * fired_values[fuzzy_sets[output_key][i][0]] * base)
            print ("Area: ", area)
            if (a-alpha) == offset:
                center = abs(((a - alpha) + base/2)) #+ offset
            else:
                center = abs(((a - alpha) + base/2) + offset)
            print ("Center: ", center)
            numerator_values.append(area * center)
            denominator_values.append(area)

    print("top: ",numerator_values)
    print("bottom: ",denominator_values)

    solution = sum(numerator_values)/sum(denominator_values)
    return solution

if __name__ == '__main__':
    main()
