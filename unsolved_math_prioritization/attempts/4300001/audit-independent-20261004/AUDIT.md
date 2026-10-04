# Independent adversarial audit: Ward's order-of-mixing example

Problem 4300001 / AMR-042-0001; rank 604. Audit date: 2026-10-04 UTC.

## Decision and binding

**Original frozen packet: REVISE for two literal statement-precision errors.**
**Exactly corrected packet: PASS for the stated partial mathematical results.**
**Full problem: UNSOLVED, 5/5 approaches, unchanged.**

No counterexample, invalid source application, indexing error, or missing argument
was found in the substantive proofs. The required corrections concern the
meaning of multiplicative independence and saturation with finite-field
constants. They do not weaken the numerical conclusions.

This is an independent AI mathematical audit, not human peer review or formal
proof-assistant certification. It does not establish historical novelty or
present-day global openness. It does not authorize publishing or remote changes.

The reviewed original is bound by:

- SHA256SUMS: b638d8ddc60e91e7f6feeae313d58f2aa81e54216ab5d3999581a9b054859924
- PROOF.md: a184e8f7d7682cb645e1fd32a05100ff71e8deb57ea5454da42b74a74e85f0b4

The corrected PASS is bound only to the separate `corrected-public` packet:

- SHA256SUMS: 1f5d64200baaa0b571854bafde52157a559a4ff46c84cc2756cfca39e7d94a7a
- PROOF.md: 68847700cb0c2c4efe7d51da310cdde158b06b2cc0daaf8997501130e49577a9

The exact patch and file-by-file hashes are in `precision-corrections.patch`
and `correction-binding.json`. The original public directory was not modified.

## 1. Exact target and primary-source hypotheses

