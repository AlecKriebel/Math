# Turn 1: exact exhaustive certificate and order stratification

2026-10-02. First substantive author turn. Original universal conjecture remains unresolved. Source and prior-attempt gate passed before this turn. This is a scoped partial result, not a full solution or novelty claim.

## Target and prior credit
For every prime q>3 such that p=16q^4+1 is prime, prove that 3 generates F_p^*, or exhibit a counterexample. The primary Open Problem Garden page is https://www.openproblemgarden.org/op/primes_p_such_that_3_is_a_primitive_root_modulo_p . Its August24,2012 anonymous comment already reduces the question to excluding a qth-power residue. That reduction is credited, not claimed as a new result.

## 1. Exact order possibilities
Because q>3 is prime, q is odd and q^4=1 mod3. Consequently p=5 mod12. Quadratic reciprocity gives (3/p)=-1. If N=p-1=16q^4 and o=ord_p(3), Euler's criterion gives 3^(N/2)=-1, so the full 2-primary part16 divides o. As o divides N, o=16q^j for some j in{0,1,2,3,4}.

The j=0 case is impossible. An element of exact order16 has eighth power -1, so p divides3^8+1=6562. But q>=5 implies p>=10001, contradiction. Thus

    ord_p(3) is one of 16q, 16q^2, 16q^3, 16q^4.

The original conjecture is equivalent to excluding j=1,2,3, or equivalently

    3^(16q^3) != 1 mod p.

For a cyclotomic restatement, p does not divide16q, and o=16q^j exactly when p divides Phi_(16q^j)(3). For j>=1,

    Phi_(16q^j)(x)=(x^(8q^j)+1)/(x^(8q^(j-1))+1).

This identity is a polynomial quotient; it does not assume the displayed denominator is invertible modulo p. In the exact-order case it is invertible because the preceding eighth-power expression is not zero. No cyclotomic argument excluding the three remaining strata has been established.

## 2. An elementary simultaneous primality and primitive-root certificate

**Lemma.** Let n>1 be an integer with known complete factorization N=n-1. Suppose b^N=1 mod n and gcd(b^(N/r)-1,n)=1 for every prime r dividing N. Then n is prime and b is a primitive root modulo n.

**Proof.** Let l be a prime divisor of n. The first congruence implies l does not divide b and its multiplicative order t modulo l divides N. For each prime r dividing N, the gcd condition ensures t does not divide N/r. Therefore v_r(t)=v_r(N) for every r, so t=N. Since t divides l-1, l>=N+1=n. Thus n=l is prime; the same order equality proves b primitive. QED.

For n=16q^4+1 with prime q, the only prime divisors of N are2 andq. Therefore the three exact tests at base3

    3^N=1 mod n,
    gcd(3^(N/2)-1,n)=1,
    gcd(3^(N/q)-1,n)=1

simultaneously prove primality and the desired primitive-root assertion. A failure of the first congruence proves n composite by Fermat's theorem. A proper nontrivial gcd would also provide a compositeness certificate. A case passing Fermat but with no successful Lucas certificate or proper gcd must remain unresolved, never silently discarded.

## 3. Exact finite theorem

For every prime q with3<q<=1,000,000, either p=16q^4+1 is composite or3 is a primitive root modulo p. Exactly7,669 of these p are prime.

The dependency-free script certify_turn1.py exhaustively constructs all78,496 relevant prime q by an Eratosthenes sieve. For each it performs the tests above with exact integer modular exponentiation. The outcome is:

-70,827 Fermat compositeness certificates
-7,669 simultaneous Lucas primality-and-primitive-root certificates
-0 unresolved cases

The first prime case is q=17, p=1,336,337, with3^((p-1)/2)=p-1 and3^((p-1)/q)=1,267,487. The last prime case in range is q=999,863, p=15,991,233,801,659,439,044,405,777. Exact output is turn1_exact_results.json; all per-q certificates are turn1_certificates.json. Canonically encoded certificate rows have SHA256 f3d31714d79c7d11d55522e037e0afb53b216d454bbdc07cb57945a5cf80393e.

Reproduce using only Python's standard library:

    python certify_turn1.py --bound 1000000 --output replay.json

The initial exploratory scan used SymPy primality screening, but no claim here depends on that screening. The complete final loop has no probable-prime predicate and cannot omit a genuine prime passing Fermat. The certificates and elementary lemma make the finite conclusion exact, not probabilistic.

## Remaining gap
The universal obstruction is still the possible occurrence of a prime q>1,000,000 with p=16q^4+1 prime and ord_p(3)=16q^j for j in{1,2,3}. A finite scan, quadratic reciprocity, the integer factorization of p-1, and general Artin heuristics do not exclude these strata. No complete proof, counterexample or claimed resolution follows. Four substantive author turns remain unless the target is settled earlier.

Subjective completion estimate for the universal proof goal:10%; an uncalibrated planning estimate, not a correctness probability or statistical extrapolation from the finite scan. Any final publication requires separate review.
