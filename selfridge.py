import time

# Selfridge/Pomerance/Wagstaff Conjecture about primality testing:
# IF  2^p−1   ≡ 1 (mod p) 
# AND f_{p+1} ≡ 0 (mod p),
# THEN p is prime


def two_pow_n_mod_x0(n, x):
    return (2**n) % x

# Numbers 1-100,000: 281s
def two_pow_n_mod_x1(n, x):
    s = 1
    for _ in range(n):
        s = (s * 2) % x
    return s

# Numbers 1-100,000: 0.2s
# Numbers 1-1,000,000: 3.2s
# Numbers 1-10,000,000: 37s
# Numbers 1-100,000,000: 450s
def two_pow_n_mod_x2(n, x):
    s = 1
    while n:
        if n % 2:
            s = (s * 2) % x
        s = (s * s) % x
        n = n//2
    return s

def fib_n_mod_x0(n, x):
    a,b = 1,1
    for _ in range(n-2):
        a,b = b, a+b
    return b % x

# Numbers 1-100,000: 394s
def fib_n_mod_x1(n, x):
    a,b = 1,1
    for _ in range(n-2):
        a,b = b, ((a+b) % x)
    return b

def mm_mod_x(m1, m2, x):
    a = ((m1[0][0]*m2[0][0] %x)+(m1[0][1]*m2[1][0] %x)) % x
    b = ((m1[0][0]*m2[0][1] %x)+(m1[0][1]*m2[1][1] %x)) % x
    c = ((m1[1][0]*m2[0][0] %x)+(m1[1][1]*m2[1][0] %x)) % x
    d = ((m1[1][0]*m2[0][1] %x)+(m1[1][1]*m2[1][1] %x)) % x
    return [[a,b],[c,d]]
# Numbers 1-100,000: 2.7s
# Numbers 1-1,000,000: 34s
# Numbers 1-10,000,000: 419s
def fib_n_mod_x2(n, x):
    # Insight: A=[[1, 1],
    #             [1, 0],]
    # A^n[0][0] = F_n
    # A^n can be calculated with binary squaring method
    A = [[1, 1],[1,0]]
    S = [[1, 1],[1,0]]
    n = n - 1
    while n:
        if n % 2:
            S = mm_mod_x(A, S, x)
        S = mm_mod_x(S, S, x)
        n = n//2
    return S[0][0]

# Numbers 1-1,000,000: 9s
# Numbers 1-10,000,000: 123s
# Numbers 1-100,000,000: 1391s
def fib_n_mod_x3(n, x):
    # current n is 1
    fn = 1 # F_{n}
    fn_minus = 0 # F_{n-1}
    while n:
        if n % 2:
            fn_minus, fn = fn, (fn+fn_minus)%x
            # n increment by 1
        a = fn*fn % x
        b = fn_minus*fn_minus % x
        c = fn*fn_minus % x
        c2 = 2*c % x
        fn_minus, fn = (a+b) % x, a+c2 % x
        # double n
        n = n//2
    return fn

def modmult1(a,b,x):
    if a>b:
        a,b=b,a
    r = 0
    bits = []
    while a:
        bits.append(a%2)
        a = a//2
    bits.reverse()
    for bit in bits:
        r = r * 2 % x
        if bit:
            r = r + b % x
    return r

# Slower, abandoned
def fib_n_mod_x4(n, x):
    fn = 1
    fn_minus = 0 
    while n:
        if n % 2:
            fn_minus, fn = fn, (fn+fn_minus)%x
        a = modmult1(fn, fn, x)
        b = modmult1(fn_minus, fn_minus, x)
        c = modmult1(fn, fn_minus, x)
        c2 = modmult1(2, c, x)
        fn_minus, fn = (a+b) % x, a+c2 % x
        n = n//2
    return fn

# Numbers 1-100,000: 25s
def is_prime0(x):
    for i in range(2,x):
        if x % i == 0:
            return False
    return True

# Numbers 1-100,000: 0.15s
# Numbers 1-1,000,000: 3.6s
# Numbers 1-10,000,000: 97s
# Numbers 1-100,000,000: 3065s
def is_prime2(x):
    for i in range(2,int(x**0.5)+1):
        if x % i == 0:
            return False
    return True

