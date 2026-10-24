# Fresh adversarial audit of the p-group partial theorem

Opened 2026-10-24 19:44 UTC. This reviewer did not author the original proof.
The reviewed original sources were frozen before verification; see
`REVIEWED_MANIFEST.json` and `snapshot/`. A separate later coefficient delta is
frozen in `DELTA_MANIFEST.json` and `delta_snapshot/`.

## Verdict and exact claim

No counterexample or substantive gap was found in the following conditional
claim:

> If `n>2` and `Q_n mod (p,x_0^n,...,x_(n-1)^n)` is nonzero, every n-element
> subset of every finite abelian p-group has a cyclic enumeration with pairwise
> distinct neighboring sums.

Here `Q_n` is exactly the Vandermonde in the vertices times the differences of
sums on **disjoint** pairs of edges of an n-cycle. The coefficient premise is
sufficient, not asserted necessary. The claim allows every exponent and rank.

The baseline integer coefficient witnesses for `3<=n<=9` have been independently
reproduced by generic integer finite differences; their gcds are powers of two.
Thus they establish the displayed premise for every odd prime at those sizes.
This audit therefore supports the baseline finite-size p-group partial result.
The polynomial transfer does not require the residue prime to be at least n.

A separately audited later delta establishes finite witnesses at n=10 (gcd2)
and n=11 (gcd1); see below. Neither part proves the full Kourovka 21.130 claim,
the all-n coefficient statement, a mixed-prime reduction, or novelty.

## Analytic and embedding attacks

A separately assigned adversarial reviewer audited this part without relying
on the coefficient computations; its detailed derivation is
`analytic_attack/AUDIT.md`. The original Lubin--Tate PDF was independently
visually inspected at printed pp.382--384, rather than relying only on its
extracted text. Theorem 1 explicitly supplies the integral commutative formal
group and Theorem 2(b) identifies its pi^k torsion with O_K/pi^k O_K.

The key convergence estimate missing from the compressed wording, but following
from its hypotheses, is

    T^alpha E subset m^(sum_i floor(alpha_i/n)) E.

The exponent tends to infinity uniformly with total degree because

    |alpha| <= n sum_i floor(alpha_i/n) + n(n-1).

The quotient is finite free over the complete DVR, so all integral formal
series really do converge there. Modulo m the quotient is the **graded**
monomial quotient by `(x_i^n)`. Higher-degree terms can fold down over O only
with an m factor, and hence cannot cancel the unit degree-d coefficient modulo
m. This proves nonzero remainder without equating an integral remainder
coefficient to its original coefficient.

Evaluation on E at every grid tuple is continuous and agrees with monic
reduction on polynomials. Limits give equality with the analytic evaluation.
The evaluation map on E is injective over the fraction field by repeated
univariate interpolation, even though the distinct-point differences are
nonunits in O. The remainder map from the whole formal power-series ring is
**not** asserted injective: its kernel contains the monic grid equations.

For `G=direct_sum_j Z/p^(e_j)`, choose `k>=max e_j` and h at least the number
of cyclic factors. The maps `a -> p^(k-e_j)a` embed G in `(Z/p^k)^h`. The
unramified degree-h extension K/Q_p has additive quotient
`O_K/p^k O_K = (Z/p^k)^h`; its pi is p. Lubin--Tate torsion therefore contains
G as a subgroup. One can take the explicit allowed polynomial
`f(T)=pT+T^(p^h)`: the iterate f^k is monic, reduces to `T^(p^(hk)) mod p`,
and has all roots of positive valuation in a finite splitting field L/K.
The finite extension is complete, so every required series converges there.
No claim is made that a single fixed formal group over Q_p contains all ranks.

Cancellation on adjacent edges is legitimate because the evaluated formal
law is commutative and admits its convergent inverse on m. The case n=3 has
no disjoint-edge factors and still works. The exclusion n=2 is necessary.
Zero among the grid points and arbitrarily close torsion coordinates cause no
gap.

## Fresh baseline coefficient reproduction

`independent_coefficients.py` imports no reviewed software. It independently
forms disjointness from endpoint sets, reverses **every** factor relative to
the source's multiplication order, and packs exponents into hexadecimal
digits. It also implements a generic integer finite-difference calculation
with no optimized denominator-ratio identities. Standalone witness results are
saved in `finite_difference_all_witnesses.json`.

For an eligible exponent tuple t, total degree gives the exact identity

    [x^t]Q = sum_(0<=a_i<=t_i) Q(a) product_i (-1)^(t_i-a_i) binom(t_i,a_i)
                / product_i t_i!.

Since every `t_i<=n-1`, a nonzero Vandermonde value in this grid must be a
permutation of `0,...,n-1`. Restricting the sum to those permutations is exact.
Every numerator, denominator, and coefficient is an unbounded Python integer;
all divisions assert zero remainder. There is no modular factorial inversion.

