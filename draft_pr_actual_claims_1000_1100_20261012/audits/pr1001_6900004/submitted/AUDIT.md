# Independent audit: full labeled tensegrity partitions

**Publication context:** This audit is preserved as a historical review report below. Its references to the original candidate, separate derivative, and original audit receipt filenames describe that review stage. The delivered `REPORT.md` incorporates the attribution correction and updates only its disposition and receipt references. The complete superseded original is omitted. This delivery has fresh `CHECK_RUNS.json`, mode-specific output references, `PUBLICATION_MANIFEST.json`, and an externally pinned `BOOTSTRAP.py`; the historical audit's prior manifests are not substitutes for those fresh records. Source PDFs and source bodies are not included or replayed.

## Verdict

**ACCEPTED for the precise literal-partition theorem, with the attribution correction supplied. The interpretation hold on the unqualified original problem remains.**

For every integer n >= 1 and d >= 1, simple graphs G and H on the same labeled n-element vertex set induce identical full partitions of (R^d)^n by connected sign-equivalence classes if and only if their edge sets coincide. The report gives a complete proof of this statement. No mathematical repair of the argument is required.

The correction explicitly attributes its singleton-support collision criterion to Panina's Lemma 4, which already contains that criterion. It also records a narrow arithmetic discrepancy in two source examples. It preserves the full-partition transport proof and every source-interpretation caveat. No claim of novelty or resolution under a weaker comparison of stratifications is approved.

The original REPORT.md and all other original candidate files were left byte-for-byte unchanged. REPORT_CORRECTED.md is a separate derivative; ATTRIBUTION_CORRECTION.patch shows the complete contextual change. The original report's historical pending-review sentence remains unchanged in that derivative; this audit is the separate review disposition.

## Independent reconstruction of the proof

Let E be the edge set of a simple labeled graph. Its stress space at P consists of real edge weights satisfying force balance at each vertex. Fix an edge e = {i,j}. A stress positive on e and zero elsewhere is possible exactly when p_i = p_j: the only potentially nonzero forces are positive scalar multiples of p_j - p_i at i and its negative at j. Consequently, a sign-preserving homeomorphism cannot identify fibers on opposite sides of this collapse condition. In particular, preservation of zero coordinates is essential; dimension alone cannot replace the sign condition.

Now suppose e belongs to G and not to H. Put all vertices on a line with a nonzero direction a in R^d. Let x_j(t)=0, x_i(t)=t for t in [-1/2,1/2], and place the other labeled vertices at mutually distinct fixed coordinates greater than 1. Every H-edge has nonzero scalar length throughout this interval. Each such length is continuous with constant sign. For an H-edge {u,v}, multiplication of its stress coordinate by

    (x_v(0)-x_u(0))/(x_v(t)-x_u(t))

is therefore a strictly positive, finite, nonzero scaling. At either endpoint, multiplying the new stress coordinate by the new displacement gives exactly the old stress coordinate times the old displacement. Thus the diagonal map takes the old equilibrium kernel into the new one. The reciprocal diagonal map gives the reverse inclusion. It is a linear homeomorphism preserving every coordinate sign, including zero.

Every point of this continuous configuration path is in the same H-fiber equivalence class as P(0). The image of the interval is connected. Every connected subset of an equivalence class lies in a single connected component of that class, so P(0) and P(1/4) are in one H-stratum. This is stronger than merely comparing the endpoint fibers.

For G, e is collapsed at P(0) and separated at P(1/4). The positive singleton-support stress exists only at the first configuration. A sign-preserving homeomorphism from its fiber to the other fiber would have to send that vector to a vector positive on e and zero elsewhere, which cannot satisfy equilibrium. Hence the two points lie in distinct G-strata. The partitions of the same ambient set assign a common pair of points differently and are unequal. Reversing G and H covers either direction of edge-set difference. Identical edge sets give identical fibers and therefore identical partitions.

This is the same single proof approach under audit, independently reconstructed; it is not a second search for another solution.

## Boundary and definition checks

- **n=1:** there is only one simple graph, and its zero stress fiber is constant. The ambient space is connected. The conclusion is immediate.
- **d>=1:** a nonzero direction exists in every permitted dimension. Extra coordinates introduce redundant force-balance equations; no general-position assumption is used. At d=0 the base has one point, and every graph would induce the same one-piece partition, so excluding d=0 is necessary and matches the source.
- **Isolated vertices:** they contribute only zero equilibrium equations. They may be placed freely at the prescribed fixed positions. Padding a subgraph with missing labeled vertices is an explicit convention needed to compare partitions of the same ambient space.
- **Empty H:** its stress space is R^0, the empty diagonal transformation is its unique linear automorphism, and the whole connected ambient space is one stratum.
- **Disconnected H:** transport works edge by edge, independently of graph connectivity.
- **Orientation:** reversing an edge reverses both numerator and denominator and leaves the ratio unchanged. The stress is a scalar on an unoriented edge, with opposite geometric force vectors at its endpoints.
- **Coordinate redundancy:** the embedding into symmetric n-by-n arrays repeats the edge coordinate and fills every nonedge, including diagonal entries, with zero. It induces exactly the same coordinate-sign equivalence.
- **Connected components:** equivalent endpoint fibers alone need not imply one stratum. For a single edge in R, configurations with opposite endpoint order have the same zero fiber but lie in different components. The candidate avoids this gap by constructing a path entirely inside the H-equivalence class.
- **Equal dimension:** for collinear K3 with exactly one colliding pair, the stress fiber has dimension 1, as it does for three distinct collinear points. Its singleton support changes. This directly demonstrates why rank comparisons alone would be insufficient.
- **Full ambient space:** the witness uses retained collisions and low-affine-span configurations. Nothing is asserted for an injective-only, generic-only, or selected-codimension partition.
- **Relabeling:** a prescribed permutation carries the partition for G to the partition for the correspondingly relabeled graph. The theorem applies after this identified coordinate permutation. Arbitrary ambient homeomorphisms or abstract adjacency equivalences are outside the accepted statement.

