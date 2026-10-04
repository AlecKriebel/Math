# Independent adversarial audit: entropy and asymptotic pairs

Audit date: 2026-10-04 UTC. Target: 30004994 / OWR-9790354-005.

## Verdict

**PASS for the mathematical conclusion and prior-result classification.** The exact unrestricted universal equivalence is false. The frozen packet correctly reconstructs a previously published counterexample: an expansive algebraic action of a countably infinite amenable abelian group, with positive entropy and no distinct whole-group asymptotic pair. No mathematical correction to `verification.md` is required.

**Publication qualification:** omit the repository-coordination section identified in `corrections.json` from a publication copy. That qualification concerns redistribution scope, not the proof. Preserve the frozen originals; if a publication copy is changed, its new hashes must be recorded separately rather than replacing the reviewed identity.

The independent audit found an indexing defect in a displayed formula in the inspected preprint. The packet's explicit coordinate-replacement formula already avoids that defect. Thus this audit does not merely accept the cited theorem: the complete construction has been checked independently.

The original 191,386 controls replayed with byte-for-byte identical output. An independently authored program passed 1,853 additional exact checks. These are supporting controls, not a machine-checked proof of the infinite statement.

## 1. Exactly what was reviewed

The input was the seven-file packet listed in `reviewed_manifest.json`. Its external `SHA256SUMS` had SHA-256

`ff552a0423012fdfaf604fa9a8664f0bbb372928180947239349dc08aa03e61a`.

The mathematical proof file `verification.md` had SHA-256

`fdc52dcef5f14b22ec347680c581235ee0feb33c1041b315ad5df98f51792b23`.

All seven individual hashes were checked before the audit and rechecked at completion. The audit did not modify these files or perform remote writes. `result.json` saying that the independent audit was pending describes the earlier freeze and is not a mathematical inconsistency.

The classification is restricted to the stated universal question. It does not classify all expansive algebraic actions, establish a finitely generated counterexample, or determine the current status of any strengthened residual question. No originality or proof-priority claim is supported or needed.

## 2. Primary-source match

