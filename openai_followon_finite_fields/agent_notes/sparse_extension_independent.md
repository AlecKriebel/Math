# Independent sparse extension derivation

Checkpoint: 2026-10-07 05:26 UTC. This is a new route under examination, not a
novelty-certified publication result. Mathematical mechanism completion estimate:
85% (proof below; independently adversarial review still pending). Publication
package estimate: 0% for this sparse extension. Estimates are not evidence.
No frozen version-3 artifact has been edited by this work.

## Exact claim being tested

Let `K=F_p[T]/(h)` be the same explicit represented finite field as the core
project: `p` is a promised prime, `h` is monic irreducible of degree `m>=1`, and
coefficients use the power basis. Let a nonzero sparse polynomial be supplied as
distinct pairs `(e_i,c_i)`, `0<=e_i<=N`, `c_i!=0`, with binary exponents. Combine
duplicate exponents and remove zero coefficients first if input is not canonical.
Write `a=min e_i`, `f=X^a u`, so `u(0)!=0`, and `n=deg u`.

Assume every nonconstant monic irreducible factor of `u` has multiplicity not
divisible by `p`. Multiplicity itself is NOT bounded by `p`, `t`, or a unary input
parameter. Let `D` be the sum of the degrees of the DISTINCT irreducible factors
of `u`, without weighting by multiplicity. There is a deterministic reduction
to one dense factorization of degree `D`, with bit cost polynomial in
`t, log(N+2), D+1, m, log p`. It returns the leading coefficient, the factor `X`
with multiplicity `a` if `a>0`, and all other irreducibles densely, with their
exact multiplicities in binary. It checks the promise by degree accounting,
without expanding any huge power. The missing dense primitive is exactly the
core project's validated cited-source dense factorization algorithm; no new
prime-field breakthrough is claimed here.

The algorithm also recovers exact multiplicities of all visible factors on an
arbitrary nonzero sparse input. If any hidden factor has multiplicity divisible
by `p`, it detects incompleteness and does not report a complete factorization.
Thus the domain condition has a deterministic success certificate. This does
NOT solve general sparse factorization with arbitrary mixed p-divisible
multiplicities, nor low-degree-factor extraction where other factors can have
enormous total distinct degree.

## 1. Exact denominator of the logarithmic derivative

Over the finite field, every irreducible polynomial is separable. For
`u=c product g_j^{mu_j}`,

`u'/u = sum_j (mu_j mod p) g_j'/g_j`.

At a root of `g_j`, the corresponding summand has a simple pole if and only if
`p` does not divide `mu_j`: its residue is nonzero and other summands are regular.
Consequently the reduced denominator is precisely

`R = product_{p does not divide mu_j} g_j`.

It is squarefree, has nonzero constant coefficient, and its reduced numerator
has degree strictly less than `deg R`. Under the promise, `R` is the full
radical, `deg R=D`. If `u` is constant, the reduced rational function is `0/1`.
No evaluation at an enumerated field element or shift is needed: the known
nonzero constant coefficient supplies the Taylor center.

## 2. Adaptive rational reconstruction and sparse exact checks

For `B=1,2,4,...`, compute the first `2B` Taylor coefficients `s_k` of `u'/u`
at zero. Only the coefficients of sparse `u` of degrees at most `2B` are needed;
ordinary derivatives multiply each coefficient by its exponent modulo `p`.
Division of truncated series uses its invertible constant term and `O(B^2)`
field operations.

Solve the following `B` affine equations in `q_1,...,q_B`, with `q_0=1`:

`sum_{i=0}^B q_i s_{k-i}=0` for `B<=k<2B`, treating negative-index `s` as zero.

If inconsistent, increase `B`. Otherwise set `Q=sum q_i X^i`, and let `P` be
the degree-`<B` truncation of `Q sum_{k<2B}s_kX^k`. Reduce `P,Q` by their gcd.
Check the exact sparse polynomial identity `u'Q=uP`, by forming sparse/dense
products, combining equal binary exponents, and comparing every coefficient.
If it fails, increase `B`.

