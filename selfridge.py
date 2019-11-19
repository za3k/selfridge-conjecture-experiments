"""
Selfridge/Pomerance/Wagstaff Conjecture about primality testing:
  IF  2^{p−1} ≡ 1 (mod p) 
  AND f_{p+1} ≡ 0 (mod p),
  THEN p is prime

This program both searches for counterexamples, and tests methods for correctness/speed.
"""
import time

def timeit(f):
    a = time.time()
    r = f()
    b = time.time()
    return r, b-a

# In general most of the left-to-right methods could be converted to be right-to-left methods,
# but the speeds don't really seem to change appreciably
def bits(n, msb_first=False):
    b = []
    while n:
        b.append(n%2)
        n = n//2
    if msb_first:
        b.reverse()
    return b

def two_pow_n_mod_x0(n, x):
    return (2**n) % x

# Numbers 1-100,000: 281s
def two_pow_n_mod_x1(n, x):
    if x == 1:
        return 0
    s = 1
    for _ in range(n):
        s = (s * 2) % x
    return s

def two_pow_n_mod_x2a(n, x):
    # Explicit bits method
    if x == 1:
        return 0
    s = 1
    for bit in bits(n, msb_first=True):
        s = (s * s) % x
        if bit:
            s = (s * 2) % x
    return s

