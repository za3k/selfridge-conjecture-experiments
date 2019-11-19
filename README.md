The Selfridge/Pomerance/Wagstaff Conjecture about primality testing conjectures that:
```
  IF  2^{p−1} ≡ 1 (mod p) 
  AND f_{p+1} ≡ 0 (mod p), where F_n is the nth fibonacci number
  THEN p is prime
```
This program both searches for counterexamples, and tests methods for correctness/speed.
There is also a C version, which is 5-10 times faster, and should handle numbers up to 2^64.

Here is an example output run on my computer:
```
Testing that all methods agree for numbers 1-999.
Self-test passed in: 1.69s
All methods should be correct.

Running timing test--testing how many numbers we can crunch by iteratively increasing range sizes
Timing fermat test methods
  Fermat test    two_pow_n_mod_x0     over numbers 1-10^4 took 0.09s
  Fermat test    two_pow_n_mod_x0     over numbers 1-10^5 took 12.42s
  Fermat test    two_pow_n_mod_x1     over numbers 1-10^4 took 3.11s
  Fermat test    two_pow_n_mod_x2a    over numbers 1-10^4 took 0.02s
  Fermat test    two_pow_n_mod_x2a    over numbers 1-10^5 took 0.31s
  Fermat test    two_pow_n_mod_x2b    over numbers 1-10^4 took 0.02s
  Fermat test    two_pow_n_mod_x2b    over numbers 1-10^5 took 0.32s
  Fermat test    two_pow_n_mod_x3     over numbers 1-10^4 took 0.01s
  Fermat test    two_pow_n_mod_x3     over numbers 1-10^5 took 0.13s
Timing fibonacci test methods
  Fibonacci test fib_n_mod_x0         over numbers 1-10^4 took 5.75s
  Fibonacci test fib_n_mod_x1         over numbers 1-10^4 took 3.44s
  Fibonacci test fib_n_mod_x2a        over numbers 1-10^3 took 0.56s
  Fibonacci test fib_n_mod_x2b        over numbers 1-10^4 took 0.22s
  Fibonacci test fib_n_mod_x4         over numbers 1-10^4 took 0.64s
  Fibonacci test fib_n_mod_x3         over numbers 1-10^4 took 0.05s
  Fibonacci test fib_n_mod_x3         over numbers 1-10^5 took 0.69s
Timing prime test methods
  Prime test     is_prime0            over numbers 1-10^4 took 0.29s
  Prime test     is_prime2            over numbers 1-10^4 took 0.01s
  Prime test     is_prime2            over numbers 1-10^5 took 0.15s
  Prime test     is_prime3            over numbers 1-10^4 took 0.01s
  Prime test     is_prime3            over numbers 1-10^5 took 0.08s
  Prime test     is_prime3            over numbers 1-10^6 took 2.01s
  Prime sieve    all_primes0          over numbers 1-10^4 took 0.30s
  Prime sieve    all_primes4          over numbers 1-10^4 took 0.00s
  Prime sieve    all_primes4          over numbers 1-10^5 took 0.01s
  Prime sieve    all_primes4          over numbers 1-10^6 took 0.12s

Searching for counterexamples between 1 and 999999.
Method 1 (test all 3 properties for every number)
  Fermat: 1.74s (15.6% time,  7.9% of numbers)
  Fib:    9.30s (83.3% time,  3.9% of numbers)
  Prime:  0.12s ( 1.1% time,  7.8% of numbers)
  Total:  11.17s
  No counterexamples found.

Method 2 (skip fib test based on fermat test outcome, use sieve)
  Fermat: 1.72s (64.8% time,  7.9% of numbers)
  Fib:    0.80s (30.2% time,  3.9% of numbers)
  Prime:  0.12s ( 4.4% time,  7.8% of numbers)
  Setops: 0.01s ( 0.5% time)
  Total:  2.65s
  No counterexamples found.
```
