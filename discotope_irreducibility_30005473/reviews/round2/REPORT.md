# Fresh independent adversarial preprint review — round 2

Review date: 2026-10-01 UTC / 2026-09-30 America/Los_Angeles. Author reviewed: Alec Kriebel, ORCID 0009-0001-9320-500X. This is an AI adversarial review, not human peer review or formal proof certification. No outside individual was contacted, and no publication, commit, push, or branch change was performed.

## Verdict

**No outstanding mathematical, attribution, reproducibility, metadata, or exclusion defect was found in the frozen target. No canonical repair is required.** Both theorems are valid under their stated assumptions. The former addresses the exact 2023 exposed-point conjecture; the latter supplies the generic identification needed for the distinct 2022 purely nonlinear-part conjecture. Historical first priority remains unconfirmed, as the manuscript and metadata explicitly state.

This review independently read all of `paper.tex`, visually inspected all four pages of the deposited PDF, fetched and checked the primary conjecture sources, reconstructed the mathematical proof, and tested its failure mechanisms. Earlier verdicts were not read until after this fresh mathematical assessment. A separately delegated mathematical falsifier likewise read no earlier verdicts or check scripts; its report and new exact checks are retained in this folder.

The frozen target is:

| Object | SHA-256 |
| --- | --- |
| `paper.tex` | `3576dcc78bf1a9188ee8a8b5c56f5914357d90d437767e29dc42e3a85ceedab4` |
| `paper.pdf` | `c13dc861e8e5b5c1d980bdd78d14aff8e4b1a130800c4f942b3bedafbc5f6b2a` |
| `source-and-verification.zip` | `0b37678640290c024cd2cb35c9b9620ccdcf2d2076c695f754956794e2558e70` |
| `zenodo-upload-kit.zip` | `d9f352d8aebf3f1ca4eebc68b1767c322db14554447f20e6e0300b785eb0dd94` |

The necessarily later round-two evidence must be added to the final package. That is final assembly, not a mathematical modification. After adding it, the root must rebuild and check the final member inventory, PDF/source binding, nested kit bytes, metadata and checksums, and record the final archive hashes. The paper, canonical exact checks/results, source snapshot, priority evidence and metadata should retain the frozen bytes. This review does not execute publication.

## Independent deductive reconstruction and attempted falsification

### Connected complement

For every excluded kernel `M_i=ker(A_i^T)`, rank at least two gives `dim M_i<=d-2`. For regular endpoints `x,y`, each `M_i+Rx` and `M_i+Ry` remains proper. A finite union of proper real linear subspaces cannot fill the ambient space, since a product of their nonzero vanishing linear forms is a nonzero polynomial. Choosing `z` outside this enlarged union ensures neither segment from an endpoint to `z` can enter any `M_i`: solving the segment equation for `z` would put it in the corresponding enlarged space. The endpoints also remain regular. The complement is nonempty and open because the original finite union is closed and proper.

This proof covers repeated kernels, coincident spans, and common ambient kernels. The rank assumptions themselves force `d>=2`; in the smallest case the excluded rank-two kernels are the origin. There is no concealed full-dimensionality assumption.

### Exact singleton-face normal domain

Maximizing the linear functional on `A_i B` reduces to maximizing `(A_i^T u)·v` on the unit ball. A nonzero projection has exactly one maximizing unit vector. A zero projection exposes the whole positive-dimensional summand. For a sum point, the total support deficit is the sum of nonnegative individual support deficits, so the total face equals the Minkowski sum of the individual faces.

A nonsingleton face cannot cancel in a Minkowski sum: fixing points in all other faces embeds it by translation in the total face. This proves the singleton equivalence without independent spans or unique decomposition. It follows that the exposed points are exactly `F(U)`, rather than only a subset dense in them. All normals in `U` are nonzero. Normals orthogonal to an entire lower-dimensional sum expose the whole sum and correctly lie outside `U`.

Repeated discs, dependent quadratic forms, nonorthogonal ellipses and redundant normals preserve these conclusions. Replacing an arbitrary defining linear map by its nonzero singular directions correctly produces an injective map of the actual summand rank.

### Complex prime ideal

Every radicand is strictly positive on `U`; the positive inverse square root is real analytic there. For arbitrary complex polynomials `P,Q`, if `PQ` vanishes on the image and `P` does not, there is an open neighborhood on which `P∘F` is nonzero. Hence `Q∘F` vanishes on that neighborhood. Analytic uniqueness on connected `U`, applied separately to its real and imaginary parts, makes `Q∘F` vanish everywhere. The image is nonempty, so its complex vanishing ideal is proper and prime.

