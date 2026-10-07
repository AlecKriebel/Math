# Audit of a smaller incidence parameter

Audit checkpoint: 2026-10-07 05:50 UTC (2026-10-06 22:50 America/Los_Angeles).
This is a separate research note. It does not alter the reviewed manuscript,
PDF, archive, publication status, or mathematical attribution.

## Conclusion and exact scope

The October 4 construction works with `q=32` in place of `q=128`, after the
numeric substitutions listed below and a fresh choice of all dependent
constants. Its rose has **532 geometric edges**, so its finitely presented,
torsion-free cone group has a presentation with at most 532 generators and a
finite two-dimensional classifying complex. Its scalar witnesses still
satisfy `ab=1`, `ac=0`, `c!=0`; the already verified idempotent and projective
module consequences therefore apply unchanged.

Van Kampen's theorem gives a surjection from the rose's free group to the
cone group: attaching a cone on each connected graph component kills its
fundamental group and introduces no generators. Thus the rose count really
is an upper bound for the group, rather than just an alphabet statistic.

More precisely, **32 is the least admissible dyadic parameter for the
unchanged Fano-complement type design, its prescribed inverse pairs, its
leading turn weights, and its squared-word-decay argument**. Exact positive
rational vector certificates prove that `q=4,8,16` fail squared-word decay,
including every possible choice of positive contraction vector. The fixed
type-count formulas cannot be integral at `q=2`. This is not a lower bound on
the number of generators of all counterexamples, and does not exclude a
different type design, weights, conditioning argument, or method at smaller
parameters.

The 532-generator existence statement is subsumed by a classical
two-generator embedding, including preservation of a finite two-dimensional
classifying complex; see the final section. The sharp local threshold is
checkable additional information about this construction. It is a modest
parameter analysis using the source's existing estimates, not a new mechanism
for the conjectures. No novelty, priority, or publication clearance is
certified here. In particular, this audit alone does not remove the existing
duplication gate.

Completion estimates for this branch: exact mathematical parameter audit
100%; independent parameter falsification 100%; novelty/publication gate
unresolved, 0% certified. These estimates concern this branch, not a revision
of the persistent project's success criteria.

## Primary input and reproducibility

The original request was read from `notes/ORIGINAL_REQUEST.txt`. The primary
construction was read directly from the pinned source, not inferred from the
old favorable reviews. Let `S` denote

`sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/sections/`.

