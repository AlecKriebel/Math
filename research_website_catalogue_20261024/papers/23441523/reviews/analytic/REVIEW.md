# Independent analytic review — Zenodo 23441523

**Paper:** *A polynomial versus superpolynomial gap in vertex-distribution-free graph testing*, Alec Kriebel, version 1.0.0, 17 October 2026.

**Verdict:** No mathematical defect identified in the published theorem. The five-page argument gives a valid all-size polynomial classical tester and a valid transfer of the established adaptive two-sided triangle-testing lower bound. I also reconstructed the longer authored parity/exposure proof supplied in the archive. The theorem is about oracle complexity for one fixed property, with a lower bound along a rational proximity sequence; it does not claim a polynomial-time implementation or a sample-only lower bound when arbitrary-name adjacency queries are free.

This is an independent AI review, not human peer review, formal proof-assistant verification, or a priority/novelty certificate. Archived and parallel review reports were not opened before this verdict. The packaged authored supporting proof contains an introductory sentence reporting an earlier audit status; I disregarded that sentence and evaluated its mathematical argument. No website, spreadsheet, published source, Git, Zenodo or outreach change was made.

## 1. Source binding and reading scope

Primary record: [Zenodo 23441523](https://zenodo.org/records/23441523), [DOI 10.5281/zenodo.23441523](https://doi.org/10.5281/zenodo.23441523). The fresh acquisition receipt reports retrieval at 2026-10-25T00:23:23.993622+00:00. I independently hashed the delivered objects.

| Object | SHA256 |
|---|---|
| Published PDF, 5 pages, 80465 bytes | `a9d81e3b765adc8ee9bee044d23008515e31bbeb57a916358f32e8d3c021a1f0` |
| Source-and-verification ZIP, 301162 bytes | `4367fad39640b11fb1809c2302a91947a9343dd8179590a51ef87e5756caa5cb` |

Read all five published PDF pages and the complete `main.tex`; the complete authored `audit/inputs/PROOF.md` mathematical support; the public verifier; and all six mathematical checker sources under `verification/`. The checker sources are mathematical evidence even though some directory names preserve historical review labels. Archived reports, research logs, root decisions and reviewer verdicts were not consulted as evidence.

Fresh primary references and their hashes are in `primary_source_receipts.json`. Reference PDFs, rendered inspection images and extraction caches are locally ignored. Authored review sources, results, logs, hashes and URLs are retained.

## 2. Exact theorem and model

All graphs are finite, simple and undirected. The distribution is a probability measure on a nonempty vertex set, and each unordered changed pair costs `D(u)D(v)`. Uniform distance is therefore the number of changed edges divided by `n²`, not by the number of unordered pairs. Repairs may add or delete edges.

The fixed property is

`P = {K4-free graphs} ∩ {graphs made 3-colorable by deleting at most one vertex}`.

It contains every 3-colorable graph, is hereditary, is closed under edge deletion, and is extendable by adding an isolated vertex. These claims follow directly from the definitions: an induced subgraph retains the old exceptional vertex if present; deleting edges cannot destroy a valid coloring; an isolated extension leaves both restrictions intact.

The published theorem states:

- A one-sided classical canonical tester works for every nonempty input size, without receiving n, using `O(ε^-6 log(1/ε))` uniform sample calls and `O(ε^-12 log²(1/ε))` adjacency queries.
- Along a sequence of positive rational ε tending to zero, every adaptive two-sided VDF tester has worst-case **total sample-plus-adjacency cost** at least `exp(Ω(log²(1/ε)))` on some inputs. The tester may be given the entire vertex set, n, the complete positive rational weight vector and the heavy vertex.
- Consequently no fixed polynomial in classical canonical complexity and `1/ε` can bound VDF complexity, even after fixed positive constant rescaling of classical proximity.

The property is fixed as ε and the input size vary. Only the input graphs and distributions change. Success probability is at least 2/3 for every member and every ε-far input; no behavior is required inside the proximity gap. The lower bound is worst-case, not an expected-cost theorem as stated. The stronger information gifts do not include adjacency information or a secret correspondence between labels and a hard host graph.

## 3. Independent proof reconstruction

### 3.1 Classical colorability lemma

For a proper partial coloring of S, each uncolored vertex has the colors absent from its already colored neighbors as its list. Empty-list vertices form U. For a vertex with a nonempty list, δ(v) is the smallest number of remaining neighbors whose lists contain one of its feasible colors.

Coloring each nonempty-list vertex by a minimizing color and coloring U arbitrarily yields a 3-colorable repair after deleting at most `n|U|+Σδ(v)` monochromatic edges. There are no monochromatic edges inside the proper partial coloring or between it and a vertex using a feasible list color. Every other monochromatic neighbor of v is counted in the δ(v) upper bound; double-counting only makes the bound conservative. Thus ε-farness implies that U together with vertices having `δ(v)≥εn/2` contains at least `εn/2` vertices.

The potential is the total number of feasible list colors outside S, initially 3n. Coloring any vertex in that latter set, using any feasible color, removes at least `εn/2` colors from other lists. A vertex in U immediately closes a branch. Hence more than `6/ε` successful extension levels are impossible.

The proof is an existence argument over a ternary tree of partial colorings, not an implementable instruction to compute U and W using the sample alone. At each level a fresh independent block supplies the first member of the current U∪W, if there is one. For every fixed possible node address, conditioning on earlier blocks gives failure probability at most `exp(−εℓ/2)`. There are fewer than `3^h` addresses to union-bound. Sharing a block among nodes does not require independence of those nodes. With the declared h and ℓ, total failure probability is at most 1/12.

A proper coloring of all sampled labels would choose a feasible branch at every step, contradicting potential exhaustion. Repeated labels are correctly identified, and a chosen vertex is outside the already colored set on its own path. The argument is valid for small n as well; it does not borrow an asymptotic large-input condition.

### 3.2 From colorability to the fixed property at every input size

Because `C3⊆P`, distance from P is no larger than distance from C3. Hence an ε-far P input is ε-far from C3. For `n≥N=12r²`, two r-sample blocks each fail 3-colorability except with probability 1/12. Their label sets intersect with probability at most `r²/n≤1/12`. A union bound therefore yields two disjoint non-3-colorable induced subgraphs with probability at least 3/4. Deleting one vertex cannot remove both obstructions. The full sample lies outside the “delete at most one vertex” condition, so it is outside P regardless of K4-freeness.

For `1<n<N`, `M=ceil(N log(3N))` samples see every vertex with probability at least 2/3, since `n exp(−M/n)≤N exp(−M/N)≤1/3`. The one-vertex case has no far input. The same tester works in both cases without knowing which applies, and M is at least 2r. Since `h=O(ε^-1)`, `ℓ=O(ε^-2)` and `r=O(ε^-3)`, the stated sample and adjacency bounds follow. Membership in P can be decided by exhaustive search, so no polynomial running-time claim follows from this oracle bound.

One coloring obstruction alone is insufficient: the six-vertex odd wheel belongs to P while failing 3-colorability. Two such obstructions sharing their exceptional center are also in P. The proof's disjointness condition is therefore substantive, not cosmetic.

### 3.3 Exact heavy-apex distance, including arbitrary repairs

Let H be 3-colorable on n vertices, and join it to a universal vertex a with mass 1/2; each tail vertex has mass `1/(2n)`. A minimum tail triangle-deletion repair remains 3-colorable. Its join is K4-free, and deleting a leaves a 3-colorable graph. Each tail deletion has one quarter of its uniform tail cost. This gives

`dist_D(J(H),P) ≤ dist_unif(H,triangle-free)/4`.

For the reverse inequality, take any target F in P, including targets obtained using additions. Let S be tail vertices whose original apex edge was deleted. On the remaining tail vertices F must be triangle-free, since a surviving triangle together with a would form a K4. Retain F on that restriction and isolate S to get a triangle-free repair of H. At most `4n²δ_tail+n|S|` tail edges change. The removed apex edges cost `|S|/(4n)`, yielding the claimed lower bound and therefore equality.

There is no deletion-only assumption on the minimizer F. The argument only uses K4-freeness for its lower inequality and uses 3-colorability for its upper inequality. The latter premise is necessary. A triangle-free 4-chromatic Mycielski graph has triangle distance zero, while its apex join is not in P; finite positive weights then give positive distance from P. This is one of the controls independently checked below.

### 3.4 Tripartite cover and normalization

The three-copy graph L(H) is 3-colorable by part. A triangle projects to three distinct vertices because H has no loops, and its projection is a triangle of H. Thus triangle-free H gives triangle-free L(H).

Triangle-free repair distance can be minimized using deletions: intersecting any repaired edge set with the original set preserves triangle-freeness and cannot raise cost. Project every deleted cover edge to its original edge. At most t original edges are deleted if t cover edges were deleted. Any remaining original triangle would have all six cross-copy realizations of each of its edges intact and would lift to a surviving cover triangle. This is impossible. Hence the minimum number of cover deletions is at least the minimum number of original deletions. The change from n to 3n vertices introduces exactly the factor 1/9 in normalized distance.

Applying the apex identity to this always-3-colorable cover gives

`dist_D(J(L(H)),P) ≥ dist_unif(H,triangle-free)/36`.

The final weights are `D(a)=1/2` and `D(i,v)=1/(6n)`. They are strictly positive rational values and sum to one. The implication from triangle-free H to membership in P also holds. The factor 1/36 is conservative but sufficient; no tightness claim is needed.

### 3.5 Adaptive oracle simulation and quantifiers

Given source graph H with known n, the simulator creates the known labels `(i,v)` and a. Distribution samples can be generated locally without querying H. Apex adjacency, self-queries, same-part pairs and pairs sharing an original vertex are determined locally. Every remaining adjacency answer uses at most one H adjacency query. Adaptivity and early stopping do not change this correspondence: each requested answer is supplied exactly, so the transcript has the correct conditional law.

A run using s samples and e adjacency calls mentions at most `s+2e≤2Q` distinct source vertices if total VDF cost is at most Q. Allowing all induced source adjacencies on those inspected vertices for free only helps the source tester. This is the direction of oracle conversion needed for the lower bound. It does not assert that arbitrary induced-vertex and adjacency-query costs are globally constant-factor equivalent; the reverse conversion may be quadratic. The manuscript supplies the necessary endpoint inequality before its brief convention comparison.

The established triangle lower bound therefore transfers at a constant proximity rescaling. Ordered versus unordered edge conventions and strict versus non-strict thresholds likewise alter only constants. `exp(Ω(log²(1/(cε))))` remains `exp(Ω(log²(1/ε)))` for fixed positive c. The explicit supporting construction below independently supplies a rational ε sequence, so no irrational-weight limit argument is needed.

A universal polynomial upper comparison would bound the VDF cost polynomially along every small rational ε as well. The superpolynomial lower bound along one sequence already contradicts it. The theorem does not need an asserted lower bound for every ε or every input size.

## 4. Load-bearing primary references

The original workshop report's pp. 1138–1139 define the cost as the total number of sample and adjacency calls and pose the comparison for extendable hereditary properties. The [publisher report](https://ems.press/content/serial-article-files/46798) was retrieved afresh; its SHA256 is `f88f89375b4b427312169552c106d6395dd249cacc6040b8eb8b23726a95d8de`.

The [Gishboliner–Shapira arXiv v5 manuscript](https://arxiv.org/abs/1905.09903v5), §1 and Problem 5.6, uses the same product-weight distance and total-cost convention, and asks the claimed comparison question. Its primary text also specifies the canonical induced-sample comparison and a positive result for blowup-avoidable properties. Fresh PDF SHA256: `6ddba2d03267d367dffb8dd3ce23f6f5f6afb36496ee68142c02119d398c2b4d`. This confirms that the result addresses the stated problem rather than a sample-only variant with free unrestricted queries.

The cited TAU address for Alon–Shapira failed during this review. I obtained the [author-hosted Princeton manuscript](https://web.math.princeton.edu/~nalon/PDFS/testdig5.pdf), SHA256 `4062298c6ef20e0ee1dfe469057052a2d713765c6e2e9768352081507293b5ff`. Its font encoding defeats ordinary text extraction, so I rendered and visually read the relevant primary pages: p. 2 for the n-aware adjacency model; p. 4 for the inspected-vertex convention and Theorem 4(ii); pp. 5 and 23 for the explicit undirected non-bipartite consequence; and pp. 24–26 for the adaptive/Yao lower-bound mechanism. These provide the needed `(1/δ)^{c log(1/δ)}` two-sided bound for triangles. The source does not restrict the theorem to canonical one-sided rejection on a witnessed triangle.

The classical colorability citations motivate the method, but the paper proves the conservative all-size bound itself. They are not an unresolved black-box dependency. Bibliographic firstness is a separate question: this review confirms the comparison problem and the imported hardness theorem, not the absence of all earlier or recent solutions. In particular, I did not certify the paper's bounded priority audit or independently complete its missing journal-version and forward-citation search. The manuscript discloses those limitations.

## 5. Authored supporting direct construction

The longer supporting proof is not needed to make the short published reduction valid, but I checked its independent mechanism.

With `B=2^d`, `m=(2B)^d=2^{d(d+1)}` and `K=floor(2^{d²−2d}/d)`, a squared-norm pigeonhole class in `{0,…,B−1}^d` contains at least K vectors. Encoding in base 2B creates no carries in a three-term arithmetic-progression equation. Equal norms then force all three vectors to coincide. This supplies a K-element progression-free set A.

The tripartite host on parts of sizes m, 2m and 3m contains T=mK designated triangles `(x,x+a,x+2a)`. Each edge determines its triangle; the progression-free property excludes extra triangles. Independent even-parity versus odd-parity edge patterns on each designated triangle have identical marginals on at most two edge coordinates. GOOD has no triangle. BAD retains a full designated triangle with probability 1/4, and its triangles remain edge-disjoint. Its exact apex distance is therefore `Z/(4n²)`, with `Z~Bin(T,1/4)` and `n=6m`.

The stated exponential-moment bound `Pr[Z<T/8]≤exp(−T/32)` follows from λ=log 2 and `log 2≤3/4`. Thus `ε_d=K/(1152m)` is a positive rational proximity for which almost all BAD inputs are far.

After a secret uniform relabeling of the host, a newly named vertex has uniform remaining host identity conditional on all previously exposed identities and observations. The unused-name permutation has not participated in previous graph observations. This remains true for adaptive choices of new labels and for locally generated distribution samples. Revealing every induced edge on exposed labels for free strengthens the tester. Until a whole designated triangle is exposed, the parity worlds can be coupled identically; partial pattern conditional distributions agree. Padding the sequence of newly exposed identities to k entries gives a uniform ordered sample without replacement, including for early stopping. The chance of exposing a designated triangle is at most `T(k)_3/(n)_3`, and hence at most `2Tk³/n³` for n≥6.

Correctness on GOOD and on the far fraction of unconditional BAD forces a rejection-probability difference of at least 1/6 for these parameters. Consequently `s+2e≥(n³/(12T))^{1/3}` and total cost `Q≥(n³/(96T))^{1/3}≥m^{1/3}`. The exact rational bounds

`1/(2304 d 2^{3d}) ≤ ε_d ≤ 1/(1152 d 2^{3d})`

make `log(1/ε_d)=Θ(d)` while `log m=Θ(d²)`. This independently produces the claimed superpolynomial sequence without relying on a one-sided triangle witness argument.

The doubled odd-wheel example correctly shows that P is outside the blowup-avoidable class: any internal doubled-class edge creates K4, while independent doubled classes retain a non-3-colorable wheel after any one deletion. Thus the example does not contradict the primary paper's positive theorem for that narrower class.

## 6. Fresh computational evidence

The six public controls were freshly executed in temporary copies by `verification/verify_all.py`, both normally and with Python optimization enabled. All **12 executions passed**, and their mathematical outputs matched the hash-bound expected values. The verifier confirms the checker bytes and rejects optimization-sensitive `assert` statements. Exact fingerprints and execution-mode results are retained in `published_replay.json`; stderr was empty.

The inspected controls cover classical color/list inequalities and parameters, arbitrary weighted repairs, the progression-free construction, parity marginals, exact finite adaptive decision trees and posterior permutation checks, the cover projection, and the doubled-wheel boundary. Their scopes are finite, not universal certificates. Some parameter checks use high-precision Decimal logarithms; those are supporting boundary calculations, not a proof of exact real inequalities. The integer/rational controls use exact arithmetic.

I separately wrote `independent_checks.py`, importing no published checker, catalogue or reviewer result. It passed:

- **74** 3-colorable tail cases on one through four vertices, minimizing over **60,876** arbitrary target graphs in P in total, including additions and apex-edge deletions. All obey the exact heavy-apex identity; 23 cases have positive triangle distance.
- Exhaustive consideration of the **117,649** triangle-free retained-edge subgraphs of the K3 tripartite cover. Every deletion repair projects to a valid source repair; the exact cover minimum is six deletions.
- A triangle-free 4-chromatic Mycielski(C5) negative control, showing the apex identity fails without its tail assumption.
- Shared-center versus disjoint odd-wheel controls, showing that one deletion may erase two overlapping coloring obstructions.
- **97** exact rational parameter cases, d=4 through 100, verifying the ε bounds and the quantitative total-cost inequality.

All these independent tests use integers, rational numbers and finite exhaustive search. Their source hash and exact results are retained in `independent_checks.json`. They support the reviewed reasoning and detect omitted premises, but they cannot establish asymptotic tester lower bounds by finite enumeration alone.

## 7. Strongest supported result and exact gap

**Strongest supported result:** The single fixed hereditary, extendable, edge-deletion-closed property P has an n-oblivious one-sided classical canonical tester with the stated polynomial sample/query bounds, while every adaptive two-sided VDF tester needs `exp(Ω(log²(1/ε)))` worst-case total oracle cost along a positive rational proximity sequence, even with the full positive distribution, vertex set, size and heavy vertex supplied. Consequently the requested polynomial complexity comparison fails, including under constant proximity rescaling.

**Exact remaining gap:** No unresolved mathematical gap was identified in the published theorem or the checked supporting construction. This review is not a formal proof or human peer review, and it does not certify novelty or priority. The result supplies no polynomial running-time bound for exhaustive membership decisions, no matching VDF upper bound, no optimal classical exponent, no lower bound for every ε/input size, and no sample-only hardness theorem when arbitrary-name adjacency calls are unlimited and free. The main result is theoretical oracle complexity, not a demonstrated practical testing algorithm.
