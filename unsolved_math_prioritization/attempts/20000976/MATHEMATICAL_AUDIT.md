# Independent audit: periodic sandpile partial decision

Problem 20000976 / AIM-COMBINATORICS-0101. Audit date: 2026-10-10.

## Verdict

**Accepted as rigorous partial progress. No blocking mathematical error found.**

The accepted theorem is an exact decision on periodic backgrounds taking only
heights 2 and 3: explosion occurs exactly when every row and every column has a
3. The one-direction deficient-line certificate, explicit source bound,
periodic-Laplacian certificate extension, and periodic infinite-avalanche example
are valid. The proof does not resolve the original four-height decision problem.
No originality or exhaustive literature claim is accepted or required.

The distributed [mathematical report](MATHEMATICAL_REPORT.md) is 12,940 bytes,
SHA-256 `3093769ff3a0fa12f86dbf343b1c4092ddfe03f0f90b5380ab08d713bd033768`.
Its analytic arguments and qualifications are preserved in full. This
AI-assisted, unrefereed audit is not external human peer review, journal
acceptance or formal proof-assistant certification.

## 1. Stabilization and least action

The proof uses the correct pointwise notion of finite toppling counts. A
stabilizing comparison function must be a nonnegative, finite-valued integer
function, but its support and sum need not be finite. The formal configuration
obtained by applying its Laplacian need only be at most 3; it need not be
nonnegative and the proposed topplings need not be legal.

The first-violation argument is valid. Immediately before a proposed first
violation at z, the legal count agrees with the comparison function at z and
is no larger at every neighbor. The current height at z is therefore at most
3. This contradicts the condition for a legal toppling. The argument examines
only z and its four neighbors, so no infinite summation is hidden.

A fair sequential procedure exists, for example by visiting larger finite
sets in rounds. A pointwise comparison bound makes every site's count finite.
The count at a site and all four neighbors eventually stops changing; an
unstable limiting height would contradict fairness. Thus the procedure has a
stable limit. This justifies the sufficient direction of least action rather
than assuming stabilization beforehand. The actual legal limit remains
nonnegative even if the formal comparison configuration has negative heights.

If a legal sequence topples every site, any hypothetical stabilizing odometer
u must be at least one everywhere. Subtracting the harmonic constant one gives
a smaller nonnegative stabilizing function, contradicting least action. The
sequence establishing this fact need not itself be fair. Fairness is needed
only for the subsequent assertion that nonstabilization forces infinitely many
topplings at each vertex. That assertion is correct by connectedness and
unbounded receipt of chips from an infinitely toppling neighbor.

## 2. One-direction tent barrier

For q≥1, 0≤r<q, and t congruent to 2r modulo q with 0≤t<q, the endpoints

a_j=r−jq,  b_j=t−a_j

satisfy a_j<0≤t<b_j and a_j≡b_j≡r modulo q. The positive endpoints are
pairwise distinct, including across the left and right families. The height
function given in the proof rises to −a_j on [a_j,0], stays at that value on
[0,t], falls to zero on [t,b_j], and vanishes outside the interval.

Its discrete first difference changes by +1 at each endpoint and by −1 at
0 and t. This proves the stated second-difference identity. If t=0, the two
negative changes coincide and contribute −2. Neither an even source size nor
an endpoint at a particular representative of the deficient row is required.

Summing n tents gives Laplacian at most +1 on the deficient lines and at most
zero elsewhere. At y=0 it is at most −n, which absorbs the full source at the
origin. Negative Laplacian also acts at all other x-coordinates on these rows;
this is harmless because an upper certificate has no lower final-height
constraint. The pointwise bound is exactly the sum of the plateau heights,
q n(n+1)/2−nr. The exterior of the outermost strip has comparison value zero,
so the actual odometer vanishes there.

Consequently one periodic family of deficient rows OR one family of deficient
columns is enough for pointwise stabilization of every finite source size.
It does not establish a finite toppled set. In particular, the proof correctly
does not apply the stronger finite-growth conclusion of a surrounding-box
criterion to a single strip barrier.

## 3. Explosive seed and face propagation

With a=ceil((P−1)/2), b=ceil((Q−1)/2), and D=a+b, the rectangle
[−a,a]×[−b,b] contains at least P consecutive x-coordinates and Q consecutive
y-coordinates. The exponent D−|x|−|y| is nonnegative throughout it.

The proposed source 4^(D+1) supplies the origin's scheduled 4^D topplings.
Every other seed vertex has a predecessor one step closer to the origin
inside the rectangle. That predecessor sends four times the later vertex's scheduled number
of topplings, hence exactly enough chips for its whole batch. More precisely,
it sends 4^(D−d+1) chips, while the later vertex's whole batch consumes
4·4^(D−d) chips. No previous toppling at the later vertex has spent these
chips. Hence every individual toppling of every batch is legal, independent
of any unused background chips or extra arrivals.

The successive outer faces are untoppled before processing. Each has received
at least one chip from its inward neighbor and so has height at least 3,
using the essential lower background bound c≥2. Each vertical face contains
a full y-period and hence a background-3 site; the horizontal argument is
identical. Starting from that unstable site, an ordered walk in each direction
along the face legally topples all face sites once. The enlarged rectangle
preserves the induction invariant. Cycling all four directions exhausts the
grid and therefore proves explosion by Section 1.

