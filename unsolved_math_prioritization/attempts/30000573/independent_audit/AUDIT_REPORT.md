# Independent adversarial audit: chaotic operators on nuclear Fréchet spaces

Problem 30000573, OWR-1323-010, rank 813. Audit date: 2026-10-06 UTC.

## Verdict

**Accept the frozen packet as a correct, explicitly scoped partial-results checkpoint. The original problem remains unsolved by this work.** No substantive mathematical defect or required correction was found in the five authored approaches. This is a fresh mathematical and reproducibility audit, not peer review, formal verification, or a claim of originality.

The audited author ZIP contains 10 files, is 19,303 bytes, and has SHA-256 `5c52306f764afdbda9c2520fa54a02c068cbbe8c61ef6899a11116eac0d57000`. Its manifest SHA-256 is `36bedb158def6832a026b31ad1d249aad1745710eef914ba1cf7f5e91a6a68e6`. The audited packet is an editorially redacted distribution with unchanged mathematical content. Its proofs, diagnostic code, and computed results are byte-identical to the previously audited versions. This audit is a separate artifact.

The accepted conclusions concern the countable product, an intertwining obstruction, one explicitly specified nuclear Köthe space, one failed diagonal-plus-shift construction, and scalar-plus-finite-rank operators. None is an existence theorem or counterexample for all nuclear Fréchet spaces.

## 1. Statement, conventions, and provenance

The entire supplied problem record and its absent associated report were checked, with the absent report represented by `{}`. Default Python sorted-JSON serialization of their pair has length 3,388 bytes and SHA-256 `a793ed8d4861266772759842273abfac389f345b3bced87a2ffecd648bf9673f`, agreeing with the catalog. The statement hash and all three complete corpus byte counts and hashes also agree. No source record or corpus contents are included in this audit release.

