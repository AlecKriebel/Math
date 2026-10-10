# A complete decision on the periodic {2,3} subclass

Problem 20000976 / AIM-COMBINATORICS-0101. Accepted partial result, attempt 1/5.

## Result and scope

The general decision problem for stable periodic backgrounds with heights in
{0,1,2,3} is **not resolved here**. The exact partial result is:

**Theorem.** Let c:Z²→{2,3} have rectangular periods P,Q. Then some finite
addition at the origin explodes if and only if every horizontal row and every
vertical column contains a site of height 3. Equivalently, the finite P×Q cell
has a 3 in every row and column. This is a terminating decision algorithm on
this subclass, taking O(PQ) time after the cell has been read.

The explosion implication is the known Fey–Levine–Peres face criterion. The
non-explosion implication below uses an explicit one-direction barrier
certificate. It requires only one periodic family of entirely deficient rows
OR columns, and it applies to all stable heights, not just {2,3}. We do not
claim literature novelty for this elementary consequence of least action.

An explicit (deliberately generous) threshold upper bound on the explosive
subclass is

    N(c) ≤ 4^(ceil((P−1)/2) + ceil((Q−1)/2) + 1).

The proof also gives a larger, decidable finite certificate class obtained by
periodic integer-Laplacian modification. Neither that class nor the {2,3}
subclass is asserted to exhaust the original problem.

## 1. Model and the stabilization lemma

Use Δu(x,y)=u(x+1,y)+u(x−1,y)+u(x,y+1)+u(x,y−1)−4u(x,y).
A legal toppling requires height at least 4. All initial configurations here
are nonnegative, and a fair procedure eventually topples every unstable site.
“Stabilizable” means that every site's total toppling count is finite. It
does not mean that there are finitely many topplings in total.

For such an initial configuration η, the following least-action form holds:

    η stabilizes ⇔ there is w:Z²→Z≥0 with η+Δw≤3.

Here w is finite at every site but need not have finite support or be a legal
toppling count. For completeness, every finite prefix v of a legal procedure
satisfies v≤w: at the first attempted violation at z, one has v(z)=w(z) and
v(t)≤w(t) for all neighbors t, so η(z)+Δv(z)≤η(z)+Δw(z)≤3, contradicting
legality. A fair procedure is therefore bounded at every site by w, and its
limit is stable. Conversely its odometer is itself such a w. The same argument
shows that the odometer u is the pointwise least nonnegative stabilizing
function.

In particular, a legal procedure that topples every site at least once proves
nonstabilizability. Otherwise its odometer u is everywhere at least one;
u−1 is another nonnegative stabilizing function since Δ1=0, contradicting
minimality. For a fair procedure, nonstabilizability means that some vertex
topples infinitely often. On the connected square grid an infinitely
toppling vertex forces each neighbor to topple infinitely often: otherwise
that neighbor receives infinitely many chips after its last toppling and
fairness is contradicted. Hence every vertex topples infinitely often.

These facts agree with FLP, Section 2, especially Lemmas 2.1–2.3. This
argument does not sum an infinite Laplacian or assume finite total mass.

## 2. Explicit one-direction barriers

**Lemma.** Suppose c:Z²→{0,1,2,3} and, for some integers q≥1 and 0≤r<q,

    c(x,y)≤2 whenever y≡r (mod q), for every x.

Then c+nδ₀ stabilizes for every positive integer n. In fact its odometer is
bounded by a nonnegative integer function supported on a finite-width
horizontal strip. The transposed statement holds for columns.

**Proof.** Set t to the representative of 2r modulo q in {0,…,q−1}.
For j=1,…,n put

    a_j = r−jq < 0,       b_j = t−a_j > 0,
    h_j(y) = max(0, min(y−a_j, b_j−y, −a_j)),
    w(x,y) = Σ[j=1..n] h_j(y).

The graph of h_j rises with slope 1 from a_j to 0, is constant on [0,t],
falls with slope −1 from t to b_j, and vanishes outside [a_j,b_j].
Its integer second difference is exactly

    h_j(y−1)+h_j(y+1)−2h_j(y)
      = 1[y=a_j]+1[y=b_j]−1[y=0]−1[y=t].