The [official Oberwolfach report](https://publications.mfo.de/bitstream/handle/mfo/3925/OWR_2022_03.pdf?sequence=1), printed pages 140–143, supplies the definitions, exact question, and reference. Page 141 explicitly credits Meyerovitch with failure of the positive-entropy implication for an abelian group. The inspected report has no finite-generation hypothesis in the question. The report's statement about an abelian example should not itself be quoted as explicitly saying “non-finitely generated”; that additional fact follows from the prior paper and construction.

[Meyerovitch's preprint](https://arxiv.org/abs/1701.01318), identified on its first page as version 2, 6 February 2017, gives the relevant Theorem 1.2 on page 2, the cofinite asymptotic definition in Definition 2.6 on page 4, and the construction in Section 4 on pages 12–14. Theorem 1.3 concerns a different homeomorphism example and is not needed. The exact theorem and OWR question pages were rendered and visually inspected; the formula discussed below was separately rendered and inspected. The pinned preprint's actual mathematical contents were read, rather than treating bibliographic metadata as proof.

The [publisher DOI page](https://doi.org/10.1017/etds.2017.126) confirms online publication on 24 January 2018 and the journal citation, *Ergodic Theory and Dynamical Systems* 39(9), September 2019, 2570–2591. Its abstract independently identifies the non-finitely generated abelian algebraic example. The journal full text was not represented as inspected. Targeted title/erratum searches did not reveal a correction or retraction invalidating the result; this limited negative search is not a proof of absence. The currently served arXiv record still identifies v2 as its latest revision.

The direct versioned arXiv URLs initially returned a web cache failure. The unversioned official record and PDF were successfully retrieved and explicitly identify v2; this is a verified alternate route, not an inferred version match.

## 3. Source-formula caution, already repaired by the packet

On preprint page 13, the displayed formula (37) uses an index of the form g multiplied by chosen h_n, while the choices are described as h_n different from the distinguished gamma_n. Literally this need not index E. For example, in the first factor take gamma_1 nonidentity and g=gamma_1. The allowed choice h_1=identity leaves g unchanged, still excluded from E. The indicated free-coordinate value is then undefined.

A correct formula replaces each distinguished coordinate by h_n. In multiplicative notation it uses g multiplied by gamma_n^{-1} h_n in each replaced coordinate. The packet says exactly to replace coordinates, and does not copy the defective product index. This corrects the presentation defect without changing X or the theorem. No claim is made about whether the journal version retains or fixes this display.

There is also no need to rely on shorthand in the preprint's finite-support calculation: directly applying the zero-sum equation to a fiber with one supported coordinate yields that coordinate equal to zero. The packet does this explicitly.

## 4. Independent mathematical challenge

### 4.1 All target hypotheses

Let H_n be the vector space of dimension n+1 over F_2, for n at least 1. Its order is q_n=2^{n+1}. The direct sum G is countable, infinite, discrete and abelian. Its increasing finite subgroups F_N exhaust G. For each fixed s, translation by s fixes F_N for all sufficiently large N; therefore these F_N form a Følner sequence. Every finitely generated subgroup is contained in one F_N, so G is not finitely generated.

The binary product indexed by countable G is a compact metrizable abelian group. Each fiber-sum equation is a continuous homomorphism to F_2, so their joint kernel X is closed and is a compact metrizable abelian group. Shifts preserve every equation and are continuous group automorphisms. In particular, the zero point belongs to X.

Put coordinate zero first in the summable product metric. Any disagreement can be shifted to that coordinate and has distance at least 1/2. Hence 1/4 is a strict expansive constant. Neither finite type nor a finite presentation is required by the question.

Faithfulness is not a missing hypothesis in the target, but also holds. Given nonzero s, choose each distinguished a_n nonzero and, when s_n is nonzero, different from s_n. This is possible because q_n is at least 4. Then both 0 and s belong to E, and their values can be prescribed differently using the extension below. Thus the shift by s is not the identity automorphism.

### 4.2 Global extension, not merely locally allowed patterns

Fix nonzero a_n in each H_n, and let E consist of elements having no a_n coordinate. A group element has only finitely many nonzero coordinates, so its set I of a_n coordinates is finite. Replacing every coordinate in I by an arbitrary value other than a_n produces another element of G, now in E. Thus the packet's finite sum of prescribed w-values is well-defined for every group element and every function w on E.

Fix a fiber direction n and the values of all other coordinates. For its a_n entry, the replacement sum separates into a sum over b in H_n excluding a_n. Each inner sum is exactly the value defined at the corresponding b-entry of the fiber. In characteristic two, summing those b-values together with their sum gives zero. This reasoning applies to every direction and every translated fiber, including directions beyond an arbitrary finite observation window. Consequently the extension satisfies all infinitely many defining equations at once.

For a finite window F_N, every allowed value at an a_n coordinate is determined by the same fiber equation from values with one fewer distinguished coordinate. This induction gives injectivity of restriction to E intersect F_N. For surjectivity, an arbitrary assignment there may be extended arbitrarily to all of E and then extended by the preceding formula. Because all tail a_n are nonzero, E intersect F_N has exactly the product of (q_n-1), for n from 1 to N, elements. Hence the number of globally realizable F_N-patterns is exactly 2^{D_N}, where D_N is that product.

This resolves the main potential gap: a finite-stage nullspace count by itself would not show global realizability. Here realizability is established explicitly. The construction would fail as written if a_n were zero infinitely often, since I(0) could be infinite. The packet expressly chooses every a_n nonzero.

### 4.3 Exact entropy, both directions

The partition by the value at coordinate zero is clopen. Its F_N join has exactly 2^{D_N} nonempty atoms. This proves the entropy lower bound using actual globally realized patterns.

For the upper bound, any finite open cover is refined by a partition on some finite coordinate set K: use the cylinder basis and compactness, and combine the finitely many coordinate sets. Enlarge K to include zero. Once F_N contains K, its translates of K cover exactly F_N. In the chosen left-shift convention, pullbacks use K-F_N; because F_N is a subgroup containing K, this is still F_N. Therefore the joined cylinder partition has exactly the same number of atoms, and bounds the entropy of the original cover. Taking the supremum over covers proves

h = log(2) times the infinite product over n at least 1 of (1-2^{-(n+1)}).

The infinite product is the decreasing limit of its partial products P_N. The elementary finite inequality product(1-u_i) at least 1-sum(u_i), followed by a limit, gives P_N at least 1/2+2^{-(N+1)}, and hence the limit at least 1/2. Thus h is at least log(2)/2 and is strictly positive. No decimal estimate is used for positivity.

The report uses natural-log units. If the source's algebraic-action entropy notation is read as Haar-measure entropy, the same value follows directly: restriction onto each finite pattern group is a surjective compact-group homomorphism, so normalized Haar measure projects to the uniform distribution on its 2^{D_N} elements. The coordinate partition generates the Borel sigma-algebra under shifts. Its Shannon entropy rate is therefore the same displayed value. The counterexample is unaffected by this convention.

### 4.4 Whole-group asymptotic pairs and the fresh-coordinate obstruction

For a binary subshift, a pair is asymptotic outside every finite subset of G exactly when its difference has finite coordinate support. If the support is infinite, shifting each differing coordinate to zero gives infinitely many distinct shifts with distance at least 1/2. If the support S is finite, choose a finite coordinate window K leaving metric tail less than epsilon. Only shifts in the finite set K-S can move S into K. Every other shift has distance less than epsilon. This proves both implications with the required whole-group quantifier. On a compact space, uniform equivalence of compatible metrics also makes this condition independent of the particular chosen product metric.

If z in X has finite support S, choose one factor direction n outside the union of the supports of all elements of S. Along any fiber g+H_n through g in S, every point except g has nonzero n-coordinate and lies outside S. The defining parity equation then has only the term z(g), forcing it to be zero. This holds for every g in S, so z=0. Differences of points of X remain in X, proving that all asymptotic pairs are diagonal.

There is no conflict with the freedom to prescribe arbitrary values on E. A free-coordinate delta generally extends to infinitely many nonzero coordinates. The interpolation is an isomorphism of compact groups to a binary product indexed by E, but it is not asserted to conjugate the G-action to an ordinary full shift on that set.

### 4.5 Boundaries that do not invalidate the conclusion

- The action uses a non-finitely generated group, which the exact target allows.
- Convergence outside finite subsets of the entire group is different from forward-time convergence for a single transformation.
- If all factor orders were 2, positive finite entropy ratios would tend to zero. The growing factor orders and the infinite-product bound are essential.
- Nonzero finite-window codewords do exist, but extending them by zero outside that window violates a fresh-direction equation. Local admissibility cannot be substituted for global support.
- A universal equivalence is disproved by this one positive-entropy example without distinct asymptotic pairs. No proof of a new theorem about the reverse implication is necessary.

## 5. Independent computational controls and exact bounds

Run `python3 independent_tests.py` in this audit directory and compare stdout to `independent_results.json`. The program has no third-party dependencies and does not import the author's implementation. It uses set-based Gaussian elimination and explicit configuration enumeration, rather than the packet's integer-bitset implementation. Its checks remain enabled under `python3 -O`.

Coverage includes:

- Nullspace dimensions for six finite shapes, including the actual initial factors (4,8,16).
- Full enumeration of 131,328 binary configurations across three small shapes, with exact admissible counts.
- Bijection to punctured-coordinate assignments for all 40 distinguished-coordinate choices in those shapes.
- Eleven exact restriction-map image dimensions, including nonzero tail cosets, proving finite-level surjectivity rather than just comparing dimensions of separate spaces.
- Fresh-factor constraints of orders 2 and 4, forcing the old-window-supported kernel to zero, with explicit rejection of nonzero zero-extensions.
- Thirty fiber equations for a deterministic function defined on all finitely supported free-coordinate tuples, including sparse tail coordinates beyond the finite boxes used for rank tests.
- Nontrivial translation controls, the defective source-formula indexing control, and exact rational product and logarithm bounds.

For each N, the tail sum is 2^{-(N+1)}, so

P_N times (1-2^{-(N+1)}) <= P_infinity <= P_N.

For log(2), use 2 times the sum over k at least zero of 1/((2k+1)3^{2k+1}). Truncating after m terms underestimates log(2), and the remaining tail is at most

2 / ((2m+1)3^{2m+1}) divided by (1-1/9).

The audit uses N=60 and m=32 and stores the exact rational endpoints in `exact_bounds.json`. Their products yield the certified, outward-rounded interval

0.400345307777 <= h <= 0.400345307778.

These decimal endpoints are exact rational bounds, not floating-point estimates. The simple symbolic lower bound log(2)/2 remains sufficient for the result.

## 6. Corrections and publication limits

`corrections.json` separates three issues:

1. No required mathematical change to the frozen packet.
2. A source-indexing caution that is already resolved by the packet's coordinate-replacement construction.
3. Removal of repository-coordination prose from a redistributable copy under the stated scope limit.

This audit's portable directory contains only authored analysis, scripts, numerical output, and hashes. It contains no source PDFs, rendered source pages, extracted full text, raw source corpus, or private coordination snapshots. The seven frozen originals remain separate and unchanged. Any later editing or publication requires a fresh manifest for the new bytes; this audit's input identity must not be silently repointed.