When `B>=deg R`, a solution exists because the normalized true denominator has
constant coefficient one. ANY solution represents the true rational function:
cross-multiplying it with the true reduced `P_*/R` yields a polynomial of degree
at most `(B-1)+deg R<=2B-1` which vanishes to order at least `2B`. It is zero.
Hence the method does not rely on an unproved minimal-recurrence selection
inside a singular Padé system. After gcd reduction and monic normalization the
denominator is exactly `R`. An exact identity at an earlier bound also gives
the true reduced denominator, so a false early stop is impossible.

The final bound is at most `max(1,2deg R)`. A geometric sum of naive arithmetic
costs gives `O((D+1)^3+t(D+1))` operations in `K` before the one dense factor
call; sparse exponent sorting/comparison adds polynomial bit work in
`t,D,log(N+2)`. The linear system dimension is `B` by `B+1` augmented, not `N`.

## 3. Binary multiplicities: initial-term recursion on exponent digits

This is the essential separate issue; residues of `u'/u` recover only
`mu_j mod p`, so reporting them as full multiplicities is incorrect.

Let `g!=X` be one returned monic irreducible, of degree `delta`. In the explicit
quotient field `E=K[Z]/g`, let `alpha=Z mod g`. Since `g(0)!=0`, `alpha!=0`.
Its degree over `K` is `delta`; arithmetic is on `delta` coefficients in `K`.
For the sparse input define `w_i=c_i alpha^{e_i}` by binary exponentiation.
Each weight is nonzero. The formal polynomial

`F(Y)=u(alpha(1+Y))=sum_i w_i(1+Y)^{e_i}`

has initial order equal to the multiplicity of `g` in `u`. This equality uses
separability and the invertible change of local coordinate `X-alpha=alpha Y`.

The following recursion computes both the initial order and initial coefficient
of any nonzero `F(Y)=sum w_i(1+Y)^{e_i}` with distinct exponents and nonzero
weights in an arbitrary field of characteristic `p`:

1. If there is only one term, return `(0,w_i)`.
2. Group exponents by their least significant base-`p` digit `r`; write
   `e_i=p q_i+r`. Form `H_r(V)=sum_{i in bucket r} w_i(1+V)^{q_i}`.
3. Recursively compute `(nu_r,a_r)` for every nonempty bucket.
4. Let `v=min nu_r`. Keep the buckets with `nu_r=v` and let their number be `s`.
5. For `j=0,...,s-1`, compute
   `b_j=sum_{nu_r=v} a_r binom(r,j)` in the field. Return the first nonzero
   `(pv+j,b_j)`.

Proof: Frobenius gives the exact identity

`F(Y)=sum_r (1+Y)^r H_r(Y^p)`.

Therefore

`F(Y)=Y^{pv} [sum_{nu_r=v}a_r(1+Y)^r + O(Y^p)]`.

The active residues are distinct elements of `F_p`, and `s<=p`. The square
matrix `binom(r,j)` with columns indexed by active residues and rows
`0<=j<s` has determinant equal, up to a nonzero sign, to
`product_{r<r'}(r'-r) / product_{j=0}^{s-1}j!`.
It is invertible because `s-1<p`. Since the `a_r` are not all zero, some
`b_j`, `j<s`, is nonzero. The first such `j` is strictly less than `p`, so the
omitted `O(Y^p)` terms cannot affect the initial order or coefficient. This
proves the recursion by induction on the maximum exponent. Branches terminate
because their exponents divide by `p` at each descent and distinct original
exponents eventually become separated.

Importantly, the scan length is at most `s<=t`, even if `p` is enormous.
Binomial coefficients use the recurrence
`binom(r,j+1)=binom(r,j)(r-j)/(j+1)` only when `j+1<s<=p`, so the inverse is
always legal. No factorial through `p`, characteristic-sized loop, or scan
through `mu_j` occurs. An iterative postorder implementation avoids any
runtime-stack restriction on `log N`.

