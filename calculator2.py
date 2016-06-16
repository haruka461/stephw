def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readTimes(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def readParenthesis(line, index):
    if line[index] == '(':
        token = {'type': 'PAROPEN'}
    elif line[index] == ')':
        token = {'type': 'PARCLOSE'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    count = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)
            
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readParenthesis(line, index)
        elif line[index] == ')':
            (token, index) = readParenthesis(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    if count > 0:
        print 'Invalid syntax1'
    return tokens

def evaluate_times_div(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'TIMES':
            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER':
                tokens[index - 1]['number'] = tokens[index - 1]['number'] * tokens[index + 1]['number']
                del tokens[index  : index + 2]
                index -= 2
            else:
                print 'Invalid syntax2'
                #exit(1)
        elif tokens[index]['type'] == 'DIVIDE':
            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER':
                tokens[index - 1]['number'] = tokens[index - 1]['number'] * 1.0 / tokens[index + 1]['number']
                del tokens[index  : index + 2]
                index -= 2
            else:
                print 'Invalid syntax3'
                exit(1)
        index += 1
    return tokens

def evaluate_plus_minus(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax4'
        index += 1
    return answer

def make_parindexlist(tokens):
    index = 0
    count = 0
    parindex = []
    while index < len(tokens):
        if tokens[index]['type'] == 'PAROPEN':
            parindex.append({'pos': index})
            count += 1
        elif tokens[index]['type'] == 'PARCLOSE':
            if count > 0:
                count -= 1
            else:
                print 'Invalid syntax5'
                exit(1)
        index += 1
    if count > 0:
        print 'Invalid syntax6'
        exit(1)
    return parindex

def evaluate_parenthesis(tokens):
    parindex = make_parindexlist(tokens)
    while len(parindex) > 0:
        index = parindex[-1]['pos'] + 1
        while index < len(tokens):
            if tokens[index]['type'] == 'PARCLOSE':
                part_answer = evaluate(tokens[parindex[-1]['pos'] + 1 : index])
                tokens.insert(parindex[-1]['pos'], {'type': 'NUMBER', 'number': part_answer})
                del tokens[parindex[-1]['pos'] + 1 : index+2]
            index += 1
        parindex.pop()
    return tokens

def evaluate(tokens):
    evaluate_times_div(tokens)
    answer = evaluate_plus_minus(tokens)
    return answer


while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    tokens = evaluate_parenthesis(tokens)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer
