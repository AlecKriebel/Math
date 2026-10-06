# Second independent mathematical review: SIRSN tree obstruction, ID 9700036

## Decision and exact scope

**ACCEPT: resolved by prior literature, with the pinned application clarification and source-proof repair used together.** No remaining mathematical gap was found in that combined argument. This is an independent AI mathematical/source review, not human peer review, formal proof verification, or an exhaustive novelty search. The obstruction is credited to David Aldous's 2021 theorem. Applying it to this numbered problem and checking its route conventions are explicitly identified in the target as an inference.

The original author archive is retained as historical input, not accepted without the correction. The acceptance applies exactly to:

- `SIRSN_TREE_9700036_CLARIFIED_SAFE.zip`: 12,085 bytes; SHA-256 `6b2264154ecdd680c2fd888d1d8c63d0b6bd0a3ba174dcece23b4fed677fe0a1`.
- Its `RESULT.md`: 10,540 bytes; SHA-256 `88a73cdede0a1513d05d9834f693b2446b94e6e8dbe688da17872d7cdc6ef5aa`.
- `SOURCE_PROOF_REPAIR_V1.md`: 12,374 bytes; SHA-256 `5d6598108c9fc3aacc7d127eb16da1af1f2ca3a4654222864036963df6ceddeb`.

The original archive and both external manifests are bound in `TARGET_BINDINGS.json`. Any substantive revision requires a new review against new pins. No third-party source text, source PDFs, dataset contents, exact corpus records, or private coordination material is included in this review package.

## 1. Sources actually checked

