from random import randint as rnt
import numpy as np
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

    a = (1 if a == '' else int(a))
    b = (1 if b == '' else int(b))
    c = (0 if c == '' else int(c))
    for i in range(a):
        c += rnt(1,b)

    return c