def two_pow_n_mod_x2b(n, x):
    # Recursive method
    if x == 1:
        return 0
    if n==0:
        return 1
    s = two_pow_n_mod_x2b(n//2, x)
    if n % 2:
        return (s*s*2) % x
    else:
        return s*s % x

def two_pow_n_mod_x3(n, x):
    return pow(2, n, x)

def fib_n_mod_x0(n, x):
    if x == 1:
        return 0
    a,b = 1,1
    for _ in range(n-2):
        a,b = b, a+b
    return b % x

def fib_n_mod_x1(n, x):
    if x == 1:
        return 0
    a,b = 1,1
    for _ in range(n-2):
        a,b = b, ((a+b) % x)
    return b % x

def mm_mod_x(m1, m2, x):
    a = ((m1[0][0]*m2[0][0] %x)+(m1[0][1]*m2[1][0] %x)) % x
    b = ((m1[0][0]*m2[0][1] %x)+(m1[0][1]*m2[1][1] %x)) % x
    c = ((m1[1][0]*m2[0][0] %x)+(m1[1][1]*m2[1][0] %x)) % x
    d = ((m1[1][0]*m2[0][1] %x)+(m1[1][1]*m2[1][1] %x)) % x
    return [[a,b],[c,d]]
def fib_n_mod_x2a(n, x):
    # Insight: A=[[1, 1],
    #             [1, 0],]
    # A^n[0][0] = F_n
    # A^n can be calculated with binary squaring method
    if x == 1:
        return 0
    A = [[1, 1],[1,0]]
    S = [[1, 1],[1,0]]
    for _ in range(n-2):
        S = mm_mod_x(S, A, x)
    return S[0][0]
def fib_n_mod_x2b(n, x):
    # Insight: A=[[1, 1],
    #             [1, 0],]
    # A^n[0][0] = F_n
    # A^n can be calculated with binary squaring method
    if x == 1:
        return 0
    A = [[1, 1],[1,0]]
    S = [[1, 1],[1,0]]
    for bit in bits(n-1, msb_first=True)[1:]:
        S = mm_mod_x(S, S, x)
        if bit:
            S = mm_mod_x(A, S, x)
    return S[0][0]

def fib_n_mod_x3(n, x):
    # current n is 1
    fn = 1 # F_{n}
    fn_minus = 0 # F_{n-1}
    for bit in bits(n, msb_first=True)[1:]:
        a = fn*fn % x
        b = fn_minus*fn_minus % x
        c = fn*fn_minus % x
        c2 = 2*c % x
        fn_minus, fn = (a+b) % x, (a+c2) % x
        if bit:
            fn_minus, fn = fn, (fn+fn_minus)%x
    return fn

def modmult1(a,b,x):
    if a>b:
        a,b=b,a
    r = 0
    for bit in bits(a, msb_first=True):
        r = r * 2 % x
        if bit:
            r = r + b % x
    return r
# Slower than fib_n_mod_x3
def fib_n_mod_x4(n, x):
    fn = 1
    fn_minus = 0 
    for bit in bits(n, msb_first=True)[1:]:
        a = modmult1(fn, fn, x)
        b = modmult1(fn_minus, fn_minus, x)
        c = modmult1(fn, fn_minus, x)
        c2 = modmult1(2, c, x)
        fn_minus, fn = (a+b) % x, (a+c2) % x
        if bit:
            fn_minus, fn = fn, (fn+fn_minus)%x
    return fn

def is_prime0(x):
    if x == 1:
        return False
    for i in range(2,x):
        if x % i == 0:
            return False
    return True

def is_prime2(x):
    if x == 1:
        return False
    for i in range(2,int(x**0.5)+1):
        if x % i == 0:
            return False
    return True

def is_prime3(x):
    # This is a "wheel method: only check the things that are correct mod 10"
    if x == 1:
        return False
    if x in (2,3,5,7):
        return True
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
    for x in range(start, end+1):
        r.append(is_prime0(x))
    return r

# Classic sieve of eratosthenes
# Note: poss improvement, can cache, also to generate primes from X to Y, we need all primes up to X**0.5 only
# Note: poss improvement, can use wheel method again
def all_primes4(start, end):
    """Return an array of True/False for all numbers from start to end (inclusive)"""
    is_prime = [True]*(end+1)
    is_prime[0] = False
    is_prime[1] = False
    assert start >= 0
    ub = int(end**0.5)+1
    for x in range(2, ub):
        if is_prime[x]:
            for composite in range(x*2, end+1, x):
                is_prime[composite] = False
    return is_prime[start:end+1]

def count_true(l):
    i = 0
    for x in l:
        if x:
            i+=1
    return i

# For these, the first in each list is a definitely-correct "reference" implementation
# The last is used in the main program--it's the fastest
powmods = (two_pow_n_mod_x0, two_pow_n_mod_x1, two_pow_n_mod_x2a, two_pow_n_mod_x2b, two_pow_n_mod_x3)
fibmods = (fib_n_mod_x0, fib_n_mod_x1, fib_n_mod_x2a, fib_n_mod_x2b, fib_n_mod_x4, fib_n_mod_x3)
prime_tests = (is_prime0, is_prime2, is_prime3)
batch_prime_calcs = (all_primes0, all_primes4)
def test():
    test_range = range(1,1000)
    ref_powmod = powmods[0]
    LARGE=1000000
    print("Testing that all methods agree for numbers 1-{}.".format(test_range.stop-1))
    t0 = time.time()
    for powmod in powmods[1:]:
        for x in test_range:
            actual, expected = powmod(x-1, LARGE), two_pow_n_mod_x0(x-1,LARGE)
            assert actual == expected, "{} != {} (n={}, x={}, f={})".format(actual, expected, x-1, LARGE, powmod.__name__)
            actual, expected = powmod(x-1, x), two_pow_n_mod_x0(x-1,x)
            assert actual == expected, "{} != {} (n={}, x={}, f={})".format(actual, expected, x-1, x, powmod.__name__)
    ref_fibmod = fibmods[0]
    for fibmod in fibmods[1:]:
        for x in test_range:
            actual, expected = fibmod(x+1, LARGE), ref_fibmod(x+1, LARGE)
            assert actual == expected, "{} != {} (n={}, x={}, f={})".format(actual, expected, x+1, LARGE, fibmod.__name__)
            actual, expected = fibmod(x+1, x), ref_fibmod(x+1, x)
            assert actual == expected, "{} != {} (n={}, x={}, f={})".format(actual, expected, x+1, x, fibmod.__name__)
    ref_prime_test = prime_tests[0]
    for prime_test in prime_tests[1:]:
        for x in test_range:
            actual, expected = prime_test(x), ref_prime_test(x)
            assert actual == expected, "{} != {} (x={}, f={})".format(actual, expected, x, prime_test.__name__)
    ref_all_primes_calc = batch_prime_calcs[0]
    ref_primes = ref_all_primes_calc(test_range.start, test_range.stop-1)
    for all_primes in batch_prime_calcs[1:]:
        check_primes = all_primes(test_range.start, test_range.stop-1)
        assert len(check_primes) == len(ref_primes) == len(test_range), "{} returned the wrong size array: {} == {} == {}".format(all_primes.__name__, len(check_primes), len(ref_primes), len(test_range))
        for actual,expected,x in zip(check_primes, ref_primes, test_range):
            assert actual == expected, "{} != {} (x={}, f={})".format(actual, expected, x, all_primes.__name__)
    t1=time.time()
    print("Self-test passed in: {:.2f}s".format(t1-t0))
    print("All methods should be correct.")

def timing():
    print("Running timing test--testing how many numbers we can crunch by iteratively increasing range sizes")
    maxpower = 10
    time_min = 0.1 # Don't report numbers over this value
    power_min = 4 # Report all numbers over this value
    timelimit = time_min # once an iteration goes over this time limit, stop
    print("Timing fermat test methods")
    for powmod in powmods:
        for power in range(1,maxpower):
            r = range(2, 10**power)
            result, time = timeit(lambda: [powmod(x-1, x)==1 for x in r])
            if time > time_min or power >= power_min:
                print("  Fermat test    {:20} over numbers 1-10^{} took {:.2f}s".format(powmod.__name__, power, time))
            if time > timelimit:
                break
    print("Timing fibonacci test methods")
    for fibmod in fibmods:
        for power in range(1,maxpower):
            r = range(2, 10**power)
            result, time = timeit(lambda: [fibmod(x+1, x)==1 for x in r])
            if time > time_min or power >= power_min:
                print("  Fibonacci test {:20} over numbers 1-10^{} took {:.2f}s".format(fibmod.__name__, power, time))
            if time > timelimit:
                break
    print("Timing prime test methods")
    for primetest in prime_tests:
        for power in range(1,maxpower):
            r = range(2, 10**power)
            result, time = timeit(lambda: [primetest(x) for x in r])
            if time > time_min or power >= power_min:
                print("  Prime test     {:20} over numbers 1-10^{} took {:.2f}s".format(primetest.__name__, power, time))
            if time > timelimit:
                break
    for primesieve in batch_prime_calcs:
        for power in range(1,maxpower):
            r = range(2, 10**power)
            result, time = timeit(lambda: primesieve(r.start, r.stop))
            if time > time_min or power >= power_min:
                print("  Prime sieve    {:20} over numbers 1-10^{} took {:.2f}s".format(primesieve.__name__, power, time))
            if time > timelimit:
                break

def main(limit=1000):
    print("Searching for counterexamples between 1 and {}.".format(limit-1))
    block = limit
    num_blocks = 1
    for y in range(0, block*num_blocks, block):
        if y==0:
            start, stop = 1, block-1
        else:
            start, stop = y, y+block-1
        r=range(start, stop+1)

        print("Method 1 (test all 3 properties for every number)")
        t0 = time.time()
        fert = [powmods[-1](x-1, x)==1 for x in r]
        t1 = time.time()
        fibt = [fibmods[-1](x+1, x)==0 for x in r]
        t2 = time.time()
        primet = batch_prime_calcs[-1](start, stop)
        t3 = time.time()
         
        fermat_time, fib_time, prime_time, total_time = t1-t0, t2-t1, t3-t2, t3-t0
        print("  Fermat: {:.2f}s ({:4.1f}% time, {:4.1f}% of numbers)".format(fermat_time, fermat_time/total_time*100, count_true(fert)/len(fert)*100))
        print("  Fib:    {:.2f}s ({:4.1f}% time, {:4.1f}% of numbers)".format(fib_time, fib_time/total_time*100, count_true(fibt)/len(fibt)*100))
        print("  Prime:  {:.2f}s ({:4.1f}% time, {:4.1f}% of numbers)".format(prime_time, prime_time/total_time*100, count_true(primet)/len(primet)*100))
        print("  Total:  {:.2f}s".format(total_time))
        for x in r:
            if fert[x-start] and fibt[x-start] and not primet[x-start]:
                print("  {} is a counterexample".format(x))
                exit(0)
        print("  No counterexamples found.".format(start, stop))
        print()

        print("Method 2 (skip fib test based on fermat test outcome, use sieve)")
        t0 = time.time()
        fert = [powmods[-1](x-1, x)==1 for x in r]
        t1 = time.time()
        fibt = [fert[x-r.start] and fibmods[-1](x+1, x)==0 for x in r]
        t2 = time.time()
        primet = batch_prime_calcs[-1](start, stop)
        t3 = time.time()
        counterexamples = set(fibt)-set(primet)
        t4 = time.time()
        fermat_time, fib_time, prime_time, set_time, total_time = t1-t0, t2-t1, t3-t2, t4-t3, t4-t0
        print("  Fermat: {:.2f}s ({:4.1f}% time, {:4.1f}% of numbers)".format(fermat_time, fermat_time/total_time*100, count_true(fert)/len(fert)*100))
        print("  Fib:    {:.2f}s ({:4.1f}% time, {:4.1f}% of numbers)".format(fib_time, fib_time/total_time*100, count_true(fibt)/len(fibt)*100))
        print("  Prime:  {:.2f}s ({:4.1f}% time, {:4.1f}% of numbers)".format(prime_time, prime_time/total_time*100, count_true(primet)/len(primet)*100))
        print("  Setops: {:.2f}s ({:4.1f}% time)".format(set_time, set_time/total_time*100))
        print("  Total:  {:.2f}s".format(total_time))
        for x in counterexamples:
            print("  Counterexample found: {}".format(x))
            exit(0)
        print("  No counterexamples found.")

if __name__ == "__main__":
    test()
    print()

    timing()
    print()

    main(1_000_000)