This proves the exact numerical upper bound claimed, including degenerate
periods P=1 or Q=1. It is deliberately nonsharp; for example the all-3 cell
already explodes from one added chip. No infinite search for a source size is
needed to compute this upper bound.

The complementary case on {2,3} has a cell row or column with no 3, hence an
entire periodic family of all-2 lines. Section 2 applies. Reading the cell and
marking which rows and columns contain a 3 gives the stated O(PQ) decision.

## 4. Full-rank lattice input

For an integer basis matrix A, let m=|det A| and s=sign(det A). The identity
A(s·adj(A))=mI proves mZ²⊆AZ², with either determinant sign. Thus the original
finite quotient table determines an m×m rectangular cell effectively. This
may enlarge the input substantially, but only decidability is claimed for
this conversion; the O(PQ) statement is about the expanded rectangular cell.
The grid, edge weights, source location, and ambient dimension are unchanged.

## 5. Periodic modifications

If p is periodic integer-valued, p is bounded. Choose K≥−min p. For an upper
modified background b=c+Δp that is at most 3 and at most 2 on one residue
line, the same tents work without any lower bound on b. Their sum w yields
p+K+w≥0 and c+nδ₀+Δ(p+K+w)≤3. The original configuration, rather than the
possibly negative modified one, is the nonnegative input to least action.

The finite feasibility claim is valid. For each candidate deficient row or
column, the periodic Laplacian and upper bounds are finitely many integer
linear inequalities in the PQ integer potential values. Their feasibility is
an existential Presburger question. Additive-constant freedom does not prevent
decidability. For period lengths 1 or 2, the periodic Laplacian must count all
four grid directions with their multiplicities; this is the operator in the
proof.

For two nonnegative backgrounds related by a bounded integer potential, the
forward certificate transfer is w+p+K and the reverse is w−p+K'. Thus every
fixed nonnegative finite source has the same stabilization outcome on the two
backgrounds. Equality of their full one-source threshold sets follows.

The certificate class strictly extends the at-most-2 modified class:
the periodic stripe example has mean 5/2 and is already accepted with p=0,
whereas a periodic Laplacian has zero finite-cell sum and cannot reduce that
mean to at most 2. This uses a finite periodic-cell sum, not an invalid infinite
sum of a nonperiodic odometer.

No exhaustiveness of either certificate family is proved for arbitrary
four-height input. The manuscript states this limitation accurately.

## 6. Periodic infinite avalanche

For c=3 on even rows and c=2 on odd rows, the residue class y=1 modulo 2
provides the strip barrier for every source size. For one chip, the proposed
odometer 1_{y=0} has Laplacian −2 on the central row and +1 on its adjacent
rows. The resulting heights are 2 at the origin, 1 elsewhere on the central
row, 3 on the adjacent rows, and unchanged farther away, all stable.

Toppling the origin and then the alternating outward tips of the central row
is legal. No off-row site becomes unstable. Every central-row site topples,
and least action bounds every count by the proposed indicator. This establishes
the exact odometer, infinitely many total topplings, and no site toppling more
than once. Full-rank periodicity therefore does not identify an infinite
avalanche with explosion.

## 7. Source and scope checks

The model and quantifiers match Levine's [primary problem note](https://www.slmath.org/ckeditor_assets/attachments/278/msri-open-problem.pdf):
full-rank periodic stable input on the standard square grid, a positive scalar
source at the origin, and pointwise infinite toppling as explosion.

[Fey–Levine–Peres](https://arxiv.org/abs/0901.3805) define robustness by a finite
toppled set for every source size and explicitly distinguish infinite avalanches
from explosion. Their Section 2 supports least action; Theorem 4.1 supplies the
known face-propagation mechanism; Theorem 4.2 concerns surrounding deficient
boxes and finite total growth. The weaker pointwise non-explosion property is consistently distinguished
from this finite-growth notion.

[Cairns](https://arxiv.org/abs/1508.00161) proves three-dimensional
undecidability. Neither that dimension nor arbitrary finite perturbations may
be silently replaced by this two-dimensional scalar-source problem.

The report gives an explicit proof and certificate analysis,
not a verified priority claim. The author note's undated availability is not
assigned a publication date from search-engine crawling. No broad current
literature status is inferred merely from the existence of these older sources.

## 8. Supporting audit metadata and acceptance limits

The mathematical acceptance rests on the complete analytic arguments above
and in the distributed report. The audit also recorded these aggregate exact-
integer check totals:

- 2,907 tent cases and 670,833 second-difference comparisons
- 9,418 {2,3} cells, including 4,809 positive and 4,609 negative cases, and
  1,320,741 individually checked legal topplings
- 13,808 full-rank integer basis matrices
- 20,736 background/potential pairs, with 1,421 accepted row certificates,
  including 688 with a negative modified height
- 915 sites checked against the stripe formula and a 201-toppling legal prefix

These are recorded supporting checks, not proofs of infinite-time behavior.
Programs, fixtures and detailed computational outputs are not distributed;
no excluded file is a premise of any mathematical conclusion. Edition
preparation did not rerun the checks. The universal analytic proofs establish
the claims independently of these aggregate observations.

No ILP solver implementation, exhaustive certificate coverage, full four-height
decision procedure, undecidability reduction, or novelty certification was
accepted. No mathematical proof correction is required for the accepted partial
claims. The original four-height decision remains unresolved by this work.