The question was independently compared with the text and a fresh rendering of printed p. 2271, PDF page 45, of the [Oberwolfach report](https://ems.press/content/serial-article-files/46067?nt=1). It concerns arbitrary infinite-dimensional nuclear Fréchet spaces. The neighboring question about hypercyclicity of every nonzero scalar multiple is a different problem. The report's chaos terminology is hypercyclicity together with dense periodic points. The packet does not substitute distributional or Li–Yorke chaos for it.

The nonzero assumption in the product theorem is appropriate. If E is zero, its product is a singleton and ordinary sensitivity-based Devaney terminology becomes degenerate; that case is neither needed nor claimed. A nonzero real or complex topological vector space has no isolated points. For nonzero E the product is infinite-dimensional, so the packet's dense-orbit/dense-periodicity convention is compatible with the intended setting. Finite-dimensional nonzero targets are not counterexamples to the question, whose hypothesis is infinite-dimensional.

The field distinctions are maintained: the product construction, factor obstruction, strong stability, and finite-rank argument work over R or C. The displayed root-of-unity example and the imported basis-class existence result are complex results. No general real-space existence claim is accepted through a complex citation.

## 2. Independent mathematical checks

### Preliminary topological facts

The separability argument is valid. Each Banach completion associated with a defining seminorm is the closure of a nuclear map's range and therefore separable. The canonical map from E into the countable product of those completions is a topological embedding, not merely an injection. A countable product of separable metric spaces is second countable, so its subspace E is separable. This avoids the false general inference that every subspace of any separable topological space is separable.

The nonnormability argument is also valid: on a nuclear Banach space the identity is nuclear and hence compact, forcing finite dimension. A continuous norm need not determine the topology. The proof does not conflate those two properties or derive a basis from nuclearity.

### Approach 1: the product shift

Continuity is immediate from coordinate projections in the product topology. Basic open sets may prescribe arbitrary finite coordinate sets; extending each prescription to an initial block gives exactly the cylinder form used in the proof. For every sufficiently large displacement the initial and shifted blocks are disjoint, which proves mixing for all such displacements, rather than just one return time.

Finite words over a countable dense subset form a countable collection. Their concatenation produces a single dense forward orbit. Repeating any permitted finite block gives a periodic point in each cylinder. These arguments work even if the factor E has no basis or continuous norm. For nuclear E, domination of product seminorms by finitely many coordinate seminorms reduces the nuclearity check to a finite direct sum of nuclear canonical maps. Completeness and metrizability follow from the countable product construction.

The precise scope is E^N. Neither a complemented copy of E in its product nor a projection onto E supplies an invariant factor automatically.

### Approach 2: intertwining

For a continuous norm p on the target, continuity of p composed with A implies that it vanishes on a sufficiently long coordinate tail. One can see this without any operator-norm assumption: the controlling product neighborhood puts no restrictions on that tail; scaling a tail vector arbitrarily forces its p-image to be zero. Definiteness of p then gives A equal to zero on the tail.

Let A_j be the restriction of A to coordinate j and choose L with A_j=0 for j at least L. The identity AB=TA at input coordinate L gives A_(L-1)=T A_L=0. Descending induction gives every earlier A_j=0. Finally, every input splits into a finite prefix and a tail killed by A. This last step is essential; vanishing on finite-support sequences alone would otherwise require a separate density argument.

The case L=0 is immediate. No Banach topology or continuity of a norm inverse is assumed. The boundary equation at input L cannot be removed by a finite truncation. The dense-range factor lemma is independently correct: every nonempty target open set has a nonempty open inverse image, and periodicity passes through the intertwining identity.

### Approach 3: the lacunary Köthe space

The weighted l1 completions are compatible; finite sequences are dense in every defining norm. Completeness of the projective intersection and unconditional convergence of coordinate expansions follow. Between consecutive completions the diagonal nuclear coefficients are 2^(-2^j), a summable sequence. The ratio of consecutive defining norms on e_j is unbounded, so no one of these norms generates the topology. In particular p_0 is a continuous norm without normability.

For the shift, the estimate on p_0 alone gives constants C at least 1 and an integer m at least 0 with |w_j| at most C times 2^(m 2^j). At output coordinate r of W^n, the weights are exactly w_(r+1) through w_(r+n). The exponent sum is 2^(r+n+1)-2^(r+1), so no endpoint has been dropped. Writing s=r+n and q=k+2m+1, the ratio of its p_k coefficient to the p_q coefficient of x_s is at most

    C^n 2^[-2^s + k(2^r-2^s) - m 2^(r+1)]
    ≤ C^n 2^(-2^n).

Summing over s at least n gives the authored all-seminorm estimate. Its factor tends to zero for each fixed C because 2^n dominates n log_2(C). Thus the argument proves convergence for every vector and every defining seminorm, with zeros and arbitrary phases in the weights permitted. It is not an extrapolation from finite supports or sampled weights.

A nonzero periodic vector would contradict convergence along its period multiples. A nonzero coordinate functional maps every orbit to a convergent scalar sequence, so no such orbit can be dense. The argument excludes weighted backward shifts only. The complex space has an unconditional basis and therefore is in the previously resolved positive class for unrestricted operators; it is not a counterexample to the original question.

### Approach 4: periodic density without hypercyclicity

For j at least 1 the chosen diagonal entries are distinct roots of unity on the short first-quadrant arc, separate from lambda_0=-1. The diagonal part preserves each defining norm. Since the weights have modulus at most 1 and the coordinate weights increase, the backward-shift part is bounded in each of those norms.

The finite-support right-eigenvector formula satisfies the coordinate recurrence including its top coordinate. Its triangular diagonal is a product of nonzero eigenvalue differences, so the first N+1 vectors span the first N+1 coordinates. Finite sums are periodic because a common multiple of their periods exists. This proves periodic density in the actual infinite-dimensional topology.

The left-functional recurrence has the correct sign. Since |-1-lambda_j| is at least 1, its coefficients have modulus at most 1. Consequently the series defines a continuous complex-linear functional bounded by p_0, with value 1 at e_0. Checking the recurrence on coordinates and extending by continuity gives fT=-f. Every orbit's image is confined to two scalars, so hypercyclicity is impossible. The failed construction is rigorously diagnosed, not merely observed numerically.

### Approach 5: finite-rank and compact perturbations

If fT=lambda f and f is nonzero, its image is the entire scalar field. The projected orbit is bounded for |lambda| at most 1; for |lambda| greater than 1 it either equals zero or omits a neighborhood of zero. It cannot be dense. This includes lambda=0 and both fields.

In an infinite-dimensional Hausdorff locally convex space, the finite-dimensional range of F is closed and proper. Its Hausdorff locally convex quotient has a nonzero continuous functional, yielding a continuous annihilator of the range and hence the required eigenfunctional for lambda I+F.

The packet properly distinguishes this elementary hypercyclicity obstruction from the cited compact-perturbation obstruction to chaos. For Fréchet spaces, the relevant compactness notion requires a zero-neighborhood with relatively compact image; merely sending bounded sets to relatively compact sets is insufficient. Nuclearity does not make every continuous endomorphism compact in that sense.

## 3. Imported results and literature limits

The [14-page arXiv v1](https://arxiv.org/pdf/1005.1416v1) was checked at Theorems 2.4 and 3.1 and their proof sections. The first requires a separable complex space with continuous norm and an unconditional Schauder decomposition; the second treats an infinite-dimensional complex space with an unconditional basis without requiring a continuous norm. The surrounding infinite-dimensional convention matters. The [9-page v2](https://arxiv.org/pdf/1005.1416v2) announces the Fréchet extensions in the introduction and cites a separate preprint. It does not contain those proof sections. The packet's attribution distinguishes these versions correctly. The imported constructions are accepted as literature inputs, not as independently reproved results of this audit.

In [Charpentier–Grosse-Erdmann–Menet, Example 3.8](https://arxiv.org/pdf/1911.09186v2), the parameter family rho^(2^n) gives the same topology as 2^(k 2^n), because the latter positive parameters are cofinal. The no-hypercyclic-weighted-shift example is therefore prior work. Proposition 4.2 is consistent with it: for alpha_n=2^n the relevant partial-sum/last-term ratio is bounded. The packet credits the example and does not claim priority for its stronger explicit decay estimate.

[Bonet's article](https://jbonet.webs.upv.es/wp-content/uploads/papers/bonet0000a_p.pdf) was checked for the neighborhood-based boundedness/compactness convention, Theorem 2, and Theorem 3. It supports the compactness obstruction and the nuclear-basis subclass attribution. Its global scalar-field convention is complex.

All four available source PDFs match their stated byte counts and SHA-256 hashes. Current web retrieval corroborated the versioned arXiv texts and Bonet's source. Direct opening of the live problem page failed in this audit, so its current contents were not certified. Targeted searches found no authoritative full resolution, but such a search result does not prove that no resolution exists anywhere. The author's historical repository-search narrative was not independently replayed against GitHub in this mathematical audit; it is not used in the acceptance decision.

## 4. Reproducibility and hostile-input checks

The independent checker first verifies the external ZIP anchor, exact archive membership, manifest anchor, and every member's byte count and hash before executing any bundled code. Four baseline runs passed: normal and Python -O, each at the original extracted location and a relocated nested path containing spaces. Each replays the author's 13,722 exact finite diagnostic cases.

Thirty-six independent negative controls were rejected: eighteen mutation classes in each optimization mode. These cover missing/extra files, an unexpected directory, same-size proof damage, file/root/entrypoint symlinks, modified manifest bytes, result-count damage, code damage, bad anchors, and four semantic control mutations. For the semantic mutations the manifest was intentionally rebound, so rejection came from the replay rather than an unchanged hash. They remove the stability buffer, change a triangular sign, change the left-eigenfunctional sign, and omit the last boundary equation.

Two additional expected-pass diagnostics deliberately change proof prose and replace the manifest anchor. They correctly demonstrate that the verifier does not interpret mathematical prose. An anchor is meaningful only if independently trusted, and executing an arbitrary modified verifier is not a secure bootstrap. Neither the author nor this audit is claiming otherwise. The independently pinned ZIP is checked before execution here.

The entire computational audit was freshly rerun against the editorially redacted distribution. The independent checker itself was run normally and under -O, with byte-identical JSON output. It uses explicit checks rather than Python assert statements. These tests validate arithmetic diagnostics and integrity behavior. The all-parameter arguments in section 2, not the finite case counts, justify mathematical acceptance.

## 5. Disposition and remaining gap

No correction patch is required. Keep the original status **unsolved**, the original five-of-five approach count, and the distinction between credited literature and authored auxiliary proofs. Acceptance does not assert a new-priority result.

The missing step is either a general chaotic-operator construction on arbitrary nuclear Fréchet spaces without the imported structural assumptions, or a genuine nuclear Fréchet space on which every continuous operator is nonchaotic. The packet supplies neither. The audit performed no remote mutation, publication, or outreach.

The release contains only this authored audit, authored verification code/results, an acceptance record, public verification/source metadata, and its manifest. It contains no third-party PDFs or extracts, source corpus records, datasets, private sources, or private coordination material.
