# Independent source-checkpoint adversarial review

Reviewer: AI subagent `independent_source_adversary`.
Initial independent assessment completed 2026-10-06, Pacific time
(2026-10-07 UTC). This is a review of the imported source proofs, not a
full preprint/publication-package review or external peer review.

I did not read any other agent's mathematical audit conclusions before
forming this assessment. The only inter-agent message received before
assessment described source locations and proposed issues to test, without
disclosing findings. I read the actual family197 sections and family090
sections and reconstructed the checks below directly from their formulas.

## Outcome and limits

No decisive counterexample or substantive error was identified in the
manuscript proof chains inspected here. In particular, the family197
proof does not merely assert an injection of a graph into a quotient, and
family090 does not certify global signs by sampling. The former supplies
a probabilistic diagram-exclusion argument and relative cone surgeries;
the latter supplies an infinite-space inverse, exact zero jets, finite
Bernstein checks, and a quadratic tail barrier.

This assessment does **not** provide full formal verification, validate
the consequence/embedding/product-program literature, establish priority,
or approve a publication package. Family090's finite inverse/residual
claims require their complete rigorous computation checks in the program's
other source-validation artifacts; this reviewer independently checked all
2,436 finite Bernstein coefficients, but did not independently recompute
every matrix and residual entry. The source-review receipts identify the
exact partial computational coverage.

A substantive scope finding is that the associated family197 Lean
documentation and comparator describe another construction with
odd-prime torsion and a possibly larger finite field. They do not
formalize the torsion-free prime-field graph/cone theorem. The comparator
file contains `sorry`; it is not evidence that the manuscript theorem was
proved in Lean. The supplied `Main.lean` instead imports a separately
prescribed characteristic-two construction. No formal compilation is
claimed by this reviewer.

## Family197: graph/cone construction

Exact inspected source statement: there exist a finitely presented
torsion-free group G, admitting a finite two-dimensional classifying
complex, and a,b,c in F₂[G] with ab=1, ac=0, c≠0. Hence ba≠1.

The dependency chain and adversarial checks were:

1. **Parity algebra.** The simultaneous-step graph counts geometric
   edges once, retains parallel edges distinctly, and has degree
   |Sx∩Sy|. The root-root component in A×A has one even-degree vertex,
   so it has odd cardinality; every other component has even cardinality.
   The contributions gx gy⁻¹ remain constant under a common right step.
   The A×B components have even cardinality. Root protection at xB alone
   gives identity coefficient one in c, irrespective of collisions among
   its other coefficients. Thus the claimed algebra follows without
   cancellation, linear independence of all vertices, or assuming G is
   Hopfian.

2. **Types and matching model.** The projective-plane and Fano-plane
   counts give ordinary size 129, extra intersections 0,2,4, and the
   unique extra self-intersection 7 at xA. m≡1 mod4 makes the prescribed
   extra counts integral. Label populations on A and B are independently
   balanced. Pairing slots rather than distinct vertices handles the
   overlap of a letter and inverse-letter population. Conditioning on
   girth later excludes loops and parallel edges.

3. **Word decay.** I checked the two weighted matrix row comparisons:
   ordinary inverse-letter row ≤128/129+7p²+21/129²<1 and extra row
   ≤6/4+(16513+21)p²<4. The positive-vector domination implies a spectral
   bound strictly below one and ∑P(W)²≤4|T|λ^(h−1). The later choice of
   δ absorbs the constant for sufficiently long words. Constants are
   fixed independently of n.

4. **Conditioning and expansion.** The switching operation deletes only
   the two matched prescriptions. Selecting a distant unprescribed edge
   preserves every prescription already exposed, and no new cycle of
   length <L can traverse one or both changed edges. The output determines
   the input switch, so the counting bound is valid without estimating
   the tiny probability of the conditioning event. The resulting
   prescription error is exp(O(E(E+r_n)/n))=exp(o(L)) for E=O(L).
   Expansion uses at least ceil(129k/2) distinct edges, not the number of
   edge traversals. The union bound's power 62.5 is 129/2−2. Its stated
   choice of a fixed small ρ makes the sum tend to zero. Disjoint balls
   centered on a geodesic give diameter O(log n)=O(L).

