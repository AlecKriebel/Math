# PR371 independent hyperbolic and arithmetic audit

**Scoped PASS; original source problem remains unsolved, 5/5. No mandatory mathematical or packet correction found at frozen head `51fddd150e8da33f4cf17b1a642a0ffd3466bf5d`.** This is an independent AI-assisted audit of the stated partial deductions, not external peer review or a historical novelty certification.

The live draft [PR371](https://github.com/AlecKriebel/Math/pull/371) still had exactly that head when checked on 3 October 2026 at 10:59 UTC. Its base is `efd29c05204703acca9a0860812f54b94fae54b1`. The candidate was read from the frozen snapshot, with private copies used for execution. No candidate file was edited, and no branch, commit, push, release or external individual communication was performed.

## Independence and evidence stages

The source-first baseline was sealed at 10:43:00 UTC, followed by the mathematical verdict at 10:48:19 UTC. Both original files and their SHA-256 seals are preserved. Candidate code, stored checks, final/result/status files, old reviews and sibling/root mathematical findings were unread until the mathematical verdict was sealed. The only root message before that seal was the assignment; the subsequent root message supplied a usable dependency runtime and a disk-space constraint, not mathematical findings.

The exact source was fetched independently, after an initial web-open timeout, and its printed 2404–2406 contribution was read; printed 2405 was rendered. All required geometry/transcendence primary sources were independently fetched and read. The additional Chapuy1006 trisection excerpt was completed immediately before reading candidate proofs. The published BGL Dirichlet-law details were completed during proof verification, before the mathematical seal, rather than before the baseline; that timing is recorded expressly in the verdict. The baseline used OWR's specified Lebesgue metric-map model and the independent CFF reconstruction. This qualification does not alter the proof conclusions but prevents a misleading claim that every later source-law detail was read before the baseline.

The baseline and verdict explain the independent acceptance criteria, model boundaries, attempted falsifications and universal mathematical reconstructions. The present report adds the complete computational and provenance findings, obtained after the seal.

## Exact source and accepted scope

Louf's Question 4 is a broad request for a geometric adaptation of Chapuy's bijection to construct random surfaces. Its motivating comparison is normalized Weil–Petersson measure on closed curvature−1 surfaces and Lebesgue measure on one-face metric ribbon graphs of perimeter12g. The adjacent volume-identity request is Question 6, and the spine question is Question 3. Neither was added to this target. Report year 2024 and publication14 February 2025 are separately correct. [OWR report and publisher metadata](https://ems.press/journals/owr/articles/14298589).

The five turns correctly leave the broad question open. They show that certain direct constructions fail, while retaining a valid classical positive construction. A stronger metric correspondence, a controlled surface law, a successful approximate coupling and a sufficiency theorem are absent. Existing CFF, Dirichlet, dessin, transcendence, triangle-spectrum and disk-isoperimetric results are credited rather than presented as new work.

| Claim family | Strongest verified result | Material hypotheses and remaining gap |
|---|---|---|
| Equiangular analytic holonomy | Fixed positive algebraic perimeter gives an almost-sure nonclosure obstruction for any simplex density | Positive edges, curvature−1, prescribed120° corners; free real angles and metric changes remain available |
| Algebraic angle palettes | A closed polygon cannot have all positive side lengths algebraic and all interior-angle cosines algebraic; continuous fixed-perimeter palettes are null | Angles strictly between0 and2π; countable algebraic palettes only, without an assertion for unrestricted real profiles |
| Regular-polygon/dessin replacement | Smooth closed surface of the intended genus; its short-geodesic count law has a persistent discrepancy from WP | Cubic one-face map, fixed regular geometry, index 12g−6 triangle subgroup; deformed geometries and scales tending to0 remain outside the claim |
| Intrinsic cut-disk geometry | (P\ge4\pi\sqrt{g(g-1)}\), excluding direct source-perimeter12g realizations for every (g\ge12\) | Smooth closed surface, curvature−1, one face, positive sectors, same edge correspondence; no inference to arbitrary Gromov–Hausdorff comparisons |
| Adaptive repairs | Bounded-factor changes on (o(g)\) edges fail with probability tending to1 under the established Dirichlet law | Necessary perimeter increase and unchanged unselected edges; unbounded sparse repairs and dense changes are not excluded |

## Hyperbolic and arithmetic reconstruction

For a cubic one-face genus-g map, (3V=2E) and Euler's equation give (V=4g-2\), (E=6g-3\), and (N=2E=12g-6\). Thus the clean dessin has **N** subdivided edges/darts, and the orientation-preserving triangle subgroup has indexN. Using E as its index, or using the reflection-triangle area in place of the orientation-preserving orbifold area, would be an error. The candidate makes neither error.

The regular N-gon has corner angle2π/3 and side length (2\operatorname{arcosh}(2\cos(\pi/N)/\sqrt3)\). Valid orientation-compatible map pairings glue three corners at each original vertex, total2π; edge midpoints and the face center are also smooth. Its area is 4π(g−1). The uniform monodromy cycles have full lengths2,3,N. Every nontrivial finite-order element of the triangle group is conjugate to a nontrivial power of an elliptic generator; those permutations have no fixed dart. Hence the stabilizer-preimage subgroup is torsion-free. Divisibility by a larger signature without uniform full cycles would not suffice. Normality is unnecessary and is not asserted. [Uniform-dessin construction, section 2 and Lemma 1](https://arxiv.org/abs/2306.09543).

There is an independent algebraic realization of the rotation pair. With (u=\cos(\pi/N)\), (v=\sqrt{u^2-3/4}\), take

\[
A=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
B=\begin{pmatrix}1/2&u+v\\-u+v&1/2\end{pmatrix}.
\]

They have determinant1 and traces0,1,2u for A,B,AB. Their elliptic centers are separated by the triangle-law distance with hyperbolic cosine2u/√3. Their entries are algebraic for integerN>6. Therefore every word trace is algebraic. A hyperbolic word with absolute trace t>2 has (\exp(\ell/2)=(t+\sqrt{t^2-4})/2\); a positive algebraic ℓ would contradict Hermite–Lindemann. This corroborates the arithmetic nature of this construction. It does **not** turn its countable support or transcendental lengths into an asymptotic-law obstruction.

The actual law obstruction uses Philippe's classification, not a finite word search. Its orientation-preserving p=3 formula is (b_N=2\operatorname{arcosh}(2\cos^2(\pi/N)-1/2)\). Every surface subgroup has systole at least b_N, without necessarily attaining it. For N≥18, (b_N>1\), by the exact rational bounds in the proof. Thus every produced surface has zero primitive-geodesic count on[1/2,1], regardless of the map distribution. [Philippe, Corollary 5.2, printed 2686](https://aif.centre-mersenne.org/item/10.5802/aif.2424.pdf).

For WP surfaces, the exact displayed theorem gives a Poisson limit with μ equal to the integral of(cosh t−1)/t over that interval. Its positive power series gives μ>3/16, and (1-e^{-\mu}>3/19\). The total variation distance between the count laws is exactly (1-\mathbb P_{WP}(\text{count}=0)\), tending to (1-e^{-\mu}\). A finite-support sampler is WP-null at fixed genus, but that fact alone could coexist with asymptotic convergence; the persistent systolic gap is what supplies the stronger conclusion here. The nearby erroneous small-epsilon sentence in the source PDF is not used. [Mirzakhani–Petri, displayed Theorem 4.1](https://webusers.imj-prg.fr/~bram.petri/RandSurf.pdf).

The algebraic-palette polygon theorem is independently reconstructed by the maximal exponent in the framed trace. Its coefficient is the product of positive half-angle cosines; positivity of all side lengths makes that exponent unique. Lower equal-exponent groups and the constant±2 cannot cancel it. Classical Lindemann–Weierstrass then prevents framed closure. This is a universal proof, including concave and straight corners within the declared angle bounds. [Classical introductory TheoremsA/C in Delaygue](https://arxiv.org/abs/2210.12046v2).

The strongest geometry is independent of angles and arithmetic. The intrinsic cut completion of a positive-sector cellular one-face graph is a topological disk with no interior cone points. Repeated face-word vertices split into distinct boundary occurrences; a bridge still contributes two boundary edges. No injective planar development is needed. With (A=4\pi(g-1)\), (P=2\sum_e\ell'_e\), the credited disk inequality (P^2\ge4\pi A+A^2\) gives the stated perimeter bound. It permits reentrant sectors and a2π sector at a leaf. Its applicability would fail without the smooth/full-area/one-face assumptions. [Izmestiev, definitions and Theorem 1](https://arxiv.org/abs/1409.7681).

The source length law is (X_e=\ell_e/(6g)\sim\operatorname{Dirichlet}(1^E)\). Independent exponentials normalized by their sum give this law and independence of proportions and total. Exponential spacings yield (\mathbb E[T_{E,k}]=(k/E)(1+H_E-H_k)\). Adaptive choice cannot increase selected mass above the top-k mass. Markov and Jensen then give the stated success and expected-stretch bounds. k=0,C=1,k=E,E=1 and nonmeasurable geometric-existence events are handled correctly; the outer-probability version uses containment in a measurable necessary event. [Published BGL model, pages 5 and25](https://doi.org/10.1017/fms.2025.31).

## Complete code inspection and execution

All five author verifiers and both prior-review programs were read in full before execution. The programs perform finite exact controls and print receipts; they do not secretly certify external geometric classification, transcendence or infinite random laws. Turn 3 reads the stored Turn 1 examples; the fresh Turn 1 output is byte-identical to that input, so this dependency is consistent.

| Replay | Result | Exact assertion count | Byte comparison |
|---|---|---:|---|
| Author Turn 1 | PASS with Python 3.14.6/SymPy 1.14.0 | 467 | Exact |
| Author Turn 2 | PASS | 1,004 | Exact |
| Author Turn 3 | PASS | 961 | Exact |
| Author Turn 4 | PASS | 1,136 | Exact |
| Author Turn 5 | PASS | 12,050 | Exact |
| Prior independent controls | PASS | 24,692 | Exact |
| Own triangle-character/index/scaling controls | PASS | 3,988 | Newly owned receipt |
| Own candidate/nested manifest binding verifier | PASS | 911 | All declared checks |

The author total is 15,618. Every successful replay has complete stdout, stderr and parsed JSON in the owned artifacts; each successful stderr is empty. Initial default and bundled Python dependency probes failed because SymPy was missing. A temporary own environment creation also failed during ensurepip; installation was never reached. These original outputs and the original unsuccessful all-five replay receipt remain preserved. A supplied existing dependency runtime then replayed all five successfully. Only the failed own temporary environment was removed after its failure records were saved.

The own family program checks the algebraic rotation pair in ℚ[u,v]/(v²−u²+3/4), 1,365 words through length 5, cubic signature/genus parity, orientation/reflection index distinction, and coefficients of the globally scaled density. It explicitly disclaims infinite-law or length-spectrum certification. A positive constant scale a transforms the source density to ρ(t/a)/a, whose leading coefficient is 1/(2a²); preserving this density forces a=1. This supports the normalization audit, without ruling out a distinct limiting mechanism for geometry scaled toward zero.

The first own binding-verifier attempt used a repository path one level too high. It stopped immediately at the first Git read; that original code/stdout/stderr are preserved. Correcting the owned path made all911 checks pass. The frozen candidate was unaffected.

## Packet, source and status binding

The snapshot contains46 target files plus its modified queue file. All 47 files match snapshot byte counts, SHA-256 and Git blobs and the locally resolved frozen PR head. The 37 historical author files additionally match author checkpoint`308b3ee53312800cfe6a82a2cdcc9763e1f90422`. All 26 historical turn-manifest entries,36 final-author entries,6 review-manifest entries,37 old remote-blob bindings and45 publication entries verify. The 37-file author public scope includes its manifest; the7-file review scope includes its own manifest. The publication wrapper additionally includes reviewed-result and publication-manifest files. The complete scope matches the actual frozen target inventory.

All historical dispositions remain unresolved/unsolved, followed by the additive reviewed wrapper retaining unsolved 5/5. Earlier pending-review states are correctly treated as immutable historical snapshots. The frozen queue row is also unsolved 5/5. There is no sixth author search or implicit claim that this audit solves the original problem.

The candidate declares27 source entries with25 distinct paths; the two repeated Delaygue PDF/text bindings agree. Ten independently fetched primary PDFs were compared: nine reproduce the candidate's exact SHA-256, while the published Cambridge BGL PDF is dynamically watermarked and has a different byte hash. Its mathematical statements were independently read and rendered. Historical text extraction and screenshot hashes were not reproduced at identical tool versions/resolutions, so they are recorded as declarations rather than falsely certified raw-byte checks. Source hashes bind bytes but do not alone prove reading or novelty. Public provenance records distinguish these limits.

## Final assessment and exact remaining gap

The five-turn package is fit to retain as a carefully scoped partial result, with original disposition **unsolved 5/5** and primary inputs credited. The strongest verified statement excludes same-edge, one-face smooth curvature−1 realizations at perimeter12g for every g≥12; under the actual law, sparse bounded-factor corrections cannot overcome the required increase with nonvanishing asymptotic probability. The classical regular replacement is smooth but uniformly misses the source's short-geodesic law. These results are compatible and do not overclaim a full geometric obstruction.

The exact unresolved gap is a constructive or negative result covering the source's broader adaptations: controlled length/angle or holonomy changes, alternate correspondences, dense or unbounded corrections, and a specified surface law or asymptotic comparison. Satisfying the necessary bounds does not supply such a construction. No paper, release, DOI or full novelty claim is supported by this audit.

The owned `PUBLIC_MANIFEST.json` explicitly enumerates public files relative to this review root, excludes itself, and excludes every private source/API payload and replay copy. `verify_public_manifest.py` checks the public file hashes and exact owned inventory. Research checkpoints, source receipts, sealed baseline/verdict, complete failures and successful replays, owned code and this report are included.