At depth `k`, buckets partition the original `t` terms, so the sum of squares
of bucket sizes is at most `t^2`. There are at most
`ell=1+floor(log_p N)<=1+floor(log_2(N+1))` levels. Computing initial terms costs
`O(t^2 ell)` additions and prime-scalar multiplications in `E`. Computing all
weights first costs `O(t log(N+2))` multiplications in `E`.

Using elementary quotient multiplication gives `O(delta^2)` operations in `K`
per multiplication in `E`, and additions/scalar products give `O(delta)`.
Summing over distinct factors, `sum delta=D` and `sum delta^2<=D^2`, gives

`O(t log(N+2) D^2 + t^2 log(N+2) D)` additional `K` operations,

plus polynomial integer work in `t,log(N+2),log p`. One can safely bound each
elementary `K` operation by `O(m^2(log p+1)^3)` bit operations using schoolbook
arithmetic and polynomial extended Euclid for inverses. Quotient coefficients
remain `m`-tuples of residues of `log p` bits. The multiplicity result itself
has `O(log(N+2))` bits; returning it in binary is essential.

## 4. Completeness and promise checking

The factors of `R` are actual factors of `u`. Each recovered multiplicity is
exact, including arbitrarily large multiplicities and p-divisible ones if a
factor is supplied independently. Let `M=sum_j mu_j deg g_j` for factors of
`R`. Unique factorization proves `M<=n`, with equality if and only if `R`
contains every factor of `u`. Thus `M=n` is a checkable completeness
certificate; under the promised p-prime multiplicities it always holds. If it
fails, report a violated promise and the exact unaccounted degree `n-M`, not
a factorization of the original polynomial.

For example over `F_3`, `(X-1)^3(X+1)` has an invisible multiplicity-three
factor. Its logarithmic denominator alone is `X+1`; the degree check fails.
The trie itself does not need the p-prime promise and computes multiplicity
three at `X-1` correctly when that factor is supplied.

The leading coefficient is read directly from the largest-exponent sparse
term. Accounting for the stripped monomial adds the factor `X` with exact
binary exponent `a`; no zero-root shift is used.

## 5. Falsifiable exact checks

`sparse_extension_independent_checks.py` implements only the independently
derived initial-term/multiplicity mechanism. It uses the frozen project's
checked elementary field arithmetic but no factorization oracle; irreducible
root examples explicitly supply their modulus. It compares against direct
repeated dense polynomial division for small inputs. The exact test counts
and source hashes are saved in `sparse_extension_independent_checks.json`.

The initial run passed 13,102 exhaustive comparisons over `F_2,F_3,F_5,F_4,F_8`
and against irreducible quadratic quotient roots over `F_2,F_3`. Huge examples
include multiplicity `2^2048+1` from four terms (4,101 trie nodes), an
approximately billion-sized characteristic without a characteristic-sized
loop, and nonprime extension degrees. A subsequent amended run includes
huge characteristic-three p-divisible multiplicities and sparse powers of
irreducible quadratic factors. Results are evidence for the implementation,
not a substitute for the proofs above or the dense factorization input.

Run from the project root:

`python3 agent_notes/sparse_extension_independent_checks.py`

## 6. Priority and exact boundaries

The rational reconstruction/Padé machinery and the identity of the reduced
logarithmic denominator are classical. No claim is made to have invented them.
The following current primary sources were inspected online on 2026-10-07 UTC;
no research-only source downloads were added while disk space was tight.

* James L. Massey, Daniel J. Costello, Jr., and Jørn Justesen, *Polynomial
  Weights and Code Constructions*, IEEE Transactions on Information Theory
  IT-19(1), January 1973, pp.101–110. Primary author archive:
  https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI419.pdf.
  Lemma 1 (p.102) gives the base-p digit product for the weight of `(X-c)^mu`,
  using Lucas's congruence. Theorems 1.1 (binary) and 6.1/6.2 (general p)
  establish weight retaining under addition of higher powers. In particular,
  a t-sparse polynomial's nonzero-root multiplicity has every base-p digit
  at most `t-1`. These established structural facts positively overlap the
  present digit mechanism. Their stated theorem is a weight bound; an exact
  binary-exponent sparse multiplicity algorithm theorem was not identified
  in the inspected statements. That absence is not proof of novelty.
