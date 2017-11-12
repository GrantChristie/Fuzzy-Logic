import re
from FileReader import read_file
from MembershipCalculator import membership
from RuleReader import read_rule
from RuleFirer import fire

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

def defuzzification(fired_values, fuzzy_sets, output_key):
    numerator_values = []
    denominator_values = []
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
