# Independent adversarial arithmetic review of PR 280 / 30000156

Reviewed original head `091bdecef6f84154f5d5c205a4b07eeb6391b8f8`.
Original proof SHA256: `ba5fc8850a665da5130e3791fb49015c998ed0eee317576712ad3b66bc228c05`.

**Verdict: the original arithmetic theorem is correct. No arithmetic gap or
counterexample was found.** This verdict does not certify historical priority
or settle interpretations of the original source's quantifier over admissible
prime sets. It verifies the theorem on the specified fixed class p = 3 mod 4.

The first independent mechanism/objection checkpoint is timestamped in
FIRST_CHECKPOINT.json and RESEARCH_LOG.md. No previous review conclusion
documents were consulted. After that checkpoint I inspected the original
verifiers and two existing standard-library verification scripts; all replays
and added work are confined to this review directory. All 17 original files
match their supplied SHA256, Git blob and byte-count pins.

## Strongest arithmetic result verified

Write N=p-1, theta_p=phi(N)/N, and
P_p=#{u in F_p : ord_p(u^2+1)=N}. For every p=3 mod 4, L(u,v)=(u,(u^2+1)v)
is a permutation of all p^2 affine points. For each fixed x in [1/2,1),

    D_p(x) = 1 - (p-1)P_p/p^2                  when p>1/(1-x),
    |P_p/p-theta_p| <= theta_p(2^omega(N)-1)/sqrt(p),
    |D_p(x)-(1-theta_p)| <= 1/p+64p^(-1/4).

Consequently the claimed limsup 1, liminf <=23/24, and absence of a weak limit
hold unconditionally. The same cited unconditional lemma also gives the
optional stronger bound

    1/2 <= liminf D_p(x) <= 1-A <= 17/24,
    limsup D_p(x) = 1,

where A=product over primes ell of (1-1/(ell(ell-1))). The strengthening is
derived below; it is not needed to repair or validate the original proof.

## Full phase space and point weighting

For p=3 mod 4, u^2+1 is never zero. Hence multiplication by u^2+1 permutes
each vertical fiber, and the displayed rational inverse is defined at every
finite-field point. At v=0 the period is 1; at v nonzero it is exactly the
multiplicative order of u^2+1. Thus all p^2 points, including the zero section
and the fiber u=0, are correctly counted.

Every proper divisor of N is at most N/2, which is strictly less than p/2.
For x>=1/2 all such periods are included. The full order N is excluded exactly
when x<N/p, equivalent to p>1/(1-x). Each primitive parameter contributes N
points, not one cycle or one parameter, to the exclusion. This proves the
counting formula with the correct point weight.

The strict cutoff is essential. At p=3, D_p(1/2)=5/9 but D_p(3/4)=1, since
the primitive cycles already lie below 3p/4. At the moving threshold
x_p=(p-1)/p, D_p(x_p)=1 for every admissible p. These are successful negative
controls against dropping the eventual clause or claiming uniformity in all
x<1. Neither falsifies the stated fixed-x theorem. At x=1 the CDF is 1, as it
must be. Primes 2 and 1 mod 4 fail the full-plane permutation requirement;
the supplied and new checks explicitly expose their collapsed fibers.

## Character expansion and every exceptional case

For a=g^k in a cyclic group of order N, the primitive-element indicator is

    theta_p sum_(d|N) mu(d)/phi(d) sum_(ord chi=d) chi(a).

The inner sums are Ramanujan sums. Factoring over the distinct primes of N
gives zero when some prime divisor of N divides k, and otherwise gives one.
This proves the convention and coefficient, including k=0 and repeated prime
powers in N. No fixed-base primitive-root assertion enters.

Extend every character by zero at zero. Counting the square roots of t and
then putting t=-s gives, for every nontrivial chi,

    sum_u chi(u^2+1) = eta(-1) J(eta,chi).

If chi is not eta, all three characters eta, chi, eta*chi are nontrivial, so
the elementary Gauss product identity gives Jacobi magnitude sqrt(p).
If chi=eta, the inverse-character identity is
J(eta,eta)=-eta(-1); consequently the original sum is -1, of magnitude 1.
This exceptional term satisfies the claimed weaker sqrt(p) bound. The
trivial-character sum is p, because there are no zero values in this prime
class. The nonzero mu(d) terms with d>1 number 2^omega(N)-1, and their
phi(d) character multiplicities cancel the denominators. The quoted primitive
count error follows without an extra phi(N), tau(N), or factor of p.

Only six primes are below 16. Bounding their individual factors of 2 by 2 and
using 2<=ell^(1/4) for ell>=17 proves 2^omega(N)<=64N^(1/4). If
delta_p=P_p/p-theta_p, then

    D_p(x)-(1-theta_p) = theta_p/p-(1-1/p)delta_p.

This proves the stated explicit eventual error. It tends to zero along every
sequence in the class, including either specially constructed subsequence.

## Unconditional analytic input and residue-class extraction

The primary source is Menici--Pehlivan, *Average r-rank Artin conjecture*,
Acta Arith. 174 (2016), DOI 10.4064/aa8258-4-2016. I read equation (1), the
definition (8), and Lemma 2 with its full proof on printed pp.262--263 from
the existing complete text and the live institutional PDF:
https://www.impan.pl/shop/en/publication/transaction/download/product/91625.
The definition and lemma at r=m=1 give the ordinary totient mean. Its proof
uses unconditional Siegel--Walfisz; the introductory GRH discussion concerns
other results about specified generators and is not a hypothesis of Lemma 2.

Independently, finite Mobius inversion yields

    sum_(p<=X) theta_p = sum_(d<=X-1) mu(d)/d * pi(X;1,d).