* Erich Kaltofen, *Factorization of Polynomials Given by Straight-Line
  Programs*, 1989 (author manuscript dated November 17, 1987),
  https://kaltofen.math.ncsu.edu/bibliography/89/Ka89_slpfac.pdf.
  The introduction explicitly measures complexity in straight-line input size
  AND the full polynomial degree; positive-characteristic p-divisible
  multiplicities introduce the separate power issue. This does not immediately
  subsume complexity polynomial in `log N` and distinct-factor degree `D`.
  The adjacent Kaltofen–Trager black-box work must also be included in any
  complete priority audit.
* Ruichen Qiu, Yichuan Cao, Qiao-Long Huang, Ruyong Feng, Xiao-Shan Gao,
  *Output-sensitive Sparse Polynomial GCD over Finite Fields is NP-hard*,
  arXiv:2606.12144v1, submitted June 10, 2026:
  https://arxiv.org/html/2606.12144v1.
  Their output measure is the sparse size of the gcd, potentially tiny while
  the inputs have huge distinct-factor degree. This route pays for dense
  degrees of EVERY distinct factor of a single input and assumes a checkable
  p-prime multiplicity condition. It does not imply the forbidden general
  output-sensitive sparse gcd algorithm. Introducing such a gcd oracle would
  invalidate the reduction rather than complete it.

No 'first' claim or publication recommendation follows from these checks.
The publication novelty condition remains unresolved until a full independent
priority audit determines whether the complete promised sparse reduction is
already an established immediate consequence. The original dense core
remains intact; this extension does not replace it.

## 7. Stronger route: rational Frobenius descent without the promise

Checkpoint 2026-10-07 05:34 UTC. The parent proposed a materially stronger
mechanism. The following is my independent verification. Its mathematical
proof has no identified gap at this checkpoint; exact tests are separate.
Priority and fresh adversarial verification remain pending. Mathematical
mechanism estimate 90%; publication package estimate 0% for this sparse route.

**Stronger theorem, conditional only on dense factorization.** For EVERY
nonzero sparse polynomial over the represented finite field, complete
factorization in dense distinct irreducibles and binary multiplicities reduces
deterministically to dense factorization calls of degrees polynomial in
`D,log(N+2)`, with total cost polynomial in
`t,D+1,log(N+2),m,log p`. The multiplicity promise is unnecessary. This claim
still pays for the dense degrees of ALL distinct factors, not just small
factors or a small gcd. The original dense core is preserved.

### Invariant and one exact descent

Maintain a nonzero polynomial `F=U/V` where `U` is sparse with at most the
original t terms and `U(0)!=0`; V is dense with `V(0)!=0` and `V|U`.
Initially `U=u,V=1`. Write `e_U(g),e_V(g)` for irreducible valuations;
`e_U(g)>=e_V(g)` follows from polynomial divisibility.

Recover the reduced denominator of `U'/U` by Section 2, factor it densely,
and recover exact numerator multiplicities by Section 3. Form the dense
monic polynomial

`A_U=product_g g^(e_U(g) mod p)`.

Factors with zero residue are absent. Its degree is at most
`min(t-1,p-1) D_U`, where `D_U=deg rad U`. The trie proves the t-1 residue
bound directly, so dense construction does not cost polynomial in numeric p.
Factor the dense V and form `A_V=product_g g^(e_V(g) mod p)` similarly.

Perfectness gives unique polynomials INCLUDING SCALAR UNITS such that

`U=A_U H_U^p`, `V=A_V H_V^p`.

Compute `H_V=(V/A_V)^(1/p)` explicitly by dense exact division and inverse
coefficient Frobenius. There is no need to compute the huge dense H_U.