This formula includes t=0, when the two negative terms coincide. Both a_j
and b_j are congruent to r modulo q. All 2n positive endpoints are distinct:
the a_j are distinct and negative, while the b_j are distinct and positive.
Because w is independent of x, its two horizontal terms cancel in Δw.
Consequently Δw≤1 on the deficient lines, Δw≤0 everywhere else, and
Δw(x,0)≤−n. Thus

    c+nδ₀+Δw≤3

at every site, including the origin. Least action proves the lemma. More
quantitatively,

    0≤u(x,y)≤w(x,y)≤q n(n+1)/2−nr,
    u(x,y)=0 if y<a_n or y>b_n.

The certificate has infinite support in x; no finite-total-toppling claim
has been made. ∎

## 3. The converse on {2,3}, with an explicit source bound

Assume c:Z²→{2,3} is P×Q periodic and its cell has a 3 in each row and
column. Put

    a=ceil((P−1)/2),  b=ceil((Q−1)/2),  D=a+b,
    R=[−a,a]×[−b,b],  n=4^(D+1).

First perform the following finite legal schedule, toppling only inside R.
Process vertices z∈R in nondecreasing distance d(z)=|z₁|+|z₂| from the
origin, and topple z exactly 4^(D−d(z)) times consecutively. The origin can
do this because the added n chips alone suffice. Every other vertex has a
neighbor of distance d(z)−1 in R. That neighbor was processed earlier and
sent it 4^(D−d(z)+1) chips. Since z has not previously toppled, these chips
alone suffice for all its scheduled topplings. Every scheduled toppling is
legal. At the end every vertex of R has toppled at least once and no vertex
outside R has toppled.

Now repeatedly expand the current rectangle by its right, top, left and
bottom outer faces, one face at a time. Each outer-face site has at least
one already-toppled inward neighbor, so its current height is at least 3.
Every vertical face contains at least Q consecutive y-coordinates, and the
fixed x-residue has a height-3 site somewhere in a Q-period. Hence that face
has at least one site with current height at least 4. The same reasoning
uses P on horizontal faces. Start at such a site and topple sites of the
face once each, spreading consecutively in both directions along the face.
Each next site already has height at least 3 and receives one chip from
the preceding face site, so each toppling is legal.

No site on the face was toppled earlier. After processing the face, the
enlarged rectangle has every site toppled and all sites outside it still
untoppled. This proves the induction invariant. Cycling the four directions
exhausts Z², so every site topples at least once. Section 1 proves explosion.

This is the same face-propagation argument as FLP Theorem 4.1, with a
separate elementary finite seed schedule replacing the constant-background
growth input. It proves the stated threshold bound without having to run
an unbounded source-size search.

If instead some cell row lacks a 3, the whole corresponding periodic family
of rows consists of 2s, and Section 2 proves non-explosion. A missing cell
column is handled by transposition. These are the complementary cases, so
the theorem and the terminating {2,3} decision follow. ∎

## 4. Full-rank lattice input

The original input need not supply rectangular periods. If the supplied
full-rank lattice has integer basis matrix A and m=|det A|, then mZ²⊂AZ²
by the adjugate identity. Thus P=Q=m is an effectively computable rectangular
period pair, and the original finite quotient table determines this expanded
cell exactly. More economical rectangular periods can be used if known.
No change of graph, edge weights, dimension, or perturbation is involved.

## 5. A finite enlarged certificate class

Let p be an integer-valued P×Q-periodic function. It is bounded, and adding
a constant makes it nonnegative without changing Δp. If the finite cell
satisfies

    b=c+Δp≤3 everywhere,
    b≤2 on one entire residue row or one entire residue column,

then c is non-explosive. Indeed, the Section 2 construction works for b
using only these upper bounds; b itself need not be nonnegative. If w is
its constructed certificate, p+K+w≥0 for a sufficiently large constant K,
and

    c+nδ₀+Δ(p+K+w)=b+nδ₀+Δw≤3.

