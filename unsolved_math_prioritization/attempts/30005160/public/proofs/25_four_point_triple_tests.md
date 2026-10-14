# Proof 25  Four collinear points satisfying every primitive triple test

This chapter classifies the necessary triple tests. For the actual majorant property, [Proof 30](30_all_odd_triples.md) removes every Q_K with odd K>=5. Only Q_1 and Q_3 remain collinear four-point candidates; neither is classified here.

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Primitive circuit tests between four and six](07_tests_between_four_and_six.md); [A fixed counterexample on zero two seven](19_uniform_027.md); [Fixed counterexamples on zero two nine and zero two eleven](20_uniform_029_0211.md); [Uniform counterexamples for sufficiently large odd frequencies](23_large_odd_counterexamples.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Statement

Fix 4<p<6 and put q=p/2. Four distinct collinear integer frequencies pass every primitive three-point leading test if and only if, after parametrizing their integer line, translating the parameters, dividing by the gcd of all parameter differences, and possibly reflecting, their parameters are

    Q_K = {0,2,K,K+2},             K a positive odd integer.

For K=1 this is the four-term arithmetic progression {0,1,2,3}. For K=3 it is {0,2,3,5}.

In particular, an MP_p configuration of four collinear frequencies must have one of these forms. This implication does not assert that the displayed forms have MP_p.

## Analytic input and invariances

Write B(j)=binom(q,j). The circuit argument in [Proof 07](07_tests_between_four_and_six.md), based on the Gressman–Guo–Pierce–Roos–Yung dominant-coefficient expansion, gives the following equivalent three-point tests. If a triple of distinct integer parameters has pairwise distances d_1,d_2,d_3 and g=gcd(d_1,d_2,d_3), it passes the tests precisely when

    B(d_1/g)>0, B(d_2/g)>0, B(d_3/g)>0.

For q in (2,3), B(j)>0 exactly when j<=3 or j is odd. Consequently a positive even normalized distance must equal 2.

Primitive affine relations are unchanged by an injective affine transformation of the parameters, including division by their global common divisor. A rational affine line containing two integer points has a primitive integer direction vector v: its integer points are n_0+t v with t integral. The resulting one-dimensional Fourier variable t preserves every finite polynomial norm, because the nonzero integer character x -> v dot x mod 1 sends normalized Haar measure on the ambient torus to normalized Haar measure on the circle. Replacing every t by c+g t, where g is a nonzero integer, likewise preserves the norms. Thus the reductions preserve both the primitive tests and the actual majorant property.

The analytic input is credited to P. T. Gressman, S. Guo, L. B. Pierce, J. Roos and P.-L. Yung, *On the strict majorant property in arbitrary dimensions*, Q. J. Math. 74 (2023), 139–161, Proposition 4.1; https://doi.org/10.1093/qmath/haac021 and https://arxiv.org/abs/2106.12538v2. The present arithmetic deduction uses the specialized test in [Proof 07](07_tests_between_four_and_six.md).

## Necessity

Let T be the four distinct integer parameters, normalized so that the gcd of all their differences is 1. They include both parities: otherwise every difference would be even.

First, their residues modulo 4 are distinct. Indeed, if u!=v had the same residue, choose w of opposite parity. The triple gcd

    g = gcd(|u-v|, |u-w|)

is odd. Thus |u-v|/g is a positive multiple of 4, contradicting the necessary condition that every normalized even distance is 2. Four distinct residues give exactly two even parameters e_1,e_2 and two odd parameters o_1,o_2.

For i=1,2 put

    g_i = gcd(|e_2-e_1|, |o_i-e_1|).

The second argument is odd, so g_i is odd. The normalized distance |e_2-e_1|/g_i is positive and even. Passing the triple test forces

    |e_2-e_1|/g_i = 2,
    g_i = |e_2-e_1|/2 =: h.

Therefore h divides e_2-e_1 and each o_i-e_1. These three differences generate all pairwise differences of T. Their gcd is 1, so h=1 and |e_2-e_1|=2. Interchanging the roles of the parities gives |o_2-o_1|=2.

Translate the smaller even parameter to 0. The even pair becomes {0,2}; the odd pair becomes {K,K+2} for an odd integer K. If K>0, we have the claimed form. If K<0, the affine transformation t -> t-K exchanges the roles of the two parity pairs and gives {0,2,-K,2-K}=Q_{-K}. Thus the parameter may always be chosen positive and odd. This last step is another translation, not a fractional normalization. Reflection t -> K+2-t also preserves each Q_K as a set.

## Sufficiency for every primitive triple test

Every Q_K is globally primitive, since K is odd and gcd(2,K)=1.

If K=1, its triples have normalized forms {0,1,2} or {0,1,3}, up to reflection. All their normalized distances are among 1,2,3 and have positive binomials.

If K>=3, the four triples are, up to translation and reflection,

    {0,2,K}   (twice),
    {0,2,K+2} (twice).

Each of these triples is primitive since its odd maximal parameter is coprime to 2. Its pairwise distances are 2 and two positive odd integers. Every relevant binomial is positive. Therefore all four triples pass the necessary leading tests.

This proves the exact claimed classification of four-point sets for those tests.

## Actual-MP exclusions already implied by accepted triple witnesses

The fixed triple counterexamples in [Proof 19](19_uniform_027.md) and [Proof 20](20_uniform_029_0211.md) show that the triples {0,2,L} fail MP_p throughout 4<p<6 for L=7,9,11. Since MP_p is hereditary under taking subsets and invariant under affine normalization, Q_K fails throughout this interval whenever K or K+2 belongs to {7,9,11}. Equivalently,

    Q_5, Q_7, Q_9, Q_11 all fail MP_p for every 4<p<6.

For example, Q_5={0,2,5,7} contains the uniform negative triple {0,2,7}; the unused coefficient is zero. These are full majorant-property exclusions, not only leading-test failures.

The all-odd theorem in [Proof 30](30_all_odd_triples.md) strengthens these exclusions: every odd Q_K with K>=5 contains {0,2,K+2} with K+2>=7 and therefore fails at every prescribed 4<p<6. Only Q_1 and Q_3 remain candidates. Their survival is a necessary-test statement, not a positivity theorem.

## Exhaustive real-sign reduction for subsequent work

For prescribed nonnegative bounds A,B,C,D at frequencies (0,2,K,K+2), it suffices to compare the positive vertex with the following three other vertices:

    (A, B, C,-D),
    (A,-B, C, D),
    (A,-B, C,-D).

A common sign and the Haar-preserving change z -> -z independently set the signs at frequencies 0 and K to plus. The remaining signs at 2 and K+2 are free, giving exactly the four vertices including the all-positive vertex. This remains valid when some bounds vanish, by assigning arbitrary signs to their zero entries. Because p>1, convexity of the Lp norm then extends domination of all sign vertices to the entire real coefficient box. This is only a reduction; the three required comparisons are not proved here.