5. **Multiplicity and repeated edges.** I checked that the bounded-image
   rank argument retains inherited chain lengths; its non-backtracking
   walk count is used only to force two distinct reduced paths with the
   same endpoints. In a forest that is impossible. Marking the initial
   and terminal points makes all original traversals whole-chain
   traversals. A repeated oriented-edge use requires a reduced closed
   walk of length ≥L between the two starts. The incidence estimate
   2 max(m_e)≤∑m_e+a(z), summed over vertices, gives
   ∑V_j≤H+ι. Fixing the exceptional root at stage one pays for the only
   extra vertex. Distinct edge prescriptions are never replaced by the
   total traversal count.

6. **Aligned blocks and entropy.** Simultaneous Diophantine approximation
   of the bounded number of offsets gives s→∞ and s=o(L). Reflection
   reverses labels and has no allowed self-link on a reduced block:
   either a central letter equals its inverse or central adjacent letters
   are inverse. A translation self-link has nonzero integer offset
   because paired underlying edges must be distinct; its equality graph
   is a forest, leaving O(κs) free letters. Without self-links,
   2z≤S+b counts matched occurrences, so repeated traversals cannot
   falsely provide extra independent word weights.

7. **Stage expectations.** The labels at stage j are projections of
   entire compatible string assignments, not independently chosen
   strings. Consequently the minimum-bin block may be used even when
   absent from that stage. All chain endpoint fragments and bin choices
   cost exp(o(L)). Multiplying the deterministic expectation upper
   bounds and selecting their minimum uses no independence among
   stages. With ∑(V_j−E_j−k_j)≤0, the net n power is nonpositive.
   The estimate −δH/2+a₀b₀+o(L) is therefore compatible with the claimed
   single ε chosen before K₀,C,I. This order of quantifiers is essential
   and is retained by the planar extraction.

8. **Planar extraction.** Complementary regions may have multiple
   boundary components. The Euler formula includes their actual Euler
   characteristics and does not silently assume a connected pairing
   graph. A disk monogon can occur only at the one exceptional break.
   The good-digon involution and marked indexing gaps bound interval
   comparisons linearly. The recursive separator charges geometrically
   decreasing components. Short closures are immersed as linear paths;
   the added auxiliary loops avoid the join edges, which makes the
   complete closure cyclically immersed. Added occurrences remain
   unpaired. Deletion and closure losses are controlled in aggregate,
   and the extraction keeps a cluster with H≥L. The possibly short
   exceptional path is separately discarded, using the presence of an
   ordinary boundary of length ≥L. Thus the same fixed triple covers
   arbitrarily large arrangements.

9. **Topology and root protection.** The cone is not assumed embedded
   in the quotient. Replacing it by maximal-tree basis relator disks is
   a homotopy equivalence relative to its graph, since both target
   complexes are contractible and the graph inclusions are cofibrations.
   Cone pictures and transverse arc pairings use abstract cone
   factorizations. An arc pairing the same underlying graph edge permits
   four band surgeries. In each exterior case the graph endpoints stay
   fixed; the exterior-exterior surgery retains the component containing
   the marked break and uses a restriction of the old disk map, not an
   unsupported separate filling of the discarded subword. In the
   inner-inner splitting case, both caps use the same lift of the
   abstract cone to the universal cover. The homology sum preserves a
   nonzero essential sphere by Hurewicz. Total boundary length decreases,
   contradicting the chosen minimum. This addresses the key potential
   unsupported-injectivity gap directly.

