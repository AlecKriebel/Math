# Fresh probability, finite-model, and primary-source review

Review date: 2026-10-07 UTC. Exact candidate: `reviews/refinement2_manifest.json`.
Reviewed `main.tex` SHA-256: `a2d6f9dce6b65e23c0a325619ada4a50ba1fcbeb02fda555c0e9debb13b3b5b6`.

**Verdict: no substantive mathematical defect found in the audited scope.**
The exact squared-word threshold and the transfer of the complete October 4
existence proof to order 32 are supported by the independent derivations
below. No numeric good matching, presentation, or group-ring multiplication
certificate was obtained or inferred from the finite computations.

## Scope and custody

I read `/Users/alec/Documents/Math/AGENTS.md` and
`notes/ORIGINAL_REQUEST.txt` directly. I read the current manuscript and the
complete pinned October 4 source: its main TeX file, all seven sections
(`introduction`, `algebra`, `random`, `patterns`, `planar`, `topology`,
`assembly`), bibliography, and source README. I read the supplied verification
programs to assess their mathematical scope, but independently reconstructed
the finite field, plane incidences, actual letter rows, and rational bounds.
Prior favorable reports were not used as evidence for this verdict.

The independent program verifies all 47 sizes/hashes in the frozen manifest
and verifies every inspected primary TeX/bibliography identity against the
frozen `sources/SOURCE_MANIFEST.json`. Its receipt records those primary
hashes. All work and writes were restricted to this review folder; no frozen
payload, source clone, Git state, publication, tracker, or external individual
was changed or contacted.

The source introduction's broader historical and literature claims are not a
new priority audit here. Its external modern graphical-presentation references
are contextual; the needed estimates and cone criterion are actually proved
in the inspected source. The only externally supplied mathematical tools
required in those proofs are standard graph/surface topology, the planar
separator theorem with its stated constant, Hurewicz/Whitehead, and the
explicit cyclic-group cohomology calculation. The HNN extension and author
priority claims are outside this assigned mathematical review.

## Exact alphabet and quotient

The manuscript's actual-letter classes, in order, are `E` (seven extras),
`S` (their seven ordinary inverse mates), and `O` (the remaining `v-7`
ordinary letters). The classification depends on the letter itself, whereas
the turn rule depends on its inverse. This distinction is respected.

* For a row in `E`, its inverse is ordinary and excludes exactly one `S`
  successor. The three sums are `7p²`, `6/(q+1)²`, `(v-7)/(q+1)²`.
* For a row in `S`, its inverse is extra and excludes exactly one extra
  successor. Six allowed extra turns contribute `6/4=3/2`; every ordinary
  successor has squared weight `p²`.
* For a row in `O`, its inverse belongs to `O`, and it excludes one `O`
  successor. Thus the last two counts are seven and `v-8`.

These are exact row sums for every permitted pairing, not an average over
pairings. The independently written program checked every actual-letter row
for two distinct deterministic randomized pairings at each of
`q=4,8,16,32,64`. The deduction for arbitrary pairing is the preceding count,
not the finite examples. A positive Perron vector of the positive quotient
lifts to a positive eigenvector of the full matrix. Conjugating the full
matrix by its diagonal entries produces a nonnegative matrix with constant
row sum equal to that eigenvalue, proving equality of the two spectral
radii even without assuming irreducibility of the full matrix.

For `q=32`, the independent ratios for `(1,13/5,1)` are exactly

```
95146189/96562235,
579417/592826,
857592557/869060115.
```

Their maximum is strictly below `987/1000`, with exact margin
`33955301/173812023000`. The lifted vector sums to `5376/5` and dominates the
all-ones vector. Nonnegative matrix iteration therefore gives the displayed
upper bound for every integer `h>=1`.