The controlling source is David Aldous, *Route lengths in invariant spatial tree networks*, Electronic Communications in Probability 26 (2021), article 31, DOI [10.1214/21-ECP401](https://doi.org/10.1214/21-ECP401), [published repository PDF](https://escholarship.org/content/qt25v3q7sd/qt25v3q7sd.pdf). I read Theorem 1.2, the translation-invariance footnote, the entire proof in Section 2, and the pair normalization in Section 3.1. I compared Theorem 2 of [arXiv:2103.00669](https://arxiv.org/abs/2103.00669). The published theorem concerns pair distances averaged over a disk, not the conjectural assertion at every exact separation.

I checked the sampling, route compatibility, measurability and finite-mean axioms in Sections 2.2–2.3 of *Scale-invariant random spatial networks*, EJP 19 (2014), article 15, DOI [10.1214/EJP.v19-2920](https://doi.org/10.1214/EJP.v19-2920), [published PDF](https://emis.de/ft/43138), and its Open Problem 10. I also checked Open Problem 36 and the route topology in Appendix A of the [long 2012 manuscript](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf).

All four existing local PDFs were independently rehashed and freshly text-extracted. Their byte hashes and public URLs appear in `SOURCE_CHECKS.json`. The public web reader separately confirmed the 2021 published and preprint versions and the 2014 article. No new remote byte-for-byte match is claimed. The direct DOI reader failed; the verified repository PDF supplied the published text.

## 2. Sufficient precise obstruction

The repaired proof uses only the following hypotheses:

1. The terminal process has the unit-rate planar Poisson marginal.
2. Its joint law with the designated routes is translation invariant.
3. Routes are measurable, simple compact rectifiable arcs.
4. For each finite terminal set, all its designated routes form a finite topological tree, with the original arc lengths and unique connecting paths.

Under these assumptions there is a finite radius r for which the pair-intensity normalized route length D_r has infinite mean. Every larger radius then also has infinite mean. Independent route sampling, joint ergodicity, scale invariance, straight edges, and finite vertex intensity are unnecessary for this obstruction. The original SIRSN axioms are used later to obtain a finite unconditional mean.

Here is a complete audit of the repaired proof, including the delicate steps.

### 2.1 Balanced squares and local pairs

Use full-width/full-height fifth-strips of an m-square. The two printed unit-side intervals in the source have the wrong area; replacing their side 1 by m gives the intended Poisson means and makes the subsequent square-translation argument valid. Each strip has population between 0.196m² and 0.204m², so a balanced square has population between 0.98m² and 1.02m².

If a balanced m-square has blue count y in [0.1,0.88]m², its red-blue pair count is at least y(0.98m²−y) ≥ 0.088m⁴; every pair is within distance √2m. For adjacent balanced squares, if one has blue count below 0.1m² and the other above 0.88m², translate an m-square between them by fifth-strip steps. At the first crossing of the lower threshold the count is at most 0.304m², because at most 0.204m² blue points are added. Thus an intermediate square qualifies. Each translated square still consists of five controlled strips and has total count at least 0.98m². This proves the local bound in either orientation.

### 2.2 A coloring-uniform contour event

Declare grid sites bad independently with probability q₀=2⁻¹⁰⁰⁰, and write p=1−(1−q₀)²≤2⁻⁹⁹⁹ for the probability that an adjacent pair has a bad endpoint. A contour of ℓ distinct edges contains at least floor(ℓ/7) crossed primal pairs with disjoint endpoints. For ℓ≥28, fewer than ℓ/20 good selected pairs implies at least ℓ/20 bad ones. Independence and a subset union bound give probability at most 2^ℓ p^(ℓ/20).

There are at most 4k²3^ℓ candidate directed contours of length ℓ in a k-grid. This also bounds nonbacktracking edge-simple walks, so any harmless local resolution of fourfold dual contacts does not invalidate the count. Since 6p^(1/20)<2⁻⁴⁷, the probability of a failing contour with ℓ>log k is bounded by 4k² times the sum of 2⁻⁴⁷ℓ over those lengths. With natural logarithms this tends to zero.

For a zero-good-edge circuit enclosing a fixed site, choose at least ceil(ℓ/7) disjoint pairs. Its probability is at most p^(ℓ/7). Counting candidate circuits by 4(2ℓ+1)²3^ℓ and using p≤2⁻⁷⁰ bounds the enclosing probability by

4 sum_{ℓ≥4} (2ℓ+1)²/256^ℓ ≤ 4(9/256)^4/(1−9/256) = 6561/1035993088 < 1/20.

Let X_k count sites enclosed by any zero-good-edge circuit of length at most log k. These events depend only on bad sites within distance log k+1. Therefore E X_k≤k²/20 and Var X_k≤k²(4log k+5)². Chebyshev gives P(X_k>k²/10)→0. The larger dependence radius in the repair is correct; merely using log k as an independence separation would be insufficient.

Both good events are properties of the bad-site configuration alone, so they are simultaneous for every network-selected coloring. Bernoulli domination lets the same conclusions apply to any independent bad-site probability at most q₀.

### 2.3 Contour geometry and a movable excluded square

Consider a coloring with at least 0.20k² sites of each color. Resolve fourfold contacts without crossings; contours are edge-disjoint. They may be understood as infinitesimally separated Jordan curves, retaining the same discrete edge lengths and crossed primal pairs.

If contours longer than log k have total length greater than k/10, the preceding event supplies more than k/200 distinct good boundary edges. No matching is needed at this stage and no factor of two is lost.

Otherwise their total length is at most k/10. A circuit of length c encloses at most c² sites. A boundary-to-boundary contour this short cannot join opposite sides; its smaller boundary cap also contains at most c² sites. Summing squares bounds the union of long interiors by k²/100. Interiors of short boundary paths lie in the boundary strip, containing at most 4k log k sites. For sufficiently large k this is at most 0.01k².

The maximal-contour argument is sound here: after removing maximal boundary caps and circuit interiors, the remaining exterior is connected, with one color. Noncrossing caps are disjoint or nested, and the small total length excludes a contour crossing between opposite sides. Consequently sites of the other color lie in contour interiors. After discarding the long interiors and short boundary caps, maximal short circuits with disjoint interiors enclose at least (0.20−0.01−0.01)k²=0.18k² sites. Any site there not counted in X_k belongs to a circuit with at least one good edge. Each circuit encloses at most log²k sites, so the number of distinct good edges is at least 0.08k²/log²k. For large k this exceeds k/200. This confirms the necessary uniform edge bound.

Start now with both color fractions at least 0.21. Recolor an arbitrary s-by-s square, s=ceil(k/1000), to one color. For k≥8000, s≤k/800; both fractions remain above 0.20 because 0.21−1/640000>0.20. At most 4s boundary edges touch the recolored square. Removing them from the k/200 good edges leaves at least k/1000−4≥k/2000 good edges with both endpoints outside the square. The conclusion is simultaneous over every location of the square. Subtracting its perimeter from the source's weaker printed k/400 bound would not establish this; the stronger intermediate bound is essential.

### 2.4 Poisson terminals, the corrected color fractions, and pair counts

For an m-square, ten Chebyshev bounds give q_m≤125000/m². Thus m=2^510 suffices for q_m≤q₀. If M is its population, Cauchy–Schwarz gives E[M 1_bad]/m²≤sqrt((1+m⁻²)q_m)<1/2000. For k² independent squares, with probability tending to one their combined bad-square population is at most 0.001m²k² and their total population N is at least 0.99m²k². The explicit exceptional bounds in V1, 4000000(1+m⁻²)/k² and 10000/(m²k²), follow directly from Chebyshev.

The finite terminal hull has a terminal-weighted centroid. All branch weights are at most N/2; include the centroid as a singleton group if it is itself a terminal. These groups can be divided into two classes between N/3 and 2N/3: use a group already between N/3 and N/2, or accumulate smaller groups until passing N/3. Thus each terminal color has at least 0.33m²k² points, and every cross-color route passes through the centroid.

Among balanced squares let S count blue populations in [0.09,0.89]m², and S<, S> those below and above. The correct bounds are

0.24k² ≤ 0.8S+0.93S>+0.001k²,
0.20k² ≤ 0.89S<+0.8S+0.001k².

The second line uses the red upper bounds 1.02, 0.93 and 0.13 in the three square classes. When S≤0.005k², these give S>/k²≥47/186>0.21 and S</k²≥39/178>0.21. The latter is below 1/4, so the printed symmetric 1/4 conclusion cannot be inferred. The repair correctly changes the contour margin instead of assuming a symmetry that these thresholds lack.

Color squares at the threshold 0.1m². There are at least k/2000 good opposite-color adjacent pairs outside any excluded square. Splitting grid edges into four matchings leaves at least k/8000 disjoint pairs of squares. The local pair lemma gives distinct close cross-color terminal pairs numbering at least β₀m⁴k, where β₀=0.088/8000=11/1000000.

If instead S>0.005k², at least 0.004k² such balanced squares remain outside the exclusion. Each supplies at least 0.08m⁴ internal cross-color pairs; their total is more than β₀m⁴k. No terminal-pair duplication occurs, because the relevant squares or pairs of squares are disjoint.

### 2.5 Geometry and stationary pair normalization

Write n=mk and h=n/10000. A grid-aligned square of side sm can cover the intersection of [0,n]² with the centroid's L-infinity h-neighborhood: each coordinate interval has length at most 2h, and rounding requires at most 2h+2m≤sm. Clamp at the domain boundary. If a coordinate intersection is empty, every terminal is already farther than h from the centroid.

The counted endpoints outside this square are each at least h from the centroid. Their route passes through it, so its length is at least d_k=n/5000, while separation is at most r=√2m. The high-probability event therefore gives at least β₀m⁴k such unordered terminal pairs. A measurable selection of the centroid is not required: the resulting lower bound concerns a measurable pair count and holds whenever a suitable centroid exists.

For large k the expected count is at least β₀m⁴k/2. Translation invariance gives the upper bound

(1/2)n²πr² P(D_r≥d_k)=πm⁴k² P(D_r≥d_k).

To see this precisely, anchor the first endpoint in [0,n]² and allow the second anywhere within distance r. The expected marked pair measure is area times its translation-invariant intensity. Requiring the second endpoint to remain in the square can only reduce the count; division by two accounts for order. No route-length/displacement independence is used. Hence P(D_r≥d_k)≥β₀/(2πk).

Because d_{k+1}−d_k=m/5000, integrating the monotone tail on successive intervals gives a positive multiple of sum 1/(k+1). Therefore E D_r=∞. Enlarging r retains the infinite pair-length numerator while dividing by a finite disk area. This establishes the exact sufficient obstruction under the four stated hypotheses.

## 3. Measurability and finite-hull application

A jagged SIRSN route, with its endpoints included, is a compact simple rectifiable arc. Its infinitely many polygonal pieces can accumulate at endpoints; this does not introduce infinitely many branch vertices into a finite terminal hull.

Use the countable event A that every triple of distinct sampled terminals satisfies R(x,y)⊆R(x,z)∪R(z,y). Poisson points admit a measurable enumeration. The route image is a measurable compact set in the source setup: Appendix A's route convergence controls finitely many interior segments and vanishing endpoint tails, which implies Hausdorff convergence. Union is continuous on compact sets, and compact-set inclusion is closed. Thus A is measurable. Quantification over every triple makes it translation invariant, independently of enumeration.

Compatibility makes two root routes intersect in a compact initial subarc. Adjoining another root route to a finite union intersects that union in the largest of finitely many such initial subarcs. Its remaining suffix therefore attaches once. Induction gives a finite rectifiable topological tree H_F for the root routes to any finite terminal set F. On A, the triple condition with the root as z puts every other pair route inside H_F; simplicity then makes it its unique connecting arc. This proves the arbitrary-finite-hull property, not just a three-terminal assertion.

Every globally circuit-free sampled network lies in A. Conversely, failure of one inclusion gives a finite circuit: the offending route has an excursion outside the compact two-root-route tree, whose distinct excursion endpoints are joined by the unique arc inside that tree. The two arcs form a circle. No equivalence between finite hulls and the topology of an infinite union is assumed or needed.

## 4. Conditioning and the contradiction

Before conditioning, the measurable SIRSN sampling construction uses Poisson points independent of its route mechanism. Scaling and Euclidean invariance give E L(x,y)=Δ|x−y| with Δ<∞. For a bounded Borel anchor set B of positive area, the two-point Poisson formula and Tonelli give

E sum_{x∈Pi∩B, y∈Pi, 0<|y−x|≤r} L(x,y)
= |B| integral_{|z|≤r} Δ|z| dz = |B|2πΔr³/3.

The expected ordered-pair count is |B|πr², giving E D_r=2Δr/3. This is a pair-intensity/Palm normalization, not nearest-neighbor sampling or a uniformly selected realization followed by a pair. The use of SIRSN measurable finite-dimensional distributions suffices; a stronger uncountable jointly measurable route field need not be imposed.

Suppose P(A)=p>0. The conditioned joint law is translation invariant. Its Poisson marginal is unchanged: for any bounded local function f of Pi, averages of its translates over growing squares converge in L1 to E f under the Poisson law. One can prove this directly by finite-range independence of sufficiently separated local observations, or by Poisson ergodicity. Invariance of A makes the conditional expectation of each average equal to E[f|A]; unconditional L1 error divided by p bounds the conditional error. Consequently E[f|A]=E f. Bounded local functions determine the point-process law.

This uses ergodicity only of the Poisson marginal. The joint network may be nonergodic, and conditioned routes need not be independent of Pi or scale invariant. Their anchored length expectation is nonetheless at most its unconditional value divided by p, so the conditioned normalized mean is at most 2Δr/(3p)<∞ for every r. On A, Sections 2–3 give finite hulls and all the other obstruction hypotheses. The infinite-mean conclusion contradicts this finite bound. Therefore P(A)=0.

Almost surely a finite three-terminal route union contains a circuit. In particular S(1) cannot be a tree, even with positive probability. This is the requested full obstruction; it does not address how many cycles occur or any other problem ID. The same reasoning covers a weak SIRSN under the stated finite-mean and sampling axioms.

## 5. Verification boundary

The accompanying script rechecks immutable target bindings, archive membership pins, exact constant inequalities, and selected threshold calculations. It supports but does not replace the mathematical argument above. Source extraction and hashing establish what was inspected, not the truth of a theorem. This review makes no claim that a small finite computation certifies continuum topology, a Palm argument, or an infinite-volume probability limit.
