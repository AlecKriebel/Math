# Independent audit of the Bahri Xu discrete interaction inequality

Problem 30000263, OWR-1050-014. Audit date 2026-10-05 UTC.

## Verdict and audited object

**ACCEPT THE STATED PARTIAL RESULTS. NO GENERAL RESOLUTION.** No mandatory
mathematical correction was found in the authenticated author freeze.
The real collinear zero-exclusion proof, support-transfer estimate, geometric
zero exclusion through five points, six-point spatial-to-planar reduction,
two-ring exclusion, and local counterexamples survive this independent audit.
The quantitative uniform conclusions explicitly retain their cited external
collision/escape theorem. They are not self-contained consequences of
pointwise zero exclusion.

The exact audited archive is:

- Filename: DISCRETE_INTERACTION_30000263_AUTHOR_SAFE_FREEZE.zip
- Bytes: 33182
- SHA-256: e2f02d9bcc751e0551ccde2a32ab3ff701e2355b0394aeb24c56b96adb44a14e
- Entries: 14 flat files, with no duplicate archive names
- Manifest SHA-256: 40d9969d77bfd68150e59091340bfdee7a0f38d6d177282969905714d5eed0cf

Every archive member matched the supplied author release byte for byte. All
tests were conducted on copies or through read-only inputs. Neither the author
release nor its archive was changed. This audit performed no remote mutation,
publication, or external outreach.

Acceptance is limited to the mathematical statements actually made. It does
not certify novelty, the universal conjecture, a positive numerical global
lower bound, or the exclusion of six-point planar zero configurations.

## Primary question and provenance

The complete target record was extracted anew from the full problems corpus,
not accepted from the author's shortened metadata. The matching catalog record
is unique. The complete associated report is absent, so its prescribed value
is the empty object. The digest of the default sorted JSON serialization of
the pair [complete record, report-or-empty-object] is
41dce0de0472889e89c4936d3356ad2b0e568c1368a3cff52261db747b141f38.
The three full input byte counts, record counts, and hashes independently
match the author pins; see INPUT_SOURCE_CHECKS.json. No corpus contents are
included here. Rank 806 is the supplied queue identifier, not an independently
recomputed live ranking.

The live problem page independently returned HTTP 403. The original OWR
display was checked in a fresh local rendering at printed page 1658, against
the full record and the later published formulation. The first source writes
an abbreviated supremum range; the target's all-point/all-coordinate maximum
is explicitly identified rather than silently substituted. The suggestion of
a continuous extension is background, not an additional theorem proved here.
The original question is in Bahri's OWR contribution. [S1]

The five PDF files were independently fetched from their public URLs. Every
fresh byte count and SHA-256 matched the supplied source pin. The journal
theorem statement, disputed complex step, and older manuscript's sphere step
were also visually inspected in independently rendered pages. Source PDFs,
extracts, and rendered pages are deliberately excluded from this archive.

Fresh read-only repository checks found no target-specific earlier PR,
matching branch, commit-message result, or default-branch code result. The
current root tree differs from the author's earlier root-tree snapshot, while
the checked attempts subtree is unchanged and has no target path. This is a
bounded search result, not an assertion of exhaustive absence. Public hashes,
queries, and scope are in PRIOR_ARTIFACT_REVIEW.json.

## Normalization and elementary estimates

Use the report's definitions P_i, F_i, G_i=-2u_iF_i, D, and N. Direct
differentiation of both symmetric entries involving x_i gives the factor -2
in G_i. The ordered denominator can be written either with u_i squared or
with u_j squared by interchanging its dummy indices. For p at least two and
u nonzero, D is strictly positive. For p=1, the inequality itself is vacuous;
zero exclusion would be false and is not used at that point count.

Writing B=|Au|^2, M_infinity=max_{i,k}|G_i^k|, and
M_2=max_i|G_i|_2 gives M_infinity <= M_2 <= sqrt(3)M_infinity in R^3.
Thus B+M_infinity <= B+M_2 <= sqrt(3)(B+M_infinity). The norm conversion
and corresponding possible loss by sqrt(3) are correct. Rotation does not
preserve the coordinate maximum numerically, but it preserves the zero system
and admits this uniform norm comparison. No fixed numerical constant is
transported under arbitrary rotations or inversions without justification.

The same-sign expansion is correct: every off-diagonal cross product in a
potential square is nonnegative. The unbalanced-sign estimate follows from
the reverse triangle inequality and the rowwise Cauchy-Schwarz bound. Under
D_- <= D_+/[4(p-1)], its lower bound is D_+/4; division by
D <= D_+[1+1/(4(p-1))] gives exactly (p-1)/(4p-3).

