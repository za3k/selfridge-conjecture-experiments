//Selfridge/Pomerance/Wagstaff Conjecture about primality testing:
//  IF  2^{p−1} ≡ 1 (mod p) 
//  AND f_{p+1} ≡ 0 (mod p),
//  THEN p is prime

//This program searches for counterexamples

// In general most of the left-to-right methods could be converted to be right-to-left methods,
// but the speeds don't really seem to change appreciably
#include <stdio.h>
#define SINT __uint64_t
#define SINT_L 64
#define DINT __uint128_t

SINT pow2_n_mod_x(SINT n, SINT x){
    if(x==1) return 0;
    SINT s = 1;
    SINT b = 2;
    for (;n;n>>=1){
        if(n % 2) s = ((DINT)s * b) % x;
        b = ((DINT)b * b) % x;
    }
    return s;
}

SINT fib_n_mod_x(SINT n, SINT x){
    if(x==1) return 0;
    SINT fn = 1; // F_{n}
    SINT fn_minus = 0; // F_{n-1}
    SINT bit = (SINT)1<<(SINT_L-1);
    n = n-1;
    while (!(bit & n)) bit >>= 1;
    for (;bit;bit>>=1){
        SINT a = ((DINT)fn*fn) % x;;
        SINT b = ((DINT)fn_minus*fn_minus) % x;
        SINT c = ((DINT)fn*fn_minus) % x;
        SINT c2 = ((DINT)2*c) % x;
        fn_minus = ((DINT)a+b) % x;
        fn = ((DINT)a+c2) % x;
        if (n & bit){
            SINT t = ((DINT)fn+fn_minus)%x;
            fn_minus = fn;
            fn = t;
        }
    }
    return fn;
}

// Classic sieve of eratosthenes
// Note: poss improvement, can cache, also to generate primes from X to Y, we need all primes up to X**0.5 only
// Note: poss improvement, can use wheel method again
void sieve(unsigned char is_prime[], SINT start, SINT end){
    is_prime[0] = 0;
    is_prime[1] = 0;
    for (SINT x=2; x<=end; x++) {
        is_prime[x] = 1;
    }
    for (SINT x=2; x*x<=end; x++) {
        if (is_prime[x]){
            for (SINT ci=x*2; ci<=end; ci+=x) {
                is_prime[ci] = 0;
            }
        }
    }
}

#define UPPER 10000000000
unsigned char is_prime[UPPER+1];
int main(){
    printf("Searching for counterexamples between 1 and %lu...\n", UPPER-1);
    sieve(is_prime, 2, UPPER);
    for (SINT x=2; x<=UPPER; x++) {
        if (pow2_n_mod_x(x-1, x)==1 && fib_n_mod_x(x+1, x)==0 && !is_prime[x]){
            printf("%lu %lu %lu %d\n", x, pow2_n_mod_x(x-1, x), fib_n_mod_x(x+1, x), is_prime[x]);
            printf("Counterexample found: %lu\n", x);
            return 0;
        }
    }
    printf("No counterexample found.\n");
}