The upstream commit is `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
Relevant hashes are:

| Input | SHA-256 |
|---|---|
| `S/random.tex` | `bb172b92ba622e262c2bf124e70c3cd55922200083c09db658615759b81323c4` |
| `S/patterns.tex` | `20c6cc1f3fb035150831e5091c98313f04e7a9d8aaa347507020b176394ed4ea` |
| `S/planar.tex` | `e3a1a4e23dd6871a9746ffde05d32297e695f3167b8efa0f0a4cad5da8c9ae6b` |
| `S/algebra.tex` | `71fe26eab4e6a01564a687c522bbceb8923182c0201af9685eac84d9f86a141f` |

Run from the project root:

```sh
python3 notes/extensions_parameter/check_parameter.py
```

This standard-library script checks source hashes and every rational
inequality below. Its saved output is
`notes/extensions_parameter/exact_certificates.json`. Decimal output is
orientation only; no decimal comparison establishes a claim. An independent
subagent checked the exact source and saved its findings in
`notes/extensions_parameter/independent_check.md`. It found the closure
degree replacements as well as the expansion replacements and supplied an
independent growth certificate at `q=16`.

No actual matching outcome, finite presentation word list, or numerical
group-ring multiplication certificate is produced here.

The publication-oriented version is the new
`verification/verify_parameter.py`. It runs with standard-library rational
arithmetic from a clean package that omits the upstream working copy. When
the four source files are present it checks their hashes; when absent it
explicitly labels those optional checks skipped. All mathematical outputs
are identical in both modes. The isolated-run receipt is
`notes/extensions_parameter/portable_verification_receipt.json`.

## Types and balances at q=32

Use the projective plane over `F_32`, the same seven extra letters, the same
seven Fano-line complements, and the same rule pairing every extra letter
with a distinct ordinary letter. The unpaired ordinary letters number
`1057-7=1050`, an even number.

The field `F_32` here specifies the incidence plane only. The scalar
group-ring witnesses still have coefficients in `F_2`. Put

\[
q=32,\quad v=q^2+q+1=1057,\quad |T|=1064,\quad
p=\frac{33}{1057},\quad n=1057m,\quad m\equiv1\pmod4.
\]

Thus `n≡1 (mod 4)` and `|B|=1057(m-1)` is divisible by four. The exact
source extra-type multiplicities become

\[
a_m=\frac{33m-1}{4},\qquad b_m=\frac{33(m-1)}4.
\]

Both are integers. The ordinary and extra occurrence counts are respectively
`33m=np` in A and `33(m-1)=(n-v)p` in B. Inverse letters therefore have equal
numbers of slots on each side, as required by every random bijection.

For each of the seven complements, distribute its occurrences among line
classes with counts differing by at most one. The total demand in a class,
including the reserved root when needed, is at most `7 ceil(a_m/v)+1` in A
and `7 ceil(b_m/v)` in B. The common leading capacity coefficient is

\[
\frac{7(q+1)}{4v}=\frac{33}{604}<1.
\]

Consequently all seven assignments can be realized on disjoint vertices in
every line class for all sufficiently large admissible m: allocate their
quotas successively while reserving the A root. The exact bounds already
hold at `m=13`; larger admissible m also satisfy them. This certifies the
types only, not successful edges.

Intersections of ordinary parts have size 33 for equal lines and one for
different lines. The Fano-complement intersections have size zero, two, or
four; only the full seven-letter root set has odd self-intersection. Thus
the source's odd-intersection hypotheses and single even-degree exception
are unchanged. Vertex degrees are precisely among 33, 37, and 40, with the
distinguished A root having degree 40.

References: `S/random.tex:14–128`, especially the extra-count, label-balance,
type-parity, and degree-bound equations.

## Exact quotient for optimal weighted contraction

Write E for the seven extra letters, O for their seven ordinary inverse
mates, and R for the remaining `v-7` ordinary letters. These are classes of
the input letter t, not of its inverse. Put

\[
\alpha=(q+1)^{-2},\qquad\beta=p^2.
\]

For the squared turn matrix `M_{t,u}=w(t,u)^2`, vectors constant on E,O,R
are preserved, and its exact quotient in that order is

\[
Q_q=\begin{pmatrix}
7\beta&6\alpha&(v-7)\alpha\\
3/2&7\beta&(v-7)\beta\\
7\beta&7\alpha&(v-8)\alpha
\end{pmatrix}.
\]

For example, an E input has an ordinary inverse in O, so the forbidden
successor removes one of the seven O letters. An O input has an extra
inverse, so its six permitted extra successors each have squared weight
one quarter. An R input loses one R successor. This count is independent of
which ordinary points were selected as the extra-letter mates.

All entries of Q are positive at `q≥4`. Its positive Perron eigenvector
lifts to a positive full-alphabet eigenvector of M. The full matrix is
irreducible (indeed its square is positive), so

\[
\rho(M)=\rho(Q_q).
\]

Therefore the three-class calculation finds the best possible spectral
contraction for the entire squared turn matrix, rather than merely testing
one favorable vector. For the word weights in the source,

\[
\sum_{W\in T^h}P(W)^2={\bf1}^{\mathsf T}M^{h-1}{\bf1}.
\]

No reduction in this identity ignores the unreduced words: their weights
are zero through the forbidden-turn entries.

References: `S/random.tex:132–220` (turn weights, frequencies, word weights,
and word-decay proof).

## Exact positive upper certificate at q=32

Set `f=(1,13/5,1)` on E,O,R. Direct rational evaluation gives

\[
\frac{Q_{32}f}{f}=
\left(
\frac{95146189}{96562235},\quad
\frac{579417}{592826},\quad
\frac{857592557}{869060115}
\right)
<\left(\frac{987}{1000},\frac{987}{1000},\frac{987}{1000}\right).
\]

Lift f to the full alphabet. Since `1≤f` coordinatewise and
`sum_t f(t)=5376/5`, positivity yields the explicit bound

\[
\sum_{W\in T^h}P(W)^2
\le\frac{5376}{5}\left(\frac{987}{1000}\right)^{h-1}.
\]

The source's choice `δ=−(1/4)log(987/1000)>0` consequently gives its
required large-h bound `exp(−2δh)`.

The source's unoptimized vector `(1,4,1)` already suffices at 32: its two
displayed row upper bounds are

\[
\frac{57694220}{57937341}<1,\qquad
\frac{116319}{182408}<1.
\]

In fact it suffices at every q≥32. For the ordinary row it is enough that

\[
\frac{21}{q+1}+\frac{7(q+1)}{q^2}<1.
\]

Both summands decrease for q≥32, and their sum at 32 is
`9709/11264<1`. For the extra row use
`(v+21)p^2≤1+1/q+22/q^2`, whose value at 32 added to 3/2 is less than four.
Thus every larger dyadic parameter also remains admissible.

## Exact obstruction at every smaller admissible dyadic parameter

For `q=4,8,16`, take the same positive vector

\[
x=(193/500,1,97/250).
\]

The following exact row ratios all strictly exceed `503/500`:

| q | E row | O row | R row |
|---|---|---|---|
| 4 | `480733/303975` | `26959/21000` | `500011/305550` |
| 8 | `10342603/9256473` | `5726739/5329000` | `10523789/9304434` |
| 16 | `35146373/34932807` | `3571543/3549000` | `2078707/2065518` |

Because `0<x≤1`, iteration after lifting to the full alphabet gives

\[
\sum_{W\in T^h}P(W)^2
\ge\left(7x_E+7x_O+(v-7)x_R\right)
\left(\frac{503}{500}\right)^{h-1}.
\]

For q=16 the prefactor is `11291/100`. Thus exponential decay is false,
not merely unproved by the source's original vector. In particular no
alternative positive contraction vector can repair this same matrix.

At q=2 the source's count formulas are inconsistent: integrality of
`b_m=3(m-1)/4` forces `m≡1 (mod4)`, while integrality of
`a_m=(3m-1)/4` forces `m≡3 (mod4)`. There is no admissible m. This count
obstruction is specific to the prescribed formulas.

Together with the uniform q≥32 upper bound, these exact inequalities prove
the stated least-dyadic-parameter claim.

## Girth, expansion, closures, and arrangement exclusion

All affected hardcoded source values were searched across the complete
section sources. The substitutions are:

| Source use | q=128 value | q=32 value |
|---|---:|---:|
| Ordinary line size / minimum degree | 129 | 33 |
| Other type sizes | 133,136 | 37,40 |
| Maximum degree d_* | 136 | 40 |
| v and alphabet size | 16513,16520 | 1057,1064 |
| Number of ordinary inverse pairs plus extras | 8260 | 532 |
| Number of edges forced by a nonexpanding k-set | ceil(129k/2) | ceil(33k/2) |
| Lower and upper bounds for r/k | 64.5,65 | 16.5,17 |
| Sufficient linear-exposure bound | 65ρ<p/4 | 17ρ<p/4 |
| Expansion union-bound exponent | 62.5 | 14.5 |
| Small-k exponent after k≤sqrt(n) | 31.25 | 7.25 |
| Minimum degree after deleting ≤2 edges | 127 | 31 |

The last entry occurs in `S/planar.tex:66,87` and is easy to miss if one
edits only `random.tex`. It remains at least three, which is the only degree
threshold needed by the short-closure counting argument.

For q=32 one may choose `c0=1/100`. The girth requirements
`c0 log(2|T|/p)<1` and `2c0 log(d_*)<1` hold, since `2|T|/p<2^17`,
`d_*=40<2^6`, and `log(2)<1`. The source's switch and prescription estimates
therefore retain

\[
L=\lfloor c_0\log n\rfloor,\qquad
r_n=vp+O(40^{2L+2})=33+O(40^{2L+2})=o(n).
\]

For a nonexpanding k-set, use `r=ceil(33k/2)`, so `16.5k≤r≤17k`.
The source's union bound becomes

\[
\Pr(\text{failure at size }k)
\le\left(C_3(k/n)^{29/2}\right)^k.
\]

Its small-k part is bounded by `(C3 n^(−29/4))^k`; its large-k part is
bounded by `2^(−k)` after shrinking ρ. Both sums tend to zero.

An explicit harmless choice is `ρ=10^(−6)`. Using `e<3`, take
`C2≤8e|T|/33`, `D=2C2/p<50000`, and `C3≤(9/4)D^17`. Then
`17ρ<p/4` and `C3 ρ^(29/2)<1/2`, all checked rationally by the script.
This still does not quantify the sufficiently-large-n errors. The same
ball-doubling proof yields a fixed diameter constant d, which must be
chosen again rather than inherited from q=128.

Short closures now begin with degree at least 33 and retain degree at least
31 after deleting two specified edges. The ≥3 nonbacktracking-walk count
and the source formula `D0≥d+8/(c0 log2)+8` therefore remain valid.

The bounded-pattern argument uses a fixed finite alphabet, a positive
minimum turn weight (now `1/33`), the squared-word decay just proved, and
the same conditioned prescription estimate. Its constants δ, a0 and ε
must be chosen for these weights; ε is still chosen before K0,C,I.
The grid and multiplicity arguments impose no special degree129 condition.
The planar extraction constants d,D0,U,η,K0,C,I are then selected in the
same order stated in `S/planar.tex`; their possibly large sizes are fixed
before m tends to infinity. Thus the absence-of-arrangements theorem still
holds, and the source's deterministic topology and parity criteria apply.

References: `S/random.tex:224–449`; `S/patterns.tex:28–49,132–170,384–593`;
`S/planar.tex:57–131` and its extraction-constants equation;
`S/algebra.tex:29–82`; `S/assembly.tex`.

## Why 532 does not establish a new generator-count discovery

Primary source checked on 2026-10-06:
G. Higman, B. H. Neumann and H. Neumann, *Embedding Theorems for Groups*,
J. London Math. Soc. 24 (1949), 247–254, §4, Theorem IV and its proof,
[DOI 10.1112/jlms/s1-24.4.247](https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms/s1-24.4.247).
For finitely generated input, its construction uses finitely many cyclic
HNN edges, one finite-rank free amalgamation, and one rank-two free HNN
edge, and yields a two-generator overgroup.

The geometric inference used here is supported by Scott and Wall,
*Topological methods in group theory*, Proposition 3.6(ii): a graph of
aspherical spaces with injective edge-group maps has aspherical total
space. The inspected primary scan is
[Scott–Wall](https://people.math.osu.edu/davis.12/courses/8800/ScottWall.pdf).
In the finite-generator HNN construction all edge spaces can be finite
graphs. A finite two-dimensional input therefore gives a finite
two-dimensional total space at every stage; its dimension does not grow.
Consequently the original source group embeds in a two-generator group
with a finite two-dimensional classifying complex. Such a group is
torsion-free. The group-algebra inclusion is injective on the group basis
and preserves the same scalar witnesses, nontrivial idempotent, and
cyclic projective defect.

This comparison is an inference from the classical construction and the
graph-of-spaces theorem, not a claim that the primary paper explicitly
states this characteristic-two corollary. It is enough to falsify an
assertion that the number 532 supplies a new minimal-generator headline.
The exact threshold for this particular probabilistic design is a separate
and narrower technical fact. No claim about its first public occurrence is
made: the pinned source and the zero-divisor companion use q=128, but a
local search finding no q=32 statement is not a completed priority audit.