The three-point spectral family has the reported potential, denominator,
force signs, and full ratio. In particular its middle force dominates the
other two for 0 < epsilon < 1. The failure of an Au-only estimate has no
implication that the full inequality fails.

## Quantitative transfer from an active support

Let S be the nonzero support and let its cardinality be s. For s >= 2, select
an active site j nearest to each inactive site k. For i in S other than j,

    |x_i-x_j| <= 2|x_i-x_k|,
    u_i^2/|x_i-x_k|^2 <= 4u_i^2/|x_i-x_j|^2.

These particular terms form a subset of D_S, because D_S is an ordered sum.
Consequently, with b_i=u_i/|x_i-x_k|,

    sum_{i != j} b_i^2 <= 4D_S,
    b_j^2 <= 2P_k^2 + 2(s-1)sum_{i != j}b_i^2,
    sum_i b_i^2 <= 2P_k^2 + 4(2s-1)D_S.

Summing the last estimate over all p-s inactive sites gives

    D <= [1+4(2s-1)(p-s)]D_S + 2Q,
    Q = sum_{k outside S}P_k^2.

The active potential rows and forces remain unchanged, while inactive forces
are zero. Hence N=N_S+Q. If N_S >= c_sD_S, then with
C=1+4(2s-1)(p-s),

    D <= (C/c_s)N_S+2Q <= max(C/c_s,2)N.

The stated min(c_s/C,1/2) is therefore valid. Nearest-site ties do not affect
the argument; any minimizer works. There is no assumption on an inactive
site's separation beyond pairwise distinctness, and no hidden dependence on
the positions of those inactive sites.

At support one, every force is zero and the sum of potential squares is exactly
D, including the terms contributed by all inactive rows. At support zero,
both sides are zero. If p=s, the displayed bound remains valid although the
unnecessary cap by 1/2 is not sharp. For s=2 and p>2, C=1+12(p-2) is at
least 13, so c_s=1 yields exactly the explicit constant 1/C. The separate
p=2 value c=1 is justified directly.

Taking a finite minimum over s <= min(5,p) is legitimate once the active
constants are uniform. For a line embedded in R^3 with arbitrary orientation,
one may first take the one-dimensional vector-norm constant and divide by
sqrt(3) before substituting c_s. The statement is about vectors with an exact
support bound. It does not control a sequence with six nonzero coordinates
merely because one coordinate tends to zero.

## The collinear zero exclusion proof

### Support and sign reductions

Begin with a nonzero solution of P_i=0 and u_iF_i=0 for p >= 2. An active
support of size one is impossible: at every other original site, its
potential is one nonzero charge divided by a positive distance. After this
case is excluded, restrict to the active sites, preserving their equations.
Every remaining charge is nonzero and every remaining force vanishes.
For s>=2, charges of one sign would make every active potential nonzero.
There are therefore both signs. In their order along the line, at least one
adjacent pair has opposite signs. This argument does not require an original
inactive site to remain in the restricted system.

### Cubic identity

For an unordered pair of sites at coordinates a and b, its contribution to
sum_i u_i x_i^3F_i is

    u_a u_b (a^3-b^3)(a-b)/|a-b|^3
      = u_a u_b(a^2+ab+b^2)/|a-b|.

Its contribution to (3/2)sum_i u_i x_i^2P_i is
(3/2)u_a u_b(a^2+b^2)/|a-b|. Subtraction leaves
-(1/2)u_a u_b|a-b|. Summing proves the identity for every real charge vector,
including zero entries. In a zero system the left side vanishes, giving zero
distance energy. No ordering convention or omitted absolute value changes
its sign.

### A finite inversion center exists

Let adjacent active charges u_l and u_{l+1} have opposite signs. On their open
gap, f(a)=sum_i u_i/(x_i-a)^2 is continuous. At the left endpoint its only
singular term has sign u_l; at the right endpoint its only singular term has
sign u_{l+1}. All other terms stay bounded in the respective limits.
Choose two interior points close enough to the endpoints that the function
has opposite signs there. The ordinary intermediate value theorem on that
closed subinterval produces a finite a in the open gap, different from every
active site, with f(a)=0. A possible inactive site at a is harmless: inversion
is applied only after restricting to the active configuration.

### Full Kelvin identity and its sign

