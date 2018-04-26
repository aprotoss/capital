import sys

filename = 'captalevent.py'

def find_CoClass(content):
    res = {}
    coclass = None
    for line in content:
        if len(line) > 5:
            token = line.split()

            #find CLSID for CoClassBaseClass
            if coclass is not None:
                tk = token[2].split('\'')
                res[coclass] = tk[1]
                coclass = None

            #find CoClassBaseClass
            if token[0] == 'class':
                try:
                    tk = token[1].split('(')
                    if tk[1] == 'CoClassBaseClass):':
                        res[tk[0]] = 0
                        coclass = tk[0]
                except:
                    pass
    return res

def find_ClassEvent(content):
    res = {}
    classevent = None
    multiline = None
    for line in content:
        if len(line) > 5:
            token = line.split()
            if token[0] == 'class':
                if multiline:
                    res[classevent] = multiline
                    multiline = None
                try:
                    if token[1][:2] == '_I' and token[1][-7:] == 'Events:':
                        res[token[1][2:-1]] = None
                        classevent = token[1][2:-1]
                except:
                    continue

            if token[0] == '#' and token[1] == 'Event' and token[2] == 'Handlers':
                multiline = str()

            if multiline is not None and line[0] == '#': 
                multiline += line
    return res

if __name__ == '__main__':
    print("Start ...")

    clsid = None
    event = None

    with open('SKCOM.py', 'r') as skcom:
        clsid = find_CoClass(skcom)
        skcom.seek(0)
        event = find_ClassEvent(skcom)

    with open('sklib.py', 'w') as sklib:
        sklib.write('# -*- coding: utf-8 -*-\n')
        sklib.write('\'\'\'\n %s \n\'\'\'\n' % 'Captal Python API Generater')


        sklib.write('\'\'\'\n%s \n\'\'\'\n' % 'CLSID')
        for cid in clsid:
            sklib.write('CLSID_%s = \'%s\'\n' % (cid, clsid[cid]))

        sklib.write('\n\n')
        sklib.write('\'\'\'\n%s \n\'\'\'\n' % 'Event')

        for e in event:
            funcs = event[e].replace('=defaultNamedNotOptArg', '').replace('#', '').replace('\t', '    ').replace('', '').split(':')

            sklib.write('class %s(object):\n' % e)
            for func in funcs:
                if len(func) < 3:
                    continue
                tk = func.split()
                sklib.write(func+': \n        print(\'Event: %s\')\n' % tk[1].split('(')[0])

            sklib.write('\n\n')