For any B define the zero-residue section `B_0(Y)=sum_i b_(pi) Y^i`.
Since H_U^p has only p-divisible exponents, the exact identity gives

`U_0(Y)=(A_U)_0(Y) H_U^[p](Y)`,

where `[p]` raises coefficients, not the variable, to p-th powers. Apply
inverse coefficient Frobenius to BOTH U_0 and (A_U)_0, and define

`U_new=coefficient_Frob_inverse(U_0)`,
`W=coefficient_Frob_inverse((A_U)_0)`, `V_new=W H_V`.

Then `H_U=U_new/W`. Also

`e_(H_U/H_V)(g)=floor(e_U(g)/p)-floor(e_V(g)/p)>=0`.

Therefore `F_new=H_U/H_V=U_new/V_new` is a polynomial and the invariant
`V_new|U_new` is preserved. Its radical is contained in rad(F): when the
old quotient has valuation zero, the two old valuations and their floors
agree. All constant terms remain nonzero, including W, since A_U(0)!=0.
The sparse term count does not increase.

The exact descent identity is `F=(A_U/A_V) F_new^p`. The ratio A_U/A_V
may have negative irreducible exponents. Retain these as SIGNED residues
and add p times the subsequent exponents; discarding them is incorrect.
At the final stage the accumulated exponents are those of the original
polynomial, so they are nonnegative, and zero exponents are removed.

Scalar-unit boundary: H_V includes the p-th root of the scalar leading
coefficient of V/A_V. Replacing H_V by its monic normalization may break
F=U/V. For final monic factors, return the original sparse leading coefficient
as the output unit; intermediate polynomial identities still preserve units.

### Termination, dimensions, and bit encoding

`deg U_new<=floor(deg U/p)`, so there are at most
`ell=1+floor(log_p n)<=1+floor(log_2(N+1))` stages for n>0.
The degree of F_new itself NEED NOT drop by p: old valuations e_U=p and
e_V=p-1 give quotient multiplicity one at both stages. Termination uses
the sparse numerator degree, not the quotient degree.

Let v=deg V and `D_F=deg rad F<=D`. Because U=FV,
`D_U<=D_F+v`. Also

`deg W<=floor(deg A_U/p)<=((p-1)/p)D_U`,
`deg H_V=(v-deg A_V)/p<=v/p`.

It follows that

`deg V_new<=((p-1)/p)(D_F+v)+v/p<=v+D`.

Hence at stage k, `deg V<=kD`, `D_U<=(k+1)D`. At most two dense
factor calls per stage have degrees at most `(k+1)D` and kD respectively.
Each augmented Padé matrix has at most `2(k+1)D` rows/variables, or constant
size for zero logarithmic derivative. The temporary dense A_U has degree
at most `t(k+1)D`, which is permitted even though larger than V.
Computing coefficient inverse Frobenius uses binary exponentiation with
exponent bit length O(m log p), never a field-size loop.

For explicit conservative accounting put `b=ceil(log_2(N+2))`, `L=ceil(log_2 p)`,
and `d=D+1`, so `ell<=b+1`. Binary weight exponentiation uses b, NOT merely
the base-p digit count ell. At stage k, the bounds are:

* Padé recovery/identity: `O(((k+1)d)^3+t(k+1)d)` operations in K.
* Trie weights and initial terms across visible factors:
  `O(t b ((k+1)d)^2+t^2 b (k+1)d)` operations in K.
* Dense A_U construction: if its final degree is M, elementary binary
  powering and sequential product give `O(M^2 log(t+1))` operations in K;
  `M<=t(k+1)d`. For A_V use `O(((k+1)d)^2 log((k+1)d+1))` instead.
* Dense exact division, p-th root and denominator multiplication:
  `O(((k+1)d)^2+t(k+1)d mL)` operations in K. The coefficient Frobenius
  exponent is p^(m-1), with at most mL bits; section traversal is bounded
  by the explicit dense A_U size.

Summing over at most b+1 stages gives, in addition to at most `2(b+1)`
dense factor calls of degree at most `(b+2)d`, a valid bound