10. **Asphericity/torsion.** A simply connected two-dimensional complex
    with π₂=0 is acyclic and contractible by Hurewicz/Whitehead. Restricting
    its finite-length free ZG resolution to a cyclic subgroup of prime
    order remains free. The periodic cyclic-group resolution with
    F_l coefficients has nonzero cohomology in arbitrarily high degrees,
    contradicting that restriction. The torsion-free conclusion therefore
    follows from the actual topological argument rather than an assumed
    small-cancellation label.

These checks constitute an independent handwritten source-proof audit.
They are not a constructive list of the enormous finite matching outcome,
nor a machine proof of the probabilistic/diagram arguments. The source
selects a finite outcome by an existence argument; the theorem does not
require an efficiently enumerated presentation.

## Family090: exact Schwartz Fourier certificate

Exact inspected statement: a real radial Schwartz g on R² has ĝ(0)=1,
g(0)=2/√3, ĝ≥0 everywhere, and g≤0 for |x|≥1, with phase
exp(−2πi<x,ξ>). This certificate would supply the planar upper bound.

The dependency chain and adversarial checks were:

1. **Geometry and Fourier convention.** The covolume-one triangular
   lattice has b=√3/2 and s=b|x|². Its dual is a 90-degree rotation,
   so the same radial shell coordinates apply to both Poisson sums.
   j²+jk+k² falls in residues {0,1,3,4,7,9} modulo12; 15 is an extra
   interpolation node, so uniqueness of the chosen coefficient lists
   does not establish uniqueness among all radial Schwartz functions.

2. **Entire cardinal functions and regularity.** The divided exponential
   identities cancel both P(n) and P'(n). Their integral measures have
   support [−1,1] and uniformly bounded variation. An ℓ¹ list therefore
   converges in total variation and locally uniformly with all derivatives
   in the spectral representation. Multiplication by exp(−πbh|x|²)
   gives a Schwartz function without requiring complex analyticity of
   an arbitrary infinite-list density in the integration variable.
   The two-dimensional Gaussian transform gives exactly the stated
   λ(t), z(t), and Im z≥26/435. Thus transformed derivatives decay
   exponentially for positive real s.

3. **Full-space inversion.** The operator is bounded on unweighted ℓ¹
   by summing row envelopes uniformly over every input column.
   The finite Schur complement has norm defect <.28+.11·3.7=.687.
   The infinite Schur complement has norm defect <2521·5·10⁻¹⁰.
   These are inverses on the whole spaces, not assumed limits of finite
   sections. Combining the bounds gives 91 times the finite residual
   norm plus 2540 times the tail residual norm. The sum/difference
   equations for the pair introduce the stated factor two. The table
   enclosure .00002860012<.00003 is numerically consistent with those
   constants. Full rigorous matrix/residual computations remain an
   independent evidence requirement outside this review's own
   computational coverage.

4. **Analytic quadrature error.** For a complex disk of radius1/6 around
   each midpoint c_j, inversion of t+ih gives the disk center
   (c_j−ih)/Δ_j and radius (1/6)/Δ_j. This implies |λ|<5, |z|<6.2,
   and Im z>−.081 on every such disk. The finite-input density grows
   at most as exp(100π/6); the direct phase contributes another such
   factor, and the transformed phase contributes at most exp(100π·.081).
   The displayed divided-power bounds therefore admit M=10⁵³. The
   rule has positive weights, total mass one, and degree255 exactness;
   Cauchy's Taylor tail on the half-radius real interval is M2⁻²⁵⁵.
   Comparing both integral and quadrature gives at most
   10⁵³2⁻²⁵⁴<3.455·10⁻²⁴<10⁻²². Atoms are evaluated separately.
   This proof uses finite lists supported through100, exactly as in the
   retained computations. It does not apply to a hypothetical analytic
   continuation of a general ℓ¹ density.