# Numbers 1-10,000,000: 55s
# Numbers 1-100,000,000: 1573s
def is_prime3(x):
    # This is a "wheel method: only check the things that are correct mod 10"
    for factor in (2,3,5,7):
        if x % factor == 0:
            return False
    ub = int(x**0.5)+1
    for last_digit in (1,3,7,9):
        for factor in range(10+last_digit, ub, 10):
            if x % factor == 0:
                return False
    return True

def all_primes0(start, end):
    r = []
    for x in range(start, end):
        r.append(is_prime0(x))
    return r

# Classic sieve of eratosthenes
# Note: poss improvement, can cache, also to generate primes from X to Y, we need all primes up to X**0.5 only
# Note: poss improvement, can use wheel method again
# Numbers 1-1,000,000: 0.12s
# Numbers 1-10,000,000: 1.7s
# Numbers 1-100,000,000:
def all_primes4(start, end):
    """Return an array of True/False for all numbers from start to end (inclusive)"""
    is_prime = [True]*(end+1)
    assert start >= 2
    ub = int(end**0.5)+1
    for x in range(2, ub):
        if is_prime[x]:
            for composite in range(x*2, end, x):
                is_prime[composite] = False
    return is_prime[start:]

def fermat_test(x):
    return two_pow_n_mod_x2(x-1, x)==1

def fib_test(x):
    return fib_n_mod_x3(x+1, x)==0

def prime_test(x):
    return is_prime3(x)

def count_true(l):
    i = 0
    for x in l:
        if x:
            i+=1
    return i

def test():
    test_range = range(2,1000)
    for powmod in (two_pow_n_mod_x1, two_pow_n_mod_x2):
        for x in test_range:
            actual, expected = powmod(x-1, x), two_pow_n_mod_x0(x-1,x)
            assert actual == expected, "{} != {} (x={}, f={})".format(actual, expected, x, powmod.__name__)
    for fibmod in (fib_n_mod_x1, fib_n_mod_x2, fib_n_mod_x3, fib_n_mod_x4):
        for x in test_range:
            actual, expected = fibmod(x-1, x), fib_n_mod_x0(x+1, x)
            assert actual == expected, "{} != {} (x={}, f={})".format(actual, expected, x, fibmod.__name__)
    for prime_test in (is_prime_2, is_prime3):
        for x in test_range:
            actual, expected = prime_test(x), is_prime0(x)
            assert actual == expected, "{} != {} (x={}, f={})".format(actual, expected, x, prime_test.__name__)
    ref_primes = all_primes0(test_range.start, test_range.stop-1)
    for all_primes in (all_primes4,):
        check_primes = all_primes(test_range.start, test_range.stop-1)
        assert len(check_primes) == len(ref_primes) == len(test_range), "{} returned the wrong size array".format(all_prime.__name__)
        for actual,expected,x in zip(check_primes, ref_primes, test_range):
            assert actual == expected, "{} != {} (x={}, f={})".format(actual, expected, x, all_primes.__name__)
    assert False

def main(limit=1000):
    block = 100_000_000
    num_blocks = 1
    for y in range(0, block*num_blocks, block):
        if y==0:
            start, stop = 2, block-1
        else:
            start, stop = y, y+block-1
        r=range(start, stop+1)
        t0 = time.time()
        fert = [fermat_test(start+x) for x in r]
        t1 = time.time()
        fibt = [fib_test(start+x) for x in r]
        t2 = time.time()
        primet = all_primes4(start, stop)
        t3 = time.time()

        fermat_time, fib_time, prime_time, total_time = t1-t0, t2-t1, t3-t2, t3-t0
        print("Fermat: {} ({}% time, {}% numbers)".format(fermat_time, fermat_time/total_time*100, count_true(fert)/len(fert)*100))
        print("Fib: {} ({}% time, {}% numbers)".format(fib_time, fib_time/total_time*100, count_true(fibt)/len(fibt)*100))
        print("Prime: {} ({}% time, {}% numbers)".format(prime_time, prime_time/total_time*100, count_true(primet)/len(primet)*100))
        print("Total: {}".format(total_time))
        for x in r:
            if fert[x-start] and fibt[x-start] and not primet[x-start]:
                print("{} is a counterexample".format(x))
                exit(0)
        print("{}-{} contains no counterexamples".format(start, stop))

if __name__ == "__main__":
    test()
    #main(10_000_000)
    exit(0)

