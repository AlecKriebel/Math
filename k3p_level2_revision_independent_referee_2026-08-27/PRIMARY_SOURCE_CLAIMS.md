# Fresh primary-source claim restatement

This restatement was made after reading the revised article and reader
supplement completely and before relying on stored reports or running package
verifiers.

## The theorem class and domains

The objects are binary standard semi-directed phylogenetic networks on one
fixed finite labelled leaf set. The standard convention marks precisely the
reticulation-parent arcs, undirects all other arcs, deletes the binary root,
and merges its two incident arcs in one step. The presentation is admitted
only if that operation creates neither loops nor parallel edges and loses no
reticulation arrowhead. Isomorphisms preserve leaf labels, ordinary edges,
arrowheads, and vertex roles. The classification assumes level at most two and
strong tree-childness: an admissible rooting exists and every admissible
rooting is tree-child.

Every inheritance probability is strictly between zero and one. Every K3P
edge has fixed, observably labelled nonzero Fourier characters `C,G,T` and a
spectrum `(c,g,t)` in the principal domain

`D3,+ = {(c,g,t) in (0,1)^3: 1+c-g-t>0, 1-c+g-t>0,
1-c-g+t>0}`.

The strict continuous-time subdomain additionally satisfies `c>gt`, `g>ct`,
and `t>cg`. Zero/signed eigenvalues, boundary transition probabilities,
inheritance values zero or one, untransported permutations of `C,G,T`,
nonbinary/higher-level networks, and arbitrary weakly tree-child networks are
outside scope.

## Principal-domain classification

For two networks `N,N'` in that class, a directed relation `N <= N'` means
that at a regular source point there is a connected source-open neighborhood
of maximal source Jacobian rank and a real-analytic section into the physical
target parameter space on which the two polynomial maps agree. The target
section need not be target-open or target-regular.

Theorem 2.1 claims that this directed physical containment exists if and only
if the labelled reduced trees of blobs agree and every corresponding complete
factor is either a labelled mixed-graph isomorphism or an ordinary triangle
redirection with coherent boundary transport. This structural relation is
also equivalent to a common analytic germ that is regular and
full-dimensional in both images and has physical sections from both sides.
Consequently there is no proper one-sided regular full-dimensional
containment in the strong class. This is not equality of complete stochastic
images and does not identify all numerical parameters.

## Triangle ambiguity

An ordinary triangle redirection changes only which vertex of a three-cycle
factor incident with three external arms is reticulate and redirects its two
incoming arrowheads. The three labelled orientations are claimed to have
normalized generic rank 14 in the ambient 15-dimensional three-leaf Fourier
chart, the same irreducible eight-term quartic closure `H14`, and one common
strict-continuous-time smooth rank-14 germ relative to that hypersurface. They
do not have an ambient-open 15-dimensional common germ, and representatives
of one triangle class need not have identical complete physical images.

## Generic identifiability and exact reconstruction

For each fixed topology `N`, theorem 2.2 claims a proper complex
Zariski-closed exceptional subset `E_N` of the irreducible image closure such
that any exact physical tensor in the image but outside `E_N` determines the
labelled standard semi-directed topology uniquely modulo ordinary triangle
redirection.

Theorem 2.3 claims a terminating exact reconstruction procedure outside the
same exceptional set. Its input is an exact-real representation supporting
field operations, polynomial-sign decisions, and real-closed-field quantifier
elimination. It gives no bit-complexity, conditioning, finite-sample,
sequence-length, or practical-estimation guarantee and reconstructs topology,
not all edge parameters.

## Strict continuous time

Corollary 2.4 asserts the same containment equivalence, no-proper-containment
conclusion, generic structural identifiability, and exact reconstruction after
restricting every edge to the strict continuous-time cone. No equality case
of a continuous-time inequality is included.

## Sharpness and outer obstruction

Theorem 2.5 claims that for every `n>=3` there are two binary level-2 standard
semi-directed networks that are weakly but not strongly tree-child, are
neither labelled-isomorphic nor ordinary-triangle equivalent, and whose
strict-continuous-time K3P images share a common regular germ
full-dimensional in both images of dimension `6n-3`. At `n=3`, both maps have
rank 15 throughout a certified rational box containing one unique common
root only in the selected 15-variable equality slice. Identical labelled
cherry substitution is claimed to add exactly six observable dimensions at
each step. This proves only that replacing strong by weak tree-childness makes
the classification false, not that every weak network is ambiguous.

Proposition 2.6 separately claims proper containment of a rank-9 three-leaf
tree germ in a rank-15 level-2 double-theta image near a strict
continuous-time point. The theta network is outside even the weakly
tree-child class; it is not the sharp class-boundary example.

## Finite machine-dependent boundaries

The proof depends on exact finite classifications for directed cut transfer,
four-port relations, restoration, coherent probes, triangle algebra, global
gluing infrastructure, and weak-class sharpness. The revised papers claim an
active producer and separately implemented verifier for the entire 405,216
four-port universe, and a separately implemented semantic replay for every
one- and two-port probe row. Those claims, all stored `PASS` values, checksums,
mutation outcomes, and independence descriptions remain unverified at this
stage.