For `q=4,8,16`, the independently reconstructed ratios for
`(193/500,1,97/250)` agree with all nine manuscript fractions and each exceeds
`503/500`. The weakest margin, at order 16, is
`1984579/17466403500>0`. This vector is positive and is dominated by the
all-ones vector, giving the exact lower bounds and spectral radii greater
than one. These exhaust the smaller dyadic field orders in the stated
`q>=4` domain. They exclude the squared-word decay input, not good graphs or
idempotents by every conceivable method.

At `q=2`, both required extra counts can never be integers simultaneously:
`3m-1=0 mod 4` requires `m=3 mod 4`, while `3(m-1)=0 mod 4` requires
`m=1 mod 4`. Its exclusion is an exact failure of this unchanged prescription.
The note correctly states its domain. The independent receipt also checks
the source's coarse vector uniformly for every `q>=32`, using the decreasing
bound `21/(q+1)+7(q+1)/q²` whose value at 32 is `9709/11264<1`.

### Length boundaries

The theorem begins at `h=1`. The independent receipt contains exact total
word masses at `h=1,2,3,4` and checks the stated bounds there. At order 32,
the first four are

```
1064,
10463239/9966,
1368405281715779/1321029312141,
33523352941499103942916/32801539597932238749.
```

A separately defined empty-word mass at `h=0` is one. The positive lower
prefactor would not extend to that boundary; the manuscript does not claim
it does. With `A=5376/5` and `lambda=987/1000`, a separate exact certificate
checks `A² lambda^1098<1`. Therefore at every `h>=1100` the upper bound is
at most `lambda^(h/2)=exp(-2 delta h)`, for the source's prescribed choice
`delta=-log(lambda)/4`. This makes the large-length decay transfer explicit.

## Finite incidence and prescribed types

The independent program uses full polynomial multiplication and polynomial
division to construct `F_2[z]/(z^5+z²+1)`, independently of the package's
shift-and-reduce field multiplication. A Frobenius/gcd irreducibility test
passes. All 32,768 multiplication/distributivity triples pass.

Normalizing every one of the 32,767 nonzero triples produces exactly 1,057
projective points, each with 31 vector representatives. Independent covector
orthogonality reproduces every supplied incidence row. It checks every
point and line has degree 33, all 34,881 incidences, and all 558,096 pairs
of distinct points and all 558,096 pairs of distinct lines. Each pair has
the claimed unique line or point. The data hash is
`12791c8fbad11b6af08ec76adffef476ec01abdcd65c6b0aa9ee69ea5492b4e1`.

The seven Fano lines and complements were reconstructed from vector xor.
Each extra belongs to four complements, each distinct extra pair to two,
and each pair of distinct complements meets in two elements. The supplied
532 inverse pairs cover all 1,064 letters with no fixed points or overlap,
and every extra is mated to its specified distinct ordinary letter.

For every admissible sufficiently large `m`, the ordinary label counts are
`33m` on `A` and `33(m-1)` on `B`, and the extra label counts are exactly
`4a_m+1=33m` and `4b_m=33(m-1)`. The coefficient of the per-line demand is
`7*33/(4*1057)=33/604<1`. The independently constructed round-robin type
assignment at `m=13` has maximum per-line demands two and one on `A,B`;
this finite check illustrates type feasibility only. It is not a good graph.

Every ordinary intersection has odd size 33 or one. All allowed extra
intersections have even size except the special full-seven set with itself.
This gives the exact source parity exception. Degrees are 33,37,40. A
root on side `B` is explicitly fixed before random matching, as required by
the rooted expectation count.

## Complete proof transfer and attempts at hidden assumptions

### Source random section

The unconditioned cycle count and short-cycle switch in `random.tex`
252–294 use only fixed `T,p,d_*`, balanced inverse slots, and the two strict
girth inequalities. At order 32, `c0=1/100` works because
`2|T|/p<2^17` and `40<2^6`. Both the expected bad-edge count and the count of
edges excluded within distance `2L` are `o(n)`. Loops and doubled edges are
included in the cycle count. Switching preserves the graph types, removes
the selected bad edge, and creates no new short cycle; the arguments cover
coincident original endpoints.

