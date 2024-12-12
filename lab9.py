import random
import math

def mod_pow(a, b, p):
    result = 1
    base = a % p
    while b > 0:
        if b % 2 == 1:
            result = (result * base) % p
        base = (base * base) % p
        b //= 2
    return result

def miller_rabin_test(p, k):
    if p <= 1:
        return False
    if p == 2:
        return True
    if p % 2 == 0:
        return False

    d = p - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, p - 2)
        x = mod_pow(a, d, p)

        if x == 1 or x == p - 1:
            continue

        for _ in range(r - 1):
            x = mod_pow(x, 2, p)
            if x == p - 1:
                break
        else:
            return False

    return True

def generate_large_prime(bits, k=5):
    while True:
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if miller_rabin_test(n, k):
            return n

def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 2:
        factors.append(n)
    return factors

def is_primitive_root(g, p):
    factors = prime_factors(p - 1)
    for factor in factors:
        if mod_pow(g, (p - 1) // factor, p) == 1:
            return False
    return True

def generate_keys(bits=64):
    p = generate_large_prime(bits)
    while True:
        g = random.randint(2, p - 1)
        if is_primitive_root(g, p):
            break
    x = random.randint(2, p - 2)
    h = mod_pow(g, x, p)
    return (p, g, h, x)

def encrypt(p, g, h, m):
    k = random.randint(2, p - 2)
    c1 = mod_pow(g, k, p)
    c2 = (m * mod_pow(h, k, p)) % p
    return (c1, c2)

def decrypt(p, x, c1, c2):
    s = mod_pow(c1, x, p)
    s_inv = pow(s, -1, p)
    m = (c2 * s_inv) % p
    return m

if __name__ == "__main__":
    bits = 64
    message = 12345

    p, g, h, x = generate_keys(bits)
    print(f"Згенеровано просте число p: {p}")
    print(f"Вибрано генератор g: {g}")
    print(f"Публічний ключ h: {h}")
    print(f"Приватний ключ x: {x}")

    c1, c2 = encrypt(p, g, h, message)
    print(f"Зашифроване повідомлення: c1 = {c1}, c2 = {c2}")

    decrypted_message = decrypt(p, x, c1, c2)
    print(f"Розшифроване повідомлення: {decrypted_message}")

    if message == decrypted_message:
        print("Шифрування та дешифрування успішні!")
    else:
        print("Помилка шифрування/дешифрування!")