Put a_i=x_i-N, r_i=|a_i|, y_i=N+a_i/r_i^2, v_i=u_i/r_i, and
Q_i=I-2a_i a_i^T/r_i^2. Independent differentiation gives the full identities

    P'_i = r_i P_i,
    F'_i = r_i a_i P_i + r_i^3 Q_i F_i.

For example, exclude site i from the external potential and observe that its
transformed potential is |x-N| times the original external potential. The
inverse Jacobian is r_i^2 Q_i and Q_i a_i=-a_i; applying the chain rule yields
the displayed plus sign on the potential term. At P_i=0 it reduces precisely
to the force formula used by the report. In fact
v_iF'_i=u_i a_i P_i+r_i^2Q_i(u_iF_i), so the entire zero system is preserved
even when some charges are zero. Inversion is an involution and maps distinct
non-center sites to distinct finite sites.

In one dimension Q_i=-1. The transformed distance is
|y_i-y_j|=|x_i-x_j|/(r_i r_j), so

    v_i v_j |y_i-y_j|
       = [u_i/r_i^2][u_j/r_j^2]|x_i-x_j|.

Thus the weights in the final energy really are w_i=u_i/(x_i-a)^2, not the
Kelvin charges v_i themselves. Their total is zero by construction, and a
nonzero original charge stays nonzero.

### Strict negative distance energy

Across the gap x_{k+1}-x_k the energy coefficient is
(sum_{i<=k}w_i)(sum_{j>k}w_j). Since the total is zero, this is the negative
square of the prefix sum. Every gap is positive. Zero energy therefore
forces every prefix sum to vanish; successive differences and the zero total
force every weight to vanish. This contradicts the nonzero active charges.
The proof is valid for all finite active support sizes. It uses no complex
weights and no external uniformity theorem for the pointwise conclusion.

## Geometric reductions

### One or two points strictly above a hyperplane

There must be at least one active point in the hyperplane. For a single
off-hyperplane point, the normal component of any force at such an on-plane
point is a nonzero multiple of the off-plane charge, which is impossible.

For two off-plane points a,b at positive heights h_a,h_b, the normal equations
give opposite charge signs and a fixed positive distance ratio
|x_i-b|/|x_i-a|=K independent of i in the hyperplane. Let
T=sum_{i in H}u_i/|a-x_i|. The two potential equations are
T+u_b/|a-b|=0 and T/K+u_a/|a-b|=0, which imply u_b=K u_a.
This contradicts the sign condition. The powers in the force equation only
determine K; they do not change this last positive ratio.

### Enclosing sphere lemma

The affine-spanning hypothesis is necessary and is stated. Lift the sites to
(x,|x|^2). Their affine hull has dimension d or d+1 because projection spans
R^d. In the first case projection is an affine isomorphism onto R^d, so the
lifted hull is the graph of an affine function and all original sites are
cospherical.

In the second case, let B be the convex hull of the lifted sites. Above an
interior point of the projected hull, take the highest point of B. To make
the facet argument precise, choose that base point outside the projections
of all faces of dimension at most d-1. Such a choice exists because finitely
many lower-dimensional sets do not fill an open set. The top point then lies
in the relative interior of a d-dimensional facet. That facet is nonvertical
and has an upper supporting equation t=2c dot x+b. Its projection has
dimension d. Therefore it contains d+1 lifted vertices with affinely
independent projected sites. The supporting inequality is exactly the
enclosing-ball inequality |x-c|^2 <= |c|^2+b. The radius cannot be zero when
the set has distinct sites. This proves the report's lemma without requiring
a minimum-radius ball.

When this lemma is used, d>=2. Its sphere has infinitely many points, so one
can choose an inversion center on it outside the finite site set. Inversion
maps its boundary to a hyperplane and its strict interior to one strict
half-space. For verification, translating the center of inversion to zero
turns a sphere through zero into |x|^2-2c dot x=0; substituting x=y/|y|^2
gives the hyperplane 1-2c dot y=0 and the corresponding strict inequality.

### Counts through five points and the six-point reduction

With s nonzero charges and affine dimension s-1, the s-1 difference vectors
from any one site are independent. The zero force at that site has nonzero
coefficients u_j/|x_i-x_j|^3, an impossibility. Hence a nonzero full-support
zero system has affine dimension at most s-2.

