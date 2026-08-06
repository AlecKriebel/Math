# Sharp identifiability boundary for level-2 Jukes–Cantor networks

## Status

**PROVED.** All claims in this report are under the standard semi-directed
reduction and the open JC parameter domain

\[
0<x_e<1,\qquad 0<\lambda_r<1.
\]

The three tree-child classes are kept distinct:

- \(R_{\rm TC}\): the supplied rooted DAG is tree-child;
- \(W_{\rm TC}\): the standard semi-directed topology has at least one
  tree-child rooted partner;
- \(S_{\rm TC}\): every admissible rooted partner is tree-child.

The network class consists of binary standard semi-directed \(S_{\rm TC}\)
level-2 networks with at most one triangle in each blob.

## Primary theorem

### Theorem A — complete one-sided observational classification

**PROVED.** Let \(N,N'\) be leaf-labelled networks in the stated class. Then

\[
N\preceq_{\rm JC}N'
\]

if and only if their labelled homeomorphism-reduced bridge trees agree and,
under the induced correspondence of ports, every pair of corresponding blobs
is either labelled-isomorphic or differs only by ordinary triangle
redirection \(T\).

Every surviving local relation is in fact a symmetric regular overlap. Thus
ordinary triangle redirection is the complete observational ambiguity in
\(S_{\rm TC}\).

### Corollary B — generic identifiability modulo \(T\)

**PROVED.** For each fixed \(S_{\rm TC}\) topology \(N\), there is a proper
algebraic exceptional set in its parameter space such that every parameter
outside that set is identified by its exact JC distribution up to ordinary
triangle redirection and labelled isomorphism.

### Theorem C — sharpness

**PROVED.** The conclusion fails on replacing \(S_{\rm TC}\) by
\(W_{\rm TC}\). For every \(n\ge 4\), the inherited Theta construction gives
nonisomorphic, non-\(T\)-equivalent networks

\[
N_n,N'_n\in W_{\rm TC}\setminus S_{\rm TC}
\]

whose open JC model images share a full-dimensional regular region. Their
model dimension is \(2n\).

Consequently, the boundary is sharp:

\[
\boxed{
S_{\rm TC}\text{ is generically JC-identifiable modulo }T,
\quad
W_{\rm TC}\text{ is not.}
}
\]

## 1. The final seven-port universe

The inherited conservative completion census contained 192 records with
three additional rigid-support labels. The stale prose field saying that core
3 required at most two additions has been corrected. The explicit
machine-readable distribution had already recorded

\[
(\text{core }3,\,3\text{ additions},\,7\text{ outgoing ports})=192.
\]

A deterministic replay of the weak-presentation indexing reconstructs these
records as eight role patterns, each with all 24 outgoing-label permutations:

| orbit id | selected path-sink? | ordinary port counts on \((UV,SU,SV,UX,VX)\) |
|---:|:---:|:---|
| 629 | no | \((0,0,1,1,2)\) |
| 644 | no | \((0,1,1,2,0)\) |
| 649 | no | \((0,2,0,1,1)\) |
| 650 | no | \((0,2,0,2,0)\) |
| 685 | no | \((2,1,0,1,0)\) |
| 700 | yes | \((0,0,2,0,1)\) |
| 705 | yes | \((0,1,0,2,0)\) |
| 706 | yes | \((0,1,1,0,1)\) |

The directed core has vertices

\[
S:\text{source},\quad U:\text{tree branch},\quad
V:\text{branch reticulation},\quad X:\text{path-sink reticulation},
\]

and segments

\[
U\to V,
\quad S\to U,
\quad S\to V,
\quad U\to X,
\quad V\to X.
\]

Its minimum strong repairs are \(\{UV,VX\}\) and \(\{UX,VX\}\). These
vertex roles make the directed-core automorphism group trivial. Hence the
\(S_4\) action is free on each role pattern, the eight orbits are disjoint,
and all 192 records occur exactly once. The certificate lists every canonical
graph hash.

For the eight canonical representatives, every conservative completion by
labels \(5,6,7\) was enumerated. There are 1,686 distinct completed labelled
mixed graphs. Every one satisfies the standard \(S_{\rm TC}\) tail criterion:
each tail of a retained reticulation arrow has two incident undirected edges.
The complete displayed-tree monomial schema of every completion is hashed in
the certificate.

## 2. Universal three-port separator

For three selected ports \(a,b,c\), put

\[
F_{abc}=r_{ab}r_{ac}r_{bc}-u_{abc}^{2},
\]

where \(r_{ab},r_{ac},r_{bc}\) are the three pair coordinates and
\(u_{abc}\) is the all-distinct zero-sum Fourier coordinate.

For a cycle model with path-sink label \(s\):

\[
F_{abc}=0 \quad\Longleftrightarrow\quad s\notin\{a,b,c\}.
\]

If \(s\in\{a,b,c\}\), the induced three-port cycle has one of two forms.
Exact contraction gives

\[
F=\lambda(1-\lambda)M(1-y)^2>0
\]

when the two ordinary ports lie on one side, and

\[
F=\lambda(1-\lambda)M(1-yz)^2>0
\]

when they lie on opposite sides, where \(M\) is a positive monomial. Thus the
zero/nonzero pattern of the ten three-subsets is exactly a six-edge star
centred at the cycle sink.

### Six orbits separated before completion

**PROVED.** The exact pullbacks on the original four outgoing ports plus the
incoming port give:

- 644, 650, and 685: all ten \(F\)'s vanish;
- 629: target-zero triples containing every possible cycle-sink choice;
- 700 and 706: for each possible cycle sink, a target-positive triple omitting
  that sink.

Hence all 144 labelled records in these six orbits are stochastically disjoint
from the proposed cycle source without using the extra labels.

### The two genuine completion cases

Only 649 and 705 have the cycle-star pattern on the original five ports. It
forces the cycle sink to be old label 4.

For orbit 649, every completion has a newly selected target sink
\(e\in\{5,6,7\}\). On the complete target tensor, marginalize to
\((1,2,e)\). Exact contraction yields

\[
\begin{aligned}
F_{12e}
={}&M_A(1-\lambda_V)(1-\lambda_X)(1-a)^2\\
&\times\left[
\lambda_V(1-\lambda_X)b+
\lambda_Xc
\right] >0,
\end{aligned}
\]

with \(M_A,a,b,c\) positive products of open edge multipliers. The cycle
source has sink 4, so \(F_{12e}=0\) there.

For orbit 705, every strong completion must put at least one new label
\(e\in\{5,6,7\}\) on segment \(V\to X\). Marginalization to \((1,2,e)\)
gives

\[
F_{12e}=M_B\lambda_V(1-\lambda_V)(1-a)^2>0,
\]

while the cycle source again has \(F_{12e}=0\).

The verifier expands both identities from the full seven-port displayed-tree
parameterizations. Extra subdivisions merely replace the displayed symbols by
products in \((0,1)\), so strict positivity is unchanged.

Therefore every one of the 192 residual relations has disjoint complete open
stochastic images. No isolated-point or closure-only argument is used.

## 3. Exact local dimensions

For the lifted incoming-port parameterizations used in the seven-port
certificate, the root lies outside the local factor, its two root edges are
ordinary, and the three-edge neighborhoods of distinct reticulations are
disjoint.  Such a binary rooted parameterization on \(n\) observed boundary
leaves with \(r\) reticulations has

\[
E=2n+3r-2
\]

edges and \(E+r\) raw JC parameters.  Its Fourier parameterization has one
root-split gauge and two independent gauges per reticulation.

Indeed, if a reticulation has incoming multipliers \(a,b\), outgoing
multiplier \(c\), inheritance \(\lambda\), and descendant character sum
\(h\), then:

- when \(h=0\), switching the selected parent changes upstream descendant
  sets only by a zero character sum, so the two contributions combine with
  weight \(\lambda+(1-\lambda)=1\);
- when \(h\ne0\), the local coefficients are exactly
  \(\lambda ac\) and \((1-\lambda)bc\).

Thus four local raw parameters enter through two combinations. Consequently

\[
\dim V\le E+r-(1+2r)=2n+2r-3.
\]

For seven outgoing ports plus the incoming port, \(n=8\). Hence

\[
\dim V_{\rm cycle}=15,
\qquad
\dim V_{\rm core3}=17.
\]

The certificate supplies a nonzero exact Jacobian minor modulo the prime
1,000,003 for every one of the seven cycle side-count vectors and all 65
core-3 count vectors occurring among the 1,686 completions. An independent
implementation re-evaluates every stored minor. These lower bounds meet the
structural upper bounds exactly.

The dimension difference does not by itself rule out cycle-to-theta
containment. The strict \(F\) separators do.

## 4. Arbitrary-subdivision promotion

**PROVED.** The bounded-support reconstruction theorem supplies, in every
arbitrarily subdivided local factor:

1. a rigid support containing the path-sink children and one port on each
   segment of a minimum strong repair;
2. one-port probes locating every remaining port's directed segment;
3. two-port probes recovering the order of every pair on a segment.

For cycle factors the corresponding support consists of the sink child and
one side anchor, with one- and two-port probes recovering the two ordered
sides.

If an arbitrary cycle source were one-sided contained in a theta target, its
bounded restrictions would enter the completed cycle/theta atlas. All cases
through six outgoing ports were already closed; the only omitted completion
was precisely the 192-record core-3 universe above. Since all 192 now have a
strict open-domain separator, no cross-generator containment survives.

The canonical bounded decks use every ordered four-port restriction of the
complete joint boundary tensor: \(6P4=360\) features at five outgoing ports
and \(7P4=840\) at six.  Consequently the computational choice of an incoming
port is auxiliary.  Rerooting or changing that auxiliary designation merely
permutes the full joint-tensor coordinates, and the all-relative-labelling
atlas transports with that permutation.

The previously completed theta/theta, cycle/cycle, and theta-source/cycle-
target directions, together with ordered-word reconstruction, therefore give:

### Nonroot local theorem

**PROVED.** For arbitrary finite port-labelled nonroot \(S_{\rm TC}\) level-2
cycle or theta factors with at most one triangle,

\[
B\preceq_{\rm JC}B'
\]

occurs exactly when \(B,B'\) are port-labelled isomorphic or related by
ordinary triangle redirection \(T\).

## 5. Root reduction

**PROVED.** In any tree-child rooted partner, start at the root and repeatedly
choose a tree-or-leaf child. Acyclic finiteness produces a root-to-leaf path
containing only ordinary tree vertices and the terminal leaf.

Suppress the old root, reverse the ordinary edges on this path, and insert a
new root on the terminal pendant edge. Binary degrees are preserved,
reticulation arrowheads are unchanged, and no directed cycle is created. The
new rooting is admissible; because the topology lies in \(S_{\rm TC}\), it is
tree-child. Standard reduction forgets the reversed ordinary directions and
therefore returns the identical semi-directed topology.

For JC, uniform stationarity and reversibility make every displayed-tree
distribution root-independent.  There is one directed-edge case worth making
explicit.  If the old root's off-path child is a reticulation, then in a
switching selecting that parent the two old root-arm multipliers occur only
through their product.  In a switching selecting the other parent, the
remaining one-child root stem subtends all leaves, has total character zero,
and contributes exponent zero.  Thus suppression again gives exactly one
effective retained-edge multiplier.

If relocation splits any effective multiplier \(x\), choose

\[
y=\frac{1+x}{2},
\qquad
z=\frac{2x}{1+x}.
\]

Then \(0<y,z<1\) and \(yz=x\).  Conversely, multiplying the two old root
arms produces an open effective multiplier, so the two root placements have
the same complete JC image germ.

The resulting boundary tensor is a joint tensor; which boundary was used as
the computational incoming port is not observed.  By the all-ordered-port
covariance of the bounded atlas, every root-local factor is therefore covered
by the nonroot local theorem even when two compared topologies use different
admissible pendant root sites.

## 6. Pointwise cut preservation

The frozen pointwise certificate contains 177 canonical three-boundary
endpoint tensor types. Every type obeys exactly one branch:

\[
abc-t^2>0
\]

for 151 types, or

\[
abc-t^2=0,
\qquad
a-bc>0
\]

for 26 types.

For a crossing contained in one active local factor, the complete four-port
universe has 453 types. Of these, 421 possess a fixed-sign wrong-split minor;
the remaining 32 have all wrong-split blocks rank one and contain the tested
bridge in every switching.

For a bridge joining two active endpoint tensors, write their coordinates as
\((a,b,c,t)\), \((A,B,C,T)\), and the bridge multiplier as \(z\in(0,1)\).
Four exact wrong-split minors are

\[
\begin{aligned}
m_0&=aA-bcBCz^2,\\
m_1&=(aA-Ttz)(aA+Ttz),\\
m_2&=aA^2-bcT^2z^2,\\
m_3&=a^2A-t^2BCz^2.
\end{aligned}
\]

Rank one would imply

\[
abc=t^2,
\qquad
ABC=T^2,
\qquad
aA=bcBCz^2.
\]

The endpoint dichotomy then gives \(a>bc\) and \(A>BC\), so
\(aA>bcBC\); the third equation and \(z<1\) give \(aA<bcBC\), a
contradiction.

Hence, throughout the open JC domain, a flattening has rank at most four
exactly at a cut split. One-sided open containment therefore preserves cuts in
both directions: a cut on one side and non-cut on the other would require the
same common distribution to have flattening rank both at most and greater
than four. The labelled bridge trees agree.

## 7. Global synthesis

Recover the common bridge tree and peel its Fourier rank-one blocks. This
extracts every local tensor up to one positive reciprocal JC gauge per bridge.
The audited local invariants are multihomogeneous in the port arms, so these
gauges preserve their zero and sign tests.

Fix positive anchor entries in every rank-one cut block.  They give an
analytic gauge slice in which a regular source model germ is a Cartesian
product of its local tensor germs and open bridge parameters.  The same
factorization describes the target set; it does not require a regular target
preimage.  If a source-relative product box lies in the target model, then
projection of that box to each coordinate factor is a source-relative open
one-sided containment of the corresponding local model.  Root reduction and
the nonroot local theorem therefore force every local pair to be isomorphic
or \(T\)-related.

Conversely, an ordinary triangle in a valid standard \(S_{\rm TC}\) factor has
one reticulation and three always-present ordinary external arms.  Cutting
beyond those arms factors the network map through the same normalized
four-dimensional three-boundary tensor space for all three orientations.  The
certified common regular \(T\) germ and the positive gluing inverse therefore
survive contraction with any unchanged context, including a context that
reconnects two arms inside the same level-2 blob.  Hence any two already-valid
global endpoints differing only by local \(T\) redirections have a common
full-dimensional regular region.

This proves Theorem A.

## 8. Canonical reconstruction

For a generic exact distribution known to arise from the class:

1. Fourier-transform the distribution.
2. Test all nontrivial splits by rank-at-most-four flattenings and reconstruct
   the labelled reduced bridge tree.
3. Factor each Fourier cut block into positive rank-one factors and peel the
   tree, obtaining projective local tensors.
4. On every local tensor, inspect bounded restrictions through seven outgoing
   ports. Use the exact cycle/theta invariant atlas and the new \(F\)
   separators to determine the generator, repair support, and port roles
   modulo \(T\).
5. Use one-port and two-port probes to reconstruct every ordered segment word.
6. Reroot through an ordinary pendant path and choose the lexicographically
   least standard mixed-graph encoding among the valid \(T\)-orientations.

The procedure terminates because the split set and every bounded restriction
deck are finite. It returns exactly the canonical observational-equivalence
class. All compatible semi-directed topologies are obtained by enumerating
valid ordinary \(T\) redirections and deduplicating their labelled canonical
codes; no non-\(T\) topology can occur by Theorem A.

The exceptional set is the finite union of:

- proper rank/minor degeneracy varieties used by bridge and local extraction;
- proper local invariant-degeneracy varieties;
- Zariski closures of intersections with non-\(T\) topologies.

If one such intersection had full source dimension, semialgebraic
stratification would produce \(N\preceq_{\rm JC}N'\), contradicting Theorem A.
There are only finitely many fixed-leaf binary \(S_{\rm TC}\) level-2
networks, so the union is proper. Dominance of the parameterization pulls it
back to a proper algebraic subset of source parameter space.

## 9. Independent release checks

The primary seven-port implementation and a separately written reviewer agree
on all 192 residual records, eight free \(S_4\)-orbits, 1,686 canonical
standard-\(S_{\rm TC}\) completions, seven cycle rank certificates, and 65
theta rank certificates.  The reviewer independently reconstructs every
mixed-graph code, every complete displayed-tree monomial schema, and all 486
universal reduced witness tensors in the two genuine completion orbits.

A separate cut reviewer recomputes 547 distinct tensor-product Bernstein
expansions, all 177 endpoint signs, all 421 strict wrong-split minor signs, all
32 true-bridge signatures, the seven partial-Bernstein certificates, and the
four two-active-endpoint identities.  A separate root reviewer checks 294,132
zero-sum complement identities and the selected/unselected retained-
reticulation cases.  The final release verifier reruns these independent
programs, checks every dependency hash, and refuses to certify this report if
any theorem dependency is missing or carries an unresolved status.

## Biological consequence

Under exact infinite-data JC observations, the standard strong tree-child
condition is sufficient to recover the complete level-2 history—including its
bridge tree, blob generator types, and labelled descendant placements—except
for the local direction of an ordinary embedded triangle. This remaining
uncertainty is intrinsic: all three triangle directions share a regular JC
tensor neighborhood.

The condition is sharp. Merely requiring that *some* rooting be tree-child
allows the Theta pendant-transfer ambiguity, which changes the labelled
semi-directed history and persists for arbitrarily many leaves.