| n | Independently reproduced witness values | Witness gcd |
|---:|---|---:|
|3|1|1|
|4|4|4|
|5|14, -24|2|
|6|182, -476, -520|2|
|7|-1454, 1570|2|
|8|-108696, -2270792|8|
|9|-137176976, -1261141910|2|

The fresh reverse-order full expansion reproduced contents/support through n=8
as `(1,6),(4,16),(2,100),(2,354),(2,1582),(8,5904)`, in `(content,support)`
order. It matches every coefficient of the frozen n=8 JSON. Full n=9 expansion
status is recorded in the final checkpoint below. For the odd-prime theorem,
the witnessed gcds already suffice; knowledge of the full content is not needed.

## Separate n=10,11 delta

This delta arrived after the original source freeze. It does not silently
modify what was reviewed in the original transfer file.

`independent_delta.py` directly applies the generic integer finite-difference
formula above. It does **not** use either author's compressed fixed-zero or
minimum-one weight formula. The Vandermonde at a permutation is independently
computed as its inversion sign times `product_(i=0)^(n-1) i!`. All arithmetic
is over the integers and all division remainders are recorded as zero in
`delta_results.json`.

The freshly reproduced n=10 witnesses are:

| Exponent vector | Coefficient |
|---|---:|
|(1,7,9,9,9,9,9,9,9,9)|-299280689184|
|(1,8,8,9,9,9,9,9,9,9)|-600114405460|
|(1,8,9,8,9,9,9,9,9,9)|-643745163834|

Their gcd is 2. The freshly reproduced n=11 witnesses are:

| Exponent vector | Coefficient |
|---|---:|
|(0,9,10,10,10,10,10,10,10,10,10)|11098103614834|
|(0,10,9,10,10,10,10,10,10,10,10)|189427196282499|

Their gcd is 1. Each coordinate is below n and the total degree is n(n-2).
Thus the n=10 witnesses certify every odd residue characteristic, and the
n=11 witnesses certify every residue characteristic, including two. Combined
with the audited analytic transfer, this proves the corresponding finite-size
assertions for p-groups. It does not assert full polynomial contents at n=10
or n=11.

A second, separately assigned reviewer derived both compressed author formulas
from general Lagrange interpolation, auditing signs, denominator ratios,
repeated deficits, and permutation parity. Its generic full-grid Fraction
calculation matched all 48 targets through n=6; see
`analytic_attack/coefficient_delta/FORMULA_AUDIT.md`. This formula audit and the
fresh numerical n=10,11 witness check are independent of one another.

## Boundary counterexamples and unsupported transfers

- The additive group of a finite field has exponent p. A field embedding alone
  cannot transfer the elementary-abelian argument to p^k groups for k>1. The
  Lubin--Tate step supplies a new, valid mechanism for those groups.
- A formal group on the maximal ideal in residue characteristic p has no torsion
  of order prime to p: multiplication by such an integer has an integral inverse
  formal series because its linear coefficient is a unit. For example C_3 x C_5
  cannot be embedded this way for **any** chosen residue prime. This is a barrier
  to that transfer, not a counterexample to the cyclic-ordering problem.
- The four-element subset consisting of all of `(Z/2)^2` cannot have four distinct
  neighbor sums: opposite edge sums coincide because all four vertices sum to
  zero. The n=4 content4 correctly prevents the coefficient premise at p=2.
- At a valuation-zero coordinate, an arbitrary integral series need not converge;
  `sum X^j` at X=1 is an explicit failure. The strict maximal-ideal hypothesis
  must remain in the analytic lemma.
- Nonzero factors over a ring with zero divisors would not ensure a nonzero
  product. The successful argument evaluates in the characteristic-zero field L
  and therefore does not make that unsupported ring transfer.

The exact remaining research gaps are the all-n coefficient nonvanishing
condition and a valid mechanism for arbitrary mixed-prime finite abelian
odd-order groups. No outside input is needed for the results certified here.
No external communication, Git mutation, push, or release was performed.

## Final checkpoint

Completed 2026-10-24T19:53:27.998450+00:00. Completion of the assigned adversarial audit: **100%**. No necessary checks remain. This is not a completion estimate for the unrestricted research problem.

The optional reverse-order n=9 full expansion completed naturally with exit code 0 after 398.7575 seconds. Its support is 23694 and its content is 2; every coefficient matches the frozen n=9 JSON. Thus the independently reproduced full contents for n=3 through9 are **1,4,2,2,2,8,2**, with supports **6,16,100,354,1582,5904,23694**. The witness-gcd theorem does not depend on these additional full-support checks.

The reviewed mathematical conclusion is **PASS for 3<=n<=11 and every odd prime p, in every finite abelian p-group**, plus **n=11 for p=2**. The two remaining unrestricted-target gaps are unchanged. The original and delta snapshot bytes were rechecked against their frozen manifests at close. All audit computations have exited; no live audit process remains.