`O(b^4 d^3+t b^4 d^2+t^2 b^3 d+t^2 b^3 d^2 log(t+1)`
`  +b^3 d^2 log(bd+2)+t b^2 d mL)`

operations in K. Prime-field coefficients always have L bits and field
coefficients mL bits. Binary exponent grouping, sorting sparse products,
and maintaining exponent sums add polynomial bit work in t,b,d,L, with
all exponent values occupying O(b+L) bits. Multiplying this displayed
field-operation bound by the elementary `O(m^2(L+1)^3)` bit cost produces
an explicit polynomial bound, plus the displayed dense calls' bit cost.
Signed accumulators are weighted by p^k; at nonterminal stages `p^k<=N`,
so their encoding length stays polynomial in b and L. No optimized or
practical efficiency claim is made.

### Exact checks, including a falsified example claim

`sparse_rational_independent_checks.py` independently implements Padé,
sparse identity, zero sections, denominator update and signed accumulation,
using only the frozen field arithmetic and small-field test factor routine.
The latter's toy oracle is not the uniform dense algorithm. The script
compares against dense complete factorization on exhaustive small inputs
and saves exact source hash and stage dimensions to its companion JSON.
Huge test inputs have a nontrivial section denominator and actual negative
signed residues; they do not expand huge powers for validation.

The final independent rational run passed 777 exhaustive comparisons,
including 557 nonconstant-denominator stages and nine negative signed
residues. The huge F_2 quadratic example used nine terms and 63 stages;
the huge mixed F_3 example used 16 terms and 31 stages, with a negative
signed residue. Exact SHA-256 values and software version are in the JSON.
Two additional cases over F_4 and F_9 explicitly exercise a nonprime-field
unit, a stripped monomial of multiplicity seven, and other multiplicities
five and six; both reconstructed the exact dense polynomial and agreed
with the old dense factor routine. The independent multiplicity checker
also includes a composite extension degree four (F_16) huge example.

The initial suggested family
`(X-1)^(1+2*3^(k+1))(X+1)^2` over F_3 was claimed to force a negative
carry late in descent. Exact tests FALSIFIED that claim for k>0: the new
denominator cancels after the next step. For k=0 it does force a negative
carry. This failed test-family prediction is preserved, not silently removed.

The repaired huge family is
`F=(X-1)^(7+3^(k+1))(X+1)^2`, k>=1. Its first residue polynomial is

`A=(X-1)(X+1)^2=X^3+X^2+2X+2`.

Its zero-residue section is Y+2=X-1. The next numerator therefore has
multiplicity `3+3^k` at X-1 while the denominator has multiplicity one.
Their residues give `0-1=-1`, compensated by the subsequent positive carry.
Generate the sparse input by a fixed degree-nine polynomial
`(X-1)^7(X+1)^2` times the binomial `X^(3^(k+1))-1`, so sparsity stays
bounded while multiplicity and degree grow exponentially with k.

The stronger route removes the earlier promise as a necessary hypothesis;
Sections 1–6 remain a correct specialization and a record of the isolated
gap. Novelty is still unestablished, so no publication recommendation follows.

Further priority lead, searched 2026-10-07 UTC: Giesbrecht and Roche,
*On Lacunary Polynomial Perfect Powers*, ISSAC 2008 pp.103–110,
https://roche.work/research/papers/lacunary-pp.pdf, and the later version
*Detecting lacunary perfect powers and computing their roots*,
https://arxiv.org/abs/0901.1848. This is adjacent primary literature on
binary-degree root/multiplicity compression. The initial author PDF imposes
large-characteristic conditions for finite-field detection and conjectural
sparse-root computation. Those inspected statements do not visibly
subsume the all-characteristic rational-denominator reduction here.
That observation does not establish priority: exact later theorem versions,
citation chains, and other related sources still require an independent
audit. The output measures differ: the current theorem pays for the dense
radical degree, not the sparsity of the extracted root polynomial.