The quantitative switch in 300–360 has an injective inverse determined by
the output matches at the prescribed domain and target slots. Overlapping
domain/codomain vertex sets do not invalidate this inverse. Avoiding the
old prescribed edges preserves every prefix condition. The resulting
conditional estimate requires no probability lower bound for the rare
girth event. Its error `r_n=o(n)` and its uniform `E=O(L)` prescription
bound remain valid. The manuscript's slightly looser added `O(log n)`
term is harmless.

For expansion, minimum degree 33 forces `r=ceil(33k/2)` distinct edges
inside the enlarged `2k`-vertex set, with `16.5k<=r<=17k`. Exposing these
edges using the same conditional bound is valid once `17 eta<p/4` and
`r_n<np/4`. The binomial bound gives exponent `33/2-2=29/2`; splitting
the sum at `sqrt(n)` gives `29/4`. The independent exact certificate
validates `eta=10^-6`, using
`D<48|T|/(33p)=17994368/363` and
`C3<(9/4)D^17`, for which `C3 eta^(29/2)<1/2`.
The geodesic ball-packing argument then provides a fixed diameter
multiple of `L`. All constants remain fixed before `n` grows.

The original order-128 contraction itself was checked independently:
its coarse ordinary-row bound is `71589573988/72026254783<1`, and its
extra-row ratio is `195474585/311633336<1`.

### Source patterns section

I rechecked the weighted graph-rank argument (63–102), bounded chain
decomposition and multiplicity count (104–151), and the half-edge incidence
inequality (165–191). A leaf can only be an interval endpoint; the unique
root constraint in stage one loses exactly the power of `n` needed for
the two possible endpoint incidences. Suppressing degree-two vertices
does not discard inherited lengths or girth.

The simultaneous grid (215–300) uses a bounded number of affine offsets,
not the number of individual edge traversals. Its full block length
diverges uniformly and is `o(L)`. A block occurrence has at most one
match, since two proposed overlaps longer than half its length would
violate disjointness of compared positions. Endpoint and final-fragment
losses are `o(L)`.

In the self-link count (338–379), a translation of zero is prohibited by
the distinct-underlying-edge requirement. A nonzero fixed translation
has a forest of positional equalities. A reflection self-link forces a
fixed letter or two adjacent inverse letters; both are impossible for
reduced words with a fixed-point-free signed alphabet. These are genuine
constraints on underlying word blocks despite repeated traversals.

Word bins and expectation counts (382–512) use the new positive minimum
weight and decay constant. Each stage counts injective realizations with
distinct prescriptions, rather than charging repeated traversals as
independent random edges. Labels at a stage are required to extend to a
full string assignment; this legitimately allows the minimum-bin block
to be used even when that block is absent at the current stage.

The deterministic product of first-moment upper bounds (519–594) has
nonpositive total exponent of `n` by the incidence lemma. At least one
stage upper bound is no larger than the product's geometric mean. This
step needs no independence between stages. The final choice of
`epsilon=min(1/4,delta/(16(1+a0)))` precedes `K0,C,I`; each of these latter
bounds only changes the threshold in `n` and the uniform `o(L)` terms.
Slower decay at order 32 enlarges these thresholds but does not change
the order of quantifiers.

### Source planar section

After deleting at most two incident edges, the new minimum degree is
31, still at least three. The two-walk based-loop construction in
82–118 survives, including a segment whose endpoints coincide. The
chosen loops avoid the specified join edges, so added closures retain
the original occurrences without cancellation.

The Euler identity in 156–205 holds for disconnected regular neighborhoods
and multiply connected complementary surfaces. Disk monogons are
excluded by immersion apart from the unique exceptional break. A digon
using one band twice forces a degree-one gap; the stated loose bound
is sufficient. Cutting both opposite good gaps makes the interval
decomposition stable. Self-paired maximal runs are excluded by the
fixed-point-free occurrence pairing or by adjacent inverse letters.

