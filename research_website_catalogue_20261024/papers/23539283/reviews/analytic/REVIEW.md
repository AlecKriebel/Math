# Independent analytic review — Zenodo 23539283

**Verdict:** Pass within the stated analytic scope. No unresolved substantive mathematical defect was identified. This is an AI analytic review, not human peer review, proof-assistant certification, or a global-priority determination.

## Inputs and independence

Reviewed the entire published manuscript source, `sources/published-source/free-product-tensor-core-verification/manuscript/main.tex`, lines 1–726, and the checksum-bound published PDF text. Before forming this verdict I did not read the archived positive review reports, their conclusions, or the inventory judgment. The package file listing exposed the existence and names of prior reports, but not their contents. No packaged verification script was executed; the central claims are infinite-dimensional analytic claims and are not certified by bounded finite computations.

Published record: [10.5281/zenodo.23539283](https://doi.org/10.5281/zenodo.23539283), version 1.0, dated 21 October 2026. Downloaded PDF: 109,650 bytes, SHA-256 `f1fb805eacd68f455fc7d3afa1b08ac1e10592f91adfd2321be7151f7994d972`. Published package TeX SHA-256: `c2de3539519e80a5f036574555f93883df5fe7143d6ddb84077d73fb8ed6b463`. Both downloaded Zenodo files independently matched the MD5 checksums recorded in the retrieved Zenodo metadata.

The category comparison was checked against Skeide's original 2009 definition and question, institutional [Oberwolfach report PDF](https://art.torvergata.it/bitstream/2108/82891/1/Ac09_Some%20comments%20on%20product%20systems_Oberwolfach%20proceedings.pdf), PDF pages 37–38 (printed prepublication pagination). Only the relevant definition/question and surrounding distinction from the forward construction were reviewed; this is not a whole-report literature review.

## Exact claim and hypotheses

The manuscript constructs separable **complex pointed Hilbert spaces** `E_t`, for real `t >= 0`, with `E_0 = C omega`, and pointed unitaries `u_(s,t): E_s free-product E_t -> E_(s+t)`. The free product is the orthogonal sum of finite alternating centered tensor words. The maps satisfy the canonical associator identity. The first input occupies the later time interval.

For every positive time, the maximal ordered tensor subsystem is the direct sum of finite decreasing-coordinate simplex spaces. Its closed free hull is exactly the direct sum of all finite Cartesian-power word spaces. A nonzero grade-omega subspace remains orthogonal to that hull. Continuity means the explicit support-subspace Hilbert field in Section 5, locally trivial at positive times, with the dimension-one zero fibre and strongly continuous extended structural maps and adjoints. No stronger unspecified bundle condition is presumed.

## Claim-by-claim reconstruction

### 1. Recoverability and sigma-finite measure (lines 109–140)

For `x_j = a + delta 2^(-j) z_j`, the stipulated Gaussian full-measure set gives `lim x_j = a` and

`lim_N N^(-1) sum_(j<N) 4^j (x_j-a)^2 = delta^2`.

Conversely, these two limits with positive finite second limit recover `a`, `delta`, and `z_j = 2^j(x_j-a)/delta`, whose defining convergence and Cesaro conditions follow directly. Thus this is an actual Borel bijection, not an identification of mutually singular fixed-parameter Gaussian laws. Existence/values of the countable limits are Borel. The parameter domain is standard Borel. Sets `|a| <= N`, `1/N <= delta <= N` have measure `(2N)(2 log N) = 4N log N` and exhaust it, proving sigma-finiteness.

The probabilistic inputs are ordinary Gaussian tails plus Borel–Cantelli and the strong law for independent squares. One can replace the tail estimate for `2^(-j)z_j -> 0` by Chebyshev at each positive rational threshold, since the corresponding bounds are summable.

### 2. Prefix absorption and the density orientation (lines 142–193)

Deleting `k` entries leaves the limit `a` unchanged and gives

`d(tail_k x)^2 = 4^(-k) lim_N N^(-1) sum_(i=k)^(N+k-1) 4^i(x_i-a)^2 = 4^(-k)d(x)^2`.

The shift of the Cesaro endpoint contributes a ratio tending to one. Any finite real prefix can be inserted, so the map `R^k x C -> C` is a genuine bijection with Borel inverse. In the input mixture, the tail scale is `2^(-k)delta`; the scale measure `d(delta)/delta` is unchanged. The removed first `k` independent Gaussian variables become real coordinates of standard deviations `2^(k-j)d(y)`, exactly the stated product density `q_k`.

In particular, `mu = p_*(q_k dv dmu)` whereas the domain Hilbert measure is `dv dmu`. The unitary multiplier is therefore `q_k^(-1/2)`. Direct substitution gives `integral |f|^2 q_k^(-1) q_k dv dmu = integral |f|^2 dv dmu`; using the opposite square-root sign would fail. The manuscript has the correct orientation. Positivity and finiteness imply two-way equivalence even though the multiplier need not be bounded as a function. The density composition rule follows because prepending `ell` entries replaces the recovered scale by `2^ell d(y)`, aligning every Gaussian factor. No infinite-product equivalence theorem is being implicitly assumed.

### 3. Actions, finite-cut behavior, and rises (lines 195–227)

Translation changes only `a`. Positive dilation changes `(a,delta)` to `(ra,rdelta)` and contributes exactly `r` to the measure. In coordinates `(a,log delta,z)`, the corresponding unitary actions are finite-dimensional continuous actions tensored with the Gaussian identity; density extends their strong continuity to the entire L2 space.

For each **fixed** cut, coordinate and limit equalities are null under the mixture. A convergent sequence whose limit differs from the cut is eventually on one side, so it changes colors only finitely many times. No uniform conull set for all real cuts is needed or claimed. On the other hand, adjacent-pair differences have signs equal to those of independent symmetric nondegenerate Gaussians `z_(2j+1)/2-z_(2j)`. Each sign therefore occurs infinitely often almost surely. Integrating this common Gaussian conull event against sigma-finite parameter measure is legitimate.

### 4. Ordinal concatenation and the free-product isometry (lines 229–318)

Grades below `omega^2` are precisely `omega n + m` with finite `n,m`. For a **specified list of input grades**, inserting a finite suffix into the next infinite block retains every coordinate, and the inverse removes a known finite number of entries from a known block. When the second input has no infinite block, only finite suffixes combine. This is compatible with ordinal addition without pretending that ordinal addition is cancellative. The Borel bijection and two-way measure equivalence follow from the prefix calculation.

A fixed cut decomposes each output word into finitely many maximal convex monochromatic runs. The finiteness includes color changes at limit positions: each of finitely many infinite blocks has finitely many internal changes, and each block boundary adds at most one. A run starting inside an infinite block has a tail still in `C`; a run ending before a later limit has a finite final prefix; any intermediate full blocks stay separate. Thus every run has an admissible grade below `omega^2`.

Conversely, an alternating list of nonempty one-color words has exactly those maximal runs. Distinct lists of grades/colors/patterns have disjoint output supports even if ordinal totals coincide. This distinction is essential: unrestricted concatenation of arbitrary grade lists would not itself be an isometry. Here the countable run charts furnish an orthogonal direct sum, and their canonical unitaries cover the output conull set. That proves the full pointed free-product unitary, not merely an injection.

### 5. Associativity (lines 320–351)

With three time intervals, each parenthesization is identified by flattening with finite reduced words in three centered factors. On an individual chart, grouping two factors only groups maximal strings avoiding the third. Both operations retain the same ordered coordinates, with the same original infinite blocks and identical accumulated finite prefixes. The fixed-chart positive half-density chain rule then equates the operators. Common translation commutes with concatenation and preserves the density formula; the three original factors have shifts `s+t`, `t`, and `0` in both compositions. Vacua and zero times reduce to the canonical identities. Only finitely many cut-null sets enter each identity.

### 6. Separability, time zero, and inverses (lines 239–242 and 353–448)

Each sigma-finite standard-Borel sector has separable L2, and there are countably many sectors. For each nonempty word, the closure of its coordinates is compact: a finite union of convergent sequences and a finite set. Its supremum can equal a prescribed positive time only at a coordinate or block limit; that is a null event. Hence support indicators converge pointwise almost everywhere as positive time varies. At time zero any all-positive nonempty word has at least one fixed positive coordinate and is eventually excluded. Dominated convergence is applied to `|h|^2`, so no finite-total-measure assumption is required.

The sections `P_t h` pass through every fibre vector and form a countable dense fundamental family. The fixed-grade dilation exponent is `n+m`, not the ordinal length; it counts one Lebesgue `a` coordinate per infinite block and one per finite letter. The stated dilation unitaries correctly trivialize positive-time fibres. No local trivialization across the dimension change at zero is asserted.

For full structural continuity, `Q(s,t)` is strongly continuous on the free-product ambient Hilbert space by tensor-product continuity on finite patterns and uniform projection bounds. Each fixed pattern-and-grade elementary vector is sent by a **fixed** concatenation unitary after continuous support projection and translation. Finite such vectors are dense, and the independently established norm bound `||V(s,t)|| <= 1` extends the conclusion. This handles coincident output grades safely. At zero, every term with a disappearing centered factor tends to zero; the surviving single-factor and vacuum terms have the correct limits.

Strong continuity alone need not pass to adjoints. Here the final projection is the already strongly continuous `P_(s+t)`. Expanding the squared distance of `V(p)^*h` and `V(p0)^*h` gives exactly the formula in lines 439–441; its cross term converges by strong continuity on the fixed vector `V(p0)^*h`. Thus the inverse structural maps really are continuous. This is the required missing hypothesis in the usual false inference from strong continuity to adjoint continuity, and the paper supplies it.

### 7. Tensor core and maximality (lines 450–515)

For a fixed finite partition, the ordered tensor image is the full support space on words whose time-cell colors occur latest to earliest. Half-density factors do not change supports. Intersecting the two-cell cuts at rational interior points imposes nonincreasing real coordinates: every out-of-order pair is witnessed by a rational number between its values. The countable union of fixed-cut null exceptions is harmless. Infinite grades have zero measure on this support because an infinite block has infinitely many rises almost surely. Finite grades reduce to strict decreasing simplexes after deleting diagonal null sets.

This gives an upper bound on the all-partition intersection. Every finite decreasing tuple separately satisfies every fixed real-endpoint partition almost everywhere, proving the reverse inclusion without any illicit uncountable union of exceptional sets. Splitting a decreasing tuple at a time cut gives an onto tensor factorization of the simplex direct sum with density one. Any subsystem with inherited ordered tensor multiplication lies in every partition range, hence in this intersection. This proves maximality in the stated category.

### 8. Closed free hull and a nonzero orthogonal remainder (lines 517–571)

The finite-grade projection commutes with all support projections/dilations, and the full run unitary plus its inverse restrict to finite-grade words. Therefore `K` is a closed continuous free subsystem containing `F`; consequently the free hull is contained in `K` before any density argument.

For the other inclusion, almost every finite tuple has distinct coordinates, and some partition with rational interior endpoints separates them into distinct cells. The tensor product of singleton L2 cell spaces maps onto the entire support rectangle in that grade; the distinct cell colors form a reduced free word. There are only countably many such rectangles and their union covers the conull distinct-coordinate set. A vector orthogonal to all these L2 support spaces vanishes almost everywhere. Hence their closed span is the full Cartesian-power L2 space. Completion cannot reach an orthogonal infinite grade.

For positive time, the specified `a`/`delta` region has measure `(t/3)log 2`. The Gaussian failure bound is

`sum_(j>=0) 9/(2500*4^j) = 3/625`.

Every surviving coordinate differs from `a` by less than `t/3`, so it is strictly in `(0,t)`, including the endpoints of the allowed `a` region. The region has measure between `(622/625)(t/3)log 2` and `(t/3)log 2`. Its indicator is therefore a nonzero finite-norm grade-omega vector orthogonal to the whole finite-word hull. Properness is proved for every positive time, not merely almost every time.

## Minor exposition point, not a substantive defect

At lines 532–533, “Every finite-partition free word from F has finite total word length” should be read on homogeneous finite-grade vectors or their dense linear span. A general F-vector can have nonzero components in arbitrarily many finite grades. This does not invalidate containment: the immediately preceding argument has already established K as a closed free subsystem containing F, and the homogeneous-vector density argument also supplies the same conclusion. No manuscript alteration is required for this review to pass.

## Publication boundaries and remaining limits

The substantive result is a counterexample to universal tensor-core generation in the explicitly defined continuous scalar free-product category. The reviewed primary definition and question match this scope. This does not resolve adapted-cocycle questions, classify resulting noises, or establish that an arbitrary chosen extra regularity convention is satisfied. The review also does not establish global novelty, journal acceptance, human verification, or a formal proof certificate. Finite ordinal or Gaussian arithmetic checks would only be diagnostics and were not used as substitutes for the analytic arguments above.

The strongest verified statement is exactly Theorem 1 with the Section 5 continuity convention. No unresolved substantive gap remains within this analytic review scope.