5. **Independent finite Bernstein verification.** I independently
   implemented the direct node-Taylor cardinal formula, derived by
   multiplying P's entire Taylor series by R's convergent Laurent
   series. For the transformed term I independently implemented the
   degree255 Fejér rule and added the audited 10⁻²² analytic moment
   radius using Arb/Acb at192 bits. Every one of the 2,436 Bernstein
   coefficients for all84 required half-gaps exceeds its stronger
   Appendix-A grouped lower bound. The difficult printed entry at
   function2, center16, y=−1/2, k=28 encloses as
   [0.0095187595568082337 ±4.38·10⁻²⁰]. No supplied certificate module
   or prior agent implementation was imported.

6. **Lower jets and continuum signs.** The table is not forced to have
   exact node zeros. Subtracting the lower Taylor jets of the exact
   minus tabulated error before division gives the integral remainder
   bound sup|Δ^(ν)|/ν!, valid for either direction of the half-gap.
   The only odd vanishing order occurs at the rightward half-gap from
   the exclusion node1. Thus its divisor u is nonnegative. The degree28
   Bernstein polynomial is a convex combination of its positive
   coefficients. The remaining Taylor tail and coefficient error are
   bounded uniformly on the entire half-gap, not merely at samples.

7. **Unbounded region.** The rational finite-node part has poles only
   through40, so for s≥41.5 its denominators are ≥1.5. The coefficient
   error passes to this rational part without crossing a pole. For a
   nearest node m≥43, both H_i and P R_i,0 have value and slope zero,
   hence so does E_i. Its second-derivative bound applies along the
   whole segment from s to m. The quadratic sine-product barrier uses
   log concavity of P(m+u)/u² on half-gaps and midpoint values; the
   smallest is 12−8√2>.68. Consequently
   σ_i H_i(s)≥(.011·.68−.006/2)(s−m)²=.00448(s−m)².
   This proves global tails once the scalar envelope claims are
   independently certified. The tie at41.5 is resolved by taking43;
   no comparison segment falls below the region on which the derivative
   bound holds.

8. **Normalization and zeros.** Differentiating the covolume-one Poisson
   dilation sum is justified by uniform Schwartz bounds on compact
   t intervals. The nonzero shell values and Fourier slopes vanish;
   only the six first-shell physical slopes remain. Hence
   F(0)=F̂(0)=6Q₁exp(−πh)>0, independently of the sign proof.
   The final two-dimensional dilation gives ĝ(0)=1 and g(0)=1/b.
   The exact zero sets in the sign domains follow from strict quotient
   and tail inequalities; attainment of the separate triangle program
   is not proved by this certificate.

## Retained artifacts and reproduction

- `source_records.json`: SHA-256 identities for the exact local source
  files used, their upstream pinned version, and read/retrieval times.
- `independent_moments.py` and its receipt: floating-point diagnostic
  with three refinements. It is explicitly not a rigorous enclosure.
- `independent_arb_bernstein.py` and its receipt: independent rigorous
  finite Bernstein computation at192-bit precision, using the audited
  source quadrature remainder; all84 half-gaps and2,436 coefficients.

Reproduce the rigorous check with Python3.12 and `python-flint==0.9.0`:

```text
python independent_arb_bernstein.py
```

The script locates the retained family090 mathematical source/data by
its relative position inside this research folder. The local execution
used the bundled Python runtime and the program's installed python-flint
wheel. A publication package must preserve that relative data layout or
adjust its documented path consistently. It must not characterize this
one computation as verification of the finite matrix/residual system or
the whole manuscript.

## Checkpoint estimates and outstanding work

These are this reviewer's estimates for the research program at this
source checkpoint, not a completion declaration: TargetA65%, TargetB75%,
publication package5%. They may change after the other independent
audits are reconciled.

Remaining source-verification tasks before promotion are to reconcile
the full matrix/residual and scalar-envelope computation receipts with
the exact source claims, retain the formal-scope limitation accurately,
and have another independent source reviewer scrutinize the substantial
family197 diagram/entropy argument. The consequence proofs, precise
product-program convention, embedding input, attribution/priority audit,
full preprint, clean reproduction, fresh whole-package reviews, Zenodo
deposit, and tracker row are outside this source checkpoint. No such
publication gate is marked passed here.