The recursive separator charge in 253–278 is a geometric series after
each component shrinks by at least a factor `2/3`. Dividing each disk
into consecutive endpoint blocks preserves planarity even for loops and
parallel arcs. All losses in 327–430 are charged to total original or
added occurrences. The two averaging exclusions leave at least `13H0/16`;
the possible exceptional cluster shorter than `L` costs less than
`H0/2`. A positive remaining cluster obeys the *same fixed* triple
`K0,C,I`. Closure occurrences may overlap old edges, but they are
unpaired, which the bounded-pattern theorem permits. No other projective
order requirement occurs in this section.

### Source topology, algebra, and assembly

The relative graph-cone replacement in `topology.tex` 55–105 uses actual
contractible abstract cones; it does not assume their attached images
are embedded. It preserves a prescribed exterior word. General-position
level arcs in the map to the rose pair inverse letters and have one
endpoint per letter occurrence.

I attempted to falsify all four same-edge surgeries in 162–270.
The spliced paths are paths in the actual graph because the paired
traversals use the same graph edge, not just the same label. The
outer/inner and outer/outer surgeries preserve the fixed graph endpoints
of the rooted path. The outer self-surgery restricts the old disk map
and needs no unsupported filling of the discarded middle loop. For
inner self-surgery on an essential sphere, the two caps are chosen through
the same lift of the contractible abstract cone. Their homology classes
sum to the old nonzero class in the universal cover, so one remains
essential and has strictly smaller boundary length. These facts justify
the minimization argument and exclude every same-edge pairing.

Once `pi2=0`, a simply connected two-dimensional universal cover is
acyclic and then contractible by Hurewicz and Whitehead. The source's
explicit periodic resolution of a prime-order cyclic group proves the
torsion obstruction: restriction of the finite-dimensional free
resolution would kill its cohomology above degree two, whereas trivial
`F_ell` coefficients give a nonzero group in every degree. No order
parameter or characteristic-two assumption enters that torsion argument.

The parity calculation in `algebra.tex` 85–117 uses actual undirected
simultaneous-step edges. Each product contribution is constant on a
component, and the handshake lemma yields even cardinality except for
the component with the unique even-degree vertex `(x_A,x_A)`. The latter
has odd cardinality and contributes one. The mixed product has no
exception and contributes zero. Protection of `x_B` makes its identity
coefficient in `c` exactly one, independently of any other possible
coincidences among path labels. Thus the same order-32 outcome gives
`ab=1`, `ac=0`, and `c!=0` in the prime-field **scalar** group algebra.

The assembly quantifier selects one sufficiently large finite matching
outcome in a nonempty conditioned space; existence is not inferred from
the finite incidence data. The componentwise spanning-tree relators in
the manuscript use roots `x_A,x_B` in their designated components, in
agreement with the parity witnesses. Relative cone replacement gives
the finite presentation on the 532-edge rose. This supplies the
strongest asserted explicitness: a fully specified asymptotic existence
construction, with no numeric successful matching promised.

## Receipts and limits

Reproduce the independent finite checks from this folder with:

```
python3 reviews/refinement_review_two_work/fresh_probability/independent_checks.py
```

`independent_checks_receipt.json` contains exact matrix fractions,
low-length boundary masses, strict margins, incidence counts, and primary
hashes. `decay_boundary_receipt.json` records the separately checked original
contraction and a concrete length at which the source decay form holds.
`package_parameter_receipt.json` and `package_plane_receipt.json` retain
fresh read-only runs of the package programs. The independent program uses
explicit failures that remain active with optimized Python. The supplied
parameter verifier uses Python assertions, so its checks can be disabled
by `python -O`; its documented ordinary invocation passed. This is a
minor verifier robustness limit, not an unresolved mathematical gap.

No numerical group presentation, explicit reduced idempotent support,
formal Lean proof, or conventional human review is certified here. The
supplied manuscript makes those same limitations explicit. I found no
remaining substantive concern in the complete primary-source proof,
its order-32 transfer, or the exact unchanged-model least-order claim.