For 3<=s<=5, dimension d>=2 can only be 2 or 3. The enclosing sphere touches
at least d+1 sites, leaving at most two strict interior sites. Inversion and
the preceding obstruction either contradict the zero system or put every
site in dimension at most d-1. Repetition reaches the already proved line
case. Support one was handled separately, and support two has a nonzero
potential at each site. This establishes zero exclusion through five active
sites in any ambient dimension without circular use of the published
collinear argument.

For six sites in R^3, smaller-support cases are excluded by these results.
If the full-support configuration is not already planar, its enclosing
sphere touches at least four sites, leaving zero, one, or two inside. The
last two cases are impossible after inversion. Thus every such spatial
zero system has a planar representative with the same number of distinct,
nonzero-charged sites. The converse implication is simply embedding the plane
in R^3. The argument preserves zeros, not a quantitative ratio under Kelvin
inversion.

A planar enclosing circle can touch only three sites. Three off-line sites
then remain after inversion, so the two-point obstruction has no extension
from this proof. The residual 3 by 3 normal-force matrix is correctly
identified as an obstruction whose universal exclusion has not been proved.

## Use of the published uniformity theorem

For fixed ambient dimension m, the published Theorem 1.4 gives an equivalence
over every point count from 4 through p_0. Its inductive version, Theorem 2.6,
requires the inequality for every smaller count. The two- and three-point
bases are separately available. The proof first normalizes the minimum
distance and treats escaping clusters, and then uses bounded separated
configurations; the continuity step is not made on the unrestricted space.
These statement and dependency checks were performed in the final journal
PDF, including the material before Lemma 2.2. [S2, S3]

The report satisfies the hypotheses: its line proof works at every finite
count, its small-count proof supplies all counts through five, and its
six-point equivalence has the smaller counts already covered. A planar
six-point uniform theorem would exclude planar zeros, hence spatial zeros,
and Theorem 2.6 in m=3 would then give spatial uniformity. Restriction yields
the reverse implication. The audit imports this published theorem; it does
not claim an independent reproof of every collision/escape estimate. The
questioned later complex inference is not needed for this import.

## Two regular concentric rings

For 0<t<1, the potential system has coefficient matrix
[[L,S],[S,L/t]]. Its nonzero kernel requires S=L/sqrt(t), because L and S are
positive, and gives beta=-sqrt(t)alpha. Both charges are nonzero.

The derivative must hold the charges fixed. Starting from
E=nLalpha^2+nLbeta^2/t+2nS(t)alpha beta and only then substituting the
zero-potential relations gives

    E' = -nLalpha^2/t - 2n sqrt(t)alpha^2 S'
       = -2nalpha^2 (sqrt(t)S)'.

Each summand of H=sqrt(t)S is
[t+t^(-1)-2cos(phi)]^(-1/2). Its derivative is positive for 0<t<1.
Thus E' is strictly negative. If every coordinate derivative of E vanished,
its derivative along this inner-ring motion would be zero. The contradiction
is correct. Equal radii are covered by inversion of the common circle, with
a finite center outside the sites. The result assumes charges constant on
each ring; it does not cover arbitrary charges or establish uniformity over
all point configurations.

## The two local counterexamples

For the report's six-point example, the first three squared radii are 1 and
the remaining three are 1/4,1/4,1/16. The positive weights 3/8,5/16,5/16 have
unit sum and weighted center zero. Hence their weighted squared distance to
any center c is exactly 1+|c|^2. Every enclosing ball has squared radius at
least this value; the unique minimum is the unit ball at zero. A determinant
of three difference vectors is 32/25, proving full affine dimension three.
There are exactly three noncollinear contacts. Their circumcenter is zero,
so the older manuscript's division by its norm is undefined. This directly
refutes its specific minimum-ball assertion, while the non-minimal enclosing
sphere lemma remains true. No charge vector solving the zero system is
asserted for this example. The manuscript also leaves its final planar
reduction unjustified. [S4]

For the complex example, multiply both displayed weights by sqrt(2), giving
W_2=1-i and W_3=2i. The two coefficients (y_k-y_1)/|y_k-y_1|^2 are
(-1+i)/2 and -1/2. Their weighted products are i and -i, but W_2+W_3=1+i.
The weights also have the stated half-angle phases with real v_2=1 and
v_3=-sqrt(2). Thus the individual real-inner-product inference on the
published page is invalid for the displayed class of complex weights. This
example is not a solution of all the preceding simultaneous equations and
does not disprove the published theorem. [S3] The accepted real collinear
proof entirely avoids this inference.

## Independent computation and artifact controls