For each choice of residue row or column this is a finite system of linear
integer inequalities in the PQ entries of p. Its feasibility is decidable
(equivalently, it is an existential Presburger formula). Thus the disjunction
over the P+Q choices is a decidable sufficient certificate. It contains the
certificate c+Δp≤2 everywhere, and also examples of mean height
strictly greater than 2, which that at-most-2 certificate cannot admit.

For precision, bounded-potential invariance holds: if
c′=c+Δp, p is bounded integer-valued, and c,c′ are nonnegative, then for
each fixed finite source ξ, c+ξ stabilizes iff c′+ξ stabilizes. To transfer
a certificate w from c′ to c, use w+p+K≥0. In the reverse direction use
w−p+K′≥0. Therefore the complete source threshold set is unchanged.

If, in addition, a feasible modification b takes values in {2,3}, the
classification above decides c as well. Whether suitable certificates
exhaust arbitrary periodic input has not been proved.

## 6. A fully periodic infinite avalanche that does not explode

Let c(x,y)=3 for even y and c(x,y)=2 for odd y. This is full-rank periodic
with P=1,Q=2. Section 2 proves non-explosion for every finite n, despite its
mean height 5/2.

For n=1, the exact odometer is

    u(x,y)=1 if y=0, and 0 otherwise.

To see legality, topple the origin and then successively the two neighboring
sites along the row, continuing outward. Each row site of initial height 3
receives a chip from an already toppled neighbor. No other row becomes
unstable. The proposed u is a stabilizing upper bound: Δu is −2 on y=0,
+1 on y=±1, and zero elsewhere. Hence its final heights are 2 at the origin,
1 elsewhere on y=0, 3 on y=±1, and unchanged elsewhere. Least action and
the legal propagation give exactly the stated odometer.

There are infinitely many total topplings, but each individual site topples
at most once. This example rules out an attempted inference that full-rank
periodicity makes “infinite avalanche” equivalent to “explosion.”
FLP use “robust” for finite total/toppled-set growth for every n. That is
stronger than non-explosion. This report consistently says “non-explosive”
or “pointwise stabilizable” for the weaker property.

## 7. Remaining gap and acceptance limits

The general input allows both low sites (heights 0 or 1) and sites at height
3 in every row and column. The face proof then fails because an outer-face
site may not reach height 3 after one inward toppling. The one-direction
certificate may fail because there is no entire deficient row or column.
No theorem here establishes that a bounded periodic modification removes
these obstructions. In particular, the two certificates are not treated as
complementary on arbitrary input.

This is not a terminating algorithm for the original four-height problem,
and it is not an undecidability proof. No reduction to a finite torus with
the one-source perturbation has been assumed. Density alone is not used as
a classifier. Three-dimensional periodic-plus-finite undecidability is not
transferred to dimension two.

## Sources and provenance

1. Lionel Levine, *Open problem: Is there an algorithm to decide whether a
   periodic sandpile in Z² is explosive?*, undated author note:
   https://www.slmath.org/ckeditor_assets/attachments/278/msri-open-problem.pdf
   The note fixes the exact full-rank periodic, scalar-origin problem.
2. Anne Fey, Lionel Levine and Yuval Peres, *Growth rates and explosions in
   sandpiles*, J. Stat. Phys. 138 (2010), 143–159; arXiv:0901.3805v2 (2009):
   https://arxiv.org/abs/0901.3805
   Least action is Section 2; the explosion face criterion is Theorem 4.1;
   Theorem 4.2 concerns surrounding deficient boxes and finite total growth.
3. Hannah Cairns, *Some halting problems for abelian sandpiles are undecidable
   in dimension three*, arXiv:1508.00161v2, 24 March 2021:
   https://arxiv.org/abs/1508.00161
   Its dimension-three theorem does not establish the original decision.
4. Original AIM workshop problem 11:
   https://aimath.org/pastworkshops/chipfiringproblems.pdf

Recorded primary-source checks are dated 2026-10-10. The date a search
engine crawled an undated note is not a publication date. Public-source
identities, inspection observations and their limits are recorded in
[SOURCE_METADATA.json](SOURCE_METADATA.json). This AI-assisted, unrefereed
report makes no historical novelty or comprehensive current-literature
claim. The proofs are self-contained apart from the explicit mathematical
background and credited public references; no copied source document or
supplemental computation is required to assess them.