Taking the Zariski closure does not change this ideal: its closed zero set contains the image, and every polynomial in the ideal vanishes on the closure. Primality therefore establishes complex irreducibility directly. This does not assume that an arbitrary real irreducible polynomial remains irreducible over the complex numbers. It also requires neither injectivity nor immersion of `F`, simple connectivity, independent radicals, nor any global complex radical branch.

The manuscript's analytic uniqueness justification is correct. At a limit of neighborhood-zero points, continuity of every derivative makes all Taylor coefficients zero; convergence of the local analytic expansion gives a vanishing neighborhood. The neighborhood-zero set is consequently both open and relatively closed.

### Generic identification of the two varieties

Exposed points are sums of relative summand-boundary support points, giving the first inclusion. Conversely, full dimensionality gives a nonzero supporting normal at every chosen total-boundary point. Nonnegative support deficits make every summand in the chosen boundary decomposition maximize it.

For the killed index set `J`, all its spans lie in `u^perp`. Subsetwise (GP) therefore forces `sum(m_j)<=d-1`; otherwise maximal possible rank would make their sum the entire ambient space. It then forces the concatenated matrix `A_J` to have independent columns, and its transpose to be surjective. Every relative boundary point has the unique form `A_j v_j` with `||v_j||=1`; no orthonormality is needed. One can thus impose all equations `A_j^T w=v_j` simultaneously.

For positive epsilon, the killed projection is exactly `epsilon v_j`, so its normalized support point is exactly the desired point. For an un-killed projection `a_i=A_i^T u`, with perturbation `b_i=A_i^T w`, the sufficient bound `epsilon<||a_i||/(2||b_i||)` preserves nonvanishing when `b_i!=0`; a zero `b_i` needs no bound. Taking a finite minimum handles every remaining index. The un-killed support points converge by continuity. Complex algebraic sets are Euclidean closed, giving the second inclusion of Zariski closures. The empty killed-set case is directly exposed; for a nonempty killed set the perturbed normal cannot be zero. The sign of epsilon is correctly prescribed.

### Nonempty generic condition and ambient reduction

For each summand subset, failure of maximal concatenated rank is algebraic, defined by all maximal minors. There are finitely many subsets. Distinct real Vandermonde columns give a simultaneous witness: any `k<=d` columns have an invertible minor in their first `k` rows, and any larger set contains `d` independent columns. Partitioning columns into the prescribed blocks proves nonemptiness and the claimed real Zariski-open property for all allowed sizes.

When the total size reaches the ambient dimension this witness is full-dimensional. When it does not, generic summand spans form a direct sum. Working in that sum is the original source's ambient-span convention; alternatively, simultaneous transpose surjectivity then shows every sum of relative-boundary points is already exposed. Thus the full-dimensional hypothesis of the bridge has not silently lost a feasible generic type of the conjecture.

### Rank-one and nongeneric boundary cases

The segment has two exposed points and reducible closure. For the disc-plus-segment stadium, normals with positive or negative horizontal coordinate select distinct translated semicircles. A zero horizontal coordinate exposes a segment, so no missing exposed arc joins them. Each open semicircle is Zariski dense in its smooth complex conic, and the two conics are distinct for positive segment length. Rank one is therefore a real obstruction to the universal statement.

In the nongeneric repeated-disc example, `e3=e1+(-e1)+e3` is a sum of relative boundary points and lies in the face exposed by `e3`. For every regular normal, the two auxiliary x-coordinates satisfy `a²+Y²=4`, `b²+Z²=1`, and `X=a+b`. The displayed quartic vanishes by these identities, while its value at `e3` is 16. This separates the point from the entire complex closure of exposed points, establishing the strict distinction of the varieties. It is not merely non-exposure by one chosen normal and makes no unsupported claim that every nongeneric purely nonlinear variety is reducible.

### Distinct supplemental evidence

The fresh falsifier's standard-library rational checks cover a homothetic nonorthogonal rank-two sum in five-space with proportional radicals and a three-dimensional common kernel; all 63 nonempty subsets of six Vandermonde columns; two simultaneous killed nonorthogonal summands with unrelated rational unit targets; a quantified normalization error bound; four exact separator samples; and six rank-one branch samples. Its report also tests the failure of the analytic lemma for a merely smooth connected map into two axes. All checks passed. The report, script and output are `math_falsifier.md`, `math_falsifier_exact_checks.py`, and `math_falsifier_exact_results.json`.

These finite computations corroborate formulas and expose plausible assumption failures. The universal conclusions above are deductions from the proof, not statistical or numerical extrapolations. Exact remaining mathematical gap: none found within the stated scope.

