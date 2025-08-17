from random import randint as rnt

def code_roll(script: str)->int:
    '''
    :param script: deve ter o formato adbpc onde a é o número de dados, b é o tipo de dado e c é o modificador
    :return: rolagem de a dados de b faces mais c
    '''
    a = ''
    b = ''
    c = ''
    d = False
    p = False
    for i in script:
        if i.isnumeric():
            if d:
                b += i
            elif p:
                c += i
            else:
                a += i
        else:
            if i == 'd':
                d = True
                p = False
            if i == 'p':
                p = True
                d = False

    if a == '':
        a = 1
    if b == '':
        b = 1
    if c == '':
        c = 0
    a = int(a)
    b = int(b)
    c = int(c)
    for i in range(a):
        c += rnt(1,b)

    return c