## Source audit and correction

Karpenkov's [publisher PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/018-0080.pdf), journal pp.20-22, confirms positive dimension, labeled configurations, the full Cartesian base, coordinate-sign-preserving homeomorphisms, and connected strata. Examples on p.21 and the single-edge example on p.22 retain coincident vertices. Problem 4 itself gives no separate cross-graph definition of sameness. Its surrounding discussion emphasizes dimensions and adjacency, so a weaker intended comparison remains possible. The audit therefore does not certify a solution of the original unqualified problem.

Doray--Karpenkov--Schepers, [preprint v2](https://arxiv.org/pdf/0806.4976v2), Definitions 2.1 and 2.6, explicitly set nonedge coordinates to zero, identify the two orientations of an edge, and use the sign function on the entire stress vector. Their full-space definition supports the candidate's conventions. Theorem 2.8 on semialgebraicity is background and is not needed in this proof.

Panina, [preprint v4](https://arxiv.org/pdf/1902.07212v4), Section 3, Lemma 4, already gives the singleton-positive-support detection of degenerate edges. This exact attribution was missing from Observation A and is now supplied in the separate derivative. Her Proposition 4 concerns strong and weak stress equivalence; the candidate does not need to invoke it, since the transport maps are explicit. Her initial realization convention and affine quotient are not substituted for Karpenkov's full configuration space.

A narrowly checked source arithmetic issue also requires care: Karpenkov Example 1.4, p.21, and Doray et al. Example 2.7, preprint p.5, state dimension 2 for K3 with exactly two coincident vertices. Substitution into their equilibrium equations gives dimension 1. At p_1=p_2=0 and p_3=a != 0, equilibrium at vertices 1 and 2 forces w_13=w_23=0; only w_12 remains free. This is recorded as a correction to those numerical examples alone. It is not evidence against their other theorems.

The primary PDF content and declared preprint versions were independently inspected. Local source-byte hashes and sizes match the original source manifest. This audit did not rerun an exhaustive novelty search, did not obtain author clarification, and makes neither claim.

## Independent computation and reproducibility

The independent checker does not import the candidate. It constructs exact rational stress-kernel bases by starting with the ambient coordinate basis and intersecting successively with force-balance hyperplanes. This differs from the candidate's direct matrix-rescaling identity checks. It verifies both directions of diagonal transport on actual kernel bases, singleton witnesses, and the incidence-cycle-space dimension formula for collinear noncollapsed frameworks.

Coverage in each independent baseline run:

- All 205 pairs consisting of an H graph through four vertices and one of its missing edges, with three rational parameters and dimensions 1, 2, 4: 1,845 transport checks.
- Every unordered distinct graph pair through four vertices: 2,045 further kernel/witness checks, with per-n counts 0, 1, 28, 2,016.
- 108 larger checks for n=5,7,10; dimensions 1,3,5; dense, disconnected, forest, and empty graphs; several distinguished edge positions.
- Nine semantic negative controls, including inverse or absent scaling, negative or singular scaling, zero-sign erasure, rank-only equivalence, the erroneous K3 nullity, d=0, and a separated singleton witness.

The unmodified candidate checker reproduces its original full output exactly, including 25,116 pair/selected-family checks, 205 additional nonedge checks, and ten negative controls.

Both checkers pass normal Python, -O, and -OO as UID 1000. Scripts were executed with mode 0444 inside a mode-0555 directory. Actual attempts to create a file there and append to the independent checker both failed with EACCES, errno 13. Expected hashes were stored separately before execution and checked before and after each run. The external manifest itself was also unchanged.

Six actual source-code mutants were each run in all three Python modes. All 18 executions failed as expected: reversed length ratio, omitted ratio, negative ratio, changing sign(0), a zero singleton witness, and applying the same rather than opposite force sign at both endpoints. Their complete stdout, stderr, exit codes, expected rejection reasons, commands, and hashes are retained. These mutation tests validate the guards; they do not prove the mathematical theorem.

VERIFICATION.json records the runs. EXTERNAL_PINS.json fixes the candidate, source, corrected-derivative, baseline-checker, and mutant bytes. FULL_OUTPUT_MANIFEST.json identifies every full output in the accompanying evidence directory. Original inputs and source PDFs remained unchanged. Source documents and their rendered pages are not part of the public audit packet.

## Disposition

Accept the corrected literal fixed-label full-partition result. Keep an explicit interpretation hold for any claim that the unqualified original Problem 4 is solved. Do not describe the known collision criterion, sign-equivalence machinery, or this bounded source check as a novel discovery or an exhaustive novelty determination.
