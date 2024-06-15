import random
import math
import sys
import pickle

def exponentiation_modulo(a, k, n):
    kbin = str(bin(k)[2:])
    kbin = kbin[::-1]
    b = 1
    if k == 0:
        return b
    A = a
    if int(kbin[0]) == 1:
        b = a
    for i in range(1, len(kbin)):
        A = (A ** 2) % n
        if int(kbin[i]) == 1:
            b = (A * b) % n
    return b

def is_prime(n):
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    check = n - 2
    if check <= 20:
        check = check - 2
    else:
        check = 20
    for i in range(1, check):
        a = random.randint(2, n - 1)
        r = exponentiation_modulo(a, n - 1, n)
        if r != 1:
            return False
    return True

def generate_from_len(length):
    num = random.getrandbits(length)
    num |= (1 << length - 1) | 1
    return num

def generate_nlen_bit(length):
    while not is_prime(num := generate_from_len(length)):
        pass
    return num

def gen_p(plen):
    p = generate_nlen_bit(plen)
    return p

def gen_q(qlen):
    q = generate_nlen_bit(qlen)
    return q

def evklid(a, b):
    x1 = 0
    x2 = 1
    y2 = 0
    y1 = 1
    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    return x2

def encrypt(text, e, n):
    block = math.floor(math.log(n, 2))
    bintext = "".join(map("{:08b}".format, text))
    if len(bintext) % block != 0:
        bintext = bintext[::-1]
        bintext += '0' * (block - len(bintext) % block)
        bintext = bintext[::-1]
    res = []
    for i in range(0, len(bintext), block):
        a = int(bintext[i: i + block], 2)
        c = exponentiation_modulo(a, e, n)
        res.append(c)
    return res

def decrypt(text, d, n):
    block = math.floor(math.log(n, 2))
    res = []
    for i in range(0, len(text)):
        a = exponentiation_modulo(text[i], d, n)
        res.append(a)
    bintext = ''
    for i in range(1,len(res)):
        check = bin(res[i])[2:]
        while len(check) < block:
            check = check[::-1]
            check += '0'
            check = check[::-1]
        bintext += check
    bintext = bin(res[0])[2:] + bintext
    while len(bintext) % 8 != 0:
        bintext = bintext[::-1]
        bintext += '0'
        bintext = bintext[::-1]
    decr_mes = []
    for i in range(len(bintext), 0, -8):
        decr_mes.append(int(bintext[i-8: i], 2))
    return decr_mes

print('что вы хотите сделать?\n'
      '1 - сгенерировать ключи\n'
      '2 - зашифровать\n'
      '3 - расшифровать\n')
choose = int(input())
if not (choose == 1 or choose == 2 or choose == 3):
    while not (choose == 1 or choose == 2 or choose == 3):  
        print('не могу выполнить, введите еще раз')
        choose = int(input())

if choose == 1:

    print('введите длину p')
    plen = int(input())
    print('введите длину q')
    qlen = int(input())
    p = gen_p(plen)
    q = gen_q(qlen)
    # print(p, q, sep='\n')
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    while math.gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    print('открытый ключ: e = ', e)
    print('открытый ключ: n = ', n)
    d = evklid(e, phi)
    if d < 0:
        d += phi
    print('закрытый ключ: d = ', d)
    print('если желаете выйти из программы - введите 1 или любое другое число\n'
          'если желаете продолжить, то введите:\n'
          '2 - для зашифрования\n'
          '3 - для расшифрования\n')
    choose = int(input())
    if choose != 2 and choose != 3:
        sys.exit('вы захотели выйти из программы')

if choose == 2:
    print('1 - зашифровать строку\n'
          '2 - зашифровать файл')
    choise_t_f = int(input())
    if choise_t_f == 1:
        print('введите текст')
        text = input()
        text = bytes(text, 'utf-8')
        print('какой ключ хотите использовать?:\n'
              '1 - сгенерированный раннее\n'
              '2 - введу свой')
        choose2 = int(input())
        if choose2 == 1:
            openkey_e = e
            openkey_n = n
        if choose2 == 2:
            print('введите е:')
            openkey_e = int(input())
            print('введите n:')
            openkey_n = int(input())
        result = encrypt(text, openkey_e, openkey_n)
        print(result)

    if choise_t_f == 2:
        print('введите полный путь к файлу, который надо зашифровать:')
        path_for_en = input()
        with open(path_for_en, 'rb') as file:
            text = file.read()
        print('какой ключ хотите использовать?:\n'
              '1 - сгенерированный раннее\n'
              '2 - введу свой')
        choose2 = int(input())
        if choose2 == 1:
            openkey_e = e
            openkey_n = n
        if choose2 == 2:
            print('введите е:')
            openkey_e = int(input())
            print('введите n:')
            openkey_n = int(input())
        result = encrypt(text, openkey_e, openkey_n)
        print('введите полный путь к файлу, в который надо поместить результат зашифрования:')
        new_path = input()
        with open(new_path, 'wb') as file:
            pickle.dump(result, file)
        print('появился новый файл')
    print('если желаете выйти из программы - введите 1 или любое другое число\n'
          'если желаете продолжить, то введите:\n'
          '3 - для расшифрования')
    choose = int(input())
    if choose != 3:
        sys.exit('вы захотели выйти из программы')

if choose == 3:
    print('1 - расшифровать строку\n'
          '2 - расшифровать файл')
    choise_t_f = int(input())
    if choise_t_f == 1:
        print('введите числа через пробел')
        text = input().split()
        for i in range(len(text)):
            text[i] = int(text[i])
        print('какой ключ хотите использовать?:\n'
              '1 - сгенерированный раннее\n'
              '2 - введу свой')
        choose2 = int(input())
        if choose2 == 1:
            openkey_n = n
            closed_d = d
        if choose2 == 2:
            print('введите n:')
            openkey_n = int(input())
            print('введите d:')
            closed_d = int(input())
        res = decrypt(text, closed_d, openkey_n)
        result = ''
        for i in res:
            result += chr(i)
        print(result[::-1])
    if choise_t_f == 2:
        print('введите полный путь к файлу, который надо расшифровать:')
        path_for_de = input()
        with open(path_for_de, "rb") as file:
            text = pickle.load(file)
        print('какой ключ хотите использовать?:\n'
              '1 - сгенерированный раннее\n'
              '2 - введу свой')
        choose2 = int(input())
        if choose2 == 1:
            openkey_n = n
            closed_d = d
        if choose2 == 2:
            print('введите n:')
            openkey_n = int(input())
            print('введите d:')
            closed_d = int(input())
        result = decrypt(text, closed_d, openkey_n)
        res = b''
        for i in range(len(result) - 1, -1, -1):
            res += result[i].to_bytes(1, 'big')
        print('введите полный путь к файлу, в который надо поместить результат расшифрования:')
        new_path = input()
        with open(new_path, 'wb') as file:
            file.write(res)
        print('появился новый файл')
    print('если желаете выйти из программы - введите 1 или любое другое число\n'
          'если желаете продолжить, то введите:\n'
          '2 - для зашифрования')
    choose = int(input())
    if choose != 2:
        sys.exit('вы захотели выйти из программы')