For K=(log X)^6, pi(X;1,d)<=X/d implies an absolute tail at most
X sum_(d>K)1/d^2=O(X/K). For d<=K, the quoted SW estimate is uniform and
allows the modulus exponent 6 and error exponent 4 simultaneously. Its total
weighted error is O(X log K/(log X)^4), because sum_(d<=K)1/d=O(log K).
Dividing this error and the tail by X/log X makes both vanish. There is no
need for uniformity up to a power of X, Bombieri--Vinogradov, GRH or Artin.

The elementary prime-power bound phi(d)>=sqrt(d/2) proves absolute
convergence of sum 1/(d phi(d)), so its Mobius series has Euler product A.
This establishes the claimed prime mean after pi(X)~Li(X). All moduli in the
mean truncation grow only as a fixed logarithmic power. The use of Dirichlet
later is for one fixed modulus at a time, and makes no quantitative least-prime
claim.

The source's elementary A bound is valid: remove the factor 1/2 at ell=2;
the remaining sum 1/(ell(ell-1)) is at most the telescoping sum over n>=3
with n=4 omitted, namely 5/12. Product >=1-sum gives A>=7/24.
For all odd p, theta_p<=1/2. PNT in the two reduced classes mod 4 gives each
prime density 1/2. If eventually theta_p<1/24 in the 3 mod 4 class, the all-prime
mean would have limsup at most 1/4+1/48=13/48, below 7/24=14/48. Thus the
needed class contains infinitely many theta_p>=1/24. This is a valid extraction
from the global mean, rather than an unjustified assumption about a subclass.

## Both infinite subsequences and all fixed thresholds

Let Q_j be the product of the first j odd primes. The explicit residue
r_j=2Q_j+1 is 3 mod 4, 1 mod Q_j, and coprime to 4Q_j. For each j, Dirichlet
provides arbitrarily large primes in this fixed progression. Choose p_j
increasing, so every prime factor of 2Q_j divides p_j-1 and

    theta_(p_j) <= (1/2) product_(ell|Q_j)(1-1/ell) -> 0.

Euler's vanishing prime product supplies the last limit. The increasing choice
and the order of quantifiers are valid; no uniform Dirichlet error is used.
The other subsequence comes from the infinite set theta_p>=1/24 just proved.
Both subsequences are selected independently of x. For each fixed x<1 the
finite cutoff is eventually passed, proving the original two bounds at every
x in [1/2,1). Probability bounds give the exact limsup 1.

## Independent continuous-test proof of no weak limit

Define the bounded continuous function on the real line

    f(t)=max(0,min(1,2t-1)).

All proper-order normalized periods are below 1/2, while primitive ones equal
1-1/p. Thus for the actual point-weighted probability measure mu_p,

    integral f dmu_p = (1-2/p)(p-1)P_p/p^2 = theta_p+o(1).

Along p_j this tends to zero. Along the other subsequence its liminf is at
least 1/24. Weak convergence would force convergence of this single bounded
continuous integral, a contradiction. This independently validates the
original CDF/countably-many-discontinuities argument, which is also correct.

## Optional checked strengthening from the same primary lemma

This is a separate deduction, not a premise needed by the original proof.
Let S_1(X)=sum_(p<=X)theta_p and let

    S_2(X)=sum_(p<=X, p odd) phi((p-1)/2)/(p-1),
    T_3(X)=sum_(p<=X, p=3 mod 4)theta_p.

For p=3 mod 4 the summand of S_2 is theta_p; for p=1 mod 4 it is theta_p/2.
Since the p=2 contribution to S_1 is 1, for X>=2 the exact identity is

    T_3(X)=2S_2(X)-S_1(X)+1.

Lemma 2 at r=1,m=2 gives S_2(X)~C_(1,2)Li(X). Pairing n=k and n=2k for odd k
in the absolutely convergent coefficient sum gives

    C_(1,2) = (3/8) sum_(k odd) mu(k)/(k phi(k)) = 3A/4.

Therefore T_3(X)~(A/2)Li(X), and division by pi(X;3,4)~Li(X)/2 gives class
mean A. In particular limsup_(p=3 mod 4)theta_p>=A; this does not assert that
theta_p>=A itself must hold infinitely often. The pointwise error proved above
then yields liminf D_p(x)<=1-A. The other inequality liminf D_p(x)>=1/2
follows from theta_p<=1/2. The coefficient identity and finite exact residue
decomposition were checked by distinct_checks.py, separately from the supplied
orbit/cyclotomic controls.

## Reproducibility, limitations and exact remaining gap

After full inspection, byte-for-byte copies of the two existing standard-library
scripts were run under Python 3.14 with -E -B. The full finite replay passed
8,347,742 assertions and the analytic replay passed 230,780. New distinct controls
passed 2,111 assertions, including finite exact prime/Mobius rearrangements,
absolute tails, m=2 coefficient pairing, strict/equal thresholds, inadmissible
primes and the continuous-test moment. Outputs, stderr, commands, timestamps and
SHA256 hashes are preserved. Finite computations supplement the written proof;
they do not prove any infinite-prime or analytic theorem.

Both original snapshot verifiers import SymPy. Their literal replay in the
available Python fails at that import, as recorded in ORIGINAL_RUNTIME_RECEIPT.json.
No runtime was installed and no original file was modified. The standard-library
replays provide reproducible finite controls without that dependency.

No arithmetic gap remains in the original theorem. Its unconditional inputs
remain credited classical theorems. The exact original-source applicability,
historical priority, and publication decisions are separate questions and are
not promoted by this arithmetic verdict. No communications with other
individuals or unrelated agents occurred. Git refs, index and checkout location, candidate files, ledgers,
PRs, and Zenodo were not modified by this review.