Ward's December 2006 Problem A, printed page 1, has the same seven-term
polynomial, the same Z²-action, and the convention that M is the largest
mixing order. The prime is unspecified subject to irreducibility. The uniform
partial result and the special case p=2 must not be labeled a full solution.
Source: [Ward's original note](https://www.imath.kiev.ua/~skolyada/kevin.pdf).

The relevant statements were checked in the actual primary PDFs, including
rendered mathematical notation, rather than inferred from abstracts:

- [Einsiedler–Ward preprint](https://arxiv.org/pdf/math/0204174), printed page 3,
  Theorem 3.1: irreducible f and an R-sided Newton polygon give the stated
  mixing-order inequalities. Here f is irreducible, R=4, and support size=7.
- [Derksen–Masser](https://sites.lsa.umich.edu/hderksen/wp-content/uploads/sites/614/2018/05/A.I.a.55.pdf),
  printed pages 6, 9, and 10–12: the radical is inside K; pre-broad means
  nonzero coordinates with no constant pairwise ratio; Lemma 5 applies to a
  basic prime-ideal action that is n-mixing but not (n+1)-mixing, n≥2.

For this application the integer Laurent ideal is P=(p,f); irreducibility makes
it prime, and its quotient has fraction field K and constant field F_p.
Einsiedler–Ward gives 3≤M≤6 before Lemma 5 is invoked, so n=M satisfies n≥2
and the required finite first failure exists. Projective coordinates can be
represented in the radical; their sum vanishes. There is no unsupported
extension from arbitrary action coefficients to F_p coefficients: the proved
constant-field and saturation statements supply precisely that conversion.

The effective general algorithm mentioned in the report was not executed.
It supplies neither a numerical answer for this f nor a finite-search cutoff
in this submission. Neither is needed for the audited partial proof.

## 2. Absolute irreducibility: every prime, including 2, 3, and 5

The coprimality proof for A=1+x⁴ and B=x(x²+x+1) is valid over an algebraic
closure in every characteristic. In particular, the repeated root of
x²+x+1 in characteristic 3 does not create a common root with A.
Independent symbolic calculation also gives resultant(A,B)=1.

For odd p the discriminant identity and its exceptional reductions are correct.
The only primes that can invalidate the displayed simple-q-root argument are
2, 3, and 5: independently, resultant(q,r)=25, resultant(q,t)=16, and
disc(q)=-3. Thus there is no missed exceptional odd prime caused by repeated
roots of r or t away from q. At p=3 and p=5 the separately displayed factor
x²+1 is squarefree and disjoint from the other factors. A simple discriminant
zero over the algebraic closure rules out a rational square.

For p=2, w=A(y+1)/B gives w²+w=A/B. The denominator has a simple zero and the
numerator a nonzero value at x=0. A pole of h²+h has even order because the
squared term strictly dominates h. This excludes a root in the rational
function field even after algebraically closing the constants. Primitivity
then yields absolute irreducibility of f itself.

Absolute irreducibility also justifies the asserted constant field. A proper
finite subfield extension of F_p inside K would split under algebraic closure
of constants, contradicting geometric integrality. Both coordinates are
transcendental. For y, one can see this directly: an algebraic constant y=c
would force every coefficient of f(x,c) to vanish, giving simultaneously
c=0 and 1+c²=0. The reciprocal formulas are exact identities and define
involutive automorphisms of K in every characteristic.

**Result: Proposition 2.1 and the subsequent field facts pass.**

## 3. Valuations, constants, and radical saturation

The boundary points used are allowed even though they lie outside the original
torus: they are points of a smooth curve model of the same function field.
At odd p, f_y(0,β)=2β and f_x(α,0)=4α³ are nonzero. Thus the associated
geometric discrete valuations have coordinate vectors (1,0) and (0,1).
Restricting such valuations to functions in K gives integer orders, so
h^N=c x^a y^b forces N|a and N|b even when N is divisible by p. Removing
the monomial leaves an element algebraic over F_p, hence a constant.

At p=2 the smooth points have coordinate orders (2,0) and (0,4).
At (0,1), y+1 is a parameter and x has order 2. At (1,0), x+1 is a
parameter and y has order 4. These orders control every odd prime divisor
of N. Separability of K/F_2(x) follows from f_y=B≠0, so the indicated
derivation exists. Its logarithmic ratio is correctly
R=(1+x²)/(x²+x+1), with R, 1, and 1+R all nonzero. It excludes a square
root of a monomial with nonzero exponent parity.

To spell out the prime-power step, if a prime ℓ divides N, apply the relevant
ℓ-root result to h^(N/ℓ). That expresses h^(N/ℓ) as a constant times a
monomial. Repeat with N/ℓ. This validates arbitrary composite N; no
prime-power or inseparability gap remains.

The exact conclusion is sqrt(G)=F_p*G for G=⟨x,y⟩, not sqrt(G)=G at odd p.
Equivalently F_p*G is radical-saturated. Constants lie in sqrt(G) since
c^(p−1)=1. Also the valuations establish x^a y^b constant only when a=b=0.
They establish independence of the two generators, not of an arbitrary
collection of distinct monomials.

**Result: the substantive saturation proof passes after the precise statement
corrections in Section 9.**

## 4. Minimal support versus mixing order

An r-term relation with distinct exponent pairs and coefficients in F_p*
Frobenius-dilates to p^e times those exponent pairs with the same coefficients.
Every pair separates, every corresponding coefficient-character is nontrivial,
and the product-character is trivial. Thus r-mixing fails and M≤r−1.
The passage from set mixing to bounded-character correlations is valid.

Conversely, Lemma 5 applied at n=M gives M+1 radical-group coordinates with
nonconstant ratios. Saturation turns them into F_p* multiples of monomials.
Their exponents are distinct, so the resulting formal Laurent polynomial is
nonzero. Its image in K is zero; the kernel is exactly (f). Consequently
w≤M+1. This proves M=w−1, with both inequality directions correct.

There is no confusion between a six-term failure and six-mixing:

- w=6 means M=5.
- w=7 means M=6: six-mixing holds and seven-mixing fails.

Laurent denominators cause no lost cases. Multiplication by a monomial
preserves support cardinality and Laurent divisibility. Since both minimum
coordinate exponents of f are zero, normalizing g=fh to minimum coordinate
exponents zero normalizes h as well. The quotient can therefore be taken
as an ordinary polynomial when needed; no bounded degree is implied.

**Result: Corollary 3.2 passes.**

## 5. Uniform exclusion of at most five terms

The extreme coefficients of a product multiply without cancellation to zero
in the one-variable Laurent coefficient domains. Every extreme x-column is
a nonzero multiple of 1+y² and every extreme y-row a nonzero multiple of
1+x⁴. Each therefore has at least two support points. Widths are positive.

For two x-levels, P(y)+x^m Q(y)=0 implies x^m∈F_p(y). The reciprocal
involution gives x^(2m)=1, impossible for transcendental x. This is still
impossible in characteristic 2: the integer 2m is an exponent, not a scalar
coefficient to reduce modulo 2. The y-level version is identical in logic.

With at most five support points and at least one interior x-point, exactly
one remains after the two pairs on extreme columns. Specialization at any
nonzero β with β²=-1 kills both columns and leaves one nonzero Laurent
monomial. But f(x,β)=βB(x) has the nonunit factor x²+x+1, so it cannot
divide that monomial. At p=3 a repeated nonzero root is enough for this
contradiction; at p=2 the single boundary root β=1 suffices.

**Result: w_p≥6 and 5≤M_p≤6 hold for every prime.**

## 6. Characteristic-two six-term exclusion

Every step of the support/parity proof survives the requested edge cases:

1. Normalize the minimum coordinate exponents to zero. If every exponent
   pair has the same parity, that parity is (0,0); hence g is a polynomial
   square. The prime divisor f descends to its square root. A positive
   integer width strictly decreases, so descent terminates.
2. At a boundary line, coefficients are 1 and evaluation at 1 forces an
   even number of terms. Four or more on one boundary plus two on the
   opposite boundary would leave a two-level support, already excluded.
   Thus there are exactly two points on each of four boundaries.
3. The four pairing edges are distinct. A point has at most one horizontal
   and at most one vertical incident edge, hence degree at most two.
   A horizontal difference is divisible by 4 because 1+x⁴=(x+1)⁴;
   a vertical difference is divisible by 2. The multiplicity of 1 in
   1+z^d is 2^v_2(d), including the large-even-d cases.
4. A forest on at most six vertices with four edges has at most two
   components, including isolated support points. Each component has
   one parity class. In a two-class relation H and J are nonzero in K:
   each has at most five terms and cannot be divisible by f. Division
   is therefore legitimate, and would make a non-even monomial a square.
5. A cycle alternates orientations, so with four edges it is a 4-cycle.
   Its corners are the actual bounding-box corners. Any remaining
   support points are isolated: the cycle already uses all four edges.
   The only untreated possibility is four square-parity corner terms
   and two singleton terms in distinct nonzero relative parity classes.
6. Differentiating H²+U+V=0 gives U(a+bR)+V(c+dR)=0 with both factors
   nonzero. The ratio U/V lies in F_2(x). The reciprocal y-involution
   then gives y^(2(b−d))=1, forcing equality of the integer exponents
   b=d, not merely equality of their parities.
7. If b is even, the two nonzero parity classes coincide, a contradiction.
   If b is odd, the ratio requires a pure x-monomial to equal either
   (x+1)²/x or its reciprocal. Their orders at x=1 are 2 and −2;
   a pure x-monomial has order zero there. This is an equality inside
   F_2(x), so no unexamined ramification of K can remove the contradiction.

The argument is not based on a finite exponent search. Its dependence on
coefficients in F_2 is real and is explicitly disclosed. No extension of this
parity argument to odd p is justified by the packet or this audit.

**Result: w_2=7 and M_2=6 pass.**

## 7. Odd-prime necessary conditions and unresolved scope

The six-term x-column normal form is valid. A zero interior count contradicts
the two-level lemma; an interior count of one gives the same specialization
contradiction regardless of whether a boundary column has three terms.
Thus both columns and the interior each contain two terms.

When r≠s and p≠3, evaluation at both primitive cube roots implies
3|(r−s). When p=3, the double factor (x−1)² requires the value and
first derivative at 1 to vanish; together they imply the same integer
congruence. When r=s, the specialized coefficient must be zero and the
x-congruence is automatic. The two distinct roots β and −β in odd
characteristic force even u−v and the displayed signed coefficient ratio.
The logic also handles negative Laurent differences.

**Result: Proposition 6.1 passes.** These constraints are necessary, not
sufficient. No odd-prime six-term witness or universal exclusion has been
established. The exact gap is unchanged: existence of a six-term nonzero
Laurent multiple over each odd F_p. Finite multiplier boxes cannot answer it.

## 8. Reproduction and independently implemented controls

All eight original manifest entries match. Running the submitted check.py
with an output outside the frozen directory gives 62,094 passing assertions
and a byte-identical control-results file.

A separately written checker imports no code from the submitted checker:

- SymPy independently verifies the integer discriminant identity,
  exceptional reductions, reciprocal identities, characteristic-two
  transform and derivatives, and the resultants recorded above.
- Dense-array convolution re-enumerates all 59,561 projective multipliers
  in the same four declared boxes. Every histogram matches exactly:
  32,767 at p=2, 3,280 at p=3, 3,906 at p=5, and 19,608 at p=7.
- The entire relevant abstract colored-graph class is enumerated on
  four, five, and six labeled vertices. There are 1,686 admissible
  colored graphs: 126 cycle cases and 1,560 forest cases. This does
  not assume lattice coordinates or a bounded lattice box.
- 76,738 binomial congruence cases include negative Laurent differences,
  p=3 repeated roots, and primes 3,5,7,11,13; 1,995 vanish, and all
  agree with the necessary-condition formula.

The independent checker passes 78,628 assertions. It uses Python 3.12.14
and SymPy 1.14.0, unlike the standard-library-only submitted checker.
SymPy emits one modular-integer comparison deprecation warning, with no
failed or skipped check. Environment details are recorded in its JSON.

These controls are supplementary. They do not certify geometric integrality,
radical saturation, mixing, or an unbounded odd-prime support exclusion.
No new proof-search approach was spent and no larger multiplier box was used.

## 9. Required corrections and final gate

C1. PROOF.md lines 144–145 says that distinct monomials are multiplicatively
independent modulo constants. Taken literally this is false: x and x² are
distinct, yet dependent. The exact replacement says x and y are independent
modulo constants and distinct exponent pairs give nonconstant quotients.

C2. REPORT.md line 9 calls the monomial group radical-saturated. For the
explicit G=⟨x,y⟩ in the proof this is false at odd p because F_p* is in
its radical but not in G, apart from 1. The exact replacement names
F_p*⟨x,y⟩. The section title, two summary phrases in the proof, the status
partial-result label, and the related research-log phrase are also made
precise as saturation modulo constants.

The precise main formula sqrt(G)=F_p*G was already correct. No other theorem,
proof step, source claim, computation, result, target scope, or turn budget is
changed in the corrected packet. Existing review-status metadata is left as
author-submission metadata; the present hash-bound audit supplies the decision.

**Only the corrected hash-bound packet receives PASS for partial results.**
The original freeze receives REVISE, and neither packet receives a full-solution
PASS. Recommended queue disposition remains **unsolved, 5/5**.
