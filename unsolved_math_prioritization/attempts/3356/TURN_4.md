# Turn 4: polynomial-sieve counterexample search with exact certificates

2026-10-02. Fourth substantive author turn. The goal of this turn was a direct counterexample search beyond the first finite range, using the defining quartic to eliminate composites before expensive order tests. No counterexample was found. This is a finite theorem, not a universal resolution.

## 1. A complete polynomial compositeness sieve

If an odd prime ell divides16q^4+1, then ell does not divide2q and(2q)^4=-1 modulo ell. Therefore2q has exact order8 modulo ell. Consequently ell=1 mod8. Conversely, for each prime ell=1 mod8, the equation16a^4+1=0 modulo ell has exactly four roots: the cyclic group F_ell^* has four elements of order8, and multiplication by2 is invertible.

The scanner precomputes those four roots for every prime ell<=1000 with ell=1 mod8. Each prime q in a root residue class gives an explicit proper factor ell of p=16q^4+1, since q>=5 and p>=10001>ell. Every such rejection is checked by exact division; no heuristic wheel rejection is used.

A segmented Eratosthenes sieve identifies all prime q in range. In a segment[lo,hi), multiples of each prime ell<=sqrt(bound) are removed beginning at max(ell^2,ceil(lo/ell)*ell). Thus no prime is removed and every composite is removed. This is independent of the polynomial compositeness sieve.

For each surviving prime q whose p has no small polynomial-sieve factor, the scanner applies the exact base3 Fermat/Lucas certificate from TURN_1.md. A Fermat failure certifies compositeness. Success of both gcd tests certifies p prime and3 primitive, using the complete factorization p-1=16q^4. Any ambiguous case is recorded and causes the run to fail rather than being discarded.

## 2. Exact range theorem

For every prime q with3<q<=100,000,000, if p=16q^4+1 is prime then3 is a primitive root modulo p. Exactly418,013 of these p are prime.

The exhaustive exact run found5,761,453 prime q in range, partitioned into:

-3,346,393 p with a displayed proper small factor
-1,997,047 p with a failing base3 Fermat congruence
-418,013 p with complete Lucas primality-and-primitivity certificates
-0 unresolved cases

These counts sum to5,761,453. The last prime q giving a prime p in range is99,999,587, with

    p=1599973568163745789152484700540177.

For this case3^((p-1)/2)=p-1 and

    3^((p-1)/q)=1352778731308530744936952715014092,

with the requisite gcd equal1. These are exact integer values, not floating-point approximations or probable-prime evidence.

The canonical newline-delimited certificate stream has SHA256

    5805127c93aa572ae3f1e129aad3930685103d3d1cecf7c330061b85dace0b00.

The full stream is generated and hashed during execution rather than retained. The compact results file records the range, segmentation, sieve primes, exact totals and first/last examples. Reproduce it with:

    python scan_turn4.py --bound 100000000 --segment 1000000 --output replay4.json

Elapsed time is diagnostic and need not match on replay; all mathematical fields and the stream hash should. The script uses only Python standard-library exact arithmetic and has no external primality predicate. The first-turn full small-range row file is separate and need not be present.

## 3. Meaning and remaining gap

This raises the rigorous lower bound on any counterexample to q>100,000,000 and therefore p>16*(100,000,000)^4+1. It does not imply that a counterexample exists, that larger cases will obey the same law, or that a finite scan proves the universal conjecture. The original number-theoretic obstruction remains the q-primary residue condition from the first three turns. One substantive author turn remains. Completion estimate15% of the universal proof goal, not a probability or extrapolation from the418,013 positive cases.
