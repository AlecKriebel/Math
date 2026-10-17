# Proof 07  Primitive circuit tests between four and six

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md); [Arithmetic progression triples and a failed multiradius extension](05_arithmetic_progressions.md); [A fixed counterexample on zero two seven](19_uniform_027.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

Use the credited Gressman–Guo–Pierce–Roos–Yung dominant-coefficient expansion, journal Proposition 4.1, as specialized in the earlier circuit and block results. With q=p/2 in (2,3), put B(k)=binom(q,k). For a primitive affine circuit lambda of mass K, the necessary tests are B(K) B(K-|lambda_i|)>0 at all entries.

Here B(k)>0 exactly when k<=3 or k is odd, and B(k)<0 exactly when k is even and k>=4.

The tests hold at all entries if and only if one of the following occurs:

1. K=2 or K=3.
2. K>=5 is odd, and the two sign-side partitions of K are (K) and (K-2,2), in either order.
3. K>=5 is odd, and both sign-side partitions are (K-2,2).

In cases 2–3 the coefficient vectors, up to permutation and global sign, are respectively

    (K, -(K-2), -2),
    (K-2, 2, -(K-2), -2).

## Proof

K>=2 for a circuit of distinct frequencies. For K<=3 every complementary index lies between 0 and 3, so all tests hold.

If K>=4 is even, B(K)<0. Any odd entry a gives even-minus-odd complementary index, whose binomial is positive, violating the test. Since primitiveness supplies an odd entry, even K>=4 is impossible.

Suppose K>=5 is odd. Then B(K)>0. Every odd entry a must have K-a an even index at most 2; hence a is K or K-2. Every sign side has odd total K and therefore contains an odd entry. It can have only one such entry because 2(K-2)>K for K>=5. If that entry is K, its side is a singleton. If it is K-2, the remaining even entries total 2 and therefore consist of exactly one entry 2. The possible remainder 1+1 would itself contain forbidden odd entries. Two singleton sides would have support two and are impossible for a distinct-frequency circuit. This yields cases 2–3.

Conversely, all complementary indices for the displayed vectors belong to {0,2,K-2}; these have positive binomials. The mass-2 and mass-3 cases were already checked. Thus the test classification is exact.

## Three-point specialization

For a normalized collinear triple {0,a,b}, 0<a<b, gcd(a,b)=1, its primitive relation is (b-a,-b,a), of mass b. The three leading tests hold if and only if, up to reflection,

- {0,1,2};
- {0,1,3};
- {0,2,b} with odd b>=5.

The first family is positive for all p>=2 by the earlier circuit and block results. These primitive tests alone do not classify the other families. The additional [Proof 30](30_all_odd_triples.md) excludes every odd K>=7 at each prescribed exponent. In particular {0,2,7}, p=5 passes these tests but fails the majorant property by the accepted exact-rational fixed triple certificate. The status of {0,2,5} throughout (4,6) remains unresolved in this note.

## Immediate geometric consequence

Every collinear subset passing the triple tests has at most four points. Normalize its integer parameters by their common gcd so that both parities occur. If two parameters coincide modulo 4, choose a third of opposite parity. The primitive triple's normalized distance between the coinciding parameters is an even multiple of 4, whose binomial is negative, a contradiction. Thus reduction modulo 4 is injective. This gives a necessary bound for every line in an MP_p configuration when 4<p<6.
