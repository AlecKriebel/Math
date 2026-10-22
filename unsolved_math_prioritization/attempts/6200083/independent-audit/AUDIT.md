# Independent adversarial audit: 6200083 / AMR-061-0083

Audit date: October 4, 2026 (UTC). Queue rank: 647.

## Verdict and limits

**PASS for the partial obstruction results and the unsolved disposition, with
nonblocking editorial corrections. No solution of the full target is certified.**

The frozen eight-file analysis establishes a connected-limit-set obstruction to
a universal equivariant boundary-extension proof and to a universal
geometrical-finiteness reduction. The counterexample controls refute specific
shortcuts, not local connectedness itself. The target remains unsolved in this
attempt; the five substantive approaches and subjective 5% estimate are retained.
This audit is validation of those five approaches, not an additional search turn.

The audit independently recomputed every frozen file hash, compared all archive
members, replayed 5,859 author assertions, independently implemented 13,323 exact
finite checks, and freshly downloaded all six cited PDFs. Every newly downloaded
PDF matched its recorded byte count and SHA-256. Relevant theorem statements,
definitions, and proof dependencies were inspected. Long external source proofs
were not reconstructed or formally verified. Dataset corpus hashes and live
repository gates are preserved author metadata, not independently rechecked here.
There was no remote write, external outreach, or change to the frozen author files.

## 1. Identity, exact target, and theorem scope

The freshly retrieved author-hosted primary list labels the question Problem 83
on printed page 21 and gives the inspected revision date as October 24, 2007.
The 2005 date is workshop provenance. Its question concerns a finitely generated
discrete isometry group of a Gromov-hyperbolic space, assuming a connected limit
set and asking for local connectedness. The isolated sentence does not add
quasiconvexity, cocompactness, relative hyperbolicity, or a dimension restriction.
The earlier local-compactness convention appears in the CAT(0) discussion. The
packet prudently avoids using an ambiguity about that convention to claim a
counterexample. [Kapovich primary list](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf)

The confirmed positive results stay within their actual domains:

- Mj's Theorem 8.9 covers finitely generated Kleinian groups with connected limit
  sets in the hyperbolic-three-space setting. It does not establish the same
  assertion for arbitrary hyperbolic spaces. The publisher record and printed
  page 76 agree. [Mj, Annals 179 (2014)](https://annals.math.princeton.edu/2014/179-1/p01)
- Dasgupta–Hruska's Theorem 1.1 covers connected Bowditch boundaries of relatively
  hyperbolic pairs. The v2 manuscript removes the older peripheral restrictions;
  it does not identify every orbit limit set with such a boundary. The source's
  boundary conventions and uniqueness are in Definition 2.6. [Dasgupta–Hruska,
  v2](https://arxiv.org/abs/2204.02463v2)

Neither positive theorem subsumes the arbitrary-space target. No exhaustive
current-literature or priority certification is supplied by this audit.

## 2. Matsuda–Oguni specialization: accepted

Theorem 1.1 expressly yields a hyperbolic overgroup in the empty-peripheral case
and forbids every continuous equivariant boundary map. This is stronger than
only forbidding injectivity or an already chosen extension. The source's own
sentence immediately after the theorem confirms that the empty collection stays
empty. A closed orientable surface group of genus at least two is a valid
non-elementary hyperbolic input. [Matsuda–Oguni, v1](https://arxiv.org/abs/1206.5868v1)

Call that input H and the resulting overgroup K. K is an ordinary finitely
generated hyperbolic group, so a Cayley graph X for a finite generating set is
proper, geodesic, hyperbolic, and locally finite. The injection is used as an
actual subgroup inclusion. Left translations are isometries. Their orbit at the
identity vertex has finite intersection with every bounded ball. An open
identity neighborhood in Isom(X) requiring displacement of that vertex less
than 1/2 contains only the identity among these translations. Thus the
restricted H-action is proper and discrete as well as isometric. Nothing in
this step assumes quasiconvexity or a boundary extension.

The free-subgroup Baker–Riley example alone would not establish connectedness.
The packet correctly relies on the surface specialization and the separate
connected-tail argument. Baker–Riley is background and a source-theorem
construction dependency, not an independently reconstructed construction here.

## 3. Connected-tail lemma: accepted

The lemma requires a finitely generated one-ended group H, a proper geodesic
hyperbolic space X, and a proper orbit map. All are satisfied in the application.
The key steps survive the following adversarial checks.

1. Extend the vertex orbit map over every Cayley edge by a geodesic. A uniform
   upper length bound L follows from finite generation. Equivariance of this
   extension over the edges is unnecessary.
2. If an image edge meets a fixed bounded subset, one endpoint maps within L of
   it. Orbit properness gives only finitely many such vertices, and local
   finiteness gives only finitely many such edges. Closed preimages of compact
   sets are therefore compact. This proves properness of the extension without
   demanding a quasi-isometric lower bound.
3. Removing a finite combinatorial ball leaves only finitely many components:
   each component meets one of the finitely many boundary edges. One-endedness
   provides a unique infinite component C_n; all others have finitely many
   vertices. Thus C_n contains all but finitely many Cayley vertices, and the
   infinite components are nested for nested balls.
4. In the compact Hausdorff Gromov compactification of a proper geodesic
   hyperbolic space, the closures of f(C_n) are nested nonempty compact connected
   sets. Their intersection is nonempty and connected.
5. Properness excludes any point of X from that intersection. More explicitly,
   the preimage of a bounded neighborhood has compact closure in the locally
   finite Cayley graph, so it misses C_n for all sufficiently large n.
6. Removing finitely many orbit vertices cannot remove an orbit accumulation
   point. Conversely, an image-edge point is within L of a vertex image;
   bounded-distance sequences converging to infinity have the same boundary
   limit. The intersection is exactly the orbit limit set.

The construction does not presuppose local connectedness, a continuous boundary
map, or hyperbolicity of H. It proves only connectedness. Compactness of the
ambient compactification is a real hypothesis of this proof; the argument does
not automatically generalize to a nonproper ambient space.

## 4. Failure of geometric finiteness: accepted with explicit hypotheses

Write M for the connected orbit limit set of the surface group just constructed.
It is a compact metrizable invariant subset of the hyperbolic-group boundary.
The subgroup is non-elementary: a closed surface group is not virtually cyclic,
and the Cayley-graph action has no parabolic subgroups. The induced action on M
is consequently a minimal non-elementary convergence action. These are the
standard subgroup-limit-set hypotheses recorded before Lemma 2.1 in the
inspected embedding source; they should be made explicit when citing boundary
uniqueness.

Every nonidentity element of H has infinite order and is loxodromic in the
hyperbolic Cayley graph of K. Its two fixed points belong to M, since both are
limits of powers of that element in an H-orbit. Its restriction to M is still
loxodromic. An infinite parabolic subgroup of a convergence action contains no
loxodromic element; every nontrivial subgroup of this torsion-free H does contain
one. Thus the peripheral structure of H on M is empty.

Now assume for contradiction that this action is geometrically finite. M would
be a Bowditch boundary for the same pair (H, empty) as the usual Gromov boundary
of H. Equivariant uniqueness gives a homeomorphism from the latter boundary to
M. Inclusion of M into the boundary of K would yield the forbidden continuous
H-equivariant map. This is a contradiction.

This argument uses uniqueness with the **same empty peripheral structure**, not
a general statement that every convergence action is a quotient of the usual
boundary. No arbitrary peripheral structure is inserted, and no blow-down or
quotient theorem with unchecked compatibility hypotheses is needed. Dropping
geometrical finiteness from the uniqueness step would beg the central question.

The valid conclusion is a connected limit set with a non-geometrically finite
restricted action and no equivariant boundary extension. Its local connectedness
is **undetermined by these arguments**. A bare continuous parametrization of a
locally connected continuum need not be equivariant and need not extend the
orbit map. Consequently, absence of the equivariant map does not, by the
arguments audited here, establish failure of local connectedness.

## 5. Other proof mechanisms and controls

### Quasi-isometric orbit route and parabolic action

An orbit map has the asserted Lipschitz upper bound. A quasi-isometric orbit
embedding into a proper geodesic hyperbolic space provides the stated boundary
identification and positive special case. Properness alone supplies no linear
lower bound. In the parabolic cyclic action, the distance is

    d(i, T^n i) = 2 asinh(|n|/2).

For n = 2^k, the packet's logarithmic upper bound and vanishing displacement to
word-length ratio are correct. Its displayed formula omits the absolute value
without explicitly restricting n to nonnegative integers. This is a minor
notation correction; every n actually used in that argument is positive.
The example has a singleton limit set, so it refutes the orbit-embedding shortcut
without refuting the target. The independent signed negative control records why
the absolute value matters.

### Continuous-image transfer

The compact, locally connected source and Hausdorff target assumptions suffice.
The fiber is compact, so the proposed finite collection of connected open sets
exists. Every set in that collection meets the fiber, hence its image contains
the chosen target point. The union of those images is connected. The complement
of the image of the closed omitted source set is an open target neighborhood
inside that union. This gives connected neighborhoods within every prescribed
open set; the component argument then gives local connectedness. The proof is
not assuming that a continuous map is open. Compactness makes it closed.

### Comb and Hausdorff controls

The Euclidean comb is compact and path connected. The projection argument is
valid for every connected subset, not merely arcs: a connected set containing
the two designated points projects onto the interval between their x-values and
must meet a base point whose x-value is not a tooth. This gives the lower bound
1/2 on its diameter. Above height 1/4, any connected subset has constant
x-coordinate, so the component at x = 0 is not a neighborhood. Thus the infinite
comb is not locally connected.

The finite subcombs are locally connected finite graphs. The Hausdorff upper
bound 1/(N+1) is correct, though not asserted optimal. The nearby-point example
rules out a common small-continuum modulus for the family. The author's sampled
finite graphs and the audit's independent disjoint-set computations support only
the finite controls; the projection and compactness arguments establish the
infinite assertions. No comb is represented here as an orbit limit set.

### Hyperbolic-cone controls

The cited metric and normalization agree with Koivisto's page 2 and Section 3.
With the specified basepoint, the packet's exact Gromov-product expression is
correct. It tends to infinity for all pairs of tail indices precisely when the
heights tend to infinity and the base coordinates form a Cauchy sequence. On a
compact base this identifies boundary classes with base points and preserves
the base topology. [Koivisto, v6](https://arxiv.org/abs/1505.04662v6)

The fixed-height diameter bound and strict increase of horizontal distance under
a positive height shift are correct. Height-preserving lifted symmetries have
bounded orbits, and the shift is also not surjective on the one-sided cone.
This blocks the proposed elementary realization. It does not prove that every
possible group action on a suitable cone or other space is inadequate.

The inspected source only supplies roughly geodesic structure for general
bases; the cone need not be an actual geodesic space. Also, a bounded lifted
symmetry action has not been verified to be proper or discrete. The packet's
opening broad sentence about “all group-action obstruction examples” should be
narrowed to its two actual in-scope proper actions. Section 6 itself correctly
marks the desired group action as missing, so this wording does not compromise
the mathematical disposition.

## 6. Reproducibility and publication boundary

- Author manifest SHA-256:
  91313d8e77bbd9b47d478beee9aef2b6507a80063920d3853265013848d6e31d
- Author ZIP: 20,003 bytes; SHA-256:
  b8fb3c3b97601c74f91e8dba2e0b1f35b6fdc024a5a0c07009a30c8add557718
- All eight declared packet files match; the ZIP contains exactly those files,
  its matching freeze manifest, and its matching SHA256SUMS.
- Author replay: 5,859 assertions, nine finite comb cases, 512 cone cases.
- Independent implementation: 13,323 assertions, 100 finite comb cases,
  2,340 cone cases, 160 positive parabolic powers, and a signed negative control.
- Six independently re-downloaded PDFs match all expected hashes and sizes.

Run `python3 verify_audit.py` after extracting this folder. The check is offline,
uses a temporary directory for the preserved author ZIP, recomputes both finite
control outputs, and checks the complete audit manifest. To check locally held
PDF bytes too, add `--source-dir /path/to/pdfs`, using the filenames given in the
source metadata. Source files are not bundled.

The bundle contains authored mathematical review, exact finite-control code,
public source metadata, the unchanged author packet, and hash manifests. It
excludes source PDFs, extracted source text, rendered source pages, corpus
contents, private sources, and private coordination. An audit pass does not
license changing the target to solved, claiming novelty, or treating finite
controls as a proof of infinite topology.