## Primary sources, bounded priority and disclosure

The [2022 publisher paper](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734) was checked at its parameter convention, Definition 3.3, prior special cases and Conjecture 8.2, with visual checks of printed pages 149 and 167. Its purely nonlinear target and its ambient-span convention match the manuscript. The [official 2023 report](https://publications.mfo.de/bitstream/handle/mfo/4031/OWR_2023_15.pdf?sequence=4) was visually checked at printed page 830: the exposed-point target and generic spans match the manuscript's stated comparison. The manuscript accurately separates these two targets.

The [primary Kucharz–Kurdyka article](https://ruj.uj.edu.pl/server/api/core/bitstreams/52a654f7-4489-46d9-8157-6c7715c24f3e/content), printed page 95, proof of Proposition 4.3, was fetched and visually checked. Its analytic-image irreducibility observation is correctly credited. The complex-coefficient proof is provided rather than attributed verbatim to that source.

The completed two priority-family reports and citation subaudit were read after the independent proof assessment. Their scope is bounded and their positive precedents receive appropriate credit. Supplemental fresh queries and primary checks of [Chirikjian–Shiffman](https://arxiv.org/pdf/2012.15163), Theorem 1.1, and [Operatopes](https://arxiv.org/html/2602.08103v1), Section 2.1 and face results, found an earlier full-rank support formula and a class inclusion, respectively; these do not state the complete target result. This is a checked hypothesis comparison, not a certification of first publication. Search, citation-index, inaccessible-publication and private-corpus gaps remain openly described. No earlier full resolution surfaced in this bounded supplemental audit.

The manuscript gives clear early and late AI-assistance and unrefereed-status disclosures. It does not present AI adversarial reviews as human review or formal certification. The title, abstract, theorem scope, author and correct ORCID, date/version, bibliography, README, license division and Zenodo description are aligned. Degrees, birationality and an entire complex critical locus are explicitly outside the claims. All four PDF pages are legible, with coherent equations, references and page numbers; no layout or source/PDF discrepancy was found.

Primary retrieval URLs, hashes and checked locations are recorded concisely in `primary_checks.json`. Third-party PDFs, extracted source text and renders remain ignored scratch evidence; they are not new public review artifacts.

## Full package integrity and extracted-copy reproduction

`archive_checks.py` and `archive_evidence.json` bind the frozen target, not a future rebuilt archive. The audit passed:

- ZIP integrity, unique safe paths, regular file modes, no symlinks, no hidden environment or scratch members.
- Every one of the 78 source members, with an exact complete 77-member manifest excluding only itself; every listed hash, size and canonical source byte matches. The manifest separately binds the deposited PDF.
- Exact nested PDF/source bytes, metadata, upload paths and checksums in the six-member outer kit; canonical deposit and offline-kit path differences are intentional and correctly documented.
- All 16 original snapshot members match their recorded hashes and the immutable local Git blobs at PR head `a29887ed0e341851d02fa992c26500d4089267be`. Historical snapshots and reviews are clearly distinguished from the new preprint.
- A vetted extracted-copy run with CPython 3.14.6, SymPy 1.14.0, mpmath 1.3.0, optimization disabled and bytecode writes disabled. The independent results match archived values apart from recorded execution timestamp/runtime fields. The original child output is byte-for-byte identical, both runs have empty stderr, and all snapshot bytes remain unchanged.
- Restoring scratch evidence before a scratch-only builder run reproduces both frozen ZIPs byte-for-byte. Canonical files and outputs remain untouched.

The three previously problematic raw response captures are absent from the archive and the current tracked Git tree. They remain ignored local aids. Reports now explicitly distinguish public query/source comparison metadata from local raw responses, source PDFs, full extracts and OCR/renders. No substantial publisher-line capture was found among the remaining public text/JSON. The sole archived PDF is the first-party historical proof, with immutable provenance. The licenses credit first-party author prose and code while excluding third-party source re-licensing. No credentials, installed dependencies or publication receipts are included.

All eleven completed first-round report, resolution, evidence and stress-check members are present. Their historical adverse finding is retained honestly with its dated resolution. I verified the repair after independently assessing the mathematics; the source/PDF/check/metadata bytes did not change as part of that packaging repair.

## Final checkpoint

Assigned fresh review scope: **100% complete**, subject only to the root's mechanical final assembly/inventory/hash check after adding this completed evidence. This percentage measures completed review work, not mathematical correctness probability or historical priority. No actionable severity item or canonical repair remains. Preserve the unrefereed/AI and bounded-priority framing during publication.