The independently written verifier imports no author checker. It uses an
unordered-pair implementation and a different random seed. The finite tests
support, but do not replace, the analytic arguments above:

- 279 rational line configurations verify the cubic and strict distance
  identities; 837 inversion centers cover both exterior sides and an
  interior gap
- 300 rational support configurations include 40 support-zero and 40
  support-one cases, the numerator decomposition, denominator estimate, and
  the exact transfer constant
- 63 three-dimensional configurations check the full Kelvin formula with
  80-digit Decimal arithmetic; the largest scaled error is about 3.20e-78
  against a 1e-65 tolerance
- Exact rational checks independently verify the sphere counterexample and
  the Gaussian-rational local complex counterexample
- All 24 numerical rows independently replay, including the coordinate ratio,
  smooth squared-residual objective, minimum separation, gauges, and summary
  budget counts

The four minimum observed coordinate ratios are approximately 0.049667825,
0.050117202, 0.036668674, and 0.022455888 for (p,m)=(6,2),(6,3),(7,3),(8,3).
The evaluation-budget exhaustions are respectively 3,5,2,3. These are finite
observations and are not lower bounds. The full optimizer trajectories were
not rerun; independent replay checks their stored outputs only.

The author checker passed normal and optimized Python with all three complete
corpora and all five PDFs supplied, from a relocated authenticated snapshot.
Its 14-case control suite passed. The independent audit checker also passed
normal and optimized Python, relocation, changed-byte, missing-file,
extra-file, symlink, manifest-rebound semantic corruption, duplicate-key,
nonfinite-JSON, empty-manifest, author-ZIP-bit-flip, full-corpus-bit-flip, and
source-PDF-bit-flip controls. See the machine-readable result files.

These checks fail closed for their tested corruptions. They are not a formal
proof checker, a general verifier for arbitrary altered prose, or protection
against an attacker who can replace both executable code and the externally
trusted archive hash. The external receipt authenticates the concrete freeze;
an internal manifest alone does not.

## Optional improvements and remaining work

No mandatory correction is requested. The following are nonblocking editorial
or tooling improvements for a future author revision:

1. Label the Kelvin citation explicitly as arXiv Proposition 2.3 / journal
   Proposition 2.4. Both sources are already listed, but their numbering differs.
2. In the numerical discussion, say "smooth nonnegative squared-residual
   objective on the valid domain". The residual vector itself has signed
   entries, and the invalid-input penalty is not a global smooth extension.
3. If the exploratory search is extended, preserve a computed zero as a
   candidate needing rigorous validation instead of aborting because the
   reported floating-point ratio is not strictly positive. This does not
   affect the 24 authenticated positive stored results or any accepted proof.

The unresolved mathematical task is unchanged: exclude or construct a planar,
mixed-sign, full-support six-point zero configuration, and more generally
settle arbitrary active support sizes. The numerical experiments and the
local literature counterexamples do not settle it. Current literature searches
found the published partial result and the older manuscript, with no later
full proof located; this search is bounded and carries no novelty guarantee.

## Public sources

[S1] Thomas Bartsch and Andrew Dancer, organizers. Topological and Variational
Methods for Differential Equations. Oberwolfach Reports 2 (2005), 1601-1678.
Published 2006-06-30; Bahri contribution at 1658-1660.
https://ems.press/journals/owr/articles/1050
https://ems.press/content/serial-article-files/46004

[S2] Yongzhong Xu. Note on an inequality. Annales de l'Institut Henri Poincare
C 23 (2006), 629-639.
https://ems.press/journals/aihpc/articles/4077561
https://www.numdam.org/article/AIHPC_2006__23_5_629_0.pdf

[S3] Hong Chen, Jianquan Ge, Kai Jia, Zhiqin Lu. On a Conjecture of Bahri-Xu.
Acta Mathematica Sinica, English Series 37 (2021), 1721-1742.
https://doi.org/10.1007/s10114-021-0027-0
https://arxiv.org/abs/2101.10023
https://lu.math.uci.edu/pdfs/publications/2021-2025/66.pdf
https://actamath.cjoe.ac.cn/Jwk_sxxb_en/EN/lexeme/showArticleByLexeme.do?articleID=23863

[S4] Shiwei Lan and Zhiqin Lu. On a Conjecture of Bahri-Xu.
Author-hosted 13-page manuscript internally dated 2011-03-09.
https://lu.math.uci.edu/pdfs/publications/other-papers/barhi-5.pdf

Publication-list cross-check: https://lu.math.uci.edu/publications